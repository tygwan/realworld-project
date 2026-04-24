# Refinery Unity Subset Preparation

**Date**: 2026-04-24
**Task**: generate high-confidence refinery subset for Unity import
**Commit**: TBD

---

## 1. Language / Content

| Language | File | Purpose |
|----------|------|---------|
| Python | `scripts/export_refinery_unity_subset.py` | Export a small schedule/mesh subset from the refinery mapping layer. |
| Markdown | `docs/analysis/2026-04-24-refinery-unity-subset-prep.md` | Record subset rationale, commands, output, and Unity implication. |
| Markdown | `docs/PROJECT-JOURNAL.md` | Record D10 and current project status. |
| TOML / env | `config/environment.example.toml`, `.env.example` | Add subset path/config placeholders for portable setup. |

## 2. Problem

The refinery dataset is available, but importing all 8,656 GLB files into Unity
before validating the schedule mapping would create too much scene and import
noise. The project needs a controlled first import target.

## 3. Analysis

The DXTnavis-aware mapper already identifies high-confidence schedule rows.
The first Unity import should use rows that map through stable methods and keep
the mesh count low enough for manual inspection.

Medium-confidence wildcard rows are intentionally postponed because they can
overlap and need duplicate-assignment handling before full schedule playback.

## 4. Solution

Added `scripts/export_refinery_unity_subset.py`. The default selection keeps:

- high-confidence rows only
- `pipeline_piperun_properties` and `hierarchy_path_descendants` methods
- no more than 30 meshes per task
- no more than 50 unique GLB files in the subset

The script writes:

```text
unity_subset_manifest.json
subset_tasks.csv
README.md
mesh/*.glb
```

## 5. Result

Verification:

```bash
python3 -m py_compile scripts/export_refinery_unity_subset.py scripts/map_refinery_schedule_to_assets.py
python3 scripts/export_refinery_unity_subset.py "$REALWORLD_REFINERY_ROOT" --output-dir artifacts/refinery/unity_subsets/mvp_high_confidence_001 --max-meshes 50 --copy-meshes
```

Observed subset:

```text
tasks: 9
unique object IDs: 50
unique mesh URIs: 50
copied meshes: 50
missing meshes: 0
```

Generated local payload:

```text
$REALWORLD_REFINERY_ROOT/subsets/mvp_high_confidence_001/
```

This gives Unity a small, schedule-linked GLB set for the first import
smoke test before any full-refinery import.
