# Refinery Material Data Sources

**Date**: 2026-04-25
**Status**: Reviewed; Option B chosen
**Related**: M1, D8, D9, D10, refinery installation simulation

---

## Trigger

The `mvp_high_confidence_001` subset of 50 GLB files was imported into Unity
under URP. All 50 imported meshes rendered as the URP "missing shader" pink
fallback. Goal: determine whether DXTnavis-generated data can supply usable
material/color information, and decide how to color objects in Unity.

## Findings

### GLB content (DXTnavis output)

- 50/50 GLB files contain only `POSITION` and `NORMAL` attributes
- 0 materials, 0 textures, 0 images, 0 UV/COLOR vertex attributes
- glTF JSON `generator` field is `DXTnavis`
- DXTnavis source path identified at
  `/home/coffin/dev/폐기/DXTnavis/Services/Geometry/MeshExtractor.cs:1221, 1253`
  and `Services/Geometry/GeometryFileWriter.cs:212`

DXTnavis intentionally exports geometry-only GLBs.

### Side-channel material data (`AllProperties_*.csv`)

The user-provided refinery dataset includes a 136-column CSV with SmartPlant 3D
properties. Material-relevant columns:

| Column | Filled rows in subset 50 | Notes |
|--------|-------------------------:|-------|
| `SmartPlant 3D|Material` | 0 / 50 | (subset is piping; Material column is for civil/structural objects) |
| `SmartPlant 3D|Material Grade` | 0 / 50 | |
| `SmartPlant 3D|Material Type` | 0 / 50 | |
| `SmartPlant 3D|Material Name` | 0 / 50 | |
| `SmartPlant 3D|Insulation Material` | 0 / 50 | |
| `SmartPlant 3D|Spec Name` | 50 / 50 | piping spec codes (e.g., `1C0031`) — semantic but not visual |
| `SmartPlant 3D|Specification` | 50 / 50 | spec descriptions |
| `SmartPlant 3D|Construction Type` | 50 / 50 | "New" — status, not material |

In the wider dataset (12,009 rows), `SmartPlant 3D|Material` is populated for
~2,400 civil/structural rows (Cementitious, Concrete, Steel - Carbon, Fibrous).
That coverage is irrelevant for this MVP subset because the subset was selected
for high-confidence Pipeline mapping; the 50 GLBs are all piping components.

### Domain inference (`SmartPlant 3D|System Path`)

`System Path` is filled for 44/50 objects with hierarchy strings like:

```text
TRAINING\A1\U12\Civil_Structure\Cable Trenches\Cable Trenches-1-0001\...
TRAINING\A1\U12\Process\Pipelines\U12-2-MZ-0050-1S3984
TRAINING\A1\U12\Electrical\CableTrays\CableTrays-ET--0002
TRAINING\A3\Building\Beams\MemberSystem-1-0751
```

Keyword extraction over `System Path`, `Name`, and `Eqp Type 0` yields a usable
domain bucket (`Pipe`, `Civil`, `Structure`, `Equipment`, `Insulation`,
`Unknown`).

### `geometry.csv` Category column (rejected as primary)

`geometry.csv:Category` is dominated by the value `Geometry Group` (45/50). It
is not useful as a per-object discriminator. `System Path` is preferred.

### Coverage of combined inference (50 GLBs)

| Tier | Source | Count |
|------|--------|------:|
| 1 | Explicit `Material` | 0 (this subset is all piping) |
| 2 | Domain from `Name` + `System Path` | 50 |
| 3 | Unknown | 0 |

Tier 2 sub-classification (within Pipe domain, derived from `Name`):

| Bucket | Count | Example name |
|--------|------:|--------------|
| Pipe (segments) | 21 | `Pipe` |
| PipeFitting | 23 | `Flange-0032`, `Weldolet-0011`, `Reinforcing Pad-0001`, `90 Degree Direction Change-0044` |
| Valve | 6 | `VG3-0011`, `FE-523`, `FV-521` |

## Options Considered

| Option | Coverage | Effort | Pink fixed | Reproducibility |
|--------|----------|--------|------------|-----------------|
| A. CSV explicit material only + URP color LUT | 0/50 for this subset (piping has no Material col); ~2,400 / 12,009 in full data | Low | Yes (only for material-bearing objects) | LUT script + JSON next to subset |
| **B. A + Name/System Path domain fallback** | 50/50 meaningful | Low-Medium | Yes | Same |
| C. Modify DXTnavis to export glTF materials | source-data limit same as A | High (.NET build, Navisworks, re-export) | Yes; GLB self-contained | One-time cost; future exports automatic |
| D. Single neutral grey URP material for all 50 | 0/50 meaningful | Trivial | Yes | None |

## Decision (Option B)

Use a side-channel LUT built from `AllProperties_*.csv` and `geometry.csv`,
with a two-tier rule:

1. If `SmartPlant 3D|Material` is set, map by material name.
2. Otherwise, infer a domain bucket from `System Path` / `Name` / `Eqp Type 0`
   and map by domain.

Reasons:

- Covers 50/50 with meaningful color distinction.
- No upstream changes required; reuses inputs already shipped in the user
  dataset.
- Cheaper and faster than Option C; Option C does not raise coverage because
  the source data itself has only ~28% explicit material.
- Option D loses semantic information; not useful for the schedule playback
  validation that immediately follows.

Option C remains a candidate if Phase 4+ requires self-contained GLB exports
or if other downstream consumers cannot use the side-channel JSON.

## Color Palette (v0.1)

Material-driven (Tier 1):

| Material | Hex | Intent |
|----------|-----|--------|
| Steel - Carbon | `#4A4F58` | dark steel grey |
| Concrete | `#B0AFA8` | concrete grey |
| Cementitious | `#C7B299` | warm beige (fireproofing) |
| Fibrous | `#D4A574` | tan (fibrous insulation) |

Domain-driven (Tier 2 fallback):

| Domain | Hex | Intent |
|--------|-----|--------|
| Pipe | `#5A6470` | piping steel — base segments |
| PipeFitting | `#78808A` | flanges/elbows/reducers/pads — slightly lighter to read against pipe runs |
| Valve | `#884540` | valves/instrumentation — warm red-brown for emphasis |
| Structure | `#7A6F5C` | structural steel/brown-grey |
| Civil | `#9A9388` | civil concrete-like |
| Equipment | `#5A6F88` | electrical/equipment blue-grey |
| Insulation | `#D4A574` | tan |
| Unknown | `#9A9A9A` | neutral grey |

Within the Pipe family, the three sub-buckets (Pipe / PipeFitting / Valve) are
chosen so a continuous run of pipes reads as a single tone, while attached
fittings and valves stay visually distinct during schedule playback.

Palette is versioned (`palette_version: 0.1`) so future visual revisions can be
reproduced or compared without rerunning DXTnavis.

## Implementation

- Generator: `scripts/build_refinery_material_lut.py`
  - Reads `AllProperties_*.csv` + `geometry.csv` from `REALWORLD_REFINERY_ROOT`
  - Filters to a subset directory's `unity_subset_manifest.json` object set
  - Outputs `<subset>/object_material_lut.json` next to existing manifest
- Unity applier: `unity/Assets/Refinery/Scripts/RefineryMaterialApplier.cs`
  - MonoBehaviour; loads the LUT JSON via `TextAsset`
  - For each `MeshRenderer` in scene, matches GameObject name (or parent name)
    to `object_id` and assigns a URP/Lit material with the resolved color
  - Material instances cached by hex string

## Reproducible Commands

Generate LUT for the MVP subset:

```bash
python3 scripts/build_refinery_material_lut.py \
  "$REALWORLD_REFINERY_ROOT" \
  --subset-dir "$REALWORLD_REFINERY_ROOT/subsets/mvp_high_confidence_001"
```

Output written to:

```text
$REALWORLD_REFINERY_ROOT/subsets/mvp_high_confidence_001/object_material_lut.json
```

The user copies that JSON into `unity/Assets/Refinery/Manifest/` (same way the
existing `unity_subset_manifest.json` was added) and assigns it to
`RefineryMaterialApplier.lutJson` in the inspector.

## Remaining Risks

- 28% explicit material coverage is a source-data ceiling. Phase 4+ may want
  Option C for richer fidelity.
- Domain keyword detection is heuristic; misclassification possible (currently
  zero `Unknown` in the 50 subset, but expansion sets may produce more).
- The 9,602 medium-confidence wildcard objects (D9) still need duplicate
  handling before broader application.
