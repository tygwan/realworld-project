#!/usr/bin/env python3
"""Build a per-ObjectId material/color lookup table for Unity import.

DXTnavis-generated GLBs contain only geometry. To color them in Unity URP,
this script produces a side-channel JSON that Unity loads at runtime.

Resolution rule:
  Tier 1: SmartPlant 3D|Material (explicit). Mapped to a fixed palette key.
  Tier 2: Domain inferred from SmartPlant 3D|System Path, Name, Eqp Type 0.
  Tier 3: 'Unknown' fallback.

See docs/analysis/2026-04-25-refinery-material-data-sources.md for the
rationale and palette versioning policy.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import glob
import json
import os
import sys
from collections import Counter
from pathlib import Path

PALETTE_VERSION = "0.1"

# Tier 1: explicit Material values (after stripping 'DisplayString:' prefix).
MATERIAL_PALETTE = {
    "Steel - Carbon": "4A4F58",
    "Concrete": "B0AFA8",
    "Cementitious": "C7B299",
    "Fibrous": "D4A574",
}

# Tier 2: domain buckets inferred from System Path / Name / Eqp Type 0.
DOMAIN_PALETTE = {
    "Pipe": "5A6470",
    "PipeFitting": "78808A",
    "Valve": "884540",
    "Structure": "7A6F5C",
    "Civil": "9A9388",
    "Equipment": "5A6F88",
    "Insulation": "D4A574",
    "Unknown": "9A9A9A",
}

# Order matters: more specific buckets first.
DOMAIN_RULES = [
    ("Insulation",  ["insulation"]),
    ("Civil",       ["cable trench", "civil_structure", "civil structure"]),
    ("Structure",   ["membersystem", "structural", " beam", " column"]),
    ("Equipment",   ["transformer", "wiring equipment", "power distribution",
                     "switchgear"]),
    ("Valve",       ["valve", "vg3", "fv-", "pv-", "tv-", "fe-"]),
    ("PipeFitting", ["flange", "weldolet", "elbow", "reducer", "tee",
                     "direction change", "reinforcing pad", "fitting"]),
    ("Pipe",        ["piping", "pipeline", "pipe rack", "pipelines",
                     "pipe", "process\\pipe", "\\p-"]),
]


def strip_display(value: str) -> str:
    """SmartPlant export prefixes most cells with 'DisplayString:'. Strip it."""
    return value.replace("DisplayString:", "").strip() if value else ""


def find_allproperties_csv(root: Path) -> Path:
    matches = sorted(root.glob("AllProperties_*.csv"))
    if not matches:
        sys.exit(f"AllProperties_*.csv not found under {root}")
    return matches[-1]


def load_object_ids(subset_dir: Path | None, mesh_dir: Path) -> set[str]:
    """If a subset is given, use its manifest; else fall back to mesh/ filenames."""
    if subset_dir is not None:
        manifest_path = subset_dir / "unity_subset_manifest.json"
        with manifest_path.open(encoding="utf-8") as f:
            manifest = json.load(f)
        ids: set[str] = set()
        for task in manifest.get("tasks", []):
            ids.update(task.get("object_ids", []))
        if ids:
            return ids
    if not mesh_dir.is_dir():
        sys.exit(f"mesh directory not found: {mesh_dir}")
    return {p.stem for p in mesh_dir.glob("*.glb")}


def load_smartplant_rows(allprop_csv: Path, ids: set[str]) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    with allprop_csv.open(encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        idx = {col: header.index(col) for col in header}
        for row in reader:
            if not row:
                continue
            oid = row[idx["ObjectId"]]
            if oid not in ids:
                continue
            rows[oid] = {col: row[i] if i < len(row) else "" for col, i in idx.items()}
    return rows


def load_geometry_categories(geom_csv: Path, ids: set[str]) -> dict[str, str]:
    cats: dict[str, str] = {}
    with geom_csv.open(encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        i_id, i_cat = header.index("ObjectId"), header.index("Category")
        for row in reader:
            if not row:
                continue
            oid = row[i_id]
            if oid in ids:
                cats[oid] = row[i_cat] if i_cat < len(row) else ""
    return cats


def infer_domain(rec: dict) -> str:
    parts = [
        strip_display(rec.get("SmartPlant 3D|System Path", "")),
        strip_display(rec.get("SmartPlant 3D|Name", "")),
        strip_display(rec.get("SmartPlant 3D|Eqp Type 0", "")),
    ]
    text = " ".join(parts).lower()
    if not text.strip():
        return "Unknown"
    for domain, keywords in DOMAIN_RULES:
        if any(k in text for k in keywords):
            return domain
    return "Unknown"


def resolve_entry(oid: str, rec: dict | None, category: str | None) -> dict:
    material = strip_display(rec.get("SmartPlant 3D|Material", "")) if rec else ""
    if material in MATERIAL_PALETTE:
        return {
            "object_id": oid,
            "material": material,
            "domain": None,
            "applied_key": material,
            "color_hex": MATERIAL_PALETTE[material],
            "source": "explicit_material",
            "system_path": strip_display(rec.get("SmartPlant 3D|System Path", "")) if rec else "",
            "name": strip_display(rec.get("SmartPlant 3D|Name", "")) if rec else "",
            "category": category or "",
        }
    domain = infer_domain(rec) if rec else "Unknown"
    return {
        "object_id": oid,
        "material": material or None,
        "domain": domain,
        "applied_key": domain,
        "color_hex": DOMAIN_PALETTE[domain],
        "source": "domain_inference" if domain != "Unknown" else "unknown",
        "system_path": strip_display(rec.get("SmartPlant 3D|System Path", "")) if rec else "",
        "name": strip_display(rec.get("SmartPlant 3D|Name", "")) if rec else "",
        "category": category or "",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("refinery_root", help="REALWORLD_REFINERY_ROOT path")
    ap.add_argument(
        "--subset-dir",
        default=None,
        help="Optional subset directory containing unity_subset_manifest.json. "
             "If omitted, all GLBs under <refinery_root>/mesh/ are processed.",
    )
    ap.add_argument(
        "--output",
        default=None,
        help="Output JSON path. Defaults to <subset-dir>/object_material_lut.json "
             "or <refinery_root>/object_material_lut.json.",
    )
    args = ap.parse_args()

    root = Path(args.refinery_root).resolve()
    if not root.is_dir():
        sys.exit(f"refinery_root not a directory: {root}")
    subset_dir = Path(args.subset_dir).resolve() if args.subset_dir else None
    mesh_dir = root / "mesh"

    ids = load_object_ids(subset_dir, mesh_dir)
    if not ids:
        sys.exit("no object IDs resolved")

    allprop_csv = find_allproperties_csv(root)
    geom_csv = root / "geometry.csv"
    rows = load_smartplant_rows(allprop_csv, ids)
    cats = load_geometry_categories(geom_csv, ids) if geom_csv.exists() else {}

    entries = [resolve_entry(oid, rows.get(oid), cats.get(oid)) for oid in sorted(ids)]

    summary = {
        "total": len(entries),
        "by_source": dict(Counter(e["source"] for e in entries)),
        "by_applied_key": dict(Counter(e["applied_key"] for e in entries)),
    }

    payload = {
        "schema_version": "0.1",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "subset_id": subset_dir.name if subset_dir else None,
        "palette_version": PALETTE_VERSION,
        "palette": {
            "tier1_material": MATERIAL_PALETTE,
            "tier2_domain": DOMAIN_PALETTE,
        },
        "summary": summary,
        "entries": entries,
    }

    if args.output:
        out_path = Path(args.output).resolve()
    elif subset_dir:
        out_path = subset_dir / "object_material_lut.json"
    else:
        out_path = root / "object_material_lut.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"wrote {out_path}")
    print(f"  total: {summary['total']}")
    print(f"  by_source: {summary['by_source']}")
    print(f"  by_applied_key: {summary['by_applied_key']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
