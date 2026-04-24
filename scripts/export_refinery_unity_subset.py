#!/usr/bin/env python3
"""Export a small refinery schedule/mesh subset for Unity import tests.

The script selects high-confidence rows from the DXTnavis-aware mapping layer
and writes Unity-friendly manifests. Mesh payloads are copied only when
`--copy-meshes` is supplied.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from map_refinery_schedule_to_assets import (
    MappingResult,
    ScheduleMapper,
    auto_all_properties_path,
    auto_schedule_path,
    read_all_properties,
    read_schedule,
    read_unified,
)


DEFAULT_METHODS = {
    "pipeline_piperun_properties",
    "hierarchy_path_descendants",
}


def build_results(
    root: Path,
    schedule_path: Path,
    schedule_encoding: str,
    all_properties_path: Path,
) -> list[MappingResult]:
    schedule_rows = read_schedule(schedule_path, schedule_encoding)
    objects, children, path_to_ids, display_to_ids = read_unified(root / "unified.csv")
    pipeline_to_ids, property_name_to_ids, equipment_to_ids = read_all_properties(
        all_properties_path
    )

    mapper = ScheduleMapper(
        objects=objects,
        children=children,
        path_to_ids=path_to_ids,
        display_to_ids=display_to_ids,
        pipeline_to_ids=pipeline_to_ids,
        property_name_to_ids=property_name_to_ids,
        equipment_to_ids=equipment_to_ids,
    )
    return [mapper.map_row(row) for row in schedule_rows]


def select_subset(
    results: list[MappingResult],
    max_meshes: int,
    max_tasks: int,
    methods: set[str],
    max_meshes_per_task: int,
) -> list[MappingResult]:
    selected: list[MappingResult] = []
    selected_meshes: set[str] = set()

    for result in results:
        if result.confidence != "high":
            continue
        if result.method not in methods:
            continue
        if result.mesh_count <= 0:
            continue
        if max_meshes_per_task > 0 and result.mesh_count > max_meshes_per_task:
            continue

        next_meshes = selected_meshes | set(result.mesh_uris)
        if len(next_meshes) > max_meshes:
            continue

        selected.append(result)
        selected_meshes = next_meshes

        if max_tasks > 0 and len(selected) >= max_tasks:
            break
        if len(selected_meshes) >= max_meshes:
            break

    return selected


def copy_meshes(root: Path, output_dir: Path, mesh_uris: list[str]) -> list[dict[str, str]]:
    mesh_dir = output_dir / "mesh"
    mesh_dir.mkdir(parents=True, exist_ok=True)
    copied: list[dict[str, str]] = []

    for mesh_uri in mesh_uris:
        source = root / mesh_uri
        if not source.exists():
            copied.append(
                {
                    "mesh_uri": mesh_uri,
                    "source_path": str(source),
                    "staged_path": "",
                    "status": "missing",
                }
            )
            continue

        target = mesh_dir / source.name
        shutil.copy2(source, target)
        copied.append(
            {
                "mesh_uri": mesh_uri,
                "source_path": str(source),
                "staged_path": str(target),
                "status": "copied",
            }
        )

    return copied


def build_manifest(
    root: Path,
    schedule_path: Path,
    all_properties_path: Path,
    output_dir: Path,
    selected: list[MappingResult],
    mesh_copy_records: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, Any]:
    unique_object_ids = sorted({oid for result in selected for oid in result.object_ids})
    unique_mesh_uris = sorted({uri for result in selected for uri in result.mesh_uris})
    copied_by_uri = {record["mesh_uri"]: record for record in mesh_copy_records}

    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Unity refinery import smoke-test subset",
        "source": {
            "root": str(root),
            "schedule_csv": str(schedule_path),
            "all_properties_csv": str(all_properties_path),
        },
        "selection": {
            "max_meshes": args.max_meshes,
            "max_tasks": args.max_tasks,
            "max_meshes_per_task": args.max_meshes_per_task,
            "methods": sorted(args.methods),
            "copy_meshes": args.copy_meshes,
        },
        "summary": {
            "task_count": len(selected),
            "unique_object_id_count": len(unique_object_ids),
            "unique_mesh_uri_count": len(unique_mesh_uris),
            "copied_mesh_count": sum(
                1 for record in mesh_copy_records if record["status"] == "copied"
            ),
            "missing_mesh_count": sum(
                1 for record in mesh_copy_records if record["status"] == "missing"
            ),
        },
        "tasks": [
            {
                "sequence_index": index,
                "schedule_row_index": result.row.row_index,
                "task_name": result.row.task_name,
                "sync_id": result.row.sync_id,
                "task_type": result.row.task_type,
                "planned_start": result.row.planned_start,
                "planned_end": result.row.planned_end,
                "mapping_method": result.method,
                "confidence": result.confidence,
                "object_ids": result.object_ids,
                "mesh_uris": result.mesh_uris,
            }
            for index, result in enumerate(selected, start=1)
        ],
        "meshes": [
            {
                "mesh_uri": mesh_uri,
                "source_path": str(root / mesh_uri),
                "staged_relative_path": f"mesh/{Path(mesh_uri).name}",
                "copy_status": copied_by_uri.get(mesh_uri, {}).get(
                    "status", "not_copied"
                ),
            }
            for mesh_uri in unique_mesh_uris
        ],
        "notes": [
            "Use this subset to validate Unity import, scale/origin handling, hierarchy, and schedule-driven visibility before importing the full refinery dataset.",
            "This subset intentionally excludes medium-confidence wildcard mappings until duplicate-assignment handling is implemented.",
        ],
    }


def write_tasks_csv(output_dir: Path, selected: list[MappingResult]) -> None:
    csv_path = output_dir / "subset_tasks.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "sequence_index",
                "schedule_row_index",
                "task_name",
                "sync_id",
                "task_type",
                "planned_start",
                "planned_end",
                "mapping_method",
                "confidence",
                "object_count",
                "mesh_count",
                "object_ids",
                "mesh_uris",
            ],
        )
        writer.writeheader()
        for index, result in enumerate(selected, start=1):
            writer.writerow(
                {
                    "sequence_index": index,
                    "schedule_row_index": result.row.row_index,
                    "task_name": result.row.task_name,
                    "sync_id": result.row.sync_id,
                    "task_type": result.row.task_type,
                    "planned_start": result.row.planned_start,
                    "planned_end": result.row.planned_end,
                    "mapping_method": result.method,
                    "confidence": result.confidence,
                    "object_count": result.object_count,
                    "mesh_count": result.mesh_count,
                    "object_ids": ";".join(result.object_ids),
                    "mesh_uris": ";".join(result.mesh_uris),
                }
            )


def write_readme(output_dir: Path, manifest: dict[str, Any]) -> None:
    summary = manifest["summary"]
    text = f"""# Refinery Unity MVP Subset

This directory is a local-only Unity import smoke-test subset.

## Summary

- Tasks: {summary["task_count"]}
- Unique object IDs: {summary["unique_object_id_count"]}
- Unique mesh URIs: {summary["unique_mesh_uri_count"]}
- Copied meshes: {summary["copied_mesh_count"]}
- Missing meshes: {summary["missing_mesh_count"]}

## Files

- `unity_subset_manifest.json` - full task/object/mesh manifest
- `subset_tasks.csv` - compact task table
- `mesh/` - copied GLB files when generated with `--copy-meshes`

Use this before importing the full refinery dataset into Unity.
"""
    (output_dir / "README.md").write_text(text, encoding="utf-8")


def parse_methods(raw: str) -> set[str]:
    if not raw.strip():
        return set(DEFAULT_METHODS)
    return {item.strip() for item in raw.split(",") if item.strip()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root",
        nargs="?",
        default=os.environ.get("REALWORLD_REFINERY_ROOT", ""),
        help="Path to refinery dataset root. Defaults to REALWORLD_REFINERY_ROOT.",
    )
    parser.add_argument(
        "--schedule",
        default=os.environ.get("REALWORLD_REFINERY_SCHEDULE_CSV", ""),
        help="Schedule CSV path. Defaults to latest CSV under root/schedule.",
    )
    parser.add_argument(
        "--schedule-encoding",
        default=os.environ.get("REALWORLD_REFINERY_SCHEDULE_ENCODING", "cp949"),
    )
    parser.add_argument("--all-properties", default="")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Local output directory for subset manifest and optional mesh copies.",
    )
    parser.add_argument("--max-meshes", type=int, default=50)
    parser.add_argument("--max-tasks", type=int, default=0)
    parser.add_argument("--max-meshes-per-task", type=int, default=30)
    parser.add_argument(
        "--methods",
        type=parse_methods,
        default=set(DEFAULT_METHODS),
        help="Comma-separated mapping methods to include.",
    )
    parser.add_argument("--copy-meshes", action="store_true")
    args = parser.parse_args()

    if not args.root:
        raise SystemExit("Provide root path or set REALWORLD_REFINERY_ROOT.")

    root = Path(args.root)
    schedule_path = Path(args.schedule) if args.schedule else auto_schedule_path(root)
    all_properties_path = (
        Path(args.all_properties) if args.all_properties else auto_all_properties_path(root)
    )
    output_dir = Path(args.output_dir)

    if not schedule_path or not schedule_path.exists():
        raise FileNotFoundError(f"missing schedule CSV: {schedule_path}")
    if not all_properties_path or not all_properties_path.exists():
        raise FileNotFoundError(f"missing AllProperties CSV: {all_properties_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    results = build_results(root, schedule_path, args.schedule_encoding, all_properties_path)
    selected = select_subset(
        results=results,
        max_meshes=args.max_meshes,
        max_tasks=args.max_tasks,
        methods=args.methods,
        max_meshes_per_task=args.max_meshes_per_task,
    )
    if not selected:
        raise SystemExit("No matching high-confidence rows selected.")

    unique_mesh_uris = sorted({uri for result in selected for uri in result.mesh_uris})
    mesh_copy_records = (
        copy_meshes(root, output_dir, unique_mesh_uris) if args.copy_meshes else []
    )
    manifest = build_manifest(
        root=root,
        schedule_path=schedule_path,
        all_properties_path=all_properties_path,
        output_dir=output_dir,
        selected=selected,
        mesh_copy_records=mesh_copy_records,
        args=args,
    )

    (output_dir / "unity_subset_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_tasks_csv(output_dir, selected)
    write_readme(output_dir, manifest)

    print(json.dumps(manifest["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
