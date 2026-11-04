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

**Logical hierarchy:** manufacturer → base polymer (PLA or PETG) → product line → color. One JSON file per line; polymer is stored as a property, not a physical directory. Finish and optical effects remain attributes.

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

This excerpt contains one color. The [current Bambu Lab PLA Matte file](../catalog/brands/bambu-lab/pla-matte.json) holds **25 official color variants** sourced from the pinned [BambuStudio manufacturer registry](../catalog/sources/bambu-lab.json).

## Appearance inheritance and field provenance

The add-in resolves `preset.appearance`, then the line's optional `appearance`, then the specific color's optional `appearance`, **key by key**. The base color is the color variant's `hex`, not a preset property.

The renderer supports `surface_type`, `roughness`, `opacity`, estimated `transmission` (0–1), `ior`, `attenuation_distance_mm`, and optional `textures`. In Pages, Three.js uses the estimated transmission for a 2-mm sample; the future Fusion adapter must map transparency using the supported Fusion property model. Advanced transparency scale requires verification inside Fusion.

A line or color that specifies an `appearance` override should include `appearance_sources` with each modified key marked `manufacturer`, `measured` or `filamentra_estimate`. Published HEX has independent `hex_source` provenance.

Presets are **explicit estimates** until separately calibrated and Fusion-tested. They do not automatically become manufacturer specifications. Missing color values stay missing.

### Multi-color and transparency

- `rgba_swatches` preserves one or more exact 8-digit manufacturer RGBA display swatches when available (currently BambuStudio).
- `color_mode`: `solid`, `gradient`, `multicolor` or `unknown`. Gradient and multicolor retain all published colors, **not a made-up single HEX**.
- RGBA alpha from a vendor UI is **not** a measured optical transmission coefficient; `Clear` in BambuStudio is represented as `#00000000` and deliberately lacks `hex`.
- `visual_data_status: name_only` means a verified product/shade exists but no trustworthy numerical display color is available. The add-in **must not claim a color-correct Appearance** until a source-backed or clearly estimated color has been supplied.
- `manufacturer_color_code` and `manufacturer_palette_code` are optional identifiers distinct from the stable Filamentra color ID. Keep the original IDs for traceability.
- `catalog_status: listed_in_manufacturer_software` is not proof of current retail stock. BambuStudio may contain historical variants.

## Validators

- [Line Schema](../catalog/schema/line.schema.json)
- [Preset Schema](../catalog/schema/preset.schema.json)
- [Validation script](../tools/validate_catalog.py)
- [Material Appearance Specification](MATERIAL_APPEARANCE_SPEC.md)

Breaking changes after the first release require a new schema version. Dataset content versions are independent and distributed using [GitHub Releases](DISTRIBUTION.md).

## Content rights and quality

Manufacturer brand names and factual product attributes are references, not endorsement. Do not redistribute photos, logos or shader textures without rights. Published HEX values are display references; **not calibrated print measurements**. Filamentra creates visual Appearances, not engineering physical Materials.
