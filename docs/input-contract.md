# Input Contract

This repo currently consumes a locally staged HTML bundle rather than a richer
canonical content export. The current whole-book local builder reads that
bundle directly and depends on the following shape.

## Canonical Bundle Path

- Default observed bundle on 2026-04-10:
  `input/doc-web-html/story206-onward-proof-r10`
- Default builder fallback: the same committed bundle path above
- The local builder can also read:
  - `ONWARD_INPUT_SOURCE_DIR`
  - `DREAMHOST_DEPLOY_SOURCE_DIR` as a compatibility fallback

## Required Files And Directories

- `manifest.json`
  - schema observed: `doc_web_bundle_manifest_v1`
  - drives entry ordering, titles, page ranges, and file paths
- `chapter-*.html`
  - chapter pages in reading order
  - each page is expected to contain one `<article>` region with preserved
    block ids like `blk-chapter-009-0001`
- `page-*.html`
  - standalone page/image pages interleaved with chapters in the source export
- `images/`
  - relative image assets referenced from the HTML
- `provenance/blocks.jsonl`
  - per-block provenance rows keyed by `entry_id` and `block_id`
- `index.html`
  - useful as a human baseline, but the builder treats `manifest.json` as the
    source of truth for ordering and metadata

## Observed Shape On 2026-04-10

- Manifest run id: `story206-onward-proof-r10`
- Document id: `onward-to-the-unknown`
- Title: `Onward to the Unknown`
- Entry count: `33`
  - `24` chapter entries
  - `9` standalone page entries
- Provenance rows: `525`
- Images directory present and populated

## Manifest Fields The Builder Uses

Each entry row currently needs:

- `entry_id`
- `kind`
- `title`
- `path`
- `order`
- `prev_entry_id`
- `next_entry_id`
- `source_pages`
- `printed_pages`
- `printed_page_start`
- `printed_page_end`

The current builder uses these fields directly to:

- preserve manifest order for previous/next reading flow
- group entries into non-family chapters, family stories, and standalone
  page/image entries
- emit a whole-book omission audit without inventing a second metadata file

## HTML Contract Assumptions

- The `<article>` content is the reusable payload.
- Block ids are preserved on headings, paragraphs, figures, and tables.
- Relative asset references remain valid when copied into a local build output.
- The source export may include duplicated inline CSS and navigation chrome; the
  local builder ignores that surrounding shell and re-templates the article
  content instead.

## Provenance Contract Assumptions

Each `provenance/blocks.jsonl` row is expected to expose:

- `entry_id`
- `block_id`
- `block_kind`
- `source_page_number`
- `source_printed_page_number`
- `source_printed_page_label`
- `text_quote`

The current local builder keeps the raw JSONL, copies it into internal build
artifacts, and generates per-entry provenance JSON files for maintainer-facing
inspection rather than reader-facing page chrome.

## What This Contract Does Not Promise Yet

- A stable canonical chapter/section JSON model
- Machine-readable family/story grouping metadata beyond the current manifest
  kind plus the explicit family-chapter run
- Normalized companion-media wiring
- A one-command import refresh from upstream tools

Those remain follow-on steps. For now, the contract is “this specific staged
bundle shape exists locally, can be rendered repeatably as a whole-book reading
surface, and can be audited entry-by-entry for omissions.”
