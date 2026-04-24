# Data Directory

This directory defines the local data layout. Most payload files are ignored by
git. Keep metadata, manifests, and small examples in the repository.

## Layout

| Directory | Git policy | Purpose |
|-----------|------------|---------|
| `raw/` | payloads ignored | Original videos and source files |
| `interim/` | payloads ignored | Extracted frames, masks, tracks, temporary conversions |
| `processed/` | payloads ignored by default | Curated derived datasets or compact pipeline outputs |
| `manifests/` | tracked | Metadata describing local files and pipeline runs |

## Rules

- Do not commit raw site video.
- Do not commit extracted frames unless explicitly approved.
- Do not commit private GLB/CSV files by default.
- Record local file existence in manifests or asset registry instead.
- Use stable IDs in manifests so scripts can refer to data without hardcoded
  machine-specific paths.
