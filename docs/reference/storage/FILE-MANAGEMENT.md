# File Management and Workspace Layout

**Status**: Draft
**Last updated**: 2026-04-24

This project separates git-tracked control files from local heavy payloads.

## Core Rule

The repository should contain:

- source code and scripts
- docs and plans
- small config examples
- manifests and registries
- Unity project settings and scripts once the Unity project exists

The repository should not contain by default:

- raw construction-site videos
- extracted video frames
- private GLB/CSV files
- model weights
- reconstruction point clouds/splats/meshes
- Unity `Library`, `Temp`, `Logs`, or generated build outputs

## Directory Layout

```text
realworld-project/
├── data/
│   ├── raw/             local-only source videos/files
│   ├── interim/         local-only frames, masks, tracks
│   ├── processed/       local-only curated outputs by default
│   └── manifests/       tracked metadata for local files and runs
├── artifacts/           local-only reconstruction/model outputs
├── assets/
│   ├── user-provided/   local-only GLB/CSV/private assets
│   ├── private/         local-only sensitive assets
│   ├── generated/       generated assets, ignored unless approved
│   └── public/          optional approved assets
├── captures/            local screenshots/recordings
├── exports/             local exports/build handoff files
└── unity/               Unity project placeholder or future project root
```

## Unity + WSL Strategy

Unity Editor usually runs on Windows, while this repository currently lives in
WSL. Opening a Unity project directly from a WSL path can work for small tests,
but it can create file-watcher, path, and performance problems as the project
grows.

Recommended strategy:

1. Keep this WSL repo as the planning, scripts, manifests, and automation
   workspace.
2. When creating the Unity project, create a Windows-native clone of the same
   GitHub repository.
3. Create the Unity project in the Windows clone under `unity/`.
4. Commit Unity scripts/settings/package manifests from the Windows clone.
5. Pull those commits into the WSL clone for pipeline work.
6. Keep large data outside git and reference it through `.env`.

Alternative for quick prototypes:

- Open `unity/` through `\\wsl.localhost\...` from Windows Unity.
- This is acceptable for a short smoke test but not recommended as the main
  long-term workspace.

## Local Path Configuration

Use `.env` for machine-specific paths:

```text
REALWORLD_DATA_ROOT=data
REALWORLD_ARTIFACTS_ROOT=artifacts
REALWORLD_ASSETS_ROOT=assets
REALWORLD_UNITY_PROJECT=unity
REALWORLD_UNITY_PROJECT_WINDOWS=C:\dev\realworld-project\unity
REALWORLD_REFINERY_GLB=C:\data\realworld\refinery\model.glb
REALWORLD_REFINERY_SCHEDULE_CSV=C:\data\realworld\refinery\schedule.csv
```

Do not commit `.env`.

## Manifest Policy

Every local-only source file should have a stable ID in a manifest or registry.

Examples:

- construction-site video: `data/manifests/source-files.example.csv`
- refinery GLB/CSV: `docs/reference/assets/ASSET-REGISTRY.md`
- reconstruction run outputs: `data/manifests/pipeline-runs.example.csv`

## When to Commit Binary Assets

Only commit binary assets when all are true:

- the asset is not private
- the license allows repository storage
- file size is acceptable
- the asset is needed for reproducible tests or demos
- the decision is recorded in `docs/PROJECT-JOURNAL.md`

Otherwise, keep the file local and track only metadata.
