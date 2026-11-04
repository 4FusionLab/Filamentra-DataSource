# Visual data quality and sourcing — Filamentra

> **Policy date: 2026-11-04.** Scope: PLA/PETG only. Goal: **fewer reliable Appearances, not more speculative records**.

## What sources may be used?

Filamentra is **not restricted to manufacturer catalogs**. Use manufacturer data, official documentation and software, authorized distributors, independent stores, SKU-specific retailer listings, technical databases, and physical-sample measurements.

A source's **role** is distinct from its claim:

| Source role | Can establish | Cannot establish without extra evidence |
| --- | --- | --- |
| Manufacturer or official slicer registry | Official line/color identity, manufacturer numeric display swatch or code, official feature description | That the displayed swatch equals a printed surface under real illumination |
| Authorized distributor or independent retailer | Exact shade, packaging/SKU/barcode, sometimes color swatches and TDS links | That an extracted pixel or marketing photo is an official manufacturer RGB |
| Marketplace | Listing availability/packaging when product identity is reliable | Authenticity, calibrated optical values, or manufacturer approval by itself |
| Specialist catalog / measurement lab | Screen reference, verified RGB/CIELAB **when directly documented**, physical printed-sample measurements | Generalizing a measured sample to all print conditions, directions and filament batches |
| Product image | *Estimated* visual reference, if a method and image URL are recorded | Calibrated hue, reflectance, roughness, transmittance, or dispersion |

**Evidence of product existence and evidence of color are separate.** We record `source_url` for identity; `evidence[]` with `source_type`, `claim`, `url`, `checked_on` for additional sources; `color_reference_url` for a non-official HEX; and `measured_sample` for third-party physical print measurements.

## Acceptance tiers (derived at build time)

- **Curated preview**: manufacturer numeric swatch **or** independently documented physical-sample measurement for an exact line/color.
- **Uncalibrated/reference-only**: third-party estimated HEX or a storefront picture with source known. Hide by default in the public demo; may be enabled explicitly.
- **Unresolved**: verified product or color name with no usable numeric visual reference. Store as a research backlog, but never synthesize a HEX by color name.

The site renders curated references by default; estimates require an opt-in and unresolved variants require opting out of the "only with a swatch" filter. This is a **display-quality gate**, not an assertion that 3D rendering is calibrated.

## When measured and manufacturer colors disagree

**Preserve both.** A manufacturer HEX is a brand swatch; a physical measurement describes a printed sample under conditions that may not be fully disclosed.

Example from exact variant references:

| Variant | Manufacturer display HEX | Physical print measurement | Source |
| --- | --- | --- | --- |
| Bambu Lab PLA Matte **Ash Gray** | `#9B9EA0` | `#8D9499` | [FilamentSelect](https://www.filamentselect.com/filaments/bambu-lab--pla-matte--ash-gray) |
| SUNLU PLA Matte **Black** | `#000000` | `#454546` | [FilamentSelect](https://www.filamentselect.com/filaments/sunlu--pla-matte--black) |
| KINGROON Matte PLA **Red** | No numeric manufacturer swatch | `#D4454B` | [FilamentSelect](https://www.filamentselect.com/filaments/kingroon--matte-pla--red) |

The `measured_sample` object carries a **separate** hex, Lab triplet, exact evidence URL, source type, measurement-conditions status and validation date. The client can prefer this print-oriented reference for a visual preview but must label it separately.

The measurement references above say a **physical print** was measured; they do **not** provide a complete reproducible protocol for illuminant, instrument, sample geometry, layer height or color management. Thus no color match is guaranteed.

## Distributor-confirmed SKU examples

The following sources verify **specific products and packaging**, not the reported optical reflectance:

- [Bambu Lab Ash Gray — 3DJake](https://www.3djake.com/bambu-lab/pla-matte-ash-gray): refill `A01-D3-1.75-1000-SPLFREE`.
- [SUNLU Matte Black — 3DJake](https://www.3djake.com/sunlu/pla-matt-black): `6933582309626`, 1.75 mm, 1 kg.
- [ELEGOO Matte Ruby Red — 3DJake](https://www.3djake.com/elegoo/pla-matte-ruby-red?sai=22787): `50.203.0252`, 1.75 mm, 1 kg.

These appear in `variants[]` and `evidence[]`; they **do not** replace stable full catalog IDs.

## Rejection examples / failure modes

1. **Do not conflate similarly named product lines.** A listing labeled “KINGROON Matte PLA Orange” can refer to a different record from “KINGROON PLA Matte Orange”; different online HEX references alone are insufficient to merge them.
2. **Do not borrow a color from another brand.** “Ruby Red” and “Matte Ruby Red” are not universal color standards.
3. **Check color-versus-name inconsistencies.** A third-party listing representing ELEGOO Ruby Red with a dark blue HEX is not credible without direct SKU verification and stronger evidence.
4. **Don't treat packaging as material identity.** A different spool, refill, mass, region, or RFID tag does not automatically define a different Appearance.
5. **Don't copy product imagery without rights.** Store links and factual manufacturer data; render from numeric swatches or procedurally licensed assets.
6. **Never automatically promote a manufacturer's photo to `hex_source: manufacturer`.** If sampling a promotional picture, mark `estimated` with URL, calibration procedure, and uncertainty.
7. **Differentiate “brand official color code”, “brand swatch” and “physical measurement”.** All are useful, but not interchangeable.

## Pipeline and manual publication

- `tools/validate_catalog.py` enforces JSON schema, stable identity, consistency of swatches and direct evidence on measured samples.
- The ordinary validation workflow can build/test the static demo without **publishing** it.
- Publishing GitHub Pages is **manual-only** via `workflow_dispatch` in `.github/workflows/publish-demo.yml`.
- A successful CI build **does not** update GitHub Pages. A manual Pages deployment publishes the current curated view.

## Current status

At 2026-11-04, the source catalog has **8 brands, 72 lines, 902 variants**: 515 with manufacturer numeric swatches, **12** with linked third-party physical measurements (five of those also retain official manufacturer swatches), **237** remaining estimated-only references, and **143** unresolved names.

This yields **522 curated preview candidates** from official numeric source or physical-sample evidence, **not** 522 physically accurate Fusion materials. Finish, BRDF, transmission and print-layer effects remain uncalibrated.

See [six additional measured sample confirmations](MEASURED_COLOR_REVIEW.md). The CI now checks HEX-versus-Lab conversion consistency, but cannot certify the external measurement protocol.

**Next work:** resolve exact SKU-level references and expand physical-sample coverage for existing PLA/PETG color families. Do not pad catalog totals with weakly sourced colors.
