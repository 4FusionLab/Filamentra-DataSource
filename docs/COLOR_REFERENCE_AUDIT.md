# Color reference audit — 2026-11-04

> **Scope:** PLA and PETG. Color references and surface/optical properties have different evidence levels. This review improved incomplete color entries in existing brand lines; it did not claim physical color calibration.

## Evidence hierarchy

1. **Manufacturer-sourced swatch** (`hex_source: manufacturer` or manufacturer's `rgba_swatches`). This is a color code published by the manufacturer or preserved in official manufacturer software, **not** automatically a measured print color.
2. **Measured sample** (`hex_source: measured`, with method/instrument and lighting). A measured shade is meaningful only together with the measurement conditions.
3. **Estimated third-party visual reference** (`hex_source: estimated`, `visual_data_status: estimated`, `color_reference_url`, `color_reference_note`). Often an online color chip, **not** official manufacturer RGB. Use for previews with an explicit uncertainty label.
4. **Name only** (`visual_data_status: name_only` without numeric swatch). A valid product/color name is known, but no defensible display color can be asserted.

**Every product entry still retains its official manufacturer `source_url`** to document the existence of the product/variant. A third-party color reference is stored separately. Never convert `estimated` to `manufacturer` without obtaining a manufacturer publication for that exact shade.

The demo UI distinguishes **manufacturer**, **physical-print measurement** and **estimated** HEX. Only source-backed manufacturer or directly documented physical-print references appear in its curated default view; estimates require opt-in. GitHub Pages deploys **automatically after validated `main` source changes**, or manually using the dedicated workflow.

## Official catalogs rechecked

| Brand | Manufacturer sources | Finding |
| --- | --- | --- |
| Bambu Lab | [Official BambuStudio color registry](../catalog/sources/bambu-lab.json) | Source-pinned RGBA entries including dual and gradient; already incorporated |
| eSUN | [Official eSUN product references](../catalog/sources/esun-expanded-2026-11-04.json) | Publishes numeric HEX for multiple PLA/PETG lines; preserved as manufacturer data |
| SUNLU | [Official SUNLU color tables](../catalog/sources/2026-11-04-sunlu-esun-additional.json) | Publishes numeric HEX; preserved as manufacturer data |
| ELEGOO | [PLA](https://www.elegoo.com/products/pla-filament-1-75mm-colored-1kg), [PLA Basic](https://www.elegoo.com/products/pla-basic-filament-1-75mm-colored-1kg), [manufacturer filament catalog](https://www.elegoo.com/pages/elegoo-filaments) | Official sources confirm many product/color names, but no authoritative machine-readable HEX for every shade |
| Creality | [Hyper PLA manufacturer product page](https://store.creality.com/products/live-hyper-series-pla-3d-printing-filament-1kg), [CrealityPrint official source](https://github.com/CrealityOfficial/CrealityPrint) | Source verifies product families, but slicer filament defaults can omit color (empty `default_filament_colour`), so no fabricated official RGB |
| KINGROON | [PLA Basic](https://kingroon.com/products/kingroon-pla-basic), [PETG Basic](https://kingroon.com/products/kingroon-petg-basic) | Official naming and product variants; not enough calibrated or published numeric swatches |
| ERYONE | [Official PLA/PETG catalog](https://eryone3d.com/collections/filament), [PETG collection](https://eryone3d.com/collections/petg), [Download Center](https://www.eryone.com/download-center/), [High Speed PLA](https://eryone3d.com/collections/pla-high-speed) | Many more manufacturer-documented product variants and TDS files; not every shade has official RGB |
| DeepLee | [Manufacturer website](https://deeplee3d.com/) | One name-only listing so far; numeric shade remains unresolved |

## This backfill

- ELEGOO: **147 existing** records received explicitly estimated third-party HEX, and **29 additional** manufacturer-listed color variants were added with names only.
- KINGROON + Creality: **60 existing** records received estimated HEX.
- ERYONE: **3 new lines / 30 additional color variants** with independent estimated visual references; additionally **6 previously name-only High Speed PLA records** received such references.
- Total newly colorized entries: **243** (147 + 60 + 30 + 6).
- **No new colors were labeled as an official manufacturer HEX** merely because they appear on another website.

Independent source examples:
- [FilamentSelect: ELEGOO](https://www.filamentselect.com/filaments?brands=elegoo)
- [FilamentSelect: KINGROON](https://www.filamentselect.com/filaments?brands=kingroon)
- [FilamentSelect: Creality](https://www.filamentselect.com/filaments?brands=creality)
- [FilamentSelect: ERYONE](https://www.filamentselect.com/brands/eryone)

FilamentSelect can contain screen-level approximations as well as some measured entries; unless an individual reference explicitly documents a calibrated measurement, it is treated as **estimated**.

## Current completeness

| Evidence level | Records |
| --- | ---: |
| Manufacturer numeric swatch, including multi-color RGBA | 515 |
| Independently sourced estimated HEX, no physical measurement | 261 |
| Third-party physical measurement, no manufacturer swatch | 7 |
| Confirmed variant name, no defensible numeric color | 119 |
| **Total** | **902** |

Twelve individual physical-print measurement records are now linked with direct evidence: seven have no manufacturer numeric swatch, while five supplement official manufacturer swatches without overwriting them. The curated default preview therefore has **522** distinct source-backed entries (515 manufacturer + 7 measured-only); **261** estimated-only references require opt-in. See [measurement review](MEASURED_COLOR_REVIEW.md). All **18** finish presets remain experimental. [Sourcing policy](VISUAL_DATA_QUALITY.md).

## Pending work

1. **KINGROON:** 53 color names still without a numeric reference, mostly extra shades and PLA+/Matte variants. Seek source-verified per-SKU swatches or measurement; full record IDs are in [inventory](UNRESOLVED_COLORS.md).
2. **ELEGOO:** 59 names remain without numeric colors: multi-pigment Silk, PLA/PLA Basic, translucent, glow and CMYK. See [exhaustive inventory](UNRESOLVED_COLORS.md).
3. **Creality:** 6 remain: CR-PETG Yellow/Transparent Blue, lightweight PLA White/Black and two ambiguous PETG-CF color aliases.
4. **DeepLee:** one name-only product.
5. **ERYONE:** existing high-speed PLA is now colorized; more **manufacturer-verified product lines** are available to import from the official catalog, but their visual data must be independently researched rather than mass-generated from names.

**Visual product accuracy remains a separate Fusion calibration task:** verify roughness, reflection, tint, transmission and layer-direction effects with printed samples. The online color references alone do not determine these properties.
