# Project Journal - realworld-project

> Single portal for the Unity construction-site reconstruction and observation
> project. This document follows `dev-standards` R1/R4/R6.

**Standards**: dev-standards@0.5.0  
**Last updated**: 2026-04-24

---

## At a Glance

- **Current phase**: Phase 0/3 bridge - refinery subset prepared for Unity import
- **Project goal**: Build a Unity environment from construction-site video and
  generated/derived 3D assets so a human can directly control a person/avatar
  and observe site conditions.
- **Runtime target**: Human-operated simulation/observation, not autonomous
  real-time safety control.
- **Current artifact**:
  [Refinery Unity subset prep](analysis/2026-04-24-refinery-unity-subset-prep.md)
- **Open findings**: 1 validation-pending mitigation
- **Next step**: create or open the Windows-native Unity project and import the
  50-GLB high-confidence refinery subset.

---

## 1. Quick Problem Index

### Data / Design Issues

| ID | Date | Severity | Title | Status | Archive |
|----|------|----------|-------|--------|---------|
| M1 | 2026-04-24 | Major | Refinery schedule IDs do not directly map to geometry objects | Mitigated - Unity validation pending | [M1 archive](findings/2026-04-24-M1-refinery-schedule-object-mapping/) |

### Known Limitations

| ID | Description | Impact | Status |
|----|-------------|--------|--------|
| L1 | Generated images and generated 3D assets cannot be treated as factual site geometry. | Use generated assets only as editable proxies or canonical placeholders. | Accepted |
| L2 | Video reconstruction output is not automatically physics-ready. | Maintain a separate collider/proxy layer in Unity. | Accepted |
| L3 | MCP/Coplay tooling is suitable for authoring, not high-frequency runtime control. | Keep runtime behavior inside Unity scripts and explicit simulation components. | Accepted |
| L4 | The user-provided refinery GLB is unrelated to the construction-site video location. | Use it only for import/proxy sandbox work, not as reconstruction evidence. | Accepted |
| L5 | The refinery installation CSV is unrelated to the construction-site video location. | Use it only for the refinery 4D installation sandbox, not as timing evidence for the video site. | Accepted |
| L6 | Unity may run from Windows while the current repo is in WSL. | Prefer a Windows-native clone for Unity and sync through git; keep large data local. | Accepted |

### Design Decisions

| ID | Decision | When | Where documented |
|----|----------|------|------------------|
| D1 | Treat AI/MCP/Coplay as environment-authoring tools, not runtime controllers. | 2026-04-24 | [D1](#d1---use-aimcpcoplay-for-authoring-not-runtime-control) |
| D2 | Separate visual reconstruction from Unity physics proxies. | 2026-04-24 | [D2](#d2---separate-visual-reconstruction-from-physics-proxies) |
| D3 | Use `dev-standards` as the project management/documentation contract. | 2026-04-24 | [D3](#d3---use-dev-standards-for-project-management) |
| D4 | Manage environments as layered requirements and registries. | 2026-04-24 | [D4](#d4---manage-environments-as-layered-requirements-and-registries) |
| D5 | Treat the refinery GLB as an unrelated sandbox/import asset. | 2026-04-24 | [D5](#d5---treat-the-refinery-glb-as-an-unrelated-sandboximport-asset) |
| D6 | Add a later refinery GLB + CSV 4D installation simulation track. | 2026-04-24 | [D6](#d6---add-a-later-refinery-glb--csv-4d-installation-simulation-track) |
| D7 | Use a split control-plane/local-payload storage model. | 2026-04-24 | [D7](#d7---use-a-split-control-planelocal-payload-storage-model) |
| D8 | Run refinery data preflight before Unity project setup. | 2026-04-24 | [D8](#d8---run-refinery-data-preflight-before-unity-project-setup) |
| D9 | Treat refinery schedule `동기화 ID` as a semantic mapping key. | 2026-04-24 | [D9](#d9---treat-refinery-schedule-sync-id-as-a-semantic-mapping-key) |
| D10 | Use a 50-GLB high-confidence refinery subset as the first Unity import target. | 2026-04-24 | [D10](#d10---use-a-50-glb-high-confidence-refinery-subset-as-the-first-unity-import-target) |

---

## 2. Timeline

```text
2026-04-24   Initialized planning scaffold with dev-standards@0.5.0.   ae68a05
2026-04-24   Recorded initial Unity reconstruction/observation plan.     ae68a05
2026-04-24   Added environment and asset management scaffold.             9d9a09c
2026-04-24   Planned refinery GLB + CSV installation simulation track.    6d23276
2026-04-24   Added data directory and Unity/WSL file management policy.   06b8b19
2026-04-24   Inventoried local refinery GLB/CSV dataset and found M1.     7b12d41
2026-04-24   Reviewed DXTnavis ID logic and added mapping coverage script. d7c85a7
2026-04-24   Generated 50-GLB high-confidence Unity import subset.         TBD
```

---

## 3. Findings

### M1 - Refinery Schedule IDs Do Not Directly Map to Geometry Objects

Initial preflight found that the schedule CSV's `동기화 ID` values do not
directly match `geometry.csv` `ObjectId`, `DisplayName`, or `Category` values.
DXTnavis review showed that this is expected for group-level schedules.

The mitigation script maps 4,207 of 4,214 schedule rows by combining
`unified.csv` hierarchy paths, SmartPlant `Pipeline::PipeRun` properties, and
bounded fallback rules. A 9-task / 50-GLB high-confidence subset now exists for
the first Unity import test. Unity validation and duplicate handling are still
pending.

Archive: [findings/2026-04-24-M1-refinery-schedule-object-mapping/](findings/2026-04-24-M1-refinery-schedule-object-mapping/)

---

## 4. Decisions

| ID | Decision | When | Where documented |
|----|----------|------|------------------|
| D1 | Treat AI/MCP/Coplay as environment-authoring tools, not runtime controllers. | 2026-04-24 | This section |
| D2 | Separate visual reconstruction from Unity physics proxies. | 2026-04-24 | This section |
| D3 | Use `dev-standards` as the project management/documentation contract. | 2026-04-24 | This section |
| D4 | Manage environments as layered requirements and registries. | 2026-04-24 | This section |
| D5 | Treat the refinery GLB as an unrelated sandbox/import asset. | 2026-04-24 | This section |
| D6 | Add a later refinery GLB + CSV 4D installation simulation track. | 2026-04-24 | This section |
| D7 | Use a split control-plane/local-payload storage model. | 2026-04-24 | This section |
| D8 | Run refinery data preflight before Unity project setup. | 2026-04-24 | This section |
| D9 | Treat refinery schedule `동기화 ID` as a semantic mapping key. | 2026-04-24 | This section |
| D10 | Use a 50-GLB high-confidence refinery subset as the first Unity import target. | 2026-04-24 | This section |

### D1 - Use AI/MCP/Coplay for Authoring, Not Runtime Control

**Context**:
The original scenario considered Unity MCP, Coplay, Codex, SAM 3D, generated
images, and V-JEPA-style models together. The clarified goal is not real-time
autonomous simulation control. The user wants to build an environment and then
manually control a person/avatar inside Unity for observation.

**Decision**:
Use AI, MCP, Coplay, and Codex-connected tools for editor automation,
environment authoring, asset preparation, scene setup, and offline annotation.
Keep runtime simulation behavior inside Unity components and explicit scripts.

**Rationale**:
This matches the actual user workflow and reduces safety/latency risk. MCP and
Coplay are useful for manipulating Unity Editor state, generating scripts,
placing objects, configuring colliders, and iterating on scenes. They should not
be treated as the runtime authority for physics or safety decisions.

**Alternatives considered**:

- Runtime AI controller: flexible, but harder to validate and not aligned with
  the user's direct-control goal.
- Pure manual Unity workflow: reliable, but too slow for large reconstruction
  and scene setup tasks.
- Authoring-only AI workflow: keeps human oversight while accelerating setup.

**Impact**:
Future implementation should prioritize reproducible editor automation,
importers, scene builders, and validation tools. Runtime logic should use Unity
physics, raycast visibility, trigger zones, and explicitly versioned scripts.

**Related**:
- [Implementation plan](plan/2026-04-24-unity-construction-digital-twin-plan.md)

### D2 - Separate Visual Reconstruction from Physics Proxies

**Context**:
Construction-site video reconstruction can produce point clouds, Gaussian
Splats, textured meshes, or object meshes. These outputs may be visually useful
but are usually not clean, watertight, metric, stable, or simplified enough for
Unity physics.

**Decision**:
Maintain two layers in Unity:

- visual reconstruction layer for observation and context
- physics/simulation proxy layer for colliders, navigation, occlusion, safety
  zones, and equipment articulation

**Rationale**:
Unity physics needs simple, stable colliders and predictable scale/origin
metadata. Visual reconstruction needs appearance and spatial context. For this
project, conflating those two layers would make the simulation brittle.

**Alternatives considered**:

- Use reconstructed meshes directly as colliders: fast initially, but likely
  unstable and expensive.
- Build all geometry manually: stable, but loses video-derived context and is
  too slow.
- Split visual and physics layers: more pipeline work, but robust and auditable.

**Impact**:
Every reconstruction/import path must define both its visual output and its
physics proxy strategy. Blender cleanup and Unity collider generation become
first-class pipeline steps.

**Related**:
- [Implementation plan](plan/2026-04-24-unity-construction-digital-twin-plan.md)

### D3 - Use dev-standards for Project Management

**Context**:
The project has many external dependencies and several uncertain technical
paths. Without a clear documentation contract, tool comparisons, dependency
versions, and decisions will become hard to reconstruct.

**Decision**:
Use `dev-standards` as the project management and documentation framework,
with `docs/PROJECT-JOURNAL.md` as the single portal and dedicated directories
for plans, analysis, task logs, findings, and references.

**Rationale**:
The standard directly addresses this project's risk profile: external model
dependencies, rapidly changing tools, human-AI collaboration, reproducibility,
and decision traceability.

**Alternatives considered**:

- Minimal README only: quick, but insufficient for tracking decisions and model
  comparisons.
- External-only project management tool: useful for tasks, but weaker as a
  versioned technical record.
- dev-standards in-repo documentation: directly versioned with the project and
  suitable for AI collaboration.

**Impact**:
Future phases must update the journal, dependency registry, and task logs as
part of normal project work.

### D4 - Manage Environments as Layered Requirements and Registries

**Context**:
The project needs to run in multiple environments, but the stack includes
lightweight Python scripts, Unity packages, Blender, ffmpeg, COLMAP, GPU-specific
ML models, and user-provided assets. A single monolithic requirements file would
force every environment to install heavy model dependencies before the first
validated pipeline exists.

**Decision**:
Use layered environment management:

- `requirements/base.txt` for lightweight Python utilities
- `requirements/dev.txt` for test/lint tooling
- `requirements/ml-candidates.txt` as a registry for heavyweight candidates
- `docs/reference/environment/system-tools.md` for non-pip tools
- `config/environment.example.toml` and `.env.example` for local path/privacy
  configuration
- Unity package pins later through the Unity package manifest once the Unity
  project exists

**Rationale**:
This keeps the basic setup portable while still making external dependencies
explicit. Heavy ML/model dependencies can be pinned after a candidate wins a
Phase 1/2 validation instead of prematurely locking the project to a brittle
GPU-specific environment.

**Alternatives considered**:

- One large `requirements.txt`: simple, but fragile and likely to fail on
  machines without the right GPU/runtime stack.
- Separate conda environments for every candidate now: isolated, but too much
  maintenance before candidates are selected.
- Layered requirements plus registries: slightly more documentation work, but
  clearer and more adaptable.

**Impact**:
Future implementation should add candidate-specific lock files only after a
tool is selected. Installation instructions must distinguish base setup from
heavy reconstruction/model setup.

**Related**:
- [Environment analysis](analysis/2026-04-24-environment-and-asset-management.md)
- [Requirements strategy](../requirements/README.md)
- [System tools registry](reference/environment/system-tools.md)

### D5 - Treat the Refinery GLB as an Unrelated Sandbox/Import Asset

**Context**:
The user has a refinery facility `.glb` file. The model is not related to the
location shown in the construction-site video that will drive reconstruction.
It can still be useful because it is an industrial-scale GLB asset with likely
material, scale, hierarchy, and collider-proxy challenges.

**Decision**:
Register the refinery GLB as a user-provided asset but do not commit the binary
by default. Use it in Phase 3/4 for GLB import, scale/origin normalization,
material handling, Blender cleanup, collider proxy generation, occlusion volume
experiments, and a separate refinery sandbox scene.

Do not use it as evidence for the construction-site video reconstruction.

**Rationale**:
This extracts value from the asset without contaminating the video-based site
reconstruction workflow. The refinery model can stress-test Unity/Blender import
and proxy workflows before real site assets are available.

**Alternatives considered**:

- Ignore the GLB entirely: avoids confusion, but misses a useful import/proxy
  validation asset.
- Mix the GLB into the main construction-site scene: visually interesting, but
  technically invalid because it represents a different place.
- Use it as a separate sandbox asset: useful and cleanly bounded.

**Impact**:
The asset registry must track its local path and usage boundary once the user
provides the file location. Phase 3 can use it for import smoke tests; Phase 4
can use it for collider/occlusion proxy work.

**Related**:
- [Asset registry](reference/assets/ASSET-REGISTRY.md)
- [Environment analysis](analysis/2026-04-24-environment-and-asset-management.md)

### D6 - Add a Later Refinery GLB + CSV 4D Installation Simulation Track

**Context**:
The user clarified that the refinery data includes both a `.glb` model and a
CSV process plan describing installation order. The user wants to know whether
Unity can simulate modeled objects moving and being installed according to the
planned schedule.

**Decision**:
Add a later refinery-specific 4D installation sequencing track. The track will
start when the project reaches the installation simulation stage and the user
provides the GLB and CSV. It will remain separate from the construction-site
video reconstruction track.

The first target is 4D playback: schedule rows control object visibility,
color/state, and install sequence. Later targets can add kinematic movement,
installer agents, crane/forklift abstractions, collision checks, and
constructability validation.

**Rationale**:
This captures the value of the refinery data without mixing unrelated geometry
or schedule assumptions into the video reconstruction workflow. Starting with
4D playback is the lowest-risk path because it validates object mapping and
schedule quality before attempting equipment physics.

**Alternatives considered**:

- Keep the refinery GLB as import-only test data: safe, but misses the value of
  the installation CSV.
- Build detailed crane physics immediately: expressive, but depends on many
  unavailable details and could stall the project.
- Add a staged 4D installation track: validates GLB/CSV usability first, then
  expands to movement and constructability checks if the data supports it.

**Impact**:
The refinery track receives its own plan, data requirements, and later phases.
When the data arrives, the first implementation task is to inspect GLB hierarchy
and CSV schema, then create or derive an object mapping.

**Related**:
- [Refinery installation simulation plan](plan/2026-04-24-refinery-installation-simulation-plan.md)
- [Asset registry](reference/assets/ASSET-REGISTRY.md)

### D7 - Use a Split Control-Plane/Local-Payload Storage Model

**Context**:
The project needs to manage raw videos, extracted frames, reconstruction
artifacts, private GLB/CSV assets, Unity project files, and Unity-generated
caches. The current repository lives in WSL, while Unity Editor will likely run
from Windows.

**Decision**:
Use the git repository as the control plane: docs, scripts, manifests, config
examples, and eventually Unity project settings/scripts. Keep heavy or private
payloads local by default and reference them through `.env`, manifests, and
asset registries.

For Windows Unity, prefer a Windows-native clone of the same repository and
create the Unity project under `unity/` in that Windows clone. Sync WSL and
Windows work through git. Opening a Unity project directly from a WSL path is
allowed only as a quick smoke-test path.

**Rationale**:
This avoids committing private data and avoids Unity file-watcher/performance
issues caused by working directly across the WSL/Windows filesystem boundary.
It also keeps all local-only files discoverable through manifests instead of
hardcoded machine paths.

**Alternatives considered**:

- Put all data and Unity payloads in git: simple to find, but too large and
  unsafe for private videos/assets.
- Keep everything in WSL and open Unity through `\\wsl$`: simple for one repo,
  but risky for Unity performance and file watching.
- Split control files from local payloads and use a Windows-native Unity clone:
  slightly more operational discipline, but robust across environments.

**Impact**:
The repo now tracks directory READMEs and example manifests while ignoring
payloads. Future scripts should read paths from config or `.env` and should use
stable source IDs from manifests.

**Related**:
- [File management guide](reference/storage/FILE-MANAGEMENT.md)
- [Data manifests](../data/manifests/README.md)

### D8 - Run Refinery Data Preflight Before Unity Project Setup

**Context**:
The user placed refinery data under the local Windows data root. The dataset
contains 8,656 GLB files, `gap_fallback.fbx`, `geometry.csv`, `manifest.json`,
and a CP949-encoded schedule CSV with 4,214 rows. Importing all GLB files into
Unity immediately would create performance and mapping risk.

**Decision**:
Do not start with full Unity import. First run refinery data preflight,
normalize the schedule, derive schedule-to-object mapping coverage, and select
a small mapped subset for the first Unity import test.

**Rationale**:
The first preflight found M1: schedule `동기화 ID` values do not directly match
geometry object IDs. Unity playback depends on controlling the right
GameObjects, so mapping has to be solved before scene setup.

**Alternatives considered**:

- Import all GLB files into Unity now: fast to try, but likely to be slow and
  hard to debug.
- Build mapping/preflight first: adds a short upfront step, but prevents Unity
  scene churn.
- Ask for more data immediately: may be needed later, but current files are
  enough for automated mapping exploration.

**Impact**:
The mapping coverage report now exists. Unity setup should start with a small
validated high-confidence subset rather than a full 8,656-GLB import.

**Related**:
- [Refinery data preflight](analysis/2026-04-24-refinery-data-preflight.md)
- [M1 finding](findings/2026-04-24-M1-refinery-schedule-object-mapping/)

### D9 - Treat Refinery Schedule Sync ID as a Semantic Mapping Key

**Context**:
The user pointed to `https://github.com/tygwan/DXTnavis.git` as a source for
ID logic. Reviewing DXTnavis showed that `ScheduleData.SyncID` can mean either
an object GUID in object-level schedules or a composite group key in group-level
schedules. In group mode, the actual linked objects are maintained separately
as `ObjectIds`.

**Decision**:
For the refinery schedule, treat `동기화 ID` as a semantic mapping key, not as a
direct Unity GameObject ID. Build a mapping table from:

- `unified.csv` hierarchy paths after removing root labels
- `AllProperties_*.csv` `SmartPlant 3D|Pipeline::SmartPlant 3D|PipeRun`
- display/equipment-name fallback for unknown-heavy rows
- explicit confidence levels per mapping method

**Rationale**:
This matches the DXTnavis group-schedule design and explains why direct
ObjectId matching failed. It also gives Unity a deterministic import contract:
schedule row -> object IDs -> mesh URIs.

**Alternatives considered**:

- Treat `동기화 ID` as direct GUID: already disproved by preflight.
- Use row order only: acceptable for abstract playback, but loses object
  targeting.
- Ask for a manual mapping file now: still useful as a fallback, but the current
  data already supports high coverage.

**Impact**:
The repository now includes `scripts/map_refinery_schedule_to_assets.py`.
Full Unity setup should start from high-confidence mapped subsets and postpone
medium-confidence wildcard groups until duplicate-assignment handling exists.

**Related**:
- [DXTnavis ID review](analysis/2026-04-24-dxtnavis-id-logic-review.md)
- [M1 finding](findings/2026-04-24-M1-refinery-schedule-object-mapping/)

### D10 - Use a 50-GLB High-Confidence Refinery Subset as the First Unity Import Target

**Context**:
The refinery dataset contains 8,656 GLB files. Full import is the wrong first
Unity action because unresolved hierarchy, material, scale, and schedule
mapping issues would be hard to isolate at that size.

**Decision**:
Use `mvp_high_confidence_001`, a generated 9-task / 50-GLB subset, as the first
Unity import target. The subset is generated from high-confidence mapping rows
only and is stored as a local payload under:

```text
$REALWORLD_REFINERY_ROOT/subsets/mvp_high_confidence_001/
```

**Rationale**:
The subset is small enough to inspect manually in Unity while still preserving
the real schedule-to-object-to-mesh chain needed for later installation
playback. It excludes wildcard mappings until duplicate-assignment handling
exists.

**Alternatives considered**:

- Import all 8,656 GLBs now: faster to start, but high risk of slow imports and
  hard-to-debug schedule issues.
- Use a manually chosen visual-only sample: easy to inspect, but it would not
  validate schedule linkage.
- Generate a high-confidence mapped subset: balanced path for import and
  playback validation.

**Impact**:
The next implementation step is Unity project creation/opening, glTF/GLB import
setup, and a smoke-test scene that reads `unity_subset_manifest.json`.

**Related**:
- [Refinery Unity subset prep](analysis/2026-04-24-refinery-unity-subset-prep.md)
- [Asset registry](reference/assets/ASSET-REGISTRY.md)

---

## 5. External Dependencies

Initial dependency registry. Versions/commits must be pinned during
implementation.

| Name | Role | URL | Initial Status | Version Pin |
|------|------|-----|----------------|-------------|
| dev-standards | Project management/documentation standard | https://github.com/tygwan/dev-standards | Local source available | Local HEAD f98de5e; standard v0.5.0 |
| realworld-project remote | Project GitHub remote | https://github.com/tygwan/realworld-project.git | Connected; `main` tracks `origin/main` | Initial push completed 2026-04-24 |
| DXTnavis | Source of refinery export format and schedule ID logic | https://github.com/tygwan/DXTnavis.git | Reviewed for ID mapping semantics | Unpinned; inspected locally 2026-04-24 |
| Coplay Unity Plugin | Unity Editor AI copilot/workflow tool | https://github.com/CoplayDev/coplay-unity-plugin | Candidate | Unpinned; README branch install uses `#beta` |
| CoplayDev Unity MCP | Unity MCP bridge for editor automation | https://github.com/CoplayDev/unity-mcp | Candidate | Unpinned |
| SAM 3 | Text-prompted image/video segmentation and tracking | https://github.com/facebookresearch/sam3 | Candidate | Unpinned |
| SAM 3D Objects | Single-image/object 3D reconstruction candidate | https://github.com/facebookresearch/sam-3d-objects | Candidate | Unpinned |
| SAM 3D Body | Human mesh/body reconstruction candidate | https://github.com/facebookresearch/sam-3d-body | Candidate | Unpinned |
| V-JEPA 2 / 2.1 | Video representation/action anticipation candidate | https://github.com/facebookresearch/vjepa2 | Candidate | Unpinned |
| VGGT | Feed-forward camera/depth/point-map reconstruction candidate | https://github.com/facebookresearch/vggt | Candidate | Unpinned |
| COLMAP | Baseline SfM/MVS reconstruction | https://github.com/colmap/colmap | Candidate | Unpinned |
| DUSt3R / MASt3R | Uncalibrated dense 3D reconstruction candidates | https://github.com/naver/dust3r / https://github.com/naver/mast3r | Candidate | License/version review needed | Unpinned |
| MonST3R | Dynamic-scene video depth/reconstruction candidate | https://github.com/Junyi42/monst3r | Candidate | Unpinned |
| Nerfstudio / Splatfacto | Gaussian Splatting workflow candidate | https://docs.nerf.studio/nerfology/methods/splat.html | Candidate | Unpinned |
| TRELLIS | Generative 3D asset candidate | https://github.com/microsoft/TRELLIS | Candidate | Unpinned |
| Hunyuan3D 2.1 | Generative 3D asset candidate | https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 | Candidate | Unpinned |
| Stable Fast 3D | Fast image-to-3D candidate | https://github.com/Stability-AI/stable-fast-3d | Candidate | Unpinned |
| Blender | Mesh cleanup, rig/proxy preparation | https://www.blender.org | Required tool candidate | Unpinned |
| Unity | Interactive environment and physics runtime | https://unity.com | Required platform; local install observed | `6000.3.4f1` observed locally |
| Unity glTFast | GLB/glTF import candidate for Unity subset | https://docs.unity3d.com/Packages/com.unity.cloud.gltfast@6.14/manual/index.html | Candidate package; Unity release notes list `6.14.1` with 6000.3.4f1 | Pin in Unity `Packages/manifest.json` |
| User-provided refinery GLB | Unrelated industrial model for import/proxy sandbox validation | Local path in `.env`; see [asset registry](reference/assets/ASSET-REGISTRY.md) | Available locally; subset generated | Do not commit by default |
| User-provided refinery installation CSV | Unrelated process plan for refinery 4D installation sequencing | Local path in `.env`; see [asset registry](reference/assets/ASSET-REGISTRY.md) | Available locally; subset generated | Do not commit by default |

---

## 6. Open Questions

| ID | Question | Why it matters | Current handling |
|----|----------|----------------|------------------|
| Q1 | Which reconstruction baseline should be validated first: COLMAP, VGGT, MASt3R, or Gaussian Splatting? | Determines the first prototype pipeline and data requirements. | Run a small comparison on one short video. |
| Q2 | Which Unity automation path should be primary: Coplay Plugin, Coplay MCP, or direct Unity MCP? | Affects reproducibility and editor workflow. | Compare on scene setup tasks. |
| Q3 | What is the privacy boundary for construction-site video and generated frames? | Determines whether cloud tools can be used. | Default to local/offline until user approves otherwise. |
| Q4 | What minimum fidelity is required for manual observation? | Determines reconstruction quality targets and proxy simplification. | Define MVP acceptance criteria in Phase 1. |
| Q5 | How should heavy machinery articulation be represented? | Affects rigging, colliders, and user-observed behavior. | Start with simplified articulated prefabs. |
| Q6 | What is the local path and licensing/usage boundary of the refinery GLB? | Needed before import testing or committing derived assets. | Local path is recorded in `.env`; licensing/commit approval still pending. |
| Q7 | Which Unity version should be pinned? | Determines package compatibility and reproducibility. | Unity `6000.3.4f1` observed locally; pin in Unity project files once created. |
| Q8 | Does the refinery CSV contain stable object IDs that map to GLB nodes? | Determines whether schedule playback can control individual model objects. | Not direct IDs; DXTnavis-aware semantic mapping now covers 4,207/4,214 rows. |
| Q9 | Is the refinery GLB split into installable objects or merged into one mesh? | Determines whether Unity can animate individual installation steps. | Inspect GLB hierarchy before implementing Phase 6. |
| Q10 | What Windows-native path should host the Unity clone/project? | Needed before creating the Unity project outside WSL. | Choose before Phase 3; example `C:\dev\realworld-project\unity`. |
| Q11 | What local path holds the first Phase 1 test video? | Needed to start construction-video reconstruction spike. | `video/` directory exists but is currently empty. |
| Q12 | Which 10-50 refinery objects should be used for the first Unity import subset? | Needed to avoid importing 8,656 GLB files immediately. | Answered by `mvp_high_confidence_001`: 9 tasks, 50 object IDs, 50 GLB meshes. |

---

## 7. Where to Find What

| Looking for | Location |
|-------------|----------|
| Project overview | [../README.md](../README.md) |
| Current implementation plan | [plan/2026-04-24-unity-construction-digital-twin-plan.md](plan/2026-04-24-unity-construction-digital-twin-plan.md) |
| Refinery installation plan | [plan/2026-04-24-refinery-installation-simulation-plan.md](plan/2026-04-24-refinery-installation-simulation-plan.md) |
| Environment requirements | [../requirements/README.md](../requirements/README.md) |
| File management policy | [reference/storage/FILE-MANAGEMENT.md](reference/storage/FILE-MANAGEMENT.md) |
| System tools | [reference/environment/system-tools.md](reference/environment/system-tools.md) |
| User asset registry | [reference/assets/ASSET-REGISTRY.md](reference/assets/ASSET-REGISTRY.md) |
| Refinery preflight analysis | [analysis/2026-04-24-refinery-data-preflight.md](analysis/2026-04-24-refinery-data-preflight.md) |
| DXTnavis ID logic review | [analysis/2026-04-24-dxtnavis-id-logic-review.md](analysis/2026-04-24-dxtnavis-id-logic-review.md) |
| Refinery Unity subset prep | [analysis/2026-04-24-refinery-unity-subset-prep.md](analysis/2026-04-24-refinery-unity-subset-prep.md) |
| Design decisions | [§4 Decisions](#4-decisions) |
| External dependency registry | [§5 External Dependencies](#5-external-dependencies) |
| Task logs | [tasklog/](tasklog/) |
| Findings | [findings/](findings/) |
| External references | [reference/](reference/) |
