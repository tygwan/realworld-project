# File Management Layout

**Date**: 2026-04-24
**Task**: Phase 0 file storage and Unity workspace management
**Commit**: pending

---

## 1. Language / Content

| Language | File | Purpose |
|----------|------|---------|
| Markdown | `docs/reference/storage/FILE-MANAGEMENT.md` | File storage, data layout, and Unity/WSL workspace policy |
| Markdown | `data/README.md` and subdirectory READMEs | Define local data layout |
| CSV | `data/manifests/*.example.csv` | Example tracked metadata for local-only files/runs |
| Markdown | `artifacts/README.md`, `assets/README.md`, `captures/README.md`, `exports/README.md` | Define ignored payload directories |
| Markdown | `unity/README.md` | Unity workspace policy for Windows + WSL |
| Gitignore | `.gitignore` | Track directory docs/manifests while ignoring heavy payloads |

## 2. Problem

The project needs data directories, but raw video, GLB files, generated
reconstruction outputs, and Unity caches can be too large or private for git.
Unity may also run from Windows while the current repository is in WSL.

## 3. Analysis

The project needs a split storage model. Git should track the control plane:
docs, scripts, manifests, configs, and eventually Unity project settings/scripts.
Large data should stay local and be referenced through `.env` and manifests.

For Unity on Windows, a Windows-native clone is safer than opening a Unity
project directly from a WSL path.

## 4. Solution

Added directory READMEs, manifest examples, Unity workspace guidance, local path
configuration fields, and gitignore rules that keep payloads ignored while
allowing documentation and metadata to be tracked.

## 5. Result

- Data, artifact, asset, capture, export, and Unity workspace directories are
  defined.
- Large/private payloads remain ignored by default.
- Unity/WSL management strategy is documented.
- Commit hash pending.

