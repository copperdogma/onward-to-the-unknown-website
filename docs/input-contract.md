# Input Contract

This repo currently consumes locally staged `doc-web` HTML bundles rather than
a richer canonical content export. The current whole-book local builder reads
the accepted main-book bundle directly and may also attach repo-owned family
story supplements through a sibling registry in the same `input/doc-web-html/`
area. It may also publish preserved root-level archive source files from
`input/` onto a reader-facing source-library page.

## Canonical Bundle Path

- Default observed bundle on 2026-04-10:
  `input/doc-web-html/story206-onward-proof-r10`
- Default builder fallback: the same committed bundle path above
- Optional supplement registry on 2026-04-11:
  `input/doc-web-html/family-story-supplements.json`
- First accepted supplement bundle on 2026-04-11:
  `input/doc-web-html/rolland-alain-memoir-r01`
- Reader-facing source-library page on 2026-04-12:
  `build/family-site/archive-sources.html`
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
- optional `family-story-supplements.json` beside the main bundle
  - schema observed: `onward_family_story_supplement_registry_v1`
  - attaches repo-owned supplement bundles and source PDFs to the family-story
    section without changing the main-book manifest
  - each row currently needs:
    - `supplement_id`
    - `title`
    - `output_path`
    - `bundle_dir`
    - `source_pdf`
    - `group_id`
    - `insert_after_entry_id`
    - `entry_ids`
    - `absorbed_entry_ids`
    - `preamble`
- optional root-level preserved source files under `input/`
  - currently published when the file lives directly under `input/` and uses a
    supported extension: `.pdf`, `.jpg`, `.jpeg`, or `.png`
  - intentionally excludes `input/doc-web-html/` and nested asset directories
    such as `input/onward-to-the-unknown-images/`
  - published copies are written under `build/family-site/source-files/`
  - the builder emits `_internal/source-library.json` plus a public
    `archive-sources.html` page for these files
  - `input/Onward to the Unknown.pdf` is treated as the featured book-source
    path when it exists locally, but the build does not fail if that ignored
    local file is absent

## Observed Shape On 2026-04-10

- Manifest run id: `story206-onward-proof-r10`
- Document id: `onward-to-the-unknown`
- Title: `Onward to the Unknown`
- Entry count: `33`
  - `24` chapter entries
  - `9` standalone page entries
- Provenance rows: `525`
- Images directory present and populated

## Observed Supplement Shape On 2026-04-11

- Supplement bundle path: `input/doc-web-html/rolland-alain-memoir-r01`
- Document id: `rolland-alain-memoir-family-story`
- Title: `Rolland Alain Memoir Family Story`
- Entry count: `2`
  - `1` absorbed title leaf (`page-001`)
  - `1` main memoir chapter (`chapter-001`)
- Provenance rows: `101`
- Asset roots: none
- Original source PDF remains at
  `input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf`

## Observed Source-Library Shape On 2026-04-12

- Public page path: `build/family-site/archive-sources.html`
- Public asset root: `build/family-site/source-files/`
- Internal manifest: `build/family-site/_internal/source-library.json`
- Published file count in the current worktree: `7`
  - `6` PDFs
  - `1` image scan (`Jackfish-Lake-Fishing-Guide.jpg`)
- Memoir source attachment is published through the same source-library copy as
  `source-files/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf`
- `input/Onward to the Unknown.pdf` is currently present in this worktree as a
  repo-local ignored input, so the homepage and source-library page render the
  featured `Open Book PDF` actions here
- Other worktrees only show that featured-book treatment when the same local
  file exists under `input/Onward to the Unknown.pdf`

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

For supplement bundles, the builder currently preserves the same `doc_web`
bundle contract and uses the registry file for only the extra wrapper metadata:

- where the supplement card appears in the family-story run
- which bundle entry ids are reader-facing versus absorbed
- the short contextual preamble shown above the supplement body
- the original PDF attachment path, which can now resolve to a published public
  source-file copy when the file also appears as a supported root-level
  `input/` asset

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
- A fully generalized supplement system beyond the current bounded
  family-story registry plus the checked-in Rolland Alain memoir bundle
- Normalized companion-media wiring
- Rich editorial metadata beyond the current root-level source-file discovery
  and supplement title override
- A fully generic one-command import refresh for every future archive format

Those remain follow-on steps. For now, the contract is “this specific staged
bundle shape plus the bounded memoir supplement seam and the current
root-level source-library seam exist locally, can be rendered repeatably as a
whole-book reading surface, and can be audited without losing track of the
shipped supplement/source files.”
