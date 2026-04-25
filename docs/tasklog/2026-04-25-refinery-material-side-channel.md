# Refinery Material Side-Channel Pipeline

**Date**: 2026-04-25
**Task**: D11 / Phase 3 (Unity material assignment)
**Commit**: TBD

---

## 1. Language / Content

| Language | File | Purpose |
|----------|------|---------|
| Markdown | `docs/analysis/2026-04-25-refinery-material-data-sources.md` | Findings + decision record |
| Python | `scripts/build_refinery_material_lut.py` | Generates per-ObjectId color LUT JSON |
| C# | `unity/Assets/Refinery/Scripts/RefineryMaterialApplier.cs` | Applies LUT to MeshRenderers in Unity scene |
| Markdown | `docs/PROJECT-JOURNAL.md` | D11 entry + timeline |

## 2. Problem

The 50-GLB MVP subset imported into Unity URP rendered as the URP
"missing-shader" pink fallback. Goal: determine whether DXTnavis
exports usable material information and decide how to color objects
in Unity.

## 3. Analysis

- Inspected the GLB JSON chunk for all 50 files: zero materials,
  textures, images, or COLOR/UV vertex attributes. DXTnavis exports
  geometry only.
- Inspected the SmartPlant 3D properties CSV (136 columns): material
  columns are sparse (~2,400 / 12,009 rows in the full dataset, 0/50
  in this piping-heavy subset).
- Identified `Name` and `System Path` as a reliable Tier 2 fallback;
  inferred Pipe / PipeFitting / Valve / Structure / Civil / Equipment /
  Insulation / Unknown buckets via keyword matching.
- DXTnavis source identified at
  `/home/coffin/dev/폐기/DXTnavis/Services/Geometry/MeshExtractor.cs:1221, 1253`
  and `Services/Geometry/GeometryFileWriter.cs:212` — modifying it would
  not raise the source-data ceiling, so deferred.
- Found and corrected an early bug in this session: the user had
  imported the wrong 50 GLBs from the full `mesh/` root into Unity
  Assets. The subset files at
  `subsets/mvp_high_confidence_001/mesh/` are the correct 50.

## 4. Solution

Adopted Option B from the analysis doc:

- `scripts/build_refinery_material_lut.py` reads `AllProperties_*.csv`
  + `geometry.csv`, filters by either subset manifest object IDs or all
  GLBs, applies the two-tier rule, and writes
  `<subset>/object_material_lut.json` with palette metadata and per-entry
  resolution.
- `RefineryMaterialApplier` (Unity MonoBehaviour) loads the LUT as a
  `TextAsset`, walks `MeshRenderer`s, matches GameObject name (or any
  parent's name) to `object_id`, and assigns a URP/Lit material with
  the resolved hex color. Material instances are cached per hex string.
- Decision recorded as D11 in the project journal.

## 5. Result

Generator output for `mvp_high_confidence_001`:

```text
total: 50
by_source: {'domain_inference': 50}
by_applied_key: {'Pipe': 21, 'PipeFitting': 23, 'Valve': 6}
```

Pending user actions on the Windows Unity clone:

1. Delete the wrong 50 GLBs currently in `unity/Assets/Refinery/mesh/`
   (use Unity Project window, not filesystem `rm`).
2. Drag the 50 correct GLBs from
   `C:\Users\x8333\desktop\AI_PJT\unity\refinery\subsets\mvp_high_confidence_001\mesh\`
   into `unity/Assets/Refinery/mesh/`.
3. Drag `object_material_lut.json` (just generated) into
   `unity/Assets/Refinery/Manifest/`.
4. Add an empty GameObject in the scene, attach
   `RefineryMaterialApplier`, assign `lutJson`, leave `litShader` empty
   (auto-resolves to URP/Lit).
5. Place the 50 GLB prefabs in the scene (drag-import) and press Play —
   pink fallback should be replaced with palette colors.

Commit: TBD.
