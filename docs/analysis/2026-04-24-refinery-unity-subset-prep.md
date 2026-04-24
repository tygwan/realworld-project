# Refinery Unity Subset Preparation

**Date**: 2026-04-24
**Status**: Generated
**Related**: D8, D9, M1, refinery installation simulation

---

## Purpose

The full refinery dataset has 8,656 GLB files. Importing everything into Unity
before validating schedule mapping, scale, hierarchy, and material behavior
would make the first scene setup hard to debug.

This step creates a small high-confidence import subset that can be copied into
or referenced from a Unity project before attempting a full refinery import.

## Generated Subset

Default subset name:

```text
mvp_high_confidence_001
```

Local generated outputs:

```text
artifacts/refinery/unity_subsets/mvp_high_confidence_001/
$REALWORLD_REFINERY_ROOT/subsets/mvp_high_confidence_001/
```

The repo artifact directory is ignored by git. The data-root copy is also a
local payload and should not be committed unless explicitly approved.

Generated files:

```text
README.md
subset_tasks.csv
unity_subset_manifest.json
mesh/*.glb
```

## Selection Rule

The subset uses only high-confidence mapping rows from
`scripts/map_refinery_schedule_to_assets.py`.

Included methods:

```text
pipeline_piperun_properties
hierarchy_path_descendants
```

Excluded for the first Unity import:

- medium-confidence `Unknown ...` wildcard mappings
- low-confidence display-leaf-only mappings
- rows with more than 30 meshes in one task
- rows that would push the subset above 50 unique GLB files

This keeps the first import small enough to inspect manually while preserving a
real schedule-to-object-to-mesh relationship.

## Observed Result

```json
{
  "task_count": 9,
  "unique_object_id_count": 50,
  "unique_mesh_uri_count": 50,
  "copied_mesh_count": 50,
  "missing_mesh_count": 0
}
```

The selected rows start with early pipeline/branching schedule keys such as:

```text
P-204::P-204-4"-1C0031-
P-204::P-204-3"-1C0031-
U05111-P::U05-10-P-0202-1C0031_ReinforcedBranching
```

## Reproducible Commands

Generate an ignored repo-local artifact:

```bash
python3 scripts/export_refinery_unity_subset.py \
  "$REALWORLD_REFINERY_ROOT" \
  --output-dir artifacts/refinery/unity_subsets/mvp_high_confidence_001 \
  --max-meshes 50 \
  --copy-meshes
```

Generate the payload copy under the external refinery data root:

```bash
python3 scripts/export_refinery_unity_subset.py \
  "$REALWORLD_REFINERY_ROOT" \
  --output-dir "$REALWORLD_REFINERY_ROOT/subsets/mvp_high_confidence_001" \
  --max-meshes 50 \
  --copy-meshes
```

## Unity Implication

Use this subset as the first Unity import target. The MVP Unity import should:

- import the 50 copied GLB files
- preserve object IDs or store them as metadata on imported GameObjects
- read `unity_subset_manifest.json`
- drive visibility or install-state changes from the 9 schedule tasks
- validate scale/origin, material behavior, and hierarchy before full import

The local machine has Unity `6000.3.4f1` installed. Unity's official release
notes for that version list `com.unity.cloud.gltfast@6.14.1` as an added
package, so the first GLB import path should start with Unity glTFast and then
fall back to custom import tooling only if this subset exposes a blocking issue.

Reference: [Unity 6000.3.4f1 release notes](https://unity.com/releases/editor/whats-new/6000.3.4f1)

## Remaining Risks

- Unity still needs to validate whether each GLB imports as an inspectable
  GameObject hierarchy or as flattened mesh payloads.
- Full schedule playback still needs duplicate-assignment handling for
  medium-confidence wildcard rows.
- The refinery dataset remains unrelated to the construction-site video and
  must stay in a separate sandbox scene.
