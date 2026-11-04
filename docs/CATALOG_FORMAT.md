# Filamentra catalog format

> **Pre-release Schema v1.** This document describes the current source-data contract. For exact properties, inheritance, provenance and Autodesk Fusion API mapping, see [Material Appearance Specification](MATERIAL_APPEARANCE_SPEC.md).

## Directory structure

```text
catalog/
├── brands/
│   ├── README.md
│   └── bambu-lab/
│       ├── brand.json
│       └── pla-matte.json
├── presets/
│   ├── pla-matte.json
│   ├── pla-glossy.json
│   ├── pla-silk.json
│   ├── petg-standard.json
│   ├── petg-translucent.json
│   ├── fiber-matte.json
│   └── sparkle-polymer.json
├── assets/                     # Optional future maps with redistribution rights
└── schema/
    ├── line.schema.json
    └── preset.schema.json
```

**Hierarchy:** manufacturer → product line → color variant. One JSON file per line. Polymer, finish and other properties are attributes for filtering, not directory levels.

## Product identities

- Brand ID: `bambu-lab`
- Product line ID: `bambu-lab/pla-matte`
- Color ID: `ash-gray`
- Full appearance identity: `bambu-lab/pla-matte/ash-gray`

The full ID must remain stable independently of SKU or translated display name. Packaging sizes, spools and refills are not additional colors.

## Line JSON

```json
{
  "schema_version": 1,
  "id": "bambu-lab/pla-matte",
  "brand": "bambu-lab",
  "name": "PLA Matte",
  "polymer": "PLA",
  "finish": "matte",
  "source_url": "https://bambu-lab-global.myshopify.com/products/pla-matte",
  "appearance_preset": "pla-matte",
  "colors": [
    {
      "id": "ash-gray",
      "name": "Ash Gray",
      "manufacturer_color_code": "11102",
      "hex": "#9B9EA0",
      "hex_source": "manufacturer",
      "source_url": "https://bambu-lab-global.myshopify.com/products/pla-matte",
      "verified_on": "2026-11-04"
    }
  ]
}
```

This excerpt contains one color. The [actual line file](../catalog/brands/bambu-lab/pla-matte.json) holds 17 officially published HEX values and codes from the Bambu Lab PLA Matte product page.

## Appearance inheritance and field provenance

The add-in resolves `preset.appearance`, then the line's optional `appearance`, then the specific color's optional `appearance`, **key by key**. The base color is the color variant's `hex`, not a preset property.

The renderer supports direct or advanced Fusion mappings for `surface_type`, `roughness`, `opacity`, `ior`, `attenuation_distance_mm`, and optional `textures`. Advanced transparency scale requires verification inside Fusion.

A line or color that specifies an `appearance` override should include `appearance_sources` with each modified key marked `manufacturer`, `measured` or `filamentra_estimate`. Published HEX has independent `hex_source` provenance.

Presets are **explicit estimates** until separately calibrated and Fusion-tested. They do not automatically become manufacturer specifications. Missing color values stay missing.

## Validators

- [Line Schema](../catalog/schema/line.schema.json)
- [Preset Schema](../catalog/schema/preset.schema.json)
- [Validation script](../tools/validate_catalog.py)
- [Material Appearance Specification](MATERIAL_APPEARANCE_SPEC.md)

Breaking changes after the first release require a new schema version. Dataset content versions are independent and distributed using [GitHub Releases](DISTRIBUTION.md).

## Content rights and quality

Manufacturer brand names and factual product attributes are references, not endorsement. Do not redistribute photos, logos or shader textures without rights. Published HEX values are display references; **not calibrated print measurements**. Filamentra creates visual Appearances, not engineering physical Materials.
