# Catalog population progress — 2026-11-04

> **Scope:** PLA and PETG families, including PLA+/Silk/Matte/CF, PETG-CF/GF/HF, translucent and other derived formulations. ABS, ASA, TPU, PA and PC are out of scope.

## Source priority and status

**Bambu Lab → other Chinese manufacturers → Russian manufacturers.** The BambuStudio color-registry snapshot is imported; expansion of Chinese lines is under way. REC PLA/PETG has been imported; FDplast and BestFilament have conservatively selected estimated colors from independently attributed data; НИТ remains without reliable numerical swatches.

The logical selection path is **Manufacturer → Material (PLA/PETG) → Product Line → Color**. Physical files are grouped by manufacturer and product line; the polymer is an attribute.

## Verified source records

| Manufacturer | Country | PLA/PETG lines | Color variants | Evidence |
| --- | --- | ---: | ---: | --- |
| [Bambu Lab](../catalog/brands/bambu-lab/) | China | 24 | 246 | [Pinned official BambuStudio RGBA registry](../catalog/sources/bambu-lab.json), with multi-color variants |
| [eSUN](../catalog/brands/esun/) | China | 7 | 139 | Official [original](../catalog/sources/esun.json), [additional](../catalog/sources/2026-11-04-sunlu-esun-additional.json), [expanded](../catalog/sources/esun-expanded-2026-11-04.json) color tables |
| [ERYONE](../catalog/brands/eryone/) | China | 4 | 36 | 36 independent estimated HEX references; official PLA+/PETG/PETG-CF and High Speed PLA listings |
| [ELEGOO](../catalog/brands/elegoo/) | China | 19 | 224 | Official product pages, plus targeted screen-color references; **59 unresolved colors** in [audit](UNRESOLVED_COLORS.md) |
| [DeepLee](../catalog/brands/deeplee/) | China | 1 | 1 | Manufacturer name-only product record |
| [Creality](../catalog/brands/creality/) | China | 5 | 39 | Official [product lines](../catalog/sources/creality-expanded-2026-11-04.json) and third-party color references; **6 unresolved** |
| [KINGROON](../catalog/brands/kingroon/) | China | 4 | 87 | Official [PLA and PETG lines](../catalog/sources/kingroon-pla-2026-11-04.json); **53 unresolved** |
| [SUNLU](../catalog/brands/sunlu/) | China | 8 | 130 | Official [initial](../catalog/sources/sunlu-kingroon-creality.json) and [additional](../catalog/sources/2026-11-04-sunlu-esun-additional.json) HEX tables |
| [Anycubic](../catalog/brands/anycubic/) | China | 3 | 68 | Official PLA Basic, PLA+ and PETG color HEX tables |
| [Polymaker](../catalog/brands/polymaker/) | China | 3 | 15 | Official HueForge color-reference table for selected PolyLite and Panchroma PLA |
| [REC](../catalog/brands/rec/) | Russia | 2 | 24 | Official RAL and SKU; third-party RAL→HEX tagged estimated |
| **Total with material lines** | | **83** | **1019** | **13 manufacturers** |
| [FDplast](../catalog/brands/fdplast/) | Russia | 1 | 4 | Official exact PETG SKUs + [third-party estimated screen HEX](../catalog/sources/2026-11-04-russian-selective-screen-estimates.json) |
| [НИТ](../catalog/brands/nit/) | Russia | 0 | 0 | Official PLA/PETG variants and SKUs verified; numerical values still missing ([audit](RUSSIAN_COLOR_SOURCE_AUDIT.md)) |
| [BestFilament](../catalog/brands/bestfilament/) | Russia | 2 | 6 | Exact PLA/PETG SKUs + [third-party estimated screen HEX](../catalog/sources/2026-11-04-russian-selective-screen-estimates.json) |

**Important:** these totals are **cataloged manufacturer color variants**, not physically calibrated appearances or proof of inventory availability. The Bambu Lab source is an official software color list, potentially including historical variants; other brands still have unimported lines and colors.

## Visual fidelity

- **598 variants** have a manufacturer numeric display swatch: 246 Bambu Lab, 139 eSUN, 130 SUNLU, 68 Anycubic, 15 Polymaker.
- **12 exact physical-print measurement references** now have direct evidence (KINGROON 3, ERYONE 1, Bambu Lab 4, SUNLU 1, Creality 3). Five measured entries also retain official manufacturer swatches. **301** variants remain estimated-only, **113** name-only; see the [full record-by-record audit](UNRESOLVED_COLORS.md). The curated preview now has **605** source-backed entries from the 1019-record catalog. See [measured-color review](MEASURED_COLOR_REVIEW.md) and [quality policy](VISUAL_DATA_QUALITY.md).
- **18 baseline visual presets** under [catalog/presets](../catalog/presets/) approximate surface roughness, glossy/silk finish, translucent appearance, fiber and sparkle effects. None has been calibrated in Fusion against physical prints.
- Source RGBA alpha does **not** represent a measured volumetric transmission coefficient. A full transparent/multicolor Fusion render is not solved by a single web swatch.
- For eSUN Matte Dual, two official shade components are retained per color instead of collapsing them to a single HEX.
- ELEGOO RFID/emoji spools and Creality Hyper PLA RFID are not automatically separate *visual materials* when the published color/formulation is equivalent; packaging functionality is not a new Appearance identity.

For meaning, provenance, source fidelity and Fusion API constraints see [material appearance specification](MATERIAL_APPEARANCE_SPEC.md).

**Latest backfill (2026-11-04):** six exact `Plus (+)` labels in KINGROON PLA+ now have separately attributed, third-party **estimated** display swatches ([source](https://layerlookup.com/kingroon/pla/)). No new product variants were added and the strict curated preview remains at **605**. [Unresolved inventory](UNRESOLVED_COLORS.md) has been reduced to **113**.

## Distributor SKU verification — 2026-11-04

Seven previously name-only KINGROON shades now have **exact manufacturer SKUs** and independent 3DJake source evidence: PLA Basic (Cyan, Apple Green, Turquoise Green) and PETG Basic (Sky Blue, Pink, Skin, Metallic Silver). Their exact 1 kg / 1.75 mm variant identity is independently attributable; see [source manifest](../catalog/sources/2026-11-04-kingroon-sku-verification.json). **No HEX values were imported** from these SKU records: the catalog still has **113 unresolved colors** (including 47 KINGROON), **301 estimated-only** and **605 curated preview candidates**. This is a provenance improvement, not an increase in color coverage.

A retailer claiming Kingroon PETG Sky Blue `#45C4EF` was **rejected** as untraceable to a primary palette/profile or measured sample. A retail `Copper` SKU was **not** merged into `Metallic Copper` without verified alias mapping. The missing-color audit now reports which unresolved records have SKU evidence, so further research can target measured swatches instead of repeatedly confirming product existence.

## ELEGOO PLA Basic / PLA Pro SKU verification — 2026-11-04

**Nine additional name-only ELEGOO variants** are tied to exact manufacturer part numbers by line and color (PLA Basic: Cream Yellow, Dark Green, Deep Grey, Light Cyan, Olive Green; PLA Pro: Beige, Hot Pink, Neon Green, True Red). Each keeps a per-record 3DJake URL and a separate `sku_verified` evidence claim. See [verified SKU manifest](../catalog/sources/2026-11-04-elegoo-basic-pro-sku-verification.json).

**No new HEX values were imported.** Neither the retailer pages nor the official color option names supply a defensible numeric shade for these exact line/color variants. Generic ELEGOO PLA / PLA Basic / PLA Plus screen swatches have intentionally **not** been reused for PLA Pro. ELEGOO remains at **59 unresolved**, and the entire catalog at **113 unresolved**. Including the earlier KINGROON batch, **16 previously unresolved shade identities now have exact SKU evidence**, enabling targeted photo/measurement research.

The official ELEGOO PLA Basic site spells one variant `Megenta`; a similarly misspelled Bambu Lab CMYK product is not acceptable evidence for its identity or HEX. The ELEGOO record remains unresolved.

## Next Chinese import priorities

1. **ERYONE:** expanded to PLA+, PETG, PETG-CF and full High Speed PLA color references. Next verify remaining standard/matte/Silk/Speed PLA and PETG products from its [official collection](https://eryone3d.com/collections/filament) and [download center](https://www.eryone.com/download-center/).
2. **Creality:** ordinary PLA/Ender and special PLA/PETG lines; look for official color codes and check differences between the product family and RFID packaging.
3. **eSUN:** special PLA/PETG finishes and multi-color/rainbow filaments. Do not misrepresent a gradient spool by one solid HEX.
4. **SUNLU:** additional PETG/PLA finishes, dual-color variants, specialized Matte/HS/Silk. Prefer official `Color Code` tables.
5. **KINGROON and ELEGOO:** close gaps between official color variant names and reliable numeric shade references. Maintain separate color identity and packaging SKU.
6. **DeepLee:** confirm remaining official product lines and product-specific color lists, not generic marketplace references.

## Russian manufacturers (queued)

**REC** PLA and PETG are now imported (24 RAL/SKU-based shades). FDplast PETG has 4 variants and BestFilament PLA/PETG has 6, each independently estimated but with manufacturer SKU evidence. НИТ remains research-only. See [Russian source audit](RUSSIAN_COLOR_SOURCE_AUDIT.md).

## Validation and distribution

- [Schema](../catalog/schema/line.schema.json) and [validators](../tools/validate_catalog.py): structural validation, identifier uniqueness, preset references and color-provenance invariants.
- [GitHub Actions](../.github/workflows/validate.yml) runs the validator. Passing tests does not establish Fusion rendering/optical accuracy.
- [Release distribution](DISTRIBUTION.md) is still **planned**. Catalog source JSON in GitHub is not yet a downloadable signed/versioned ZIP release.
