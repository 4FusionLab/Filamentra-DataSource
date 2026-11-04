# Filamentra — Russia-first manufacturer expansion

Research date: **2026-11-04**. Scope: **PLA and PETG**, including additives/finishes such as PLA+, PLA HS, matte, silk, PETG HF and PETG-CF. This is a source discovery plan, **not an imported color catalog**.

## Demand signal and limitations

K3D surveyed its Russian-language 3D printing community on **2026-10-08 through 2026-10-10**:
https://www.k3d.tech/part-navi/filament/

K3D publishes the number of respondents evaluating each brand and a mean quality/price satisfaction score (0–10). Its table includes **31 brands with at least 50 votes**. The counts below are **not unit sales, revenue, market share, or a representative sample of Russian buyers**. The community is self-selected and scores are for brands in general, not individual PLA/PETG formulations.

Existing Filamentra brands on the high-response side: FDplast (569), НИТ (526), eSUN (467), Bambu Lab (463), ERYONE (463), ELEGOO/DeepLee (423 combined), BestFilament (303), Creality (269), KINGROON (257) and SUNLU (175). Several Russian brands have very limited numerical-color coverage today; expansion should not be mistaken for completion.

## Suggested priorities for uncovered brands

Ranked by **Filamentra usefulness + verified source accessibility**, not K3D quality rank.

| Wave | Brand | K3D 2026 votes; quality / price | Verified PLA/PETG source and what it contains | Research focus |
| --- | --- | --- | --- | --- |
| 1 | **STAR PLAST** | 138; 7.4 / 7.7 | [Official catalog](https://star-plast.com/), [PETG catalog](https://star-plast.com/catalog/petg_filament/) with individual article numbers, also PLA, PLA HS, Silk | PLA, PETG, PLA HS; exact shade names and SKUs, manufacturer photographs; do not call images official RGB |
| 1 | **KREMEN** | 119; 7.1 / 7.0 | [Official 3D filament catalog](https://kremen.ru/catalog/3dpechat/) with PLA and PETG product cards, colors, and variants | Start PLA and Start PETG; track color names and retailer/manufacturer item identity |
| 1 | **Filamentarno!** | 160; 7.4 / 3.6 | [Official catalog](https://filamentarno.ru/catalog.html) confirms PLA+ Standart, PETg Standart, PETg GF-8, PETg Lumi and a broad named palette | PLA+ / PETg; preserve transparent vs opaque and glow behavior, separate color from packaging |
| 1 | **PLASKO** | 107; 7.5 / 8.2 | [Official brand site](https://plasko.ru/) identifies PLA, PLA Pro High Speed, PETG and a stated >30-color palette | Verify that each listed color can be tied to a *line-specific* SKU and numeric source; don't assume 30 colors are all PLA/PETG |
| 1 | **JAMG HE** (China, available in Russia) | Not present in K3D 2026 >=50-vote table | [QIDI RU distributor](https://qidi3d.ru/catalog/jamg-he), [GeekStore3D retail](https://geekstore3d.ru/catalog/plastik-dlya-3d-pechati) list PLA, PLA+, Hi-Speed PLA+, PETG, Hi-Speed PETG, Matte, Silk & multicolor products | High local assortment value; check exact product/SKU and authoritative color-source availability; don't infer market share |
| 2 | **FusRock** | 50; 9.1 / 5.4 | [Official product portfolio](https://www.fusrock.com/ru/products), [PETG-Matte](https://www.fusrock.com/ru/products/petg-matte) lists named component colors | PETG-Matte, ToughPETG-HF, PETG-CF HF, PLA-Aero Pro; avoid overgeneralizing high score from 50 votes |
| 2 | **U3Print / Geek Filament** | 142; 7.2 / 6.8 | [Manufacturer identity/brand relationship](https://u3print.com/proizvoditeljam/); [local category coverage](https://shileyko.ru/proizvoditeli-filamenta/) | Verify U3Print / Geek Filament brand structure; PLA and PETG series, avoid treating manufacturing aliases as distinct brands |
| 2 | **3D-Club** | 76; 7.4 / 4.5 | [3D-Club official catalog](https://3d-club.ru/product-category/filament/) lists PET-G and PLA High Performance | Limited PLA/PETG subset; **do not confuse** 3d-club.ru with CLUB3D/club3d.club without identity evidence |
| 2 | **Пластикофф / Финик** (Некрасовский полимер) | 162; 5.7 / 7.3 for combined "Некрасовский полимер / ПластикОфф" | [Manufacturer page](https://nekras.ru/direction/filament) names two brands, PLA and PETG, >100-color claim for Пластикофф and AMS-capable Финик spools | Map the **brands and product lines separately**, establish current color/product SKU validity |
| 3 | **Гексалит** | 143; 7.2 / 8.6 | K3D community signal only verified so far | Find primary producer, official PLA/PETG catalog and exact SKU-color sources before adding |
| 3 | **Novaprint** | 105; 7.8 / 5.7 | [Company catalog](https://novaprint3d.ru/shop) appears primarily industrial (PP-GF, PA-GF, ABS-GF, composites) | Lower priority **until PLA/PETG product identity is verified**; broad brand popularity alone is not enough |
| 3 | **ATECO** | 58; 7.5 / 4.0 | [Independent polymer portfolio inventory](https://shileyko.ru/proizvoditeli-filamenta/) primarily engineering polymers | Exclude unless a current PLA/PETG product line is verified |

Other possible later candidates: Bamtco, Geeetech, Hi Tech Plast, LIDER-3D, CyberFiber, Prusament, QIDI, and RITTSUN; do not use availability or brand familiarity as a surrogate for verified color data.

## Import acceptance gate

1. **Identity:** official manufacturer or exact distributor source identifies `Manufacturer → Polymer → Product line → Shade`. All of `brand`, `polymer`, `line`, `color` must map to the **same** physical product formulation. Spool weight/refill/RFID usually belongs to a variant, not a new visual line.
2. **Numeric color:** manufacturer HEX/RGB/RGBA/RAL from its own source, a documented actual printed-sample measurement, or a **third-party exact-variant screen estimate** accompanied by its exact URL and uncertainty. Generic names ("White", "Copper") are not evidence of a specific numeric RGB.
3. **Preview:** official swatch or measured exact print only goes into strict curated preview. Estimated only if opt-in; name-only remains research backlog. **Do not add hundreds of name-only variants merely to inflate catalog size**.
4. **Effects:** multicolor needs multiple component swatches and distribution geometry; Glow needs ordinary light appearance separately from emission; translucent PLA/PETG needs explicit optical approximations rather than copying RGBA alpha as volumetric transmission.
5. **Coverage rule for new brand:** Prefer an initial well-sourced pilot of **1–2 PLA/PETG lines with several exact sourced shade references**, then expand. Do not claim first-party HEX when third-party or catalog photos are the only reference.
6. **Validation:** keep `tools/validate_catalog.py` and `tools/audit_missing_colors.py` green, update `CATALOG_PROGRESS.md` and source manifests; Pages deployment is manual-only and must **not** be triggered merely by catalog imports.

## Recommended next work package

**Batch A:** STAR PLAST + KREMEN + Filamentarno! — inspect primary color/article listings and obtain per-variant numeric values or documented estimates; import only eligible PLA/PETG subsets.

**Batch B:** PLASKO + JAMG HE — cross-check manufacturer series vs exact reseller colors/SKUs; import high-fidelity small subsets.

**Batch C:** FusRock + U3Print/Geek Filament + 3D-Club + Пластикофф/Финик — engineering/extended materials and identity-disambiguation pass.

**Key objective:** more **source-backed, visually usable shade records** per new manufacturer, not maximum raw JSON count.
