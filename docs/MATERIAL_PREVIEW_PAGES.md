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

## Estimated optical transparency (schema v1)

`appearance.transmission` is a scalar PBR visual parameter in [0,1], inherited
preset → line → color and optionally individually overridden. It is **not**
a manufacturer's alpha channel or a measured fraction of transmitted photons.
The existing `ior` and `attenuation_distance_mm` provide refraction and
optical absorption estimates; `opacity:255` remains independent alpha.

Two built-in archetypes are translucent PLA (transmission 0.49, absorption
length 7.5 mm) and translucent PETG (0.68, 12 mm). The verified Bambu PETG
Clear variant overrides PETG with transmission 0.94 and attenuation distance
75 mm. All such numbers are marked **filamentra_estimate**; line/color
values can replace them when meaningful source evidence is available.

Both the static preview generator and the interactive WebGL viewer model a
reference **2-mm wall thickness**, with the official 4FusionLab monogram image behind the specimen.
Translucent materials reveal the monogram to different degrees; opaque
materials occlude it. The result is qualitative, not a calibrated physics
prediction. The WebGL viewer converts attenuation distance from millimetres
into sample scene units and uses Three.js `attenuationColor` to tint transmitted
light. The stored color HEX remains separate from estimated optics.

Manufacturer Clear swatches such as `#00000000` have no numeric dye color.
Only for rendering such a *verified fully transparent screen swatch* the
preview uses a neutral tint (`#F6F9F7`), without writing a fictional HEX
or claiming physical color measurements. All other unknown colors still
remain without a preview.

## Branded optical reference (4FusionLab)

The source asset `demo/assets/brand/4fusionlab-logo.svg` is a **verbatim copy**
of the official 4FusionLab organization mark from
`4FusionLab/.github/assets/avatar.svg` (same repository owner; no AI-generated
replacement). `tools/build_demo.py` rasterizes it to a 512 × 512 PNG for the
Three.js texture loader. The Python WebP generator composites the same SVG at a
fixed 176 × 176 px size behind its 30-mm specimen. Opaque previews completely
cover the monogram inside the model; translucent previews reveal it in proportion
to their approximate transmission and optical attenuation. The background is
identical for every filament, so users can compare the effect directly.

The CI build checks that the rasterized logo is present and decodable and tests
that the monogram creates distinct tones inside a clear specimen. CairoSVG is
a build-time dependency only; the published site remains static.
