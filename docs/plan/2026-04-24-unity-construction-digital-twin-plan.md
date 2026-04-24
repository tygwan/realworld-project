# Unity Construction-Site Digital Twin Plan

**Date**: 2026-04-24  
**Status**: Draft v0.1  
**Project**: realworld-project  
**Standards**: dev-standards@0.5.0

---

## 1. Goal

Create a Unity-based workflow that reconstructs a construction-site environment
from user-provided video and supporting/generated assets, then lets the user
directly control a person/avatar inside that environment for observation.

The intended outcome is an explorable scene where the user can inspect:

- site layout and spatial constraints
- person-level field of view
- occlusion and blind spots
- heavy-machine proximity zones
- object placement and movement constraints
- simplified physics interactions
- candidate risk scenarios for later review

This is an authoring and observation workflow. It is not a real-time autonomous
site-control system.

---

## 2. Core Interpretation

The project should treat the proposed AI stack as a set of environment-building
tools:

- **Unity**: interactive world, physics, avatar control, visibility tests,
  safety-zone visualization.
- **Unity MCP / Coplay / Coplay MCP**: editor automation, scene setup, asset
  import, object placement, script/component generation.
- **SAM 3 / SAM 3D**: segmentation, object/person extraction, candidate mesh
  generation.
- **Codex image generation / 3D generation tools**: canonical/proxy asset
  generation when real assets are missing.
- **V-JEPA 2.1 or video models**: offline video understanding, action
  anticipation, or scenario annotation; not the runtime safety authority.
- **Blender**: mesh cleanup, collider proxy creation, rig preparation,
  coordinate/scale normalization.

The central engineering rule is to split visual reconstruction from physical
simulation:

```text
Visual layer:
  point cloud / Gaussian Splat / textured mesh / generated mesh

Physics layer:
  box/capsule/convex colliders / navmesh / trigger zones / occlusion volumes /
  articulated machine prefabs
```

---

## 3. Target User Workflow

1. The user supplies a construction-site video or selected frames.
2. The pipeline extracts frames and candidate camera/reconstruction data.
3. Segmentation identifies people, heavy machines, vehicles, barriers,
   materials, and other site objects.
4. Static background reconstruction generates a visual environment.
5. Dynamic objects are converted into editable Unity prefabs or placeholders.
6. Blender cleans meshes and creates simplified collision proxies.
7. Unity imports the visual scene and proxy layer.
8. MCP/Coplay tools automate scene hierarchy, labels, colliders, zones, and
   first-person/third-person controls.
9. The user enters Play Mode, controls a person/avatar, and observes field of
   view, blind spots, proximity zones, and scenario behavior.
10. Findings, limitations, and decisions are recorded using `dev-standards`.

---

## 4. Proposed Architecture

```text
input/
  site_video.mp4
        |
        v
frame extraction + metadata
        |
        +--> segmentation/tracking
        |       SAM 3 / Grounded-SAM family / detector fallback
        |
        +--> reconstruction
        |       COLMAP / VGGT / MASt3R / MonST3R / Gaussian Splatting
        |
        +--> object/person asset generation
                SAM 3D Objects / SAM 3D Body / TRELLIS / Hunyuan3D / SF3D

intermediate artifacts
  frames, masks, tracks, point clouds, meshes, splats, camera poses
        |
        v
Blender cleanup
  mesh repair, decimation, origin/scale normalization, proxy colliders, rigs
        |
        v
Unity import
  visual layer + physics proxy layer + semantic tags + first-person controls
        |
        v
manual observation
  field of view, blind spots, machine zones, trigger events, scenario notes
```

---

## 5. Recommended Technical Tracks

### 5.1 Unity Authoring Track

Primary candidates:

- **Coplay Unity Plugin**: good for in-editor AI-assisted work, scene editing,
  iteration, and developer ergonomics.
- **Coplay MCP / CoplayDev Unity MCP**: better for reproducible external-agent
  automation from Codex-like tools.
- **Unity Editor scripts**: necessary for stable repeatable imports and runtime
  systems.

Recommendation:

Use Coplay/Coplay MCP for interactive authoring acceleration and direct Unity
Editor automation, but encode repeatable project behavior as Unity Editor
scripts or import pipeline scripts once patterns stabilize.

### 5.2 Reconstruction Track

Candidate tools:

- **COLMAP**: reliable baseline for SfM/MVS when frames have enough parallax and
  texture.
- **VGGT**: promising feed-forward reconstruction/camera/depth candidate for
  rapid experiments.
- **DUSt3R / MASt3R**: useful for uncalibrated image sets, but license and
  production constraints must be reviewed.
- **MonST3R**: promising for dynamic videos where people/equipment move.
- **Nerfstudio / Gaussian Splatting**: strong visual layer candidate, weak as a
  physics layer unless paired with proxies.

Recommendation:

Start with one short video and compare:

| Option | What to Measure |
|--------|-----------------|
| COLMAP | camera pose success, sparse/dense reconstruction quality, setup effort |
| VGGT or MASt3R | speed, camera/depth plausibility, ease of export |
| Gaussian Splatting | visual usability inside Unity, need for proxy geometry |

### 5.3 Segmentation and Tracking Track

Candidate tools:

- **SAM 3** for text-prompted image/video segmentation and tracking.
- **Grounded-SAM / GroundingDINO-style alternatives** if SAM 3 availability or
  performance is unsuitable.
- **Construction-specific detectors** later if site PPE/heavy-equipment accuracy
  becomes a bottleneck.

Target classes:

- person / worker
- excavator / crane / truck / forklift / loader
- barrier / cone / fence / material stack
- opening / edge / trench / scaffold
- vehicle path / exclusion zone marker

### 5.4 Object and Person 3D Track

Candidate tools:

- **SAM 3D Body** for human mesh/pose candidates.
- **SAM 3D Objects** for segmented object mesh candidates.
- **TRELLIS, Hunyuan3D 2.1, Stable Fast 3D** for proxy/canonical asset
  generation when real scan/CAD assets are unavailable.

Recommendation:

Do not treat generated 3D assets as factual site geometry. Use them as editable
prefabs, visual placeholders, or canonical machine/object classes. Site-specific
scale and placement must come from video reconstruction, manual calibration,
known measurements, BIM/CAD, or user correction.

### 5.5 Physics and Interaction Track

Unity runtime should implement:

- first-person or third-person avatar control
- camera/frustum-based field of view
- raycast occlusion checks
- blind-spot volumes
- trigger colliders for restricted zones
- proximity rules around heavy machines
- simplified machine articulation using explicit joint hierarchies
- timeline/event markers for observation notes

For heavy machinery, prefer articulated rigid structures over humanoid skeletons:

```text
excavator_base
  -> cabin_yaw
  -> boom
  -> arm
  -> bucket
```

For people, use Unity Humanoid or a simpler character controller depending on
the MVP fidelity target.

### 5.6 Video Understanding / Scenario Annotation Track

Candidate tools:

- **V-JEPA 2.1** for video representation and action anticipation experiments.
- **Video-language models** such as Qwen-VL/InternVideo-style systems for
  natural-language scene summaries and event annotations.
- **Rule engine in Unity** for authoritative geometry-based observation events.

Recommendation:

Use learned video models for offline analysis and annotation. Use Unity
geometry/raycast/trigger rules for deterministic in-scene events.

---

## 6. MVP Definition

### MVP Input

- One construction-site video, 30 seconds to 2 minutes.
- Prefer steady handheld, walking, drone, or fixed-camera footage with visible
  parallax and enough site texture.
- If possible, include one known scale reference such as a cone, worker height,
  vehicle dimension, marker board, or BIM/CAD measurement.

### MVP Output

A Unity scene containing:

- visual reconstruction of the static site environment
- manually correctable origin, scale, and orientation
- simple avatar/person controller
- semantic markers for people, machines, vehicles, barriers, and materials
- proxy colliders for ground, major obstacles, walls/fences, machine bodies
- visibility/raycast checks from the avatar viewpoint
- safety/exclusion-zone trigger volumes
- one or two heavy-machine proxy prefabs
- scene notes or event markers for observed hazards

### MVP Acceptance Criteria

- The user can enter Play Mode and move through the reconstructed environment.
- Major static structures align plausibly with the source video.
- Collision proxies prevent walking through major obstacles.
- The avatar field of view and occlusion checks respond to scene geometry.
- Heavy-machine zones can be visualized and entered/exited as trigger events.
- The project journal records the selected pipeline and unresolved limitations.

---

## 7. Phases

### Phase 0 - Planning and Standards Setup

Deliverables:

- repository scaffold
- project journal
- initial plan
- dependency registry
- first decision records

Exit criteria:

- `dev-standards` structure exists
- remote repository configured
- first planning commit created

### Phase 1 - Single-Video Reconstruction Spike

Deliverables:

- frame extraction script
- candidate reconstruction outputs from at least two approaches
- visual comparison notes
- import feasibility notes

Decision:

- choose the first reconstruction baseline for the MVP.

Suggested metrics:

- reconstruction success rate
- camera pose plausibility
- Unity import effort
- visual coherence
- runtime performance
- need for manual cleanup

### Phase 2 - Segmentation and Semantic Scene Layer

Deliverables:

- segmentation/tracking outputs
- class taxonomy
- masks/tracks exported with provenance
- Unity semantic tags or metadata import

Decision:

- choose the segmentation/tracking baseline.

### Phase 3 - Unity Scene Builder

Deliverables:

- Unity project setup
- importer/editor script or MCP workflow for scene creation
- visual layer import
- proxy collider layer
- avatar controller
- basic camera/raycast visibility system

Decision:

- choose the primary Unity automation path.

### Phase 4 - Asset and Machinery Proxy Library

Deliverables:

- initial prefabs for workers and selected heavy machines
- collider proxies
- simple articulated machine hierarchy
- Blender cleanup workflow

Decision:

- decide how much fidelity the MVP needs for machines and people.

### Phase 5 - Observation and Scenario Tools

Deliverables:

- blind-spot visualization
- safety-zone trigger events
- timeline/event log
- optional video-model annotations

Decision:

- decide whether V-JEPA 2.1 or a video-language model adds enough value for
  offline scenario annotation.

---

## 8. Validation Plan

Use `dev-standards` R10 for measurable decisions. The first likely comparisons:

### Reconstruction A/B

Question:
Which reconstruction baseline gives the best MVP result on one short site video?

Metrics:

- camera pose success
- static geometry coherence
- scale/orientation correction effort
- Unity import time
- runtime visual performance
- proxy-generation effort

### Unity Automation A/B

Question:
Which editor automation path should own repeatable scene setup?

Options:

- Coplay Unity Plugin
- Coplay MCP / Unity MCP
- direct Unity Editor scripts

Metrics:

- reproducibility
- speed
- failure recovery
- ability to version generated behavior
- privacy/data boundary clarity

### Asset Generation A/B

Question:
Which method produces the most useful editable proxy assets?

Options:

- SAM 3D from extracted/video frames
- TRELLIS/Hunyuan3D/Stable Fast 3D from generated or reference images
- manual/simple geometric prefabs

Metrics:

- mesh cleanup effort
- collider generation effort
- visual recognizability
- rig/articulation compatibility
- scale correction effort

---

## 9. Risks and Controls

| Risk | Impact | Control |
|------|--------|---------|
| Construction video contains sensitive data | Legal/privacy risk | Default to local/offline processing; require explicit approval for cloud tools |
| Reconstruction is visually plausible but geometrically wrong | Misleading observation | Maintain known limitations and use manual calibration/scale references |
| Generated assets imply false factual accuracy | Bad decisions from fictional geometry | Label generated assets as proxies only |
| Meshes are too complex for Unity physics | Poor runtime performance/unstable collisions | Generate simplified collider proxies |
| Tool ecosystem changes quickly | Broken setup | Pin commits/versions and document upgrades |
| MCP/Coplay actions are hard to reproduce | Hidden project state | Promote stable workflows into scripts once proven |
| Heavy-machine motion is oversimplified | Misleading safety zone behavior | Start with explicit limitations and refine only where needed |

---

## 10. Privacy and Data Handling

Default policy:

- Raw construction-site video remains local.
- Extracted frames remain local.
- Cloud image/video/3D generation is not used on site footage without explicit
  user approval.
- Generated placeholder assets may use synthetic prompts when no private site
  imagery is involved.
- Every external data path must be recorded in `PROJECT-JOURNAL.md`.

---

## 11. Immediate Next Actions

1. Initialize git and connect the provided GitHub remote.
2. Select one short sample video for Phase 1.
3. Create a `data/` layout and artifact naming convention.
4. Run a reconstruction spike with one baseline and one modern candidate.
5. Import the first visual layer into Unity.
6. Build the first simple proxy collider layer.
7. Add a controllable avatar and basic field-of-view raycasts.
8. Record the Phase 1 decision in the project journal.

---

## 12. Source References

- Coplay Unity Plugin: https://github.com/CoplayDev/coplay-unity-plugin
- CoplayDev Unity MCP: https://github.com/CoplayDev/unity-mcp
- SAM 3: https://github.com/facebookresearch/sam3
- SAM 3D Objects: https://github.com/facebookresearch/sam-3d-objects
- SAM 3D Body: https://github.com/facebookresearch/sam-3d-body
- V-JEPA 2: https://github.com/facebookresearch/vjepa2
- VGGT: https://vgg-t.github.io
- COLMAP: https://github.com/colmap/colmap
- DUSt3R: https://github.com/naver/dust3r
- MASt3R: https://github.com/naver/mast3r
- MonST3R: https://github.com/Junyi42/monst3r
- Nerfstudio Splatfacto: https://docs.nerf.studio/nerfology/methods/splat.html
- TRELLIS: https://github.com/microsoft/TRELLIS
- Hunyuan3D 2.1: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
- Stable Fast 3D: https://github.com/Stability-AI/stable-fast-3d
- Unity ArticulationBody: https://docs.unity3d.com/ScriptReference/ArticulationBody.html

