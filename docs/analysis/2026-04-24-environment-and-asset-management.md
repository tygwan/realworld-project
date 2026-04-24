# Environment and Asset Management Analysis

**Date**: 2026-04-24
**Status**: Accepted initial direction
**Related decisions**: D4, D5

---

## Problem

The project needs to run across different machines, but the technical stack is
heterogeneous:

- lightweight Python preprocessing
- Unity project configuration
- Blender/ffmpeg/COLMAP system tools
- heavyweight ML repositories and model weights
- user-provided private video and `.glb` assets

Putting all of this into one `requirements.txt` would be fragile and would make
basic setup depend on GPU/model-specific packages before the first pipeline is
validated.

The user also has a refinery facility `.glb` file. It is valuable for testing
industrial-scale model import workflows, but it is unrelated to the future
construction-site video location.

---

## Decision Direction

Use layered environment management:

- base Python requirements for scripts that should work everywhere
- dev requirements for tests/linting
- ML candidate registry until a model is selected
- system tool registry for Unity, Blender, ffmpeg, COLMAP, and GPU runtime
- project config example for paths and privacy defaults
- asset registry for user-provided assets without committing the binaries

Treat the refinery `.glb` as a sandbox/reference asset, not as reconstruction
evidence.

---

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| One large `requirements.txt` | Simple command | Breaks easily across machines; installs unnecessary heavy packages |
| Separate conda environment per candidate | Strong isolation | Heavy maintenance before candidates are chosen |
| Layered requirements + registries | Clear, lightweight, evolves with decisions | Requires discipline to update docs |

Recommended approach: layered requirements + registries now, candidate-specific
lock files later.

---

## When to Use the Refinery GLB

The refinery `.glb` should enter the workflow after the first Unity import
pipeline exists.

Recommended sequence:

1. Phase 1: ignore the refinery GLB; focus on video reconstruction candidates.
2. Phase 2: ignore the refinery GLB; focus on segmentation/tracking outputs.
3. Phase 3: use the refinery GLB as a GLB import smoke test for Unity scene
   builder and material handling.
4. Phase 4: use it for collider proxy generation, occlusion volume experiments,
   scale/origin normalization, and navigation tests.
5. Later: split a refinery-specific scenario track if the project needs a
   second industrial environment unrelated to the construction-site video.

The key boundary: it must not be mixed into the construction-site reconstruction
as if it represents the same place.
