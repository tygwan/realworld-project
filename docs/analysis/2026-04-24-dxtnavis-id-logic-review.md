# DXTnavis ID Logic Review

**Date**: 2026-04-24
**Status**: Mapping strategy identified
**Related**: M1, D8, refinery installation simulation

---

## Source Reviewed

Repository: `https://github.com/tygwan/DXTnavis.git`

Reviewed locally under `/tmp/DXTnavis` after cloning the repository for this
analysis.

Key files:

- `Models/ScheduleData.cs`
- `Services/PipelineScheduleBuilder.cs`
- `Services/SelectionSetService.cs`
- `Services/ObjectMatcher.cs`
- `ViewModels/PipelineScheduleViewModel.cs`
- `Resources/ScheduleProfiles/schedule-profiles.json`

## Core Finding

DXTnavis does not treat `SyncID` as one fixed identifier type. It depends on
the schedule generation mode.

| Mode | `SyncID` meaning | Object link source |
|------|------------------|--------------------|
| Object-level schedule | Object GUID / `InstanceGuid` | `SyncID` itself |
| Group-level schedule | Composite group key such as `Pipeline::PipeRun` or `Area::Unit::Discipline::...` | `CustomProperties["ObjectIds"]` |

In `PipelineScheduleBuilder.AssignTaskNames()`, group schedules are assigned:

```text
group.SyncId = string.Join("::", group.SlotValues)
```

In `PipelineScheduleBuilder.ConvertToScheduleData()`, group schedules then store
the actual object GUID list separately:

```text
CustomProperties["ObjectIds"] = guid1;guid2;guid3;...
```

`SelectionSetService.CreatePipelineSets()` later parses that `ObjectIds` list
and builds Navisworks selection sets by `InstanceGuid`.

## Important Caveat

The current DXTnavis `ExportTimeLinerCsv()` writes a numeric counter into the
CSV `동기화 ID` column for TimeLiner import. The user-provided refinery schedule
does not follow that export shape: its `동기화 ID` column contains composite
group keys directly.

For this project, that is useful. We should treat the user schedule's
`동기화 ID` as a semantic key, not as a Navisworks object GUID.

## Applied to Current Refinery Data

The original direct probe was correct but incomplete:

- `동기화 ID` does not equal `geometry.csv:ObjectId`
- `동기화 ID` does not equal `geometry.csv:DisplayName`
- `동기화 ID` does not equal `geometry.csv:Category`

Using the DXTnavis-aware interpretation, the mapping is much better:

| Mapping method | Task rows | Confidence | Interpretation |
|----------------|----------:|------------|----------------|
| `hierarchy_path_descendants` | 2,786 | High | `동기화 ID` equals a `unified.csv` hierarchy path after removing root labels. |
| `pipeline_piperun_properties` | 378 | High | `동기화 ID` equals `SmartPlant 3D|Pipeline::SmartPlant 3D|PipeRun`. |
| `trim_unknown_hierarchy_prefix` | 788 | Medium | trailing `Unknown ...` segments are treated as a wildcard group suffix. |
| `trim_unknown_display_leaf` | 145 | Medium | after trimming `Unknown ...`, the remaining leaf maps by display name. |
| `leaf_display_leaf` | 110 | Low | unknown-heavy rows map only by final display-name leaf. |
| `unmatched` | 7 | None | area-like values with no usable object/equipment leaf. |

Coverage from `scripts/map_refinery_schedule_to_assets.py`:

```text
schedule rows: 4214
matched rows: 4207
unmatched rows: 7
high confidence rows: 3164
unique mapped object ids: 12004
unique mapped mesh uris: 8654
```

The 7 unmatched rows are area-like keys such as:

```text
16.35 m^2::Unknown Unit::Unknown System::Unknown Equipment
```

## Implication for Unity

Unity should not import the schedule as direct GameObject IDs. It should import
a normalized mapping table:

```text
schedule row -> sync key -> mapping method -> object ids -> mesh uris
```

The first Unity sandbox should use only high-confidence rows with a small mesh
count. That subset is now generated as `mvp_high_confidence_001` and contains
9 schedule tasks mapped to 50 copied GLB files.

The medium-confidence wildcard rows can be useful later for broad group
visibility or coloring, but they can overlap heavily. They should not be used as
the first install/move test without duplicate-assignment handling.

## Decision

Treat M1 as mitigated but not closed:

- automated mapping coverage exists
- high-confidence subset is sufficient for the first Unity import test
- full schedule playback still needs duplicate handling and Unity-side
  validation

## Reproducible Command

```bash
python3 scripts/map_refinery_schedule_to_assets.py "$REALWORLD_REFINERY_ROOT"
```

Optional local artifact output:

```bash
python3 scripts/map_refinery_schedule_to_assets.py \
  "$REALWORLD_REFINERY_ROOT" \
  --output-dir artifacts/refinery/schedule_mapping/latest
```
