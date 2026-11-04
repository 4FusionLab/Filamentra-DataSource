# Missing-color backfill — PLA/PETG — 2026-11-04

**Rule:** only records without numeric visual data may be changed. No new filament products or lines were introduced in this batch.

## Exact color references found

| Existing color variant | New reference HEX | Provenance and uncertainty |
| --- | --- | --- |
| ELEGOO PLA-CF / Carbon Fiber Black | `#0C0908` | [FilamentSelect, exact PLA-CF Black](https://www.filamentselect.com/filaments/elegoo--pla-cf--black) |
| ELEGOO PLA-CF / Carbon Fiber Blue | `#0000FF` | [FilamentSelect, exact PLA-CF Carbon Fiber Blue](https://www.filamentselect.com/filaments/elegoo--pla-cf--carbon-fiber-blue) |
| ELEGOO PLA-CF / Carbon Fiber Green | `#008000` | [FilamentSelect, exact PLA-CF Carbon Fiber Green](https://www.filamentselect.com/filaments/elegoo--pla-cf--carbon-fiber-green) |
| ELEGOO PLA Silk / Silk Sky Blue | `#62A0EA` | [FilamentSelect, exact Silk PLA Sky Blue](https://www.filamentselect.com/filaments/elegoo--silk-pla--sky-blue) |
| ELEGOO PLA Silk / Silk Peach Pink | `#F7CFD4` | [FilamentSelect, exact Silk PLA Peach Pink](https://www.filamentselect.com/filaments/elegoo--silk-pla--peach-pink) |

All five FilamentSelect product pages explicitly identify their numeric colors as **approximate screen color, source authority unverified**, not measured from a physical sample. These swatches therefore use `hex_source: estimated`, `visual_data_status: estimated`, and their own **exact** `color_reference_url` and `evidence[]` entries marked `specialist_catalog`.

The saturated `#0000FF` and `#008000` values in particular may be generic digital approximations. They are **not** trusted to reproduce the look of carbon-fiber-filled plastic under real lighting. They remain excluded from the curated default preview, but can be shown when the user explicitly enables estimates.

**Do not** use a catalog's one-color approximation to fill co-extruded/multi-color Silk products. Their geometry and separate shade components require additional source data; one HEX would be misleading.

## Coverage after this batch

- **8 manufacturers, 72 product lines, 902 catalog entries** (unchanged total).
- 515 manufacturer-provided numeric display samples.
- 12 documented physical-print measurements, five overlapping manufacturer records.
- **522** curated preview candidates (unchanged).
- **242** estimated-only color entries (was 237).
- **138** unresolved name-only entries (was 143).

**Historical snapshot:** the 138 unresolved figure above was the count at this batch. A later batch resolved 19 more; for the later **113 unresolved variants** (after six additional KINGROON PLA+ estimates), see [the exhaustive audit](UNRESOLVED_COLORS.md). Prioritize exact SKU-specific evidence, without overwriting existing colors.

GitHub Pages builds and publishes only when its workflow is manually dispatched. Catalog changes in `main` still trigger validation.
