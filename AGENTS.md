# Filamentra DataSource development

[Русская версия](AGENTS.ru.md)

A separate catalog of real 3D-printing filaments for future Filamentra integration. It is not an add-in or a database of certified materials.

## Shared 4FusionLab rules

- Shared standards: https://github.com/4FusionLab/.github/blob/main/AGENTS.md; shared CI model: https://github.com/4FusionLab/.github/blob/main/RELEASE_PLATFORM.md.
- Communicate and make plans in Russian; use English for code and Fusion UI. Retain separate README.md and README.ru.md.
- Inspect current files and Git status before changes. Use Conventional Commits; a PR with passing checks is preferred, and direct push to main is allowed.
- Do not change Fusion manifest UUIDs, command IDs, OS support or package format without a migration plan. Do not commit secrets, tokens or personal CAD files.
- Where runtime exists, a push or merge to main creates a release only for paths in .github/release-paths.txt after successful CI. Use GitVersion.Tool 6.8.2, an automatically created immutable tag and GitHub Release; do not create tags manually.
- Docs, README, tests, AGENTS.md or CI changes must not independently publish a release. Pin shared Actions only to a specific commit SHA.
- Unit tests and ZIPs do not replace native Autodesk Fusion validation. Preserve existing limitations and compatibility evidence.

## Data-quality rules

- Sources of truth: docs/CATALOG_FORMAT.md, docs/VISUAL_DATA_QUALITY.md, docs/MATERIAL_APPEARANCE_SPEC.md and catalog/schema/*.json.
- Do not invent manufacturers, product lines, SKUs, colors or measurements. Preserve links to official sources, units, provenance, dates and confidence.
- Do not present marketing swatches as calibrated color. Respect copyright for photos and textures.
- Do not break stable catalog IDs or schemas without migration; account for Appearances already installed in users' Fusion documents.
- Release data consists only of curated catalog/brands/**.json, catalog/presets/**.json and catalog/schema/**.json. Research catalog/sources/** and demo/** must not independently create GitHub Releases.
- Pages publication through .github/workflows/publish-demo.yml remains manual; do not automatically couple it to a catalog release.
- Verify with `python tools/validate_catalog.py`, `python -m unittest discover -s tests -v`, `python scripts/build_release.py --version X.Y.Z` and the other steps in .github/workflows/validate.yml. Validation failure blocks publication.
