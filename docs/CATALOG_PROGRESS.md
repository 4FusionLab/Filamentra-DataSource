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
| [ERYONE](../catalog/brands/eryone/) | China | 4 | 36 | 36 independent estimated HEX references; official PLA+/PETG/PETG-CF and High Speed PLA listings |
| [ELEGOO](../catalog/brands/elegoo/) | China | 19 | 224 | Official [manufacturer product pages](../catalog/sources/elegoo-expanded-2026-11-04.json) and 147 independent estimated HEX references |
| [DeepLee](../catalog/brands/deeplee/) | China | 1 | 1 | Manufacturer name-only product record |
| [Creality](../catalog/brands/creality/) | China | 5 | 39 | Official [product lines](../catalog/sources/creality-expanded-2026-11-04.json); 26 independent estimated HEX values |
| [KINGROON](../catalog/brands/kingroon/) | China | 4 | 87 | Official [PLA and PETG lines](../catalog/sources/kingroon-pla-2026-11-04.json); 34 independent estimated HEX values |
| [SUNLU](../catalog/brands/sunlu/) | China | 8 | 130 | Official [initial](../catalog/sources/sunlu-kingroon-creality.json) and [additional](../catalog/sources/2026-11-04-sunlu-esun-additional.json) HEX tables |
| **Total** | | **72** | **902** | **8 manufacturers** |
| FDplast | Russia | 0 | 0 | Scheduled after Chinese import; [official website](https://fdplast.ru/) |
| НИТ | Russia | 0 | 0 | Scheduled after Chinese import |
| Bestfilament | Russia | 0 | 0 | Scheduled after Chinese import; [official website](https://bestfilament.ru/) |

**Important:** these totals are **cataloged manufacturer color variants**, not physically calibrated appearances or proof of inventory availability. The Bambu Lab source is an official software color list, potentially including historical variants; other brands still have unimported lines and colors.

## Visual fidelity

- **515 variants** have at least one *manufacturer-published numeric display swatch*: 246 Bambu Lab (RGBA, including 18 gradient/multicolor), 139 eSUN (including 7 dual-shade entries), and 130 SUNLU.
- **Six exact physical-print measurements** now have direct evidence (KINGROON: 3, ERYONE: 1, Bambu Lab: 1, SUNLU: 1). Two measured records also retain manufacturer HEX independently. **239 variants** remain estimated-only, **144** remain name-only. The default curated preview contains **519** source-backed numeric references, not the entire 902-entry research corpus. See [quality policy](VISUAL_DATA_QUALITY.md).
- **18 baseline visual presets** under [catalog/presets](../catalog/presets/) approximate surface roughness, glossy/silk finish, translucent appearance, fiber and sparkle effects. None has been calibrated in Fusion against physical prints.
- Source RGBA alpha does **not** represent a measured volumetric transmission coefficient. A full transparent/multicolor Fusion render is not solved by a single web swatch.
- For eSUN Matte Dual, two official shade components are retained per color instead of collapsing them to a single HEX.
- ELEGOO RFID/emoji spools and Creality Hyper PLA RFID are not automatically separate *visual materials* when the published color/formulation is equivalent; packaging functionality is not a new Appearance identity.

For meaning, provenance, source fidelity and Fusion API constraints see [material appearance specification](MATERIAL_APPEARANCE_SPEC.md).

## Next Chinese import priorities

1. **ERYONE:** expanded to PLA+, PETG, PETG-CF and full High Speed PLA color references. Next verify remaining standard/matte/Silk/Speed PLA and PETG products from its [official collection](https://eryone3d.com/collections/filament) and [download center](https://www.eryone.com/download-center/).
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
