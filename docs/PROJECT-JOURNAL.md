# Project Journal - realworld-project

> Single portal for the Unity construction-site reconstruction and observation
> project. This document follows `dev-standards` R1/R4/R6.

**Standards**: dev-standards@0.5.0  
**Last updated**: 2026-04-24

---

## At a Glance

- **Current phase**: Phase 0 - planning and technical validation
- **Project goal**: Build a Unity environment from construction-site video and
  generated/derived 3D assets so a human can directly control a person/avatar
  and observe site conditions.
- **Runtime target**: Human-operated simulation/observation, not autonomous
  real-time safety control.
- **Current artifact**:
  [implementation plan](plan/2026-04-24-unity-construction-digital-twin-plan.md)
- **Open findings**: 0
- **Next step**: validate the first pipeline slice on one short site video.

---

## 1. Quick Problem Index

### Data / Design Issues

| ID | Date | Severity | Title | Status | Archive |
|----|------|----------|-------|--------|---------|
| — | — | — | No archived findings yet | — | — |

### Known Limitations

| ID | Description | Impact | Status |
|----|-------------|--------|--------|
| L1 | Generated images and generated 3D assets cannot be treated as factual site geometry. | Use generated assets only as editable proxies or canonical placeholders. | Accepted |
| L2 | Video reconstruction output is not automatically physics-ready. | Maintain a separate collider/proxy layer in Unity. | Accepted |
| L3 | MCP/Coplay tooling is suitable for authoring, not high-frequency runtime control. | Keep runtime behavior inside Unity scripts and explicit simulation components. | Accepted |

### Design Decisions

| ID | Decision | When | Where documented |
|----|----------|------|------------------|
| D1 | Treat AI/MCP/Coplay as environment-authoring tools, not runtime controllers. | 2026-04-24 | [D1](#d1---use-aimcpcoplay-for-authoring-not-runtime-control) |
| D2 | Separate visual reconstruction from Unity physics proxies. | 2026-04-24 | [D2](#d2---separate-visual-reconstruction-from-physics-proxies) |
| D3 | Use `dev-standards` as the project management/documentation contract. | 2026-04-24 | [D3](#d3---use-dev-standards-for-project-management) |

---

## 2. Timeline

```text
2026-04-24   Initialized planning scaffold with dev-standards@0.5.0.   ae68a05
2026-04-24   Recorded initial Unity reconstruction/observation plan.     ae68a05
```

---

## 3. Findings

No archived findings yet.

---

## 4. Decisions

| ID | Decision | When | Where documented |
|----|----------|------|------------------|
| D1 | Treat AI/MCP/Coplay as environment-authoring tools, not runtime controllers. | 2026-04-24 | This section |
| D2 | Separate visual reconstruction from Unity physics proxies. | 2026-04-24 | This section |
| D3 | Use `dev-standards` as the project management/documentation contract. | 2026-04-24 | This section |

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

---

## 5. External Dependencies

Initial dependency registry. Versions/commits must be pinned during
implementation.

| Name | Role | URL | Initial Status | Version Pin |
|------|------|-----|----------------|-------------|
| dev-standards | Project management/documentation standard | https://github.com/tygwan/dev-standards | Local source available | Local HEAD f98de5e; standard v0.5.0 |
| realworld-project remote | Project GitHub remote | https://github.com/tygwan/realworld-project.git | Connected; `main` tracks `origin/main` | Initial push completed 2026-04-24 |
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
| Unity | Interactive environment and physics runtime | https://unity.com | Required platform | Version TBD |

---

## 6. Open Questions

| ID | Question | Why it matters | Current handling |
|----|----------|----------------|------------------|
| Q1 | Which reconstruction baseline should be validated first: COLMAP, VGGT, MASt3R, or Gaussian Splatting? | Determines the first prototype pipeline and data requirements. | Run a small comparison on one short video. |
| Q2 | Which Unity automation path should be primary: Coplay Plugin, Coplay MCP, or direct Unity MCP? | Affects reproducibility and editor workflow. | Compare on scene setup tasks. |
| Q3 | What is the privacy boundary for construction-site video and generated frames? | Determines whether cloud tools can be used. | Default to local/offline until user approves otherwise. |
| Q4 | What minimum fidelity is required for manual observation? | Determines reconstruction quality targets and proxy simplification. | Define MVP acceptance criteria in Phase 1. |
| Q5 | How should heavy machinery articulation be represented? | Affects rigging, colliders, and user-observed behavior. | Start with simplified articulated prefabs. |

---

## 7. Where to Find What

| Looking for | Location |
|-------------|----------|
| Project overview | [../README.md](../README.md) |
| Current implementation plan | [plan/2026-04-24-unity-construction-digital-twin-plan.md](plan/2026-04-24-unity-construction-digital-twin-plan.md) |
| Design decisions | [§4 Decisions](#4-decisions) |
| External dependency registry | [§5 External Dependencies](#5-external-dependencies) |
| Task logs | [tasklog/](tasklog/) |
| Findings | [findings/](findings/) |
| External references | [reference/](reference/) |
