# Requirements Strategy

This project has multiple environment layers. Do not collapse them into one
large `requirements.txt` until the pipeline is proven.

## Layers

| Layer | File / Registry | Purpose |
|-------|-----------------|---------|
| Python base | `requirements/base.txt` | Lightweight local utilities for frame extraction, metadata, and small scripts |
| Python dev | `requirements/dev.txt` | Tests, linting, and formatting tools |
| Heavy ML / reconstruction | `requirements/ml-candidates.txt` | Candidate model dependencies and install notes; pin only after selection |
| System tools | `docs/reference/environment/system-tools.md` | Unity, Blender, COLMAP, ffmpeg, GPU/runtime notes |
| Unity packages | future `unity/Packages/manifest.json` | Unity package pins once the Unity project exists |
| User assets | `docs/reference/assets/ASSET-REGISTRY.md` | User-provided `.glb`, videos, generated assets, and usage boundaries |

## Setup Baseline

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements/base.txt
python -m pip install -r requirements/dev.txt
```

## Pinning Policy

- Keep base dependencies small and cross-platform.
- Pin heavyweight model repositories by commit after a candidate is selected.
- Record every selected external tool in `docs/PROJECT-JOURNAL.md`.
- Do not commit local videos, model weights, generated reconstructions, or
  private `.glb` assets unless explicitly approved.
- For GPU-specific packages, document the CUDA/driver/runtime assumptions in
  `docs/reference/environment/system-tools.md`.
