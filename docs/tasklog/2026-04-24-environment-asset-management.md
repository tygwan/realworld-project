# Environment and Asset Management Scaffold

**Date**: 2026-04-24
**Task**: Phase 0 environment and asset management
**Commit**: 9d9a09c99940caf52da58c8a497d9ae1b54e9716

---

## 1. Language / Content

| Language | File | Purpose |
|----------|------|---------|
| Text | `requirements/base.txt` | Lightweight Python runtime requirements |
| Text | `requirements/dev.txt` | Development requirements |
| Text | `requirements/ml-candidates.txt` | Heavy model/reconstruction candidate registry |
| Markdown | `requirements/README.md` | Environment layer strategy |
| TOML | `config/environment.example.toml` | Example project-level configuration |
| Shell env | `.env.example` | Local path/privacy environment variables |
| Markdown | `docs/reference/environment/system-tools.md` | Non-pip tool registry |
| Markdown | `docs/reference/assets/ASSET-REGISTRY.md` | User asset registry and refinery GLB handling |
| Markdown | `docs/analysis/2026-04-24-environment-and-asset-management.md` | Rationale for layered environment and asset handling |

## 2. Problem

The project needs to run across multiple environments, but the stack includes
lightweight scripts, Unity, Blender, system tools, heavyweight ML candidates,
and private user assets. A single requirements file would be fragile.

The user also has an unrelated refinery facility `.glb` file that could be
useful for testing import/proxy workflows but must not be treated as evidence
for the construction-site video location.

## 3. Analysis

Environment reproducibility needs to start with boundaries: base scripts should
install easily, heavy model candidates should be pinned only after selection,
and user assets should be tracked through metadata without committing private
binaries.

The refinery GLB belongs in a separate sandbox/asset-validation role because it
does not represent the site video location.

## 4. Solution

Added layered requirements, example config, local `.env` template, system-tool
registry, asset registry, and analysis notes. Updated the plan and README to
link these files and define when the refinery GLB should be used.

## 5. Result

- Base/dev Python requirement files exist.
- Heavy ML candidates are tracked but not installed by default.
- System tools and user assets have registries.
- Refinery GLB usage is scoped to Phase 3/4 import/proxy validation.
- Environment scaffold commit: 9d9a09c99940caf52da58c8a497d9ae1b54e9716
- Commit hash metadata recorded in a follow-up documentation commit because a
  git commit cannot contain its own final hash before it exists.
