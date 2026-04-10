# Runbook: Golden Build

The first real rendered slice is now the local family-site build created in
Story 004.

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
  - shows the family-story landing page
  - excludes the mixed front-matter/image-page sequence from the landing grid
  - uses larger card-like hit targets for story navigation
- `chapter-009.html`
  - preserves the source block ids inside the article body
  - shows a visible provenance card with source pages, printed pages, block
    counts, and links to inspectable provenance artifacts
- desktop width
  - reading column and provenance panel remain clearly separated
- mobile width
  - navigation buttons stack cleanly and stay easy to tap
  - typography remains legible without dense chrome

Optional local preview:

```bash
make preview-family-site
```

That serves `build/family-site/` on `http://127.0.0.1:4173` by default.
