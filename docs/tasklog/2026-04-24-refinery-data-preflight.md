# Refinery Data Preflight

**Date**: 2026-04-24
**Task**: Phase 0 refinery dataset inventory and readiness check
**Commit**: pending

---

## 1. Language / Content

| Language | File | Purpose |
|----------|------|---------|
| Python | `scripts/inventory_refinery_dataset.py` | Reproducible local metadata inventory for refinery dataset |
| Markdown | `docs/analysis/2026-04-24-refinery-data-preflight.md` | Summarize observed dataset structure and readiness |
| Markdown | `docs/findings/2026-04-24-M1-refinery-schedule-object-mapping/README.md` | Archive schedule-to-object mapping issue |
| Markdown | `docs/reference/assets/ASSET-REGISTRY.md` | Update observed refinery asset metadata |
| Config | `.env.example`, `config/environment.example.toml` | Add refinery root, mesh directory, fallback FBX, schedule encoding fields |

## 2. Problem

The user provided the actual local refinery dataset location and asked whether
to set up Unity. The data contains thousands of GLB files and a generated
schedule CSV, so importing everything directly into Unity without preflight
could create avoidable performance and mapping problems.

## 3. Analysis

The data is visible from WSL. `manifest.json` reports 12,009 objects and 8,656
meshes. The schedule CSV has 4,214 rows and uses CP949 encoding. Initial probing
shows the schedule `동기화 ID` values do not directly match geometry object IDs,
display names, or categories.

## 4. Solution

Added a dataset inventory script, documented the preflight summary, recorded a
finding for the mapping gap, and updated configuration examples for the actual
data layout.

## 5. Result

- Unity setup should wait until a small mapped subset is selected.
- First implementation task should be schedule normalization + mapping coverage.
- Commit hash pending.

