# Filamentra manufacturer catalog

One directory per manufacturer, containing one `brand.json` and one JSON file for each real product line.

```text
brands/
└── bambu-lab/
    ├── brand.json
    └── pla-matte.json
```

The first source-backed entry is **Bambu Lab → PLA Matte**, containing 17 manufacturer-published color HEX values and codes from the [official product page](https://bambu-lab-global.myshopify.com/products/pla-matte).

Each line refers to a baseline visual preset in `../presets/`. The line and individual colors may override preset parameters **when evidence is available**; manufacturer color data and Filamentra visual estimates are clearly separated. Do not create a separate color file, or treat an estimated roughness as an official manufacturer specification.

See [catalog format](../../docs/CATALOG_FORMAT.md), [Fusion Appearance mapping](../../docs/MATERIAL_APPEARANCE_SPEC.md), and [contribution guide](../../CONTRIBUTING.md).
