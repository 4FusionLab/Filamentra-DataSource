# Catalog format

> **Draft specification.** Schema v1 is the proposed initial contract for Filamentra DataSource. It has not yet been validated against a shipped add-in.

## Organization

```text
catalog/
  brands/
    example-maker/
      brand.json
      matte-pla.json
  schema/
    line.schema.json
```

Each manufacturer's directory has one `brand.json` and **one JSON file per product line**. Colors are entries in that line's `colors` array. Do not group data by polymer or finish at the filesystem level: those are searchable attributes.

## Identifiers

- Brand: `example-maker` — unique, stable lowercase slug.
- Product line: `example-maker/matte-pla` — unique across the catalog.
- Color: `sample-gray` — unique within its product line.
- Full color ID: `example-maker/matte-pla/sample-gray` — composed from the line ID and color ID.

Do not derive IDs from display names at runtime. Renaming a color or line should not change an existing ID. A manufacturer SKU is **not** a canonical ID because packaging, regional distribution, and product revisions may differ.

## Manufacturer record

```json
{
  "id": "example-maker",
  "name": "Example Maker",
  "website": "https://example.com/"
}
```

## Product line record

**Illustrative fictitious data — not an actual manufacturer's specification.**

```json
{
  "schema_version": 1,
  "id": "example-maker/matte-pla",
  "brand": "example-maker",
  "name": "Matte PLA",
  "polymer": "PLA",
  "finish": "matte",
  "source_url": "https://example.com/filaments",
  "colors": [
    {
      "id": "sample-gray",
      "name": "Sample Gray",
      "hex": "#777777",
      "hex_source": "estimated",
      "source_url": "https://example.com/filaments/sample-gray",
      "verified_on": "2026-11-04",
      "appearance": {
        "roughness": 0.85
      },
      "variants": [
        {
          "sku": "EXAMPLE-SKU",
          "diameter_mm": 1.75,
          "weight_g": 1000,
          "packaging": "spool"
        }
      ]
    }
  ]
}
```

The accompanying [line JSON Schema](../catalog/schema/line.schema.json) defines the initial field types and required fields. Adding a new optional field may be backwards-compatible; changing the meaning, nesting, or type of a field requires a new schema version.

## Semantics

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer data-format version, independent of catalog release version |
| `id` | Stable machine ID; use a lowercase kebab-case path |
| `brand` | Existing manufacturer ID |
| `polymer` | Base material, e.g. PLA, PETG, ABS, ASA, TPU |
| `finish` | Appearance category, e.g. matte, glossy, silk |
| `hex` | Optional sRGB-like visual reference, not necessarily a measured print color |
| `hex_source` | `manufacturer`, `measured`, or `estimated`; required when `hex` is set |
| `appearance` | Optional rendering hints; not certified physical properties |
| `variants` | Packaging-specific SKUs; do not duplicate color records for different spools |
| `source_url` | Source used to verify product claims |
| `verified_on` | Date source was last checked; does not imply manufacturer certification |

The `appearance.roughness` value is a proposed generic 0–1 hint, **not** a promise that Fusion API exposes or interprets a property of the same name in every Appearance type. Translation into Fusion properties belongs in the add-in.

## Data integrity rules

1. Product lines must refer to an existing brand.
2. Brand, product-line, and full-color IDs must be unique.
3. Never invent a product or turn an unverified visual estimate into a manufacturer's official value.
4. Missing color reference is preferable to an invented HEX. Omit `hex` (and `hex_source`) when no defensible estimate exists.
5. Preserve `source_url` and classify the origin of numerical or visual properties.
6. Packaging variants are optional and must not affect Appearance identity.
7. Do not redistribute product photos, logos, texture maps, or manufacturer assets without the necessary rights.

## Versioning

A **catalog release** tracks the dataset's changes. A **schema version** tracks how it must be parsed. The add-in must use schema compatibility information from the published index rather than assuming every catalog release has the same data shape.

See [distribution design](DISTRIBUTION.md).
