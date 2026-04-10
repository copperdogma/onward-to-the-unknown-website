# Runbook: Golden Build

The current real rendered slice is the local whole-book reading surface created
by expanding the Story 004 builder in Story 005.

## Golden Source

- Default source bundle:
  `input/doc-web-html/story206-onward-proof-r10`
- Override source path with:
  - `SOURCE=/absolute/path/to/bundle` in `make build-family-site`
  - or `ONWARD_INPUT_SOURCE_DIR`

## Regenerate The Slice

```bash
make build-family-site
```

This writes the local slice to:

```bash
build/family-site/
```

Refresh the checked-in omission-audit snapshot when the accepted bundle changes:

```bash
make refresh-omission-audit
```

## Validate The Slice

```bash
make test
make lint
make methodology-compile
make methodology-check
```

## Manual Inspection Points

Use the generated site under `build/family-site/` and inspect:

- `index.html`
  - shows grouped sections for `Book Chapters`, `Family stories`, and
    `Pages & Images`
  - stays free of audit/provenance commentary in the reader-facing surface
  - uses larger card-like hit targets for entry navigation
- `page-001.html`
  - keeps the standalone page/image entry reachable
  - uses simple previous/contents/next navigation
- `chapter-009.html`
  - preserves the source block ids inside the article body
  - stays focused on the reading page rather than source/audit commentary
- `chapter-001.html` and `chapter-024.html`
  - confirm non-family chapters remain reachable through the same shell
- `_internal/omission-audit.json`
  - contains `33` manifest entries for the accepted bundle
  - shows every entry with a coverage status and rationale
- desktop width
  - grouped landing sections and page navigation remain easy to scan
- mobile width
  - navigation buttons stack cleanly and stay easy to tap
  - typography remains legible without dense chrome
  - section jumps and contents links stay easy to operate

Optional local preview:

```bash
make preview-family-site
```

That serves `build/family-site/` on `http://127.0.0.1:4173` by default.
