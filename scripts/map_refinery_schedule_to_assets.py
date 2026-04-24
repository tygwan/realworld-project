#!/usr/bin/env python3
"""Map refinery schedule rows to exported object/mesh identifiers.

The script reads local refinery metadata only. It does not copy mesh payloads
or write Unity assets. Its purpose is to validate schedule-to-object coverage
before importing a subset into Unity.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


UNKNOWN_PREFIX = "unknown "
ROOT_SEGMENTS = {"For Review.nwd", "TRAINING"}


@dataclass(frozen=True)
class ScheduleRow:
    row_index: int
    task_name: str
    sync_id: str
    task_type: str
    planned_start: str
    planned_end: str


@dataclass
class UnifiedObject:
    object_id: str
    parent_id: str
    display_name: str
    hierarchy_key: str
    has_mesh: bool
    mesh_uri: str
    mesh_quality: str


@dataclass
class MappingResult:
    row: ScheduleRow
    method: str
    confidence: str
    object_ids: list[str]
    mesh_uris: list[str]

    @property
    def object_count(self) -> int:
        return len(self.object_ids)

    @property
    def mesh_count(self) -> int:
        return len(self.mesh_uris)


def clean_value(value: str | None) -> str:
    text = (value or "").strip()
    if text.startswith("DisplayString:"):
        text = text[len("DisplayString:") :].strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        text = text[1:-1].strip()
    return text


def is_unknown(value: str) -> bool:
    return clean_value(value).lower().startswith(UNKNOWN_PREFIX)


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def auto_schedule_path(root: Path) -> Path | None:
    schedule_dir = root / "schedule"
    if not schedule_dir.exists():
        return None
    candidates = sorted(schedule_dir.glob("*.csv"))
    return candidates[-1] if candidates else None


def auto_all_properties_path(root: Path) -> Path | None:
    candidates = sorted(root.glob("AllProperties_*.csv"))
    return candidates[-1] if candidates else None


def read_schedule(path: Path, encoding: str) -> list[ScheduleRow]:
    with path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[ScheduleRow] = []
        for index, row in enumerate(reader, start=1):
            rows.append(
                ScheduleRow(
                    row_index=index,
                    task_name=clean_value(row.get("작업이름") or row.get("TaskName")),
                    sync_id=clean_value(row.get("동기화 ID") or row.get("SyncID")),
                    task_type=clean_value(row.get("작업 유형") or row.get("TaskType")),
                    planned_start=clean_value(
                        row.get("계획된 시작 날짜") or row.get("PlannedStart")
                    ),
                    planned_end=clean_value(row.get("계획된 끝 날짜") or row.get("PlannedEnd")),
                )
            )
    return [row for row in rows if row.sync_id]


def hierarchy_key_from_path(path: str) -> str:
    parts = [
        part.strip()
        for part in path.split(">")
        if part.strip() and part.strip() not in ROOT_SEGMENTS
    ]
    return "::".join(parts)


def read_unified(
    path: Path,
) -> tuple[
    dict[str, UnifiedObject],
    dict[str, list[str]],
    dict[str, list[str]],
    dict[str, list[str]],
]:
    csv.field_size_limit(sys.maxsize)

    objects: dict[str, UnifiedObject] = {}
    children: dict[str, list[str]] = defaultdict(list)
    path_to_ids: dict[str, list[str]] = defaultdict(list)
    display_to_ids: dict[str, list[str]] = defaultdict(list)

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            object_id = clean_value(row.get("ObjectId"))
            if not object_id:
                continue

            parent_id = clean_value(row.get("ParentId"))
            display_name = clean_value(row.get("DisplayName"))
            hierarchy_key = hierarchy_key_from_path(row.get("HierarchyPath", ""))
            item = UnifiedObject(
                object_id=object_id,
                parent_id=parent_id,
                display_name=display_name,
                hierarchy_key=hierarchy_key,
                has_mesh=clean_value(row.get("HasMesh")).lower() == "true",
                mesh_uri=clean_value(row.get("MeshUri")),
                mesh_quality=clean_value(row.get("MeshQuality")),
            )

            objects[object_id] = item
            if parent_id:
                children[parent_id].append(object_id)
            if hierarchy_key:
                path_to_ids[hierarchy_key].append(object_id)
            if display_name:
                display_to_ids[display_name].append(object_id)

    return objects, children, path_to_ids, display_to_ids


def read_all_properties(
    path: Path,
) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    pipeline_to_ids: dict[str, list[str]] = defaultdict(list)
    name_to_ids: dict[str, list[str]] = defaultdict(list)
    equipment_to_ids: dict[str, list[str]] = defaultdict(list)

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            object_id = clean_value(row.get("ObjectId"))
            if not object_id:
                continue

            pipeline = clean_value(row.get("SmartPlant 3D|Pipeline"))
            pipe_run = clean_value(row.get("SmartPlant 3D|PipeRun"))
            if pipeline or pipe_run:
                pipeline_to_ids[
                    f"{pipeline or 'Unknown Pipeline'}::{pipe_run or 'Unknown PipeRun'}"
                ].append(object_id)

            smartplant_name = clean_value(row.get("SmartPlant 3D|Name"))
            if smartplant_name:
                name_to_ids[smartplant_name].append(object_id)

            equipment_name = clean_value(row.get("SmartPlant 3D|Equipment Name"))
            if equipment_name:
                equipment_to_ids[equipment_name].append(object_id)

    return pipeline_to_ids, name_to_ids, equipment_to_ids


class ScheduleMapper:
    def __init__(
        self,
        objects: dict[str, UnifiedObject],
        children: dict[str, list[str]],
        path_to_ids: dict[str, list[str]],
        display_to_ids: dict[str, list[str]],
        pipeline_to_ids: dict[str, list[str]],
        property_name_to_ids: dict[str, list[str]],
        equipment_to_ids: dict[str, list[str]],
    ) -> None:
        self.objects = objects
        self.children = children
        self.path_to_ids = path_to_ids
        self.display_to_ids = display_to_ids
        self.pipeline_to_ids = pipeline_to_ids
        self.property_name_to_ids = property_name_to_ids
        self.equipment_to_ids = equipment_to_ids
        self._descendant_cache: dict[str, list[str]] = {}

    def descendants(self, object_id: str) -> list[str]:
        cached = self._descendant_cache.get(object_id)
        if cached is not None:
            return cached

        result: list[str] = []
        for child_id in self.children.get(object_id, []):
            result.append(child_id)
            result.extend(self.descendants(child_id))

        self._descendant_cache[object_id] = result
        return result

    def with_descendants(self, object_ids: list[str]) -> list[str]:
        result: list[str] = []
        for object_id in object_ids:
            result.append(object_id)
            result.extend(self.descendants(object_id))
        return unique(result)

    def path_prefix_ids(self, prefix: str) -> list[str]:
        if prefix in self.path_to_ids:
            return self.with_descendants(self.path_to_ids[prefix])

        prefix_with_separator = prefix + "::"
        result: list[str] = []
        for key, object_ids in self.path_to_ids.items():
            if key.startswith(prefix_with_separator):
                result.extend(object_ids)
        return unique(result)

    def mesh_uris(self, object_ids: list[str]) -> list[str]:
        return unique(
            [
                self.objects[object_id].mesh_uri
                for object_id in object_ids
                if object_id in self.objects and self.objects[object_id].mesh_uri
            ]
        )

    def lookup_leaf(self, leaf: str, prefix: str) -> tuple[str, list[str]]:
        indexes = [
            ("display_leaf", self.display_to_ids),
            ("property_name_leaf", self.property_name_to_ids),
            ("equipment_leaf", self.equipment_to_ids),
        ]
        for label, index in indexes:
            object_ids = unique(index.get(leaf, []))
            if object_ids:
                return prefix + label, object_ids
        return "unmatched", []

    def map_row(self, row: ScheduleRow) -> MappingResult:
        sync_id = row.sync_id

        if sync_id in self.pipeline_to_ids:
            object_ids = unique(self.pipeline_to_ids[sync_id])
            return MappingResult(
                row=row,
                method="pipeline_piperun_properties",
                confidence="high",
                object_ids=object_ids,
                mesh_uris=self.mesh_uris(object_ids),
            )

        if sync_id in self.path_to_ids:
            object_ids = self.with_descendants(self.path_to_ids[sync_id])
            return MappingResult(
                row=row,
                method="hierarchy_path_descendants",
                confidence="high",
                object_ids=object_ids,
                mesh_uris=self.mesh_uris(object_ids),
            )

        segments = sync_id.split("::")
        trimmed = list(segments)
        while trimmed and is_unknown(trimmed[-1]):
            trimmed.pop()

        if trimmed and len(trimmed) != len(segments):
            prefix = "::".join(trimmed)
            object_ids = self.path_prefix_ids(prefix)
            if object_ids:
                return MappingResult(
                    row=row,
                    method="trim_unknown_hierarchy_prefix",
                    confidence="medium",
                    object_ids=object_ids,
                    mesh_uris=self.mesh_uris(object_ids),
                )

            method, object_ids = self.lookup_leaf(trimmed[-1], "trim_unknown_")
            if object_ids:
                return MappingResult(
                    row=row,
                    method=method,
                    confidence="medium",
                    object_ids=object_ids,
                    mesh_uris=self.mesh_uris(object_ids),
                )

        real_segments = [segment for segment in segments if not is_unknown(segment)]
        if real_segments:
            method, object_ids = self.lookup_leaf(real_segments[-1], "leaf_")
            if object_ids:
                return MappingResult(
                    row=row,
                    method=method,
                    confidence="low",
                    object_ids=object_ids,
                    mesh_uris=self.mesh_uris(object_ids),
                )

        return MappingResult(
            row=row,
            method="unmatched",
            confidence="none",
            object_ids=[],
            mesh_uris=[],
        )


def result_to_csv_row(result: MappingResult, max_values: int) -> dict[str, str]:
    object_ids = result.object_ids[:max_values]
    mesh_uris = result.mesh_uris[:max_values]
    return {
        "row_index": str(result.row.row_index),
        "task_name": result.row.task_name,
        "sync_id": result.row.sync_id,
        "segment_count": str(result.row.sync_id.count("::") + 1),
        "method": result.method,
        "confidence": result.confidence,
        "object_count": str(result.object_count),
        "mesh_count": str(result.mesh_count),
        "object_ids_truncated": "true" if len(object_ids) < len(result.object_ids) else "false",
        "mesh_uris_truncated": "true" if len(mesh_uris) < len(result.mesh_uris) else "false",
        "object_ids": ";".join(object_ids),
        "mesh_uris": ";".join(mesh_uris),
    }


def summarize(
    root: Path,
    schedule_path: Path,
    all_properties_path: Path,
    results: list[MappingResult],
) -> dict[str, Any]:
    method_counts = Counter(result.method for result in results)
    confidence_counts = Counter(result.confidence for result in results)
    segment_counts = Counter(result.row.sync_id.count("::") + 1 for result in results)
    object_refs_by_method = Counter(
        {method: 0 for method in method_counts}
    )
    mesh_refs_by_method = Counter({method: 0 for method in method_counts})
    unique_objects: set[str] = set()
    unique_mesh_uris: set[str] = set()

    for result in results:
        object_refs_by_method[result.method] += result.object_count
        mesh_refs_by_method[result.method] += result.mesh_count
        unique_objects.update(result.object_ids)
        unique_mesh_uris.update(result.mesh_uris)

    unmatched = [result for result in results if result.method == "unmatched"]
    recommended_subset = [
        result
        for result in results
        if result.confidence == "high" and 0 < result.mesh_count <= 50
    ][:50]

    return {
        "dataset": {
            "root_name": root.name,
            "schedule_csv": schedule_path.name,
            "all_properties_csv": all_properties_path.name,
        },
        "coverage": {
            "schedule_rows": len(results),
            "matched_rows": len(results) - len(unmatched),
            "unmatched_rows": len(unmatched),
            "unique_mapped_object_ids": len(unique_objects),
            "unique_mapped_mesh_uris": len(unique_mesh_uris),
        },
        "method_counts": dict(method_counts.most_common()),
        "confidence_counts": dict(confidence_counts.most_common()),
        "segment_count_distribution": dict(sorted(segment_counts.items())),
        "object_reference_counts_by_method": dict(object_refs_by_method.most_common()),
        "mesh_reference_counts_by_method": dict(mesh_refs_by_method.most_common()),
        "unmatched_examples": [result.row.sync_id for result in unmatched[:25]],
        "recommended_high_confidence_subset": [
            {
                "row_index": result.row.row_index,
                "sync_id": result.row.sync_id,
                "method": result.method,
                "object_count": result.object_count,
                "mesh_count": result.mesh_count,
                "mesh_uris": result.mesh_uris[:5],
            }
            for result in recommended_subset
        ],
    }


def write_outputs(
    output_dir: Path,
    summary: dict[str, Any],
    results: list[MappingResult],
    max_values: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    csv_path = output_dir / "task_mapping.csv"
    fieldnames = list(result_to_csv_row(results[0], max_values).keys()) if results else []
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result_to_csv_row(result, max_values))


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
    parser.add_argument(
        "--all-properties",
        default="",
        help="AllProperties CSV path. Defaults to latest AllProperties_*.csv under root.",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Optional directory for summary.json and task_mapping.csv.",
    )
    parser.add_argument(
        "--max-values",
        type=int,
        default=30,
        help="Maximum object IDs and mesh URIs written per CSV row.",
    )
    args = parser.parse_args()

    if not args.root:
        raise SystemExit("Provide root path or set REALWORLD_REFINERY_ROOT.")

    root = Path(args.root)
    schedule_path = Path(args.schedule) if args.schedule else auto_schedule_path(root)
    all_properties_path = (
        Path(args.all_properties) if args.all_properties else auto_all_properties_path(root)
    )
    unified_path = root / "unified.csv"

    if not schedule_path or not schedule_path.exists():
        raise FileNotFoundError(f"missing schedule CSV: {schedule_path}")
    if not all_properties_path or not all_properties_path.exists():
        raise FileNotFoundError(f"missing AllProperties CSV: {all_properties_path}")
    if not unified_path.exists():
        raise FileNotFoundError(f"missing unified.csv: {unified_path}")

    schedule_rows = read_schedule(schedule_path, args.schedule_encoding)
    objects, children, path_to_ids, display_to_ids = read_unified(unified_path)
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
    results = [mapper.map_row(row) for row in schedule_rows]
    summary = summarize(root, schedule_path, all_properties_path, results)

    if args.output_dir:
        write_outputs(Path(args.output_dir), summary, results, args.max_values)
        summary["output_dir"] = args.output_dir

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
