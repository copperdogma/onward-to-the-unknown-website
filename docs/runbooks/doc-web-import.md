# Runbook: `doc-web` Import

This repo treats `doc-web` as a sibling upstream runtime, not an embedded
library dependency.

The maintained local configuration lives in
[`doc-web-runtime.json`](/Users/cam/Documents/Projects/onward-to-the-unknown-website/doc-web-runtime.json).

When this repo is opened from a git worktree, repo-relative paths in that
manifest resolve from the worktree first and then fall back to the primary git
checkout if the sibling `doc-web` checkout or local-only input PDF only exists
there.

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

Run the bounded non-TOC scanned supplement workflow that produced the accepted
Rolland Alain memoir bundle:

```bash
python scripts/doc_web_import.py run-scanned-supplement \
  --run-id rolland-alain-memoir-r01 \
  --input-pdf "input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf" \
  --bundle-title "Rolland Alain Memoir Family Story" \
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

The first checked-in supplement bundle built this way now lives at:

```text
input/doc-web-html/rolland-alain-memoir-r01/
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

This runbook covers the import seam plus one bounded non-TOC scanned supplement
workflow that still emits the standard `doc_web_bundle` contract. It does not
yet define a fully generalized supplement pipeline or the final site content
model.
