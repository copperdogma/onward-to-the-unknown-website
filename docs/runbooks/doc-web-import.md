# Runbook: `doc-web` Import

This repo treats `doc-web` as a sibling upstream runtime, not an embedded
library dependency.

The maintained local configuration lives in
[`doc-web-runtime.json`](/Users/cam/Documents/Projects/onward-to-the-unknown-website/doc-web-runtime.json).

## Commands

Inspect the upstream contract:

```bash
python scripts/doc_web_import.py contract
```

Run the maintained Onward recipe from the sibling checkout:

```bash
python scripts/doc_web_import.py run-onward \
  --run-id onward-book-r1 \
  --force
```

Snapshot an accepted bundle from that run into this repo:

```bash
python scripts/doc_web_import.py import-run \
  --run-id onward-book-r1
```

Import an already-existing bundle directly:

```bash
python scripts/doc_web_import.py import-bundle \
  --bundle-path /path/to/output/html \
  --snapshot-id onward-book-r1
```

## Local Storage

Accepted imports are copied into:

```text
.runtime/doc-web-imports/
  active-import.json
  <snapshot-id>/
    bundle/
    import-metadata.json
```

These files are local-only by default and are ignored by git.

## What The Import Metadata Records

- source `doc-web` checkout path
- source run id when applicable
- source bundle path
- recipe path when applicable
- full `doc-web contract --json` payload
- bundle summary: document id, title, reading order, entry count, provenance row count

## Validation Rules

The importer rejects bundles when any of the following drift:

- required files are missing
- `manifest.json` or `provenance/blocks.jsonl` are invalid JSON
- schema versions differ from `doc_web_bundle_manifest_v1` /
  `doc_web_provenance_block_v1`
- `reading_order` and entry ids disagree
- an entry path escapes the bundle root or does not exist
- a provenance row references an unknown entry
- a provenance `block_id` is missing from the corresponding HTML
- an image path escapes the bundle root or points to a missing file

## Current Scope

This runbook only covers the import seam. It does not yet define the final site
content model or render pipeline.

