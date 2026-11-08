# Procedural PBR textures — Filamentra

[Русская версия](TEXTURE_GENERATION.ru.md)

Filamentra provides a *typical*, uncalibrated normal/roughness pair for each of the 18 catalog presets. These are procedurally modeled filament surface archetypes, **not** lab measurements or manufacturer maps. They make a useful preview possible without implying physical accuracy.

## What is generated?

- OpenGL tangent-space (+Y) RGB normal maps and grayscale roughness maps.
- Deterministic, tileable **384 × 384 PNG** pairs, with a **8 × 8 mm** intended real-world footprint.
- A neutral sphere preview for every preset under identical virtual lighting (not a Fusion render).
- A browsable gallery at **/textures.html**, plus **data/textures.json** with source labels.
- Three files per preset: **normal_gl.png**, **roughness.png**, **preview.png**.

All source recipes, estimates and SHA-256-derived random seeds are centralized in tools/generate_texture_maps.py. When adding a new preset, its generator recipe is required; the build rejects missing/orphaned recipes.

## Build and CI

    python -m pip install 'jsonschema>=4.21,<5' 'numpy>=2,<3' 'Pillow>=11,<13'
    python tools/validate_catalog.py
    python tools/build_demo.py --out dist

The demo build **invokes texture generation automatically**. Both validation CI and GitHub Pages regenerate them. Validation checks JSON schemas, preset recipe coverage, reproducibility and edge tiling, and publishes the gallery and all texture PNGs as the downloadable \`filamentra-typical-pbr-textures\` workflow artifact. Generated PNGs are **not committed** to git.

All catalog presets reference package-relative paths under \`assets/presets/<id>/...\`; the same paths are generated inside the Pages output \`dist/\`.

## Important limits

- Existing scalar roughness numbers and grain amplitudes are Filamentra estimates based on finish type, not measured manufacturer optical properties.
- The roughness map already embeds the base scalar roughness. When installing in Fusion, do not blindly multiply the map by the base scalar a second time.
- Normal maps describe *generic material microtexture*, not true print-layer lines. Layer height/orientation is a separate print-process concern.
- Galaxy, Marble, Sparkle and Wood may also require albedo/effect masks mixed with each specific filament color. Normal and roughness cannot represent every colored inclusion.
- Translucent presets require separate transmission/IOR treatment; normal and roughness alone are insufficient.
- The sphere previews are for quick visual comparison, not validation of Autodesk Fusion viewport or Render behavior.

## Releases

Asset profiles must be versioned together with their catalog release. When adopting this in the Fusion add-in, resolve texture paths relative to the local catalog cache, apply physical texture scale consistently, and do not silently mutate Appearances in existing saved models after a generator revision.
