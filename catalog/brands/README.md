# Filamentra manufacturer catalog

[Русская версия](README.ru.md)

One directory per manufacturer, containing one `brand.json` and one JSON file for each real product line.

```text
brands/
└── bambu-lab/
    ├── brand.json
    └── pla-matte.json
```

**Bambu Lab** has 24 imported PLA/PETG families and 246 variants from a pinned [BambuStudio registry revision](../sources/bambu-lab.json). Other Chinese brands have partial verified imports; see [population status](../../docs/CATALOG_PROGRESS.md).

Each line refers to a baseline visual preset in `../presets/`. The line and individual colors may override preset parameters **when evidence is available**; manufacturer color data and Filamentra visual estimates are clearly separated. Do not create a separate color file, or treat an estimated roughness as an official manufacturer specification.

See [catalog format](../../docs/CATALOG_FORMAT.md), [Fusion Appearance mapping](../../docs/MATERIAL_APPEARANCE_SPEC.md), and [contribution guide](../../CONTRIBUTING.md).
