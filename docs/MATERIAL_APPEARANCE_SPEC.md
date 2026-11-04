# Material appearance specification — Filamentra

> **Pre-release Schema v1.** Catalog data is source-backed; visual presets are explicitly approximate until compared with real samples in Autodesk Fusion. This document is the contract for the catalog and the future Fusion Add-In, **not** proof of a tested rendering pipeline.

## Objective: visually faithful filament, not only a flat color

The appearance of a printed part depends on **base color**, **highlight shape (microfacet roughness)**, **surface microgeometry** (layer lines, fiber/flake content), **reflection direction**, **transmission/refraction** and sometimes subsurface-like diffusion. It also depends on printing temperature, layer height, surface orientation, lighting, and Fusion rendering mode. No single HEX value can encode these effects.

For every visual parameter, prefer **manufacturer measurement → reproducible measured sample → clearly labeled Filamentra estimate**. A manufacturer's promotional photo is not a measured BRDF or scattering dataset.

## Three levels of source data

1. **Preset**: `catalog/presets/<id>.json` — an estimated family-wide baseline such as `pla-matte`, `pla-silk`, `petg-translucent` or `fiber-matte`.
2. **Product line**: `catalog/brands/<brand>/<line>.json` — references the preset; overrides it only when the specific manufacturer line has better evidence or an intentionally reviewed profile.
3. **Color variant**: one record in the line's `colors` array — official manufacturer code, optional HEX, or multiple RGBA swatches. The color may override the line's appearance for special transparent, sparkle or metallic-look shades. Verified name-only entries must not be rendered as guessed colors.

The add-in resolves the visual state with a **property-level merge**:

```text
preset.appearance
  ← line.appearance (only specified properties)
    ← color.appearance (only specified properties)
      + color.hex as the primary color
```

`appearance_sources` at line/color level describes the origin of **each overridden rendering parameter**. Presets are `provenance: filamentra_estimate` and have status `uncalibrated`, `fusion_tested` or `reference_calibrated`. A concrete manufacturer color can have `hex_source: manufacturer` even when the roughness is a Filamentra estimate.

Do not reinterpret an old appearance applied in a user's saved model just because a preset changed.

## Canonical identity

```text
brand ID:      bambu-lab
line ID:       bambu-lab/pla-matte
color ID:      ash-gray
full ID:       bambu-lab/pla-matte/ash-gray
```

The full ID is stable; line names, colors, storefront codes and SKU can change. Packaging variants (e.g. spool/refill) do **not** create new appearances.

## Real source-backed sample

```json
{
  "schema_version": 1,
  "id": "bambu-lab/pla-matte",
  "brand": "bambu-lab",
  "name": "PLA Matte",
  "polymer": "PLA",
  "finish": "matte",
  "source_url": "https://bambu-lab-global.myshopify.com/products/pla-matte",
  "appearance_preset": "pla-matte",
  "colors": [
    {
      "id": "ash-gray",
      "name": "Ash Gray",
      "manufacturer_color_code": "11102",
      "hex": "#9B9EA0",
      "hex_source": "manufacturer",
      "source_url": "https://bambu-lab-global.myshopify.com/products/pla-matte",
      "verified_on": "2026-11-04"
    }
  ]
}
```

See [Bambu Lab PLA Matte](../catalog/brands/bambu-lab/pla-matte.json) for **25** variants from the pinned [official BambuStudio registry](../catalog/sources/bambu-lab.json). The official color swatches do **not** supply physically measured microfacet roughness or scattering coefficients, so `pla-matte` remains a **Filamentra estimate**. Across the complete Bambu PLA/PETG import, gradient/multi-color RGBA components are preserved rather than collapsed to one invented color.

## Supported schema v1 visual parameters

`appearance` may be set on a **preset**, **line** and **color**. It is optional on the line and color, where omitted properties inherit.

| Field | Meaning | Fusion API mapping | Status |
| --- | --- | --- | --- |
| `surface_type` | `opaque`, `transparent`, `metallic` | `Appearances.add(name, AppearanceSurfaceTypes.*)` | Documented |
| `roughness` | Microfacet highlight roughness 0–1, not profilometer Ra | `Appearance.roughness` | Documented |
| `opacity` | Alpha 0–255; **not** bulk light transmission | `Color.create(r,g,b,opacity)` → `Appearance.color` | Documented |
| `transmission` | Filamentra PBR light-transmission estimate 0–1; not measured visible-light transmittance | Three.js `MeshPhysicalMaterial.transmission` for Pages; Fusion adapter mapping TBD | Procedural estimate |
| Color `hex` | Manufacturer swatch, measured or estimated sRGB | RGB via `Appearance.color`; slot depends on surface type | Documented |
| `textures.base_color` | Optional source/locally generated albedo texture | `Appearance.colorTexture` | Documented |
| `textures.normal_gl` | OpenGL tangent-space normal map | `Appearance.normalTexture` | Documented |
| `textures.roughness` | Grayscale microfacet-roughness map | `Appearance.roughnessTexture` | Documented |
| `textures.tile_width_mm`, `tile_height_mm` | Intended real-world texture scale | `texture_RealWorldScaleX/Y` via `appearanceProperties` | Requires in-Fusion unit test |
| `ior` | Transparent volume refractive index | `appearanceProperties.itemById('transparent_ior')` | Documented property ID; adapter must check type/availability |
| `attenuation_distance_mm` | Estimate of light-absorption length in millimetres; used together with `transmission` and tint | Three.js `attenuationDistance` via specimen scale; Fusion `appearanceProperties.itemById('transparent_distance')` | Approximation; Fusion unit conversion needs verification |

Autodesk references: [Appearances.add](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/core_Appearances_add.htm), [Appearance](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/core_Appearance.htm), [AppearanceSurfaceTypes](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/core_AppearanceSurfaceTypes.htm).

**Do not introduce unverified properties as if they are directly supported.** The current Fusion API documentation does not provide a universal `Appearance.scattering`, `Appearance.subsurfaceScattering` or `Appearance.filamentLayerLines` scalar. Diffuse-looking matte polymer is approximated using roughness; transparent/tinted material can use a transparent surface, IOR and distance attenuation; fine-scale print texture can use a normal/roughness texture. These are *approximations to physical scattering*, not measured light transport.

## Choosing the right surface model

- **Opaque dielectric**: PLA Matte, PLA Basic, most PETG/ABS/ASA, standard silk and fiber-filled plastic. Even metallic-colored or silk filaments remain **dielectrics** unless a calibrated rendering experiment justifies a different shader. Do not select `metallic` solely from a product name.
- **Transparent volume**: truly clear/tinted products with through-volume transmission. Use `transparent`, `transmission` (0–1), `ior` and `attenuation_distance_mm`. The latter three are initially **Filamentra estimates**, not measured optical properties. A manufacturer RGBA swatch alpha is a display value, not a transmission coefficient. A `Color` alpha less than 255 on opaque appearance is a different rendering effect.
- **Metallic surface**: metal-like optical behavior, only if actually justified; not a default for shiny plastic.
- **Carbon/glass fiber, glitter, marble, layer lines**: require properly licensed or procedurally generated maps, calibrated in real-world scale. Roughness alone cannot create flakes, fibers or printed ridges.

## Texture rules

- Keep catalog assets under `catalog/assets/` in source, and inside a release archive alongside catalog JSON.
- JSON texture paths are package-relative `assets/...`, **never absolute filesystem paths**.
- `normal_gl` must use the **OpenGL (+Y)** convention required by Fusion.
- Test at **the same physical scale** and with the same UV alignment. Autodesk notes that whichever texture is connected first establishes the initial UV scale for subsequently connected maps.
- The Add-In resolves the local cached asset path before setting Fusion properties. Texture image content is embedded in the Fusion document on save, but the getter's path is not a durable catalog identifier.
- Avoid manufacturer photos or textures without redistribution rights.
- Do not generate fictitious fiber/glitter texture maps and call them manufacturer-supplied.

## API adapter contract

The Add-In must not expose Fusion-specific property IDs in source product JSON. It translates the resolved catalog profile:

```python
import adsk.core

SURFACES = {
    "opaque": adsk.core.AppearanceSurfaceTypes.OpaqueAppearanceSurface,
    "metallic": adsk.core.AppearanceSurfaceTypes.MetallicAppearanceSurface,
    "transparent": adsk.core.AppearanceSurfaceTypes.TransparentAppearanceSurface,
}

def install_basic_appearance(design, full_id, label, hex_color, resolved):
    # Existing-ID lookup and safe unique-name handling happen before this call.
    app = design.appearances.add(label, SURFACES[resolved["surface_type"]])
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    app.color = adsk.core.Color.create(*rgb, resolved.get("opacity", 255))
    if "roughness" in resolved:
        app.roughness = resolved["roughness"]
    return app
```

This snippet demonstrates only the **documented basic properties**; it is not a complete installation implementation. It intentionally omits identity persistence, transactions/rollback, textures and advanced optical properties.

**Advanced adapter checks**: inspect `appearanceProperties.itemById(...)`, verify the returned type and limits, verify units/scale for `transparent_distance`, apply values, re-read them, then save/reopen and render. If a property is unsupported, fail that optional feature **visibly** and report degraded fidelity; do not silently pretend the field was applied.

For roughness maps, Autodesk resets scalar roughness to 1.0 when attaching the map. Attach the map **before** setting scalar `roughness` if an attenuation cap is desired.

## Evidence and calibration workflow

1. Identify a real product and record the manufacturer's page, code, line, official color swatch, and check date.
2. Prefer supplied numeric optical data where available (measured color, BRDF, IOR, attenuation). Preserve the source and measurement conditions.
3. Choose a base preset; use only properties confirmed by the Fusion API.
4. Render a reference geometry with fixed lighting, camera, color management and dimensions. Compare with a physical test coupon captured under controlled, recorded conditions.
5. Tune `roughness`, transmission and texture scale, document the methodology and set the preset's status accordingly.
6. Keep user-visible fidelity labels, e.g. **Official color / Estimated finish**, **Measured color / Calibrated finish**.
7. Test the final Appearance in actual Fusion (Windows and macOS as relevant), including Save → Reopen. Test **Design viewport** and **Render** separately; they need not match perfectly.
8. Record Fusion build, operating system, renderer settings, print orientation/layer height, and known mismatch.

## Quality and compatibility

- Validate each line against [line.schema.json](../catalog/schema/line.schema.json) and each preset against [preset.schema.json](../catalog/schema/preset.schema.json).
- Reject unknown keys and unknown preset references. Allow no duplicate full color IDs.
- A missing HEX stays missing; never invent a value while labeling it official.
- A preset's `status: uncalibrated` is deliberate and must survive into UI metadata.
- Until the first public release, Schema v1 is a draft that may evolve. After shipping, breaking changes require a new schema version and distribution compatibility metadata.
- Distributing validated catalog data is independent from creating an engineering `Material` in Fusion; Filamentra installs a **visual Appearance** only.
