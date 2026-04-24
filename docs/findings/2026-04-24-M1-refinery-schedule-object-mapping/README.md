# 2026-04-24 - M1 - Refinery Schedule IDs Do Not Directly Map to Geometry Objects

**Severity**: Major
**Status**: Mitigated - Unity validation pending
**Discovered by**: local dataset preflight
**Affects**: Phase 6 refinery 4D installation playback

---

## 1. Finding

The refinery schedule CSV contains 4,214 rows with a `동기화 ID` column, but
those IDs do not directly match the geometry `ObjectId`, `DisplayName`, or
`Category` fields.

DXTnavis review showed that this is expected for group-level schedules:
`동기화 ID` can be a composite group key, while actual object links are derived
from hierarchy paths, SmartPlant properties, or a separate `ObjectIds` list.

## 2. Evidence

### 2.1 Reproducible Audit

```bash
python3 scripts/inventory_refinery_dataset.py "$REALWORLD_REFINERY_ROOT"
```

DXTnavis-aware mapping audit:

```bash
python3 scripts/map_refinery_schedule_to_assets.py "$REALWORLD_REFINERY_ROOT"
```

Observed relevant output:

```json
{
  "coverage": {
    "schedule_rows": 4214,
    "matched_rows": 4207,
    "unmatched_rows": 7,
    "unique_mapped_object_ids": 12004,
    "unique_mapped_mesh_uris": 8654
  },
  "confidence_counts": {
    "high": 3164,
    "medium": 933,
    "low": 110,
    "none": 7
  }
}
```

Expected relevant output:

```json
{
  "schedule": {
    "rows": 4214,
    "unique_sync_ids": 4214
  },
  "mapping_probe": {
    "sync_matches_object_id": 0,
    "sync_matches_display_name": 0,
    "sync_matches_category": 0
  }
}
```

### 2.2 Data Artifacts

- `geometry.csv` - object geometry metadata and mesh URIs
- `unified.csv` - hierarchy path and object metadata
- `schedule/*.csv` - CP949-encoded installation sequence CSV

### 2.3 Visualizations

None yet.

## 3. Analysis

### 3.1 Root Cause

The schedule is generated at a group/work-package level using values such as
area, unit, discipline, sub-discipline, group, pipeline, and pipe run. The
geometry files use object-level UUIDs and hierarchy records. These identifiers
live at different semantic levels.

DXTnavis confirmed the intended pattern:

- object-level task: `SyncID` can be an object GUID
- group-level task: `SyncID` is a composite key and the linked object IDs are a
  separate collection

### 3.2 Impact

The first Unity implementation still needs a mapping import layer before
timeline playback. The blocker is reduced from "no mapping strategy" to
"validate mapping table and duplicate handling inside Unity."

### 3.3 Related Known Issues

- The GLB set contains 8,656 files and should be imported in a controlled subset
  first.
- The schedule CSV is CP949-encoded and should be normalized or decoded
  explicitly.

## 4. Resolution

### 4.1 Options Considered

| Option | Approach | Pros | Cons | Time |
|--------|----------|------|------|------|
| 1 | Use schedule row order only and manually map a small subset | Fastest MVP | Not scalable |
| 2 | Derive mapping from SmartPlant properties such as Area/Pipeline/Equipment fields | Likely meaningful | Requires parsing `AllProperties` and schedule semantics |
| 3 | Ask user to provide explicit object-to-task mapping CSV | Most reliable | Requires extra preparation |
| 4 | Generate grouped bounding boxes from schedule groups and animate groups abstractly | Useful without exact objects | Less visually precise |

### 4.2 Selected Approach

Use Option 2. The repository now has a DXTnavis-aware mapping script that
combines:

- `unified.csv` hierarchy paths
- `AllProperties_*.csv` `SmartPlant 3D|Pipeline` and `SmartPlant 3D|PipeRun`
- display-name and equipment-name fallback
- trailing `Unknown ...` group suffix trimming

### 4.3 Action Items

- [x] Parse `AllProperties_*.csv` for schedule-relevant fields.
- [x] Build a normalized object registry from `geometry.csv` and `unified.csv`.
- [ ] Convert/normalize schedule CSV from CP949 to UTF-8 in local artifacts.
- [x] Produce a mapping coverage report.
- [x] Select 10-50 mapped objects for the first Unity import test.
- [ ] Validate duplicate assignment handling for wildcard group rows.

### 4.4 Resolution Commit

Initial finding archived in 7b12d41fa2b4f3af9dc5cebcf82d0b34ca815d2b.
Mitigation added after DXTnavis ID review.

## 5. References

- Source script: `scripts/inventory_refinery_dataset.py`
- Mapping script: `scripts/map_refinery_schedule_to_assets.py`
- Analysis: `docs/analysis/2026-04-24-refinery-data-preflight.md`
- DXTnavis ID review:
  `docs/analysis/2026-04-24-dxtnavis-id-logic-review.md`
- Plan: `docs/plan/2026-04-24-refinery-installation-simulation-plan.md`
