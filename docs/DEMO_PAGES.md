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

The demo is **published manually only**. Use **Actions → Build and publish catalog demo → Run workflow** when a fresh snapshot is needed. Catalog pushes to `main` trigger separate validation, **not** Pages deployment.

Each deployment validates source JSON, checks browser JavaScript syntax, and verifies the generated snapshot before publishing; errors block publication. Pull requests do not deploy Pages. The independent `validate.yml` continues to validate without deploying.

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
- The search field remains visible on narrow screens even while secondary filters are collapsed.
- Grid or grouped-by-product-line browsing, color-name/manufacturer sorting, accurate manufacturer facet counts, and removable active-filter chips.
- Side-by-side comparison of up to four colors using the same static procedural-preview format; each item retains its provenance, manufacturer code, and original source link.
- Shareable catalog filter and color permalinks via URL query parameters, including direct entry into a selected color.
- Compact color details, one-click comparison and link copying, and expandable technical appearance parameters.
- Keyboard focus and mobile interaction refinements, including an inert closed details panel and phone-safe search font size.
- Clickable hero samples that open the corresponding genuine catalog record.


Comparison is an aid for relative selection, not a calibrated color-difference measurement. A source-backed HEX, a measured print sample, and a procedural surface rendering are distinct forms of evidence. The comparison intentionally uses precomputed previews rather than running four WebGL contexts at once. The interactive detail viewer retains its existing 4FusionLab-logo optical reference for translucent materials.

To run UI regression tests locally before manual publication:

```shell
node --test tests/demo_ux.test.mjs
node --check demo/app.js
```

The UI approximates multiple manufacturer swatches with a flat CSS gradient. It is **not** a Fusion 360 rendering or physically accurate simulation of extruded multicolor filament.

## Security and scope

No catalog changes are made by visiting the demo. No private tokens are exposed, and the static site contains only already-public data. Catalog data and client-side scripts are bundled during the CI build. Anyone can access a public GitHub Pages site after it has been enabled.

When the repo is made private, public distribution may require a separate visibility and access review.

## Visual design

The catalog UI follows a product-specific Material Workbench direction. Its visual polish was informed by [unslop](https://github.com/heydamir/unslop), created by Damir Sokolovsky (CC BY 4.0): quiet neutrals and controls, consistent spacing and type, restrained emphasis, and real filament colors as the main visual content. This is an independent adaptation, not an official unslop release.

The card gradients for multi-color filament represent source-provided color combinations; they are intentionally **not** decorative interface gradients or calibrated physical renders.
