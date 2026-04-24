# Refinery Installation Simulation Planning

**Date**: 2026-04-24
**Task**: Phase 0 refinery installation sequencing planning
**Commit**: 6d23276099c31b93d662e17f198b34d2582e8112

---

## 1. Language / Content

| Language | File | Purpose |
|----------|------|---------|
| Markdown | `docs/plan/2026-04-24-refinery-installation-simulation-plan.md` | Plan the later GLB + CSV installation sequencing track |
| Markdown | `docs/PROJECT-JOURNAL.md` | Record decision, timeline, dependency, and open questions |
| Markdown | `docs/reference/assets/ASSET-REGISTRY.md` | Register refinery GLB and installation CSV roles |
| TOML | `config/environment.example.toml` | Add local config fields for refinery GLB and schedule CSV |
| Env | `.env.example` | Add local path variable for refinery schedule CSV |

## 2. Problem

The refinery GLB was initially recorded as an unrelated import/proxy sandbox
asset. The user clarified that a CSV installation process plan also exists and
asked whether Unity can simulate planned movement/installation of modeled
objects according to that schedule.

## 3. Analysis

Unity can support this workflow if the CSV schedule rows can be mapped to GLB
objects. The safest architecture is to start with 4D playback, then add
kinematic movement, installer agents, and constructability checks only after
the object mapping works.

Because the refinery model and schedule are unrelated to the construction-site
video, this needs to be a separate refinery sandbox track.

## 4. Solution

Added a dedicated refinery installation sequencing plan, updated the existing
construction-site plan with Phase 6/7 refinery phases, registered the schedule
CSV as a separate user-provided asset, and recorded the boundary that the GLB
and CSV must not be used as evidence for the video reconstruction track.

## 5. Result

- Refinery GLB + process-plan CSV are now planned as a later 4D installation
  simulation track.
- The user can provide the GLB/CSV when Phase 6 starts, or provide the GLB
  earlier for Phase 3 import testing.
- Refinery installation planning commit:
  6d23276099c31b93d662e17f198b34d2582e8112
- Commit hash metadata recorded in a follow-up documentation commit because a
  git commit cannot contain its own final hash before it exists.
