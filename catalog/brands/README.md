# Manufacturer catalog

Add one directory per manufacturer using a stable lowercase kebab-case ID:

```text
brands/
└── manufacturer-id/
    ├── brand.json
    ├── product-line-one.json
    └── product-line-two.json
```

A `brand.json` contains the manufacturer's ID, display name, and official website. Each product-line JSON contains its polymer, finish, sources, and `colors` array. Do not create a separate file per color or nest by polymer.

No manufacturer entries have been verified and published yet. Please start with the [catalog format](../../docs/CATALOG_FORMAT.md) and [contribution guide](../../CONTRIBUTING.md); do not insert invented example products into the production catalog.
