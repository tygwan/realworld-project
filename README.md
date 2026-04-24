# realworld-project

> Unity-based construction-site environment reconstruction and observation toolkit.

**Standards version**: dev-standards@0.5.0

## Goal

Build a Unity workflow that turns construction-site video into an explorable
digital environment. AI tools are used for environment authoring, asset
generation, segmentation, reconstruction support, and scene setup. The target
runtime is human-operated: a user directly controls a person/avatar in Unity and
observes visibility, blind spots, equipment zones, collision proxies, and safety
scenarios.

This project does not target autonomous real-time site control.

## Current Plan

- [Implementation plan](docs/plan/2026-04-24-unity-construction-digital-twin-plan.md)
- [Project journal](docs/PROJECT-JOURNAL.md)

## Documentation

- [Project Journal](docs/PROJECT-JOURNAL.md) - single portal for decisions,
  open questions, dependencies, and timeline
- [Plan](docs/plan/) - forward-looking plans
- [Analysis](docs/analysis/) - design rationale and technical comparisons
- [Task Logs](docs/tasklog/) - completed task records
- [Findings](docs/findings/) - archived issues
- [Reference](docs/reference/) - external materials and inherited references

## Initial Technology Direction

- Unity for the interactive environment and human-controlled observation.
- Coplay Unity Plugin / Unity MCP for editor automation and scene authoring.
- SAM 3 / SAM 3D for segmentation and object/person reconstruction candidates.
- COLMAP, VGGT, DUSt3R/MASt3R, MonST3R, or Gaussian Splatting for map
  reconstruction candidates.
- Blender for mesh cleanup, collider proxy generation, and asset preparation.
- V-JEPA 2.1 or video-language models for offline scenario analysis and
  behavior/risk annotation, not as the runtime safety authority.

## Standards

This project follows [dev-standards](https://github.com/tygwan/dev-standards)
with the current local standard version `0.5.0`.

Key rules:

- R1: documentation architecture with `docs/PROJECT-JOURNAL.md` as the portal
- R2: task logging for completed units of work
- R3: finding archival for discovered issues
- R4: decision records for structural decisions
- R5: atomic git workflow
- R6: external dependency registry
- R8: explicit human-AI trade-off checkpoints
- R9: provenance and reproducibility
- R10: validation for measurable decisions

