# DXTnavis ID Logic Review

**Date**: 2026-04-24
**Task**: refinery schedule mapping investigation
**Commit**: d7c85a78ed6009ba48c9851ca5c37ce8861744a9

---

## 1. Language / Content

| Language | File | Purpose |
|----------|------|---------|
| Python | `scripts/map_refinery_schedule_to_assets.py` | Build refinery schedule-to-object/mesh mapping coverage. |
| Markdown | `docs/analysis/2026-04-24-dxtnavis-id-logic-review.md` | Record DXTnavis ID semantics and mapping result. |
| Markdown | `docs/findings/2026-04-24-M1-refinery-schedule-object-mapping/README.md` | Update M1 with mitigation evidence. |
| Markdown | `docs/PROJECT-JOURNAL.md` | Record D9 and project status. |

## 2. Problem

The refinery schedule `동기화 ID` values did not directly match object IDs or
display names. The user pointed to DXTnavis as the source of the relevant ID
logic.

## 3. Analysis

DXTnavis uses different ID semantics by schedule granularity:

- object-level schedule: `SyncID` can be a GUID
- group-level schedule: `SyncID` is a composite key and object IDs are stored
  separately

The current refinery schedule contains composite keys. Therefore Unity needs a
mapping table, not direct ID lookup.

## 4. Solution

Added `scripts/map_refinery_schedule_to_assets.py`, which maps schedule rows
using:

- `SmartPlant 3D|Pipeline::SmartPlant 3D|PipeRun`
- `unified.csv` hierarchy path descendants
- trailing `Unknown ...` suffix trimming
- display/equipment-name fallbacks
- confidence labels per method

## 5. Result

Verification:

```bash
python3 -m py_compile scripts/map_refinery_schedule_to_assets.py scripts/inventory_refinery_dataset.py
python3 scripts/map_refinery_schedule_to_assets.py /mnt/c/Users/x8333/Desktop/AI_PJT/unity/refinery
```

Observed coverage:

```text
matched rows: 4207 / 4214
high confidence rows: 3164
unique mapped mesh URIs: 8654
```

Local artifact output was generated under
`artifacts/refinery/schedule_mapping/latest/`; this directory is ignored by git.
