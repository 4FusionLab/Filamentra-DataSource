<p align="center"><img src="https://raw.githubusercontent.com/4FusionLab/.github/main/assets/banner.svg" alt="4FusionLab" width="100%"></p>

<h1 align="center">Filamentra DataSource</h1>
<p align="center"><strong>The colors behind Filamentra.</strong><br>A source-backed catalog of real 3D-printing filaments — brands, product lines, shades, and finishes.</p>

<p align="center">
  <a href="README.ru.md">Русский</a> ·
  <a href="https://github.com/4FusionLab/Filamentra">Filamentra Add-In</a> ·
  <a href="https://github.com/4FusionLab/Filamentra-DataSource/issues">Suggest a filament</a>
</p>

---

## What lives here?

**Filamentra DataSource** is the catalog-data companion to [Filamentra](https://github.com/4FusionLab/Filamentra), a planned Autodesk Fusion add-in by **4FusionLab**.

The add-in aims to let makers browse real filament products and install a matching **visual Appearance** into the current Fusion design on demand. This repository is dedicated to the **data**, not the Fusion UI or add-in code.

- **Manufacturers:** official brand names and references.
- **Product lines:** material family, finish, and documented variants.
- **Colors:** official names, stable IDs, color references, and provenance.
- **Distribution:** versioned, validated catalog bundles intended for GitHub Releases.
- **Independence:** catalog data remains usable without Autodesk Fusion.

## How the catalog is organized

```text
catalog/
├── brands/
│   └── <manufacturer>/
│       ├── brand.json
│       ├── <product-line>.json
│       └── ...
└── schema/
    └── line.schema.json

docs/
├── CATALOG_FORMAT.md
└── DISTRIBUTION.md
```

One JSON document per product line, containing its color variants. The logical hierarchy is **manufacturer → material (PLA/PETG) → product line → color**. Polymer is a field for grouping and filtering, so it does not require a physical directory level.

See [catalog format](docs/CATALOG_FORMAT.md) and the [high-fidelity Fusion Appearance specification](docs/MATERIAL_APPEARANCE_SPEC.md) for the data model, visual inheritance, API support, and evidence rules.

### Initial verified data

- **Bambu Lab:** [24 lines / 246 PLA+PETG color variants](catalog/brands/bambu-lab/) from a pinned official [BambuStudio source revision](catalog/sources/bambu-lab.json), preserving multi-color swatches and manufacturer identifiers.
- **Catalog today:** **8 manufacturers / 72 PLA+PETG product lines / 902 color variants**: **515 manufacturer swatches**, **243 explicitly estimated third-party HEX references**, and **144 name-only variants**. [Coverage](docs/CATALOG_PROGRESS.md) · [Provenance audit](docs/COLOR_REFERENCE_AUDIT.md).
- **Chinese brands:** eSUN, ERYONE, ELEGOO, DeepLee, Creality, KINGROON and SUNLU have source-backed records, but coverage and optical fidelity remain incomplete. Russian manufacturers follow the Chinese stage.
- **Visual profiles:** [18 experimental surface presets](catalog/presets/), explicitly not measured optical manufacturer properties.
- **Progress and priorities:** [catalog population status](docs/CATALOG_PROGRESS.md), including remaining Chinese lines and Russian brands.
- **Validation:** [JSON Schemas](catalog/schema/) and [catalog validation workflow](.github/workflows/validate.yml) check data structure, references and stable IDs.

**Visual fidelity policy:** retain official colors when published; approximate missing optical properties with clearly labeled, line-specific presets, then calibrate against real print samples. Rendering may differ across Fusion viewport, Render workspace and physical output.

## Browse the catalog in your browser

**[Filamentra Catalog Demo](https://4fusionlab.github.io/Filamentra-DataSource/)** — a searchable, responsive preview of PLA/PETG manufacturers, product lines, colors, and their data provenance. Colorful gradients are illustrative, not physically calibrated Fusion renderings.

The site updates **only when the [manual GitHub Actions workflow](.github/workflows/publish-demo.yml) is run** — not on every commit. The first GitHub Pages deployment **succeeded on November 4, 2026** ([workflow run](https://github.com/4FusionLab/Filamentra-DataSource/actions/runs/41860887983)). Future publishing remains manual-only: [how to rebuild the preview](docs/DEMO_PAGES.md).

## Catalog quality comes first

- **Real products only.** Do not invent a manufacturer, series, color, or SKU.
- **Evidence matters.** Prefer manufacturer sources; record when and where claims were checked.
- **Approximate means approximate.** A web swatch or product photograph is not a calibrated physical color measurement.
- **Stable identity.** Catalog IDs should survive marketing-name changes.
- **Visual, not structural.** These appearances are not certified material properties for engineering simulation.
- **Respect ownership.** Do not copy manufacturer photographs or textures without appropriate rights.

## Releases and compatibility

The intended distribution model separates **catalog content version** from **JSON schema version**:

| Item | Purpose |
| --- | --- |
| Catalog release (`vX.Y.Z`) | New or corrected product data |
| Schema version (`1`, `2`, …) | Structure the add-in can parse |
| `catalog-index.json` | Available releases, compatibility, assets, and checksums |
| `catalog-schema-vN.zip` | Downloadable snapshot for a supported schema |

The add-in will select the newest **compatible** snapshot and cache it locally for offline use. Catalog changes must not silently overwrite appearances already installed in an existing Fusion design.

**Status: first import complete for the official BambuStudio registry; other manufacturers are partially populated.** Visual presets remain uncalibrated in Fusion, and no validated GitHub Release distribution has been published. See [progress](docs/CATALOG_PROGRESS.md) and [distribution design](docs/DISTRIBUTION.md).

## Contribute a filament

Found a missing manufacturer, series, or shade? [Open an issue](https://github.com/4FusionLab/Filamentra-DataSource/issues) with the exact product name and a manufacturer reference. Please read the [contribution guide](CONTRIBUTING.md) before submitting catalog data.

**The 4FusionLab family:** [Filamentra](https://github.com/4FusionLab/Filamentra) · [Perfora](https://github.com/4FusionLab/Perfora) · [Selectra](https://github.com/4FusionLab/Selectra) · [Ejix](https://github.com/4FusionLab/Ejix) · [Planara](https://github.com/4FusionLab/Planara) · [RuEn](https://github.com/4FusionLab/RuEn)

## A little workshop mythology

**Filamentra**, goddess of filaments, keeps an endless treasury of colored threads. This repository is her ledger of shades — the records behind the appearances makers will bring into their designs.

<sub>An independent [4FusionLab](https://github.com/4FusionLab) project. Not affiliated with or endorsed by Autodesk or filament manufacturers. Product names and trademarks belong to their respective owners. No license has been selected for the catalog yet; public visibility does not itself grant reuse rights.</sub>
