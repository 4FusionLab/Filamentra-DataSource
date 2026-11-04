# Catalog population progress — 2026-11-04

> **Scope:** PLA and PETG families, including PLA+/Silk/Matte/CF, PETG-CF/GF/HF, translucent and other derived formulations. ABS, ASA, TPU, PA and PC are out of scope.

## Source priority and status

**Bambu Lab → other Chinese manufacturers → Russian manufacturers.** The BambuStudio color-registry snapshot is imported; expansion of Chinese lines is under way. Russian-brand data import has not started yet.

The logical selection path is **Manufacturer → Material (PLA/PETG) → Product Line → Color**. Physical files are grouped by manufacturer and product line; the polymer is an attribute.

## Verified source records

| Manufacturer | Country | PLA/PETG lines | Color variants | Evidence |
| --- | --- | ---: | ---: | --- |
| [Bambu Lab](../catalog/brands/bambu-lab/) | China | 24 | 246 | [Pinned official BambuStudio RGBA registry](../catalog/sources/bambu-lab.json), with multi-color variants |
| [eSUN](../catalog/brands/esun/) | China | 7 | 139 | Official [original](../catalog/sources/esun.json), [additional](../catalog/sources/2026-11-04-sunlu-esun-additional.json), [expanded](../catalog/sources/esun-expanded-2026-11-04.json) color tables |
| [ERYONE](../catalog/brands/eryone/) | China | 1 | 6 | Product names and manufacturer imagery; no verified numeric swatches |
| [ELEGOO](../catalog/brands/elegoo/) | China | 19 | 195 | Official [initial](../catalog/sources/next-chinese-brands.json) and [expanded product pages](../catalog/sources/elegoo-expanded-2026-11-04.json); no verified HEX |
| [DeepLee](../catalog/brands/deeplee/) | China | 1 | 1 | Manufacturer name-only product record |
| [Creality](../catalog/brands/creality/) | China | 5 | 39 | Official [initial](../catalog/sources/sunlu-kingroon-creality.json) and [extended](../catalog/sources/creality-expanded-2026-11-04.json) line options; selected CR-PETG SKU codes |
| [KINGROON](../catalog/brands/kingroon/) | China | 4 | 87 | Official [PETG](../catalog/sources/sunlu-kingroon-creality.json) and [PLA product pages](../catalog/sources/kingroon-pla-2026-11-04.json) |
| [SUNLU](../catalog/brands/sunlu/) | China | 8 | 130 | Official [initial](../catalog/sources/sunlu-kingroon-creality.json) and [additional](../catalog/sources/2026-11-04-sunlu-esun-additional.json) HEX tables |
| **Total** | | **69** | **843** | **8 manufacturers** |
| FDplast | Russia | 0 | 0 | Scheduled after Chinese import; [official website](https://fdplast.ru/) |
| НИТ | Russia | 0 | 0 | Scheduled after Chinese import |
| Bestfilament | Russia | 0 | 0 | Scheduled after Chinese import; [official website](https://bestfilament.ru/) |

**Important:** these totals are **cataloged manufacturer color variants**, not physically calibrated appearances or proof of inventory availability. The Bambu Lab source is an official software color list, potentially including historical variants; other brands still have unimported lines and colors.

## Visual fidelity

- **515 variants** have at least one *manufacturer-published numeric display swatch*: 246 Bambu Lab (RGBA, including 18 gradient/multicolor), 139 eSUN (including 7 dual-shade entries), and 130 SUNLU.
- **328 variants** currently have only an official name or visual product listing, with **no invented HEX**. These need a verified/estimated visual color before a color-matched Fusion Appearance can be installed.
- **18 baseline visual presets** under [catalog/presets](../catalog/presets/) approximate surface roughness, glossy/silk finish, translucent appearance, fiber and sparkle effects. None has been calibrated in Fusion against physical prints.
- Source RGBA alpha does **not** represent a measured volumetric transmission coefficient. A full transparent/multicolor Fusion render is not solved by a single web swatch.
- For eSUN Matte Dual, two official shade components are retained per color instead of collapsing them to a single HEX.
- ELEGOO RFID/emoji spools and Creality Hyper PLA RFID are not automatically separate *visual materials* when the published color/formulation is equivalent; packaging functionality is not a new Appearance identity.

For meaning, provenance, source fidelity and Fusion API constraints see [material appearance specification](MATERIAL_APPEARANCE_SPEC.md).

## Next Chinese import priorities

1. **ERYONE:** verify remaining standard/matte/PLA-Lite/Silk/Speed PLA and PETG products; its pages frequently provide photographs without precise swatch values. Avoid transcribing opaque filenames as official color names.
2. **Creality:** ordinary PLA/Ender and special PLA/PETG lines; look for official color codes and check differences between the product family and RFID packaging.
3. **eSUN:** special PLA/PETG finishes and multi-color/rainbow filaments. Do not misrepresent a gradient spool by one solid HEX.
4. **SUNLU:** additional PETG/PLA finishes, dual-color variants, specialized Matte/HS/Silk. Prefer official `Color Code` tables.
5. **KINGROON and ELEGOO:** close gaps between official color variant names and reliable numeric shade references. Maintain separate color identity and packaging SKU.
6. **DeepLee:** confirm remaining official product lines and product-specific color lists, not generic marketplace references.

## Russian manufacturers (queued)

After the above Chinese stage: **FDplast → НИТ → Bestfilament**. Create one official-source-verified line at a time, covering PLA/PETG only. Russian-language display names can remain original and use stable transliterated IDs.

## Validation and distribution

- [Schema](../catalog/schema/line.schema.json) and [validators](../tools/validate_catalog.py): structural validation, identifier uniqueness, preset references and color-provenance invariants.
- [GitHub Actions](../.github/workflows/validate.yml) runs the validator. Passing tests does not establish Fusion rendering/optical accuracy.
- [Release distribution](DISTRIBUTION.md) is still **planned**. Catalog source JSON in GitHub is not yet a downloadable signed/versioned ZIP release.
