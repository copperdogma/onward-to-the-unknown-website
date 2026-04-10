# Presentation Decisions

First recorded presentation choices for the local family-site slice built in
Story 004.

## Baseline

- The raw staged export in `input/doc-web-html/story206-onward-proof-r10` is
  the fidelity baseline.
- The local family-site builder should reshape presentation, not rewrite the
  underlying chapter content.

## Family Slice Boundary

The first reshaped local slice covers the family-story run only:

- `chapter-009` — Alma Marie (L'Heureux) Alain
- `chapter-010` — ARTHUR L'HEUREUX
- `chapter-011` — LEONIDAS L'HEUREUX
- `chapter-012` — JOSEPHINE (L'HEUREUX ) ALAIN
- `chapter-013` — PAUL L'HEUREUX
- `chapter-014` — GEORGE L'HEUREUX
- `chapter-015` — JOE (JOSEPH) L'HEUREUX
- `chapter-016` — MATHILDA (L'HEUREUX) DEVLIN
- `chapter-017` — MARIE-LOUISE (L'HEUREUX) LaCLARE
- `chapter-018` — ROSEANNA (L'HEUREUX) LANDREVILLE
- `chapter-019` — ANTOINETTE (L'HEUREUX) RICHARD
- `chapter-020` — EMILIE (L'HEUREUX) NOLIN
- `chapter-021` — WILFRID L'HEUREUX
- `chapter-022` — PIERRE L'HEUREUX
- `chapter-023` — ANTOINE L'HEUREUX

## Decisions Locked For This Pass

- Family stories stay whole pages.
- Source order inside the family run stays intact.
- The first local slice gets its own family landing page rather than reusing
  the mixed chapter-plus-page source index.
- Visible provenance is required on every rendered family page.
- Any source material omitted from a reshaped surface must be omitted
  intentionally and documented, not dropped accidentally during the rebuild.
- Accessibility is a first-order concern:
  - larger default body type
  - larger navigation targets
  - simpler page structure
  - desktop/mobile layouts that remain easy to operate for older readers

## Deliberately Deferred

- Front matter redesign
- Standalone image-page redesign
- Full-book table of contents redesign
- Audio, podcasts, and companion-media embeds
- Breaking family pages into smaller fragments
- Any claim that this is the final visual language for the entire site

## Rationale

The raw source export already preserves the content faithfully, but it mixes
front matter, chapter pages, and standalone image pages in a way that makes the
family stories harder to browse. This first local slice is intentionally narrow:
keep fidelity high, make reading easier, and learn from a concrete subsection
before reshaping the full book. That narrowness is temporary and explicit; the
project still aims to make the entire book accessible on the web rather than
silently losing non-family material.
