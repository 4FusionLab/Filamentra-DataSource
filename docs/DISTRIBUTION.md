# Catalog distribution and compatibility

[Русская версия](DISTRIBUTION.ru.md)

> **Historical design proposal, not the implemented release contract.** A curated ZIP release now exists; the proposed index, schema-specific bundles and client update flow below are not established by that release. See the [current release policy](../.github/RELEASE_POLICY.md).

## Goals

1. Distribute immutable snapshots through **GitHub Releases**.
2. Let a given Filamentra Add-In install the newest catalog it can parse.
3. Avoid requiring a token for public downloads.
4. Load a cached snapshot first; do not block the palette on network access.
5. Never modify installed appearances in saved designs merely because source data changed.

## Separate version axes

- **Catalog SemVer**, e.g. `1.2.0`: which manufacturer, line, and color records are shipped.
- **Schema integer**, e.g. `1`: the structure of the JSON records.
- **Add-In SemVer**, e.g. `0.5.0`: the client implementation; evolves separately.

Ordinary additions or corrections can use the same schema; breaking structural changes require a new schema. An Add-In declares the schema versions it understands.

## Proposed release assets

A stable `v1.2.0` release could attach:

```text
catalog-index.json
catalog-schema-v1.zip
```

If a future release supports multiple schema generations, it may include `catalog-schema-v1.zip`, `catalog-schema-v2.zip`, etc. Older catalog releases remain available as fallback.

The `catalog-schema-vN.zip` bundle contains a versioned, self-contained snapshot of `catalog/brands/` plus the applicable schema. The add-in should never fetch raw files from `main` as its production source, because the branch is not an immutable snapshot.

## Proposed index

The newest stable GitHub Release includes an index of **all retained compatible release choices**, not only its own assets.

```json
{
  "index_schema": 1,
  "releases": [
    {
      "version": "1.2.0",
      "tag": "v1.2.0",
      "variants": [
        {
          "schema": 2,
          "min_addin": "0.8.0",
          "asset": "catalog-schema-v2.zip",
          "sha256": "<64 lowercase hexadecimal characters>"
        },
        {
          "schema": 1,
          "min_addin": "0.3.0",
          "asset": "catalog-schema-v1.zip",
          "sha256": "<64 lowercase hexadecimal characters>"
        }
      ]
    },
    {
      "version": "1.1.0",
      "tag": "v1.1.0",
      "variants": [
        {
          "schema": 1,
          "min_addin": "0.3.0",
          "asset": "catalog-schema-v1.zip",
          "sha256": "<64 lowercase hexadecimal characters>"
        }
      ]
    }
  ]
}
```

**Values above are illustrative, not published releases.** When the contract is implemented, document exact compatibility bounds and index-schema evolution. If an Add-In does not understand the current index format, it must use the verified cached catalog instead of guessing.

The intended public index URL is:

```text
https://github.com/4FusionLab/Filamentra-DataSource/releases/latest/download/catalog-index.json
```

Once releases exist, the Add-In can download a chosen asset using its release tag:

```text
https://github.com/4FusionLab/Filamentra-DataSource/releases/download/<tag>/catalog-schema-v1.zip
```

GitHub's `latest` release points to the latest eligible stable release, not necessarily every prerelease or draft.

## Client update flow

1. Open the last verified cache immediately.
2. At most once per configured update interval, fetch the newest index (with short timeouts); offer a manual refresh action.
3. Parse and validate the index. Filter variants by supported schema and Add-In compatibility range.
4. Choose the newest compatible **catalog release**, then the preferred supported schema.
5. If already cached, do nothing. Otherwise download the exact release asset.
6. Verify SHA-256, maximum allowed size, expected archive paths, and every JSON record before activation.
7. Extract into a temporary directory with ZIP path-traversal protection; atomically activate the new snapshot after successful verification.
8. Keep the previous valid snapshot as rollback. On any network/validation failure, continue offline with the cache.

Do not change user-installed Fusion Appearances silently; updating a catalog is distinct from updating an Appearance in a design.

## Planned publishing pipeline

On a release tag:

1. Validate all manufacturer and product-line records against schemas.
2. Check referential integrity, duplicate identifiers, color provenance, source URLs, and data licensing constraints.
3. Build deterministic ZIP archives for the supported schema variants.
4. Compute checksums.
5. Construct the index, retaining previous release entries that remain valid and available.
6. Publish release assets and only then expose a complete index through the newest release.

This proposed index-based publishing pipeline still needs implementation and testing. Existing CI publishes a curated ZIP under the current release policy; that does not establish this proposed compatibility-index contract.

## Visibility and credentials

The repository is currently **public**, so public Release Assets can be downloaded without embedding credentials in the Add-In. If the data must become private, a GitHub token or authenticated proxy is required. Do not ship a repository access token inside an add-in.
