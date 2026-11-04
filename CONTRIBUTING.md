# Contributing to Filamentra DataSource

Thanks for helping build a reliable catalog of real 3D-printing filaments for [Filamentra](https://github.com/4FusionLab/Filamentra).

The catalog is in early development. For a new manufacturer, format change, or sizable set of products, open an [issue](https://github.com/4FusionLab/Filamentra-DataSource/issues) first.

## Suggest a product

Include:

- Official manufacturer and product-line names.
- Official color name, plus manufacturer color code or SKU if available.
- A link to the manufacturer's product page or technical reference.
- Polymer and documented finish/effects.
- Date when the source was checked.
- Whether an RGB/HEX value is published, measured, estimated, or unavailable.

Please **do not invent HEX values, SKUs, or unsupported manufacturer claims**. If a value is estimated, label it as `estimated`; if a color value is unknown, leave it absent.

## Submit catalog data

1. Add or update `catalog/brands/<manufacturer>/brand.json` and a JSON file for each product line.
2. Use stable lowercase kebab-case IDs. Do not change an existing ID because of a marketing-name edit.
3. Keep variants of the same color under one color entry. Different spool sizes or SKUs are packaging `variants`, not different Appearances.
4. Follow [catalog format](docs/CATALOG_FORMAT.md) and the [initial JSON Schema](catalog/schema/line.schema.json).
5. Include primary sources for product claims. Avoid copying protected photos and textures.
6. Explain the changes in a focused pull request, noting any uncertainty.

Data and assets should have documented redistribution rights. This repository does not yet have a chosen license; coordinate substantial contributed content with maintainers before submission.

## Review priorities

- Source-backed factual accuracy and provenance.
- Uniqueness and stability of brand, line, and color IDs.
- Correct data types and schema compatibility.
- No unlicensed photos, vendor art, or proprietary textures.
- No claim that a rendered Appearance exactly matches a printed object.

## Scope

This repository holds **catalog source data and its release contract**. Python Fusion API implementation, HTML palette behavior, and runtime installation belong in the [Filamentra Add-In repository](https://github.com/4FusionLab/Filamentra).

Visual appearance hints are not certified physical or mechanical material data.

## Report a problem

Create an issue with the affected brand/line/color ID, expected value, current value, and a verifiable source. For schema or release problems, include the catalog version and schema version.

Filamentra DataSource is independent of Autodesk and filament manufacturers.
