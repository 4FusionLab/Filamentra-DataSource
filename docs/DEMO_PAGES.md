# Filamentra Catalog Demo — GitHub Pages CI

This is a read-only, interactive static visualization of the Filamentra PLA/PETG source catalog. It is **not** a live feed, does not make API calls to GitHub, and does not modify the catalog.

GitHub Pages was enabled and the initial publish succeeded on 2026-11-04 ([deployment workflow](https://github.com/4FusionLab/Filamentra-DataSource/actions/runs/41860887983)). The deployed URL is:

https://4fusionlab.github.io/Filamentra-DataSource/

## First-time GitHub configuration

1. Open the repository **Settings → Pages**.
2. Under **Build and deployment → Source**, select **GitHub Actions**.
3. Open **Actions → Build and publish catalog demo**.
4. Click **Run workflow**, select `main`, and start the run.
5. The job validates source JSON, builds static assets, and deploys the result to Pages. After a successful deployment, the website is available at the URL above.

If GitHub reports an organization policy, Pages permission, or environment protection error, resolve it in repository/org settings before rerunning. GitHub Pages must be explicitly enabled; adding a workflow alone does not guarantee a public URL.

## When the website updates

The site is **rebuilt and deployed only on an explicit manual request** via **Actions → Build and publish catalog demo → Run workflow** on `main`. Each deployment validates the JSON, checks browser JavaScript syntax, and verifies the generated snapshot before publishing; errors stop publication.

Regular pushes and pull requests do not deploy Pages. The independent `validate.yml` workflow continues to check code and catalog quality automatically without publishing. A successful build always represents the `main` commit selected for that manual run.

The demo is a static snapshot of the `main` commit checked out by the corresponding Pages deployment, not a live API feed.

## Build locally

Run from the repository root:

```shell
python -m pip install "jsonschema>=4.21,<5"
python tools/validate_catalog.py
python tools/build_demo.py --out dist
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000`. Hosting through a web server is necessary because the interface loads `data/catalog.json` via `fetch`.

The build script needs only the Python standard library and copies `demo/index.html`, `demo/app.css`, and `demo/app.js` to `dist`. The published JSON is generated from existing `catalog/brands/*/*.json` and `catalog/presets/*.json` at build time.

## Features

- Manufacturer, PLA/PETG, and product-line filters.
- Full-text search by color name, product line, manufacturer, manufacturer code, and HEX.
- Manufacturer RGBA/HEX swatches, documented physical-print measurements, and multicolor/gradient approximations.
- Curated source-backed colors shown by default. Toggle estimated HEX references or disable the swatch-only filter to see incomplete research entries.
- Distinct links for manufacturer source, independent sample measurement and approximate color reference.
- Name-only placeholders when no numeric color is available.
- Detail panel for origin references, manufacturer color codes, and estimated surface roughness.
- Mobile-compatible layout with collapsible filters and responsive swatch grid.
- The hero samples six source-backed colors from the generated catalog snapshot; they are not invented placeholders.

The UI approximates multiple manufacturer swatches with a flat CSS gradient. It is **not** a Fusion 360 rendering or physically accurate simulation of extruded multicolor filament.

## Security and scope

No catalog changes are made by visiting the demo. No private tokens are exposed, and the static site contains only already-public data. Catalog data and client-side scripts are bundled during the CI build. Anyone can access a public GitHub Pages site after it has been enabled.

When the repo is made private, public distribution may require a separate visibility and access review.

## Visual design

The catalog UI follows a product-specific Material Workbench direction. Its visual polish was informed by [unslop](https://github.com/heydamir/unslop), created by Damir Sokolovsky (CC BY 4.0): quiet neutrals and controls, consistent spacing and type, restrained emphasis, and real filament colors as the main visual content. This is an independent adaptation, not an official unslop release.

The card gradients for multi-color filament represent source-provided color combinations; they are intentionally **not** decorative interface gradients or calibrated physical renders.
