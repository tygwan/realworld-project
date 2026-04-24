#!/usr/bin/env python3
"""Inventory the local refinery GLB + schedule dataset.

The script reads only metadata and CSV/JSON headers. It does not copy private
asset payloads into the repository.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


def read_csv(path: Path, encoding: str) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def auto_schedule_path(root: Path) -> Path | None:
    schedule_dir = root / "schedule"
    if not schedule_dir.exists():
        return None
    candidates = sorted(schedule_dir.glob("*.csv"))
    return candidates[-1] if candidates else None


def summarize(root: Path, schedule_encoding: str) -> dict[str, Any]:
    manifest_path = root / "manifest.json"
    geometry_path = root / "geometry.csv"
    unified_path = root / "unified.csv"
    validation_path = root / "validation.csv"
    tessellation_path = root / "tessellation_failures.csv"
    schedule_path = auto_schedule_path(root)
    mesh_dir = root / "mesh"

    if not manifest_path.exists():
        raise FileNotFoundError(f"missing manifest: {manifest_path}")
    if not geometry_path.exists():
        raise FileNotFoundError(f"missing geometry.csv: {geometry_path}")
    if not schedule_path:
        raise FileNotFoundError(f"missing schedule CSV under: {root / 'schedule'}")

    with manifest_path.open("r", encoding="utf-8-sig") as handle:
        manifest = json.load(handle)
    metadata = manifest.get("metadata", {})

    geometry_fields, geometry_rows = read_csv(geometry_path, "utf-8-sig")
    schedule_fields, schedule_rows = read_csv(schedule_path, schedule_encoding)

    object_ids = {row.get("ObjectId", "") for row in geometry_rows if row.get("ObjectId")}
    display_names = {
        row.get("DisplayName", "") for row in geometry_rows if row.get("DisplayName")
    }
    categories = {row.get("Category", "") for row in geometry_rows if row.get("Category")}
    sync_ids = {
        row.get("동기화 ID", "") for row in schedule_rows if row.get("동기화 ID")
    }

    mesh_quality = Counter(row.get("MeshQuality", "") for row in geometry_rows)
    glb_count = len(list(mesh_dir.glob("*.glb"))) if mesh_dir.exists() else 0

    summary: dict[str, Any] = {
        "dataset": {
            "root_name": root.name,
            "manifest_generator": metadata.get("generator"),
            "manifest_export_date": metadata.get("exportDate"),
            "manifest_object_count": metadata.get("objectCount"),
            "manifest_mesh_count": metadata.get("meshCount"),
            "glb_file_count": glb_count,
            "gap_fallback_fbx_exists": (root / "gap_fallback.fbx").exists(),
        },
        "geometry": {
            "rows": len(geometry_rows),
            "fields": geometry_fields,
            "has_mesh_rows": sum(
                str(row.get("HasMesh", "")).lower() == "true" for row in geometry_rows
            ),
            "mesh_uri_rows": sum(bool(row.get("MeshUri")) for row in geometry_rows),
            "mesh_quality_counts": dict(mesh_quality.most_common()),
        },
        "schedule": {
            "path_name": schedule_path.name,
            "encoding": schedule_encoding,
            "rows": len(schedule_rows),
            "fields": schedule_fields,
            "unique_sync_ids": len(sync_ids),
            "task_type_counts": dict(
                Counter(row.get("작업 유형", "") for row in schedule_rows).most_common()
            ),
        },
        "mapping_probe": {
            "sync_matches_object_id": len(sync_ids & object_ids),
            "sync_matches_display_name": len(sync_ids & display_names),
            "sync_matches_category": len(sync_ids & categories),
        },
        "optional_files": {
            "unified_csv_exists": unified_path.exists(),
            "validation_csv_exists": validation_path.exists(),
            "tessellation_failures_csv_exists": tessellation_path.exists(),
        },
    }

    if unified_path.exists():
        unified_fields, unified_rows = read_csv(unified_path, "utf-8-sig")
        paths = [row.get("HierarchyPath", "") for row in unified_rows]
        sample_sync_ids = list(sync_ids)[:200]
        prefix_hits = sum(
            any(path.replace("/", "::").startswith(sync_id) for path in paths)
            for sync_id in sample_sync_ids
        )
        summary["unified"] = {
            "rows": len(unified_rows),
            "fields": unified_fields,
            "sample_sync_prefix_hits_first_200": prefix_hits,
            "sample_hierarchy_paths": paths[:5],
        }

    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root",
        nargs="?",
        default=os.environ.get("REALWORLD_REFINERY_ROOT", ""),
        help="Path to refinery dataset root. Defaults to REALWORLD_REFINERY_ROOT.",
    )
    parser.add_argument(
        "--schedule-encoding",
        default=os.environ.get("REALWORLD_REFINERY_SCHEDULE_ENCODING", "cp949"),
    )
    args = parser.parse_args()

    if not args.root:
        raise SystemExit("Provide root path or set REALWORLD_REFINERY_ROOT.")

    summary = summarize(Path(args.root), args.schedule_encoding)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
