# Material specimen previews on GitHub Pages

Each eligible solid filament color gets a procedural WebP specimen derived from its numeric color reference plus the generic, uncalibrated PBR profile of its line. One Three.js WebGL viewer runs on the selected detail drawer; there are never hundreds of WebGL contexts on the catalog grid.

## Evidence and limits

- Priority: published physical printed-sample HEX, then manufacturer/catalog HEX, then an opaque single RGBA swatch.
- Missing numeric color stays unresolved, without a fabricated image.
- Multi-color and gradient records keep the documented color swatches rather than invented 3D stripes.
- Typical normal/roughness maps simulate microtexture; no physical color match, measured BRDF, layer orientation or actual Fusion Render is claimed.
- Transparent and particle-filled materials remain approximate.

## Pipeline

After catalog validation, tools/build_demo.py generates the PBR maps and calls tools/generate_material_previews.py to produce WebP images under dist/assets/material-previews. It writes paths into catalog.json and the count into meta.counts.material_previews.

The static viewer source is demo/material-viewer.js. CI builds its self-hosted ES module via the pinned Three.js and esbuild versions in package.json. The build validates all preview file references and the module. GitHub Pages deployment stays manual, as configured by the repository.

## Design direction

Existing graphite and muted sage UI remains unchanged. The physical-looking specimen carries the visual interest; source status and true numeric color swatches remain visible. The polish follows Damir Sokolovsky's unslop design guidelines: https://github.com/heydamir/unslop (CC BY 4.0).

## Local build

    python -m pip install 'jsonschema>=4.21,<5' 'numpy>=2,<3' 'Pillow>=11,<13'
    python tools/build_demo.py --out dist
    npm install --no-audit --no-fund --package-lock=false
    npm run build:viewer

Use an HTTP static server for local testing of modules and fetched textures.
