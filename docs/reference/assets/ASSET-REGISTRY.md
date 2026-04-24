# Asset Registry

**Status**: Draft  
**Last updated**: 2026-04-24

This registry tracks user-provided and generated assets without requiring the
asset binaries to be committed.

## Policy

- Private source videos, extracted frames, model weights, reconstruction
  outputs, and user-provided `.glb` files stay out of git by default.
- Asset metadata and intended use are committed here.
- If an asset is unrelated to the source video location, it must be labeled as
  unrelated and must not be used as evidence for site reconstruction.

## Assets

| ID | Asset | Type | Relationship to Site Video | Git Policy | Intended Use | Phase |
|----|-------|------|----------------------------|------------|--------------|-------|
| A1 | User-provided refinery facility model | `.glb` | Unrelated to provided construction-site video | Do not commit by default | Validate GLB import, materials, scale/origin handling, collider proxy generation, and a separate refinery sandbox scene | Phase 3/4 |

## A1 - User-Provided Refinery Facility GLB

**Known context**:
The user has a refinery facility `.glb` file. The model is not related to the
physical location shown in the future construction-site video.

**Use it for**:

- GLB import pipeline validation
- Unity material/texture handling checks
- Blender cleanup workflow validation
- collider proxy generation experiments
- scale/origin/unit normalization experiments
- separate sandbox scene for refinery-specific observation workflows

**Do not use it for**:

- reconstructing the user-provided construction-site video location
- validating map reconstruction accuracy for that video
- deriving site-specific safety conclusions from unrelated geometry

**Recommended timing**:

- Phase 3: use it as an import smoke-test asset when building the Unity scene
  builder.
- Phase 4: use it more seriously for collider proxies, occlusion volumes, and
  large industrial facility navigation tests.
- Optional later branch: create a refinery-specific scenario track if the
  project expands beyond the construction-site video.

