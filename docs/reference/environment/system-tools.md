# System Tools Registry

**Status**: Draft
**Last updated**: 2026-04-24

This file tracks tools that are not managed by `pip`.

| Tool | Role | Required Phase | Version Pin | Notes |
|------|------|----------------|-------------|-------|
| Python | Local scripts, preprocessing, validation | Phase 1 | `>=3.11` target | Exact version to pin after first script lands |
| ffmpeg | Frame extraction and video metadata | Phase 1 | TBD | Prefer system package or static binary |
| Unity | Interactive environment and physics runtime | Phase 3 | `6000.3.4f1` observed locally | Installed under Windows Unity Hub path; pin in `unity/ProjectSettings/ProjectVersion.txt` once the project exists |
| Blender | GLB/mesh cleanup and collider proxy preparation | Phase 3/4 | TBD | Use for refinery GLB and generated assets |
| COLMAP | SfM/MVS baseline | Phase 1 | TBD | Candidate, not yet selected |
| GPU runtime / CUDA | Heavy ML candidates | Phase 1+ | TBD | Only document after chosen model requires it |

## Notes

- Do not add heavyweight ML environments to the base Python requirements.
- For each selected tool, record installation source, version, and verification
  command.
- For Unity packages, pin through the Unity package manifest once the Unity
  project exists.

## Unity Package Notes

Unity `6000.3.4f1` release notes list `com.unity.cloud.gltfast@6.14.1` as an
added package. Use that as the first GLB importer candidate for the refinery
subset, then record the exact package in `unity/Packages/manifest.json`.

Reference: [Unity 6000.3.4f1 release notes](https://unity.com/releases/editor/whats-new/6000.3.4f1)
