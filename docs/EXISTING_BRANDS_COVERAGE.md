# Filamentra — existing manufacturer coverage (November 5, 2026)

English | [Русский](EXISTING_BRANDS_COVERAGE.ru.md)

The catalog's main issue is **incomplete product lines** for brands already included, rather than a lack of new brands. Statuses are assessed **only for imported variants**; 100% of colors having HEX values does not mean that 100% of a manufacturer's range has been imported.

**Status at the time:** 16 brands (all 16 with lines), 97 PLA/PETG lines, 1,072 variants: **605** in strict preview, **330** with estimated HEX, and **137** with name/SKU only.

## Priority gaps

| Priority | Manufacturer | Status | Specific next task |
| --- | --- | --- | --- |
| 1 | FDplast | **2 lines, 14 shades**; five new PLA entries without HEX; nine PETG entries with estimated values | Continue the official PLA/PETG SKU audit, then find exact digital/physical color references; do not transfer generic Black/White to branded PLA names |
| 1 | НИТ | **4 lines, 6 entries**, all without HEX so far | Continue adding official PLA/PETG colors and find numerical sources; initial lines were imported in the [Russian manufacturer audit](RUSSIAN_COLOR_SOURCE_AUDIT.md) |
| 1 | ELEGOO | **19 lines, 224 variants**, including **59 without numerical color** | Fill in exact PLA, PLA Basic and PLA Pro by line and SKU; address Silk/CMYK/Glow/translucent separately |
| 1 | KINGROON | **4 lines, 87 variants**, including **47 without numerical color** | Find exact PETG Basic and PLA Basic shades; do not substitute High Speed PETG for ordinary PETG |
| 2 | BestFilament | **3 lines, 18 variants** after importing 12 shades on November 5 | Add PLA silk, PETG and PLA Pro; check that photos/SKUs and HEX belong to the same line |
| 2 | Creality | **5 lines, 39 variants**, including **6 without numerical color** | CR-PETG, RFID Lightweight, CF; separately cover transparency and foamed-plastic properties |
| 2 | Polymaker | **3 lines, 15 variants** with official HEX | Expand PolyLite/Panchroma using its catalog and official color matcher, keeping the lines distinct |
| 2 | STAR PLAST | **5 lines, 13 variants**, all SKU/name only | Obtain an exact screen reference / RAL by SKU; do not invent a color from its name |
| 3 | Filamentarno! | **3 lines, 12 estimated shades** | Add confirmed official combinations; check PETG GF/transparency |
| 3 | REC | **2 lines, 24 estimated shades** | The manufacturer publishes RAL; physical measurements and digital appearance need refinement |
| 3 | ERYONE | **4 lines, 36 variants**, mostly estimated HEX | Replace approximate estimates with measured or official references |
| 3 | DeepLee | **1 line, 1 variant** without HEX | Verify the manufacturer/product identity; do not expand questionable entries |

**Bambu Lab (246), eSUN (139), SUNLU (130), and Anycubic (68)** already have many official numerical references, a relatively well-prepared basis for preview. However, new lines, regional variants and discontinued colors still need separate audits. The absence of complete catalogs cannot be taken as evidence of complete imports.

## CI quality checks

`python tools/audit_brand_coverage.py --format summary` provides a manufacturer summary, including registered brands without lines.

`python tools/audit_brand_coverage.py --format markdown --out dist/audit/brand-coverage.md` produces a complete line-by-line report; `--format json` works similarly.

GitHub Actions generates both files in the **filamentra-catalog-quality-audits** check artifact and builds them alongside the audit of missing numerical colors. Pages is still not published automatically.

## Rule for the next import

First **match the product/line/SKU**, then establish **numerical color reliability**, then **texture/transparency/optical properties**. If the evidence is insufficient, leave the color as `name_only`; do not inflate the share of “ready materials” by guessing HEX values.

## November 5 batch — FDplast and НИТ

Four FDplast PETG color estimates were imported as `estimated`; five FDplast PLA and six НИТ entries were confirmed by SKU/product pages as `name_only`. [Detailed manifest](../catalog/sources/2026-11-05-existing-brands-fdplast-nit.json). Status checks are repeated in GitHub Actions; growth in `name_only` reflects the honest addition of real products, not an improvement in numerical coverage.
