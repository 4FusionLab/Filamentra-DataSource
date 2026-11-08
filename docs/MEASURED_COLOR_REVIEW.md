# Print-measured color review — 2026-11-04

English | [Русский](MEASURED_COLOR_REVIEW.ru.md)

This change intentionally **does not add more products or colors**. It improves optical evidence for six pre-existing PLA/PETG variants using direct FilamentSelect pages that explicitly say **“Measured from a physical print”** and publish both RGB/HEX and CIELAB.

| Product variant | Existing display HEX | Physical print HEX | CIELAB (L*, a*, b*) | Evidence |
| --- | --- | --- | --- | --- |
| Creality Hyper PLA / Black | Missing | `#3C3C3D` | 25.41, −0.06, −0.71 | [Source](https://www.filamentselect.com/filaments/creality--hyper-pla--black) |
| Creality Hyper PLA / Red | Estimated `#C63D44` | `#C63D44` | 46.62, 54.76, 27.17 | [Source](https://www.filamentselect.com/filaments/creality--hyper-pla--red) |
| Creality Hyper PLA / Brown | Estimated `#9F523F` | `#9F523F` | 43.92, 30.17, 25.42 | [Source](https://www.filamentselect.com/filaments/creality--hyper-pla--brown) |
| Bambu Lab PLA Matte / Charcoal | Manufacturer `#000000` | `#424344` | 28.47, −0.23, −0.70 | [Source](https://www.filamentselect.com/filaments/bambu-lab--pla-matte--charcoal) |
| Bambu Lab PETG HF / Black | Manufacturer `#000000` | `#3D3E3F` | 26.21, −0.07, −0.79 | [Source](https://www.filamentselect.com/filaments/bambu-lab--petg-hf--black) |
| Bambu Lab PETG HF / Gray | Manufacturer `#ADB1B2` | `#A3A6A6` | 67.88, −0.56, −1.25 | [Source](https://www.filamentselect.com/filaments/bambu-lab--petg-hf--gray) |

For manufacturer swatches the catalog **retains the original manufacturer HEX** and adds `measured_sample` as a separate object. For existing third-party estimates, the same numeric value was upgraded to a recorded physical print measurement **only after verifying the exact product page**. For the previous name-only Creality Black, a measured primary HEX is now set.

## Why keep both?

When a web color is `#000000`, it often functions as a generic black display swatch. That does not mean a physical black print is a perfectly light-absorbing surface.

Calculated D65 **ΔE76** for manufacturer swatch versus reported printed-sample CIELAB:

| Product | Manufacturer vs printed-sample ΔE76 |
| --- | ---: |
| Bambu Lab PLA Matte / Charcoal | ~28.5 |
| Bambu Lab PETG HF / Black | ~26.2 |
| Bambu Lab PETG HF / Gray | ~4.1 |
| Bambu Lab PLA Matte / Ash Gray (previous measurement) | ~4.9 |
| SUNLU PLA Matte / Black (previous measurement) | ~29.4 |

These figures quantify the difference **between manufacturer RGB converted to CIELAB and the independent reported physical-print Lab value**. They are not direct experimental ΔE comparisons measured under identical light, geometry, and print settings. Do not interpret them as manufacturer quality failures.

## Evidence caveats

The external source states that a person confirmed colors using physical filament samples; its pages do not publish all instrumentation, illuminant, layer orientation, batch or color-management settings. The data are stronger than guessed web HEX, but **not an independently reproduced spectral BRDF or certified color standard**.

The validator checks that each `measured_sample` has source evidence with the exact same URL and checks that the recorded HEX and Lab numerically agree to ΔE76 ≤ 2.5 (transcription tolerance). That check establishes arithmetic consistency, **not truth of the sample's physical measurement**.

The first release should expose color provenance and compare swatch/print-sample values without claiming calibrated Fusion appearance. Do not copy photographs or distribution-protected textures from external pages.

See [Visual Data Quality](VISUAL_DATA_QUALITY.md). GitHub Pages is **not** republished automatically.
