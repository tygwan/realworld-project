# Refinery Installation Sequencing Simulation Plan

**Date**: 2026-04-24
**Status**: Planned later track
**Project**: realworld-project
**Standards**: dev-standards@0.5.0

---

## 1. Purpose

This plan records a later project track for simulating the installation order
of a refinery facility model in Unity.

The user has:

- a refinery facility `.glb` model
- a CSV process/construction plan describing the installation order

The refinery model is unrelated to the construction-site video location used by
the video-reconstruction track. It should therefore become a separate sandbox
and 4D installation sequencing track, not evidence for the video site.

---

## 2. Core Idea

Unity can simulate planned installation sequencing by mapping schedule rows to
objects inside the GLB scene hierarchy.

The simulation does not require a physically detailed crane at first. The first
useful version can treat each scheduled item as a controlled object with states:

```text
not_started -> staged -> moving -> installed -> inspected
```

Once the schedule playback works, the project can add:

- crane or generic installer agents
- movement paths
- lifting/placement animation
- collision and clearance checks
- exclusion zones and safety volumes
- work-package and date sliders
- progress coloring and status filters

---

## 3. Required Data When This Track Starts

The user will provide the actual GLB and CSV when the project reaches this
stage. Until then, the repository stores only the plan and expected schemas.

### 3.1 GLB Requirements

The GLB should ideally preserve object names or node names that can be mapped to
schedule rows.

Useful GLB properties:

- stable node/object names
- meaningful hierarchy by area, system, module, or equipment
- consistent unit scale
- transform/origin information preserved
- materials/textures packaged or referenced clearly

If node names do not match the schedule, a mapping CSV will be needed.

### 3.2 Schedule CSV Requirements

Minimum useful columns:

```csv
task_id,object_id,task_name,sequence,start_date,end_date,status
```

Recommended columns:

```csv
task_id,object_id,task_name,sequence,start_date,end_date,from_zone,to_zone,installer_type,predecessors,work_package,notes
```

Where:

- `task_id`: stable task identifier
- `object_id`: schedule-side object identifier
- `sequence`: planned install order
- `start_date` / `end_date`: planned time window
- `from_zone`: staging or storage zone
- `to_zone`: final installation zone
- `installer_type`: crane, forklift, transporter, generic installer, manual,
  or TBD
- `predecessors`: optional task dependencies

### 3.3 Optional Mapping CSV

If the schedule `object_id` does not match GLB node names, provide:

```csv
object_id,glb_node_path,notes
PIPE_RACK_01,Scene/AreaA/PipeRack_001,
PUMP_07,Scene/Equipment/Pump_07_Model,
```

---

## 4. Unity Simulation Architecture

```text
refinery_model.glb
        |
        v
GLB importer
        |
        v
Unity scene hierarchy + object registry
        |
        +----------------------+
                               |
installation_schedule.csv      |
        |                      |
        v                      |
schedule parser                |
        |                      |
        v                      |
timeline / task graph ---------+
        |
        v
installation simulation controller
        |
        +--> object state changes
        +--> date/sequence slider
        +--> movement animation
        +--> installer agent assignment
        +--> collision/clearance checks
        +--> progress visualization
```

---

## 5. Simulation Levels

### Level 1 - 4D Playback

Objects are shown, hidden, ghosted, or colored according to planned sequence and
date.

Deliverables:

- CSV parser
- GLB object registry
- object-to-task mapping
- timeline slider
- state coloring
- install order playback

This level is the first target.

### Level 2 - Kinematic Installation

Objects move from a staging position to the final installed position using
scripted paths or generated paths.

Deliverables:

- staging zones
- movement curves
- simple installer actor
- path preview
- placement animation

This level does not need full crane physics.

### Level 3 - Equipment-Assisted Installation

A crane, forklift, gantry, transporter, or abstract installer agent moves
scheduled items.

Deliverables:

- installer agent assignment
- lifting radius/working envelope visualization
- attachment points or bounding-box pickup points
- equipment path and rotation limits
- basic collision checks

### Level 4 - Constructability and Safety Checks

The simulation checks whether planned installation steps conflict with spatial
constraints.

Deliverables:

- collision and clearance detection
- restricted-zone violations
- path blockage reports
- predecessor/order violations
- installation feasibility notes

This level should be added only after Levels 1-2 are stable.

---

## 6. Recommended Project Timing

The refinery installation track should start after the Unity import foundation
exists.

| Phase | Use of refinery GLB / schedule CSV |
|-------|------------------------------------|
| Phase 1 | Do not use; focus on construction-video reconstruction spike |
| Phase 2 | Do not use; focus on segmentation/semantic scene layer |
| Phase 3 | Use GLB for import smoke test and scene hierarchy registry |
| Phase 4 | Use GLB for collider/occlusion proxies and sandbox navigation |
| Phase 6 | Add CSV schedule parser and Level 1 4D playback |
| Phase 7 | Add kinematic movement, installer agents, and constructability checks |

The user will provide the GLB and CSV when Phase 6 begins, unless Phase 3 needs
the GLB earlier for import validation.

---

## 7. MVP for This Track

The first refinery sequencing MVP should do the following:

1. Import the refinery GLB into Unity.
2. Build a registry of GLB nodes/GameObjects.
3. Load the installation schedule CSV.
4. Map CSV `object_id` values to Unity objects.
5. Show a date/sequence slider.
6. Change object visibility/color by installation state.
7. Play the planned sequence from start to finish.
8. Log unmapped schedule rows and unmapped GLB objects.

This MVP is enough to validate whether the GLB and CSV are structurally usable.

---

## 8. Key Risks

| Risk | Impact | Control |
|------|--------|---------|
| GLB node names do not match CSV object IDs | Schedule cannot control model objects | Add a mapping CSV |
| GLB is one merged mesh | Individual installation steps cannot move separately | Split model in Blender or request source model with hierarchy |
| CSV lacks dates or sequence | Timeline playback is ambiguous | Use sequence-only playback first |
| CSV lacks staging/final zone data | Movement paths are speculative | Start with visibility/color playback |
| Full crane physics is attempted too early | Implementation stalls | Start with abstract installer agents and kinematic movement |
| Refinery track gets mixed with construction-video track | Invalid conclusions | Keep separate scenes, configs, and docs |

---

## 9. Initial Implementation Tasks When Data Arrives

1. Inspect GLB hierarchy and count controllable nodes.
2. Inspect CSV schema and identify task/object columns.
3. Create or derive object mapping.
4. Build a Unity object registry.
5. Implement CSV parser and validation report.
6. Implement Level 1 4D playback.
7. Record data quality findings if mappings are missing or ambiguous.
8. Decide whether Level 2 kinematic movement is feasible from available data.
