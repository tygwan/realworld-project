# 2026-04-24 - M1 - Refinery Schedule IDs Do Not Directly Map to Geometry Objects

**Severity**: Major
**Status**: Open
**Discovered by**: local dataset preflight
**Affects**: Phase 6 refinery 4D installation playback

---

## 1. Finding

The refinery schedule CSV contains 4,214 rows with a `동기화 ID` column, but
those IDs do not directly match the geometry `ObjectId`, `DisplayName`, or
`Category` fields. A naive hierarchy-prefix probe also did not find immediate
matches.

This blocks direct schedule-to-GameObject control in Unity until a mapping
strategy is defined.

## 2. Evidence

### 2.1 Reproducible Audit

```bash
python3 scripts/inventory_refinery_dataset.py "$REALWORLD_REFINERY_ROOT"
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

The schedule appears to be generated at a group/work-package level using values
such as area, unit, discipline, sub-discipline, and group. The geometry files
use object-level UUIDs and display/category names. These identifiers live at
different semantic levels.

### 3.2 Impact

The first Unity implementation needs a mapping layer before timeline playback.
Without it, schedule rows cannot reliably hide/show/color/move the intended
model objects.

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

Start with Option 2 for automated mapping exploration and keep Option 3 as the
fallback if automatic mapping is insufficient.

### 4.3 Action Items

- [ ] Parse `AllProperties_*.csv` for schedule-relevant fields.
- [ ] Build a normalized object registry from `geometry.csv` and `unified.csv`.
- [ ] Convert/normalize schedule CSV from CP949 to UTF-8 in local artifacts.
- [ ] Produce a mapping coverage report.
- [ ] Select 10-50 mapped objects for the first Unity import test.

### 4.4 Resolution Commit

Initial finding archived in 7b12d41fa2b4f3af9dc5cebcf82d0b34ca815d2b.

## 5. References

- Source script: `scripts/inventory_refinery_dataset.py`
- Analysis: `docs/analysis/2026-04-24-refinery-data-preflight.md`
- Plan: `docs/plan/2026-04-24-refinery-installation-simulation-plan.md`
