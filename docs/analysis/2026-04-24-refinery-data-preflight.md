# Refinery Data Preflight

**Date**: 2026-04-24
**Status**: Initial inspection complete; DXTnavis-aware mapping added
**Related**: D6, D7, M1, D9

---

## Input Location

The user placed refinery data under a local Windows data directory. The exact
machine path is kept in local `.env`; the committed repo records only the
structure and metadata.

Observed structure:

```text
unity/
├── refinery/
│   ├── mesh/
│   ├── schedule/
│   ├── gap_fallback.fbx
│   ├── geometry.csv
│   ├── manifest.json
│   ├── unified.csv
│   ├── validation.csv
│   └── ...
└── video/
```

## Inventory Summary

| Item | Observed Value |
|------|----------------|
| Export generator | DXTnavis v1.4.0 |
| Export date | 2026-04-18T22:36:27Z |
| Manifest object count | 12,009 |
| Manifest mesh count | 8,656 |
| GLB files under `mesh/` | 8,656 |
| Refinery data size | about 550 MB |
| Mesh folder size | about 341 MB |
| Fallback FBX | `gap_fallback.fbx`, about 23 MB |
| Schedule rows | 4,214 |
| Schedule encoding | CP949 |

## Mesh Quality Counts

From `geometry.csv`:

| MeshQuality | Count |
|-------------|------:|
| full_mesh | 7,189 |
| skipped_container | 3,353 |
| fbx_supplemented | 788 |
| box_placeholder | 671 |
| line_mesh | 8 |

## Schedule CSV

Observed columns after CP949 decoding:

```text
작업이름, 동기화 ID, 작업 유형, 계획된 시작 날짜, 계획된 끝 날짜
```

The user said the dates can be ignored and the schedule can be used as order.
That is a good MVP choice. Use row order or a derived sequence number first.

## Initial Direct Mapping Result

The schedule `동기화 ID` values do not directly match:

- `geometry.csv` `ObjectId`
- `geometry.csv` `DisplayName`
- `geometry.csv` `Category`
- a naive transformed `unified.csv` `HierarchyPath` prefix sample

This means Unity playback should not assume direct ID mapping. A mapping layer
is required.

## DXTnavis-Aware Mapping Result

After reviewing `https://github.com/tygwan/DXTnavis.git`, the right
interpretation is that `동기화 ID` can be a group key rather than an object ID.
The new mapper combines hierarchy paths and SmartPlant `Pipeline::PipeRun`
properties.

Command:

```bash
python3 scripts/map_refinery_schedule_to_assets.py "$REALWORLD_REFINERY_ROOT"
```

Observed result:

| Metric | Value |
|--------|------:|
| Schedule rows | 4,214 |
| Matched rows | 4,207 |
| Unmatched rows | 7 |
| High-confidence rows | 3,164 |
| Medium-confidence rows | 933 |
| Low-confidence rows | 110 |
| Unique mapped object IDs | 12,004 |
| Unique mapped mesh URIs | 8,654 |

The 933 medium-confidence rows include wildcard-style mappings where trailing
`Unknown ...` schedule segments are interpreted as broad group suffixes. These
are useful later, but they can overlap heavily and need duplicate handling in
Unity.

## Recommended Next Step

Do not start by manually importing all 8,656 GLB files into Unity.

First implement:

1. a dataset preflight command
2. a schedule normalization step that converts CP949 CSV to UTF-8
3. a schedule-to-object mapping strategy - done for preflight
4. a small Unity import test with 10-50 high-confidence GLB objects

Only after that should the full Unity project setup begin.
