# Asset Registry

**Status**: Draft
**Last updated**: 2026-04-24

This registry tracks user-provided and generated assets without requiring the
asset binaries to be committed.

## Policy

- Private source videos, extracted frames, model weights, reconstruction
  outputs, and user-provided `.glb` files stay out of git by default.
- Asset metadata and intended use are committed here.
- If an asset is unrelated to the source video location, it must be labeled as
  unrelated and must not be used as evidence for site reconstruction.

## Assets

| ID | Asset | Type | Relationship to Site Video | Git Policy | Intended Use | Phase |
|----|-------|------|----------------------------|------------|--------------|-------|
| A1 | User-provided refinery facility model | `.glb` | Unrelated to provided construction-site video | Do not commit by default | Validate GLB import, materials, scale/origin handling, collider proxy generation, separate refinery sandbox scene, and later 4D installation sequencing | Phase 3/4 and Phase 6/7 |
| A2 | User-provided refinery installation process plan | `.csv` | Unrelated to provided construction-site video | Do not commit by default until approved | Drives object installation order, task timeline, and schedule playback for the refinery sandbox | Phase 6/7 |

## A1 - User-Provided Refinery Facility GLB

**Known context**:
The user has a refinery facility `.glb` file. The model is not related to the
physical location shown in the future construction-site video.

Observed dataset metadata:

- DXTnavis export: v1.4.0
- Manifest object count: 12,009
- Manifest mesh count: 8,656
- GLB files under `mesh/`: 8,656
- Fallback mesh file: `gap_fallback.fbx`

**Use it for**:

- GLB import pipeline validation
- Unity material/texture handling checks
- Blender cleanup workflow validation
- collider proxy generation experiments
- scale/origin/unit normalization experiments
- separate sandbox scene for refinery-specific observation workflows
- 4D installation sequencing once paired with the process-plan CSV

**Do not use it for**:

- reconstructing the user-provided construction-site video location
- validating map reconstruction accuracy for that video
- deriving site-specific safety conclusions from unrelated geometry

**Recommended timing**:

- Phase 3: use it as an import smoke-test asset when building the Unity scene
  builder.
- Phase 4: use it more seriously for collider proxies, occlusion volumes, and
  large industrial facility navigation tests.
- Phase 6: pair it with the process-plan CSV for 4D installation playback.
- Phase 7: add kinematic movement, installer agents, and constructability
  checks if the data supports those interactions.

## A2 - User-Provided Refinery Installation Process Plan CSV

**Known context**:
The user has a CSV that describes the installation order for the refinery
model. The data will be provided when the project reaches the installation
simulation stage.

The schedule data is now available locally. Initial inspection found:

- one current schedule CSV under `schedule/`
- CP949 encoding
- 4,214 schedule rows
- columns: `작업이름`, `동기화 ID`, `작업 유형`, `계획된 시작 날짜`, `계획된 끝 날짜`
- row order can be used as the first sequencing source
- `동기화 ID` is a semantic group key, not a direct object GUID
- DXTnavis-aware mapping currently matches 4,207 of 4,214 rows
- high-confidence mapping covers 3,164 rows

**Use it for**:

- schedule-driven object state changes
- date/sequence slider playback
- planned installation order visualization
- object-to-task mapping validation
- later movement/installer-agent simulation

**Minimum expected columns**:

```csv
작업이름,동기화 ID,작업 유형,계획된 시작 날짜,계획된 끝 날짜
```

For Unity import, derive a normalized mapping table with:

```csv
row_index,sync_id,method,confidence,object_ids,mesh_uris
```

**Recommended additional columns**:

```csv
from_zone,to_zone,installer_type,predecessors,work_package,notes
```

**Do not use it for**:

- construction-site video reconstruction timing
- assumptions about the unrelated construction-video location

**Related plan**:
- [Refinery installation simulation plan](../../plan/2026-04-24-refinery-installation-simulation-plan.md)
- [DXTnavis ID logic review](../../analysis/2026-04-24-dxtnavis-id-logic-review.md)
