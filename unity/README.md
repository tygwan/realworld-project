# Unity Workspace

This directory is reserved for the Unity project if this repository is opened
from an environment where Unity can safely work with the repo path.

## Recommended Setup on Windows + WSL

If Unity Editor runs on Windows, prefer a Windows-native git clone for the Unity
project instead of opening this WSL path directly through `\\wsl$`.

Recommended pattern:

```text
WSL clone:
  /home/<user>/dev/realworld-project
  - Python scripts
  - docs
  - manifests
  - planning

Windows clone:
  C:\dev\realworld-project
  - same git remote
  - Unity project under C:\dev\realworld-project\unity
```

Sync between the two clones through git. Keep large private data outside git and
reference it via `.env` paths.

## First Import Target

Before importing the full refinery dataset, use the generated MVP subset:

```text
$REALWORLD_REFINERY_ROOT/subsets/mvp_high_confidence_001/
```

That folder contains `unity_subset_manifest.json`, `subset_tasks.csv`, and 50
copied GLB files under `mesh/`. The matching repo-local artifact path is:

```text
artifacts/refinery/unity_subsets/mvp_high_confidence_001/
```

Local inspection found Unity `6000.3.4f1` installed. Start with Unity glTFast
for GLB import and pin the package in `unity/Packages/manifest.json` once the
Unity project exists.

## Tracked vs Ignored

When the Unity project is created, track:

- `unity/Assets/` scripts and small approved assets
- `unity/Packages/manifest.json`
- `unity/Packages/packages-lock.json`
- `unity/ProjectSettings/`

Do not track:

- `Library/`
- `Temp/`
- `Obj/`
- `Logs/`
- `UserSettings/`
- large private imported assets unless explicitly approved
