# Catalog population progress — 2026-11-04

> **Scope:** 3D-printing filaments based on PLA and PETG, including blends/modifications such as PLA-CF, PETG-CF, Silk, Matte, High Flow and Translucent. Other base polymers are out of scope for now.

## Import priority

**Bambu Lab first → Chinese manufacturers → Russian manufacturers.** The source screenshot grouped ELEGOO / DeepLee, but these are separate brands in the data model.

Current logical hierarchy: **Manufacturer → Polymer (PLA/PETG) → Product Line → Color**. Files are physically organized by manufacturer and line; the `polymer` field supplies the logical material level.

## Snapshot

| Manufacturer | Region | PLA/PETG lines | Color variants | Source / status |
| --- | --- | ---: | ---: | --- |
| [Bambu Lab](../catalog/brands/bambu-lab/) | China | 24 | 246 | Official pinned BambuStudio color registry; 8-bit RGBA swatches, codes, multi-color preserved |
| [eSUN](../catalog/brands/esun/) | China | 2 | 79 | Official eSUN PLA+ and PETG color HEX lists |
| [ERYONE](../catalog/brands/eryone/) | China | 1 | 6 | Official Hyper Speed PLA image labels; no verified numeric colors |
| [ELEGOO](../catalog/brands/elegoo/) | China | 3 | 39 | Official PLA Matte, PETG Pro, Rapid PETG color names; HEX unknown |
| [DeepLee](../catalog/brands/deeplee/) | China | 1 | 1 | Official PLA Black description; numeric color unknown |
| [Creality](../catalog/brands/creality/) | China | 1 | 15 | Official Hyper PLA product variants; numeric color unknown |
| [KINGROON](../catalog/brands/kingroon/) | China | 1 | 35 | Official PETG Basic product variants; numeric color unknown |
| [SUNLU](../catalog/brands/sunlu/) | China | 3 | 60 | Official color-code tables for PLA+, PLA+2.0 and PETG |
| **Current total** | | **36** | **481** | **8 manufacturers represented** |
| FDplast | Russia | 0 | 0 | Queued; [manufacturer catalog](https://www.fdplast.ru/catalog/plastik_dlya_3d_pechati/) |
| НИТ | Russia | 0 | 0 | Queued; [manufacturer catalog](https://plastik-nit.ru/) |
| Bestfilament | Russia | 0 | 0 | Queued; [manufacturer catalog](https://bestfilament.ru/) |

These are **seeded catalog entries, not full retail assortment coverage** for each brand. In particular, Bambu Lab coverage reflects everything in a specific official **BambuStudio registry snapshot**; it may include discontinued products. Other Chinese manufacturers have additional PLA/PETG lines still to collect.

## Visual completeness

- **246 Bambu Lab variants:** manufacturer RGBA swatches from its own software repository; 18 gradient/multicolor variants retain multiple color components. One Clear variant uses an entirely transparent swatch and deliberately has no solid HEX.
- **79 eSUN variants + 60 SUNLU variants:** manufacturer web HEX values recorded, but these are not calibrated printed-surface measurements.
- **96 variants from ERYONE, ELEGOO, DeepLee, Creality and KINGROON:** official names verified, **no invented HEX**. These must not receive a falsely color-matched Fusion appearance until a trustworthy visual color estimate or measurement is added.
- **18 visual finish presets:** `uncalibrated` Filamentra estimates, not manufacturer optical measurements.

Manufacturer swatch values, physical colorimetry, and rendering fidelity are **different levels of evidence**. Do not equate them.

## Next import batches

### Chinese manufacturers — expand each real product line

1. eSUN: PLA-Basic, PLA-Matte, PLA+HS, PLA Silk, PETG variants; use official eSUN product color/HEX tables when available.
2. ERYONE: Standard PLA, PLA+, PETG, matte, silk, fast/transparent; product pages often show image labels without numeric values.
3. ELEGOO and DeepLee independently: additional PLA/PETG collections; verify each available color and separate packaging from color identity.
4. Creality: Hyper PETG, Hyper PLA RFID, Ender PLA, and PLA/PETG modifications.
5. KINGROON: PLA lines and PETG color swatch measurements.
6. SUNLU: PLA, PLA Matte, Silk, PETG2.0 and special appearance lines with official HEX tables.

### Russian manufacturers — after the Chinese phase

7. FDplast: standard PLA/PETG and separately identified SILK PLA variants; manufacturer uses named shades such as “Терракотовый воин”.
8. НИТ: official PLA/PETG ranges, PLA Matte and PLA Aero; verify line separation and product-level source links.
9. Bestfilament: PLA, PLA-шёлк and PETG based on official Bestfilament product pages.

**Do not automatically include other materials** (ABS, TPU, ASA, PA, PC). Do not introduce arbitrary color references for products without manufacturer numeric color values. For non-published optical data, add labeled uncalibrated presets and test them in Fusion.

## Source and quality trace

- Pinned [Bambu Lab source revision](../catalog/sources/bambu-lab.json).
- [eSUN import record](../catalog/sources/esun.json).
- [ERYONE/ELEGOO/DeepLee sources](../catalog/sources/next-chinese-brands.json).
- [SUNLU/KINGROON/Creality sources](../catalog/sources/sunlu-kingroon-creality.json).
- [Catalog specification](MATERIAL_APPEARANCE_SPEC.md) and [data schema](../catalog/schema/line.schema.json).
- [GitHub validation](../.github/workflows/validate.yml) checks shape, duplicate identifiers, references, HEX formats and source metadata. Successful validation does not prove physical visual fidelity or current inventory.

**Distribution:** A public release ZIP and compatibility index are still planned; no release pipeline or published catalog version is implied by these source entries.
