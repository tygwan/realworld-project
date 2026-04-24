# Project: realworld-project

> Runtime activation point for dev-standards rules in Codex/Claude-style AI
> development sessions.

## Dev Standards Version

- **Source**: https://github.com/tygwan/dev-standards
- **Version pinned**: `0.5.0`
- **Rules applied**: R1-R12

## Project-Specific Context

- **Goal**: Build a Unity-based construction-site environment reconstruction
  and observation workflow from site video and generated/derived 3D assets.
- **Current phase**: Phase 0 - planning and technical validation.
- **Primary target**: Human-controlled Unity exploration, not autonomous
  real-time site control.
- **Key data sources**: construction-site video, frame extraction outputs,
  segmentation masks, camera/reconstruction outputs, generated 3D assets, Unity
  scene metadata.

## Working Principles

- Treat AI/MCP/Coplay tools as environment authoring tools, not runtime safety
  controllers.
- Separate visual reconstruction from physics simulation proxies.
- Record every structural technical choice in `docs/PROJECT-JOURNAL.md`.
- Track external repositories, models, and plugins in the dependency registry.
- Pin versions/commits once implementation begins.
- Do not put private construction-site video into external services unless the
  user explicitly approves that data path.

## Documentation Contract

- `docs/PROJECT-JOURNAL.md` is the single project portal.
- New plans go in `docs/plan/`.
- Technical comparisons and rationale go in `docs/analysis/`.
- Completed tasks get a 5-section log in `docs/tasklog/`.
- Discovered issues get archived in `docs/findings/`.
- External references and inherited docs go in `docs/reference/`.

## Human-AI Collaboration Rule

For structural decisions, present alternatives and trade-offs before changing
architecture or committing to a dependency. After the user chooses, record the
decision as a stable decision record in the project journal.

