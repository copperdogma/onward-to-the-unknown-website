# UI Scout — 2026-04-10 — `whole-book-reading-surface` — `local`

**Scenario:** `WB1`
**Date:** 2026-04-10
**Operator:** Codex
**Story:** `Story 006`
**Trigger:** freshness run
**Source bundle:** `input/doc-web-html/story206-onward-proof-r10`
**Surface:** `build/family-site/` built through the normal whole-book reading shell
**Environment:** local preview at `http://127.0.0.1:4173`
**Git:** detached `5a4251c`
**Overall result:** Fail
**Functional reach:** Pass
**UX / trust:** Fail
**Accessibility / readability:** Fail

## Environment Checks

- Build command: `make build-family-site` — Pass
- Preview / public URL: `python -m http.server 4173 --directory build/family-site` — Pass
- Bundle / revision checked: committed accepted bundle `story206-onward-proof-r10`

## Exact Path Walked

| Surface | Route / action | Result |
|---|---|---|
| Landing | `index.html` | Pass functionally, but too dense to feel ready to ship |
| Book chapter | `chapter-001.html` | Pass |
| Family story | `chapter-009.html` | Pass functionally; top-of-page reading experience is calm |
| Page / image entry | `page-001.html` | Pass functionally, but the surrounding labeling remains too generic |
| Mobile spot-check | `index.html` and `chapter-009.html` at narrow viewport | Navigation stacks cleanly, but landing-page scan burden stays high |

## Honest Current Boundary

The whole-book reading shell is now materially usable and functionally complete
for the staged bundle: all `33` manifest entries render, the grouped landing
page works, and representative desktop/mobile reading pages are reachable
without route hunting. It is not yet ready to ship as the family-facing site,
because the landing page still asks too much scanning effort from older readers
and the `Pages & Images` lane uses labels that feel like internal placeholders
instead of trustworthy reader-facing titles.

## Findings

### 1. Landing-page cards are too dense for first-pass scanning

- Type: Accessibility
- What happened: The top of the landing page is clear, but the card grid uses
  long excerpts across a very large set of entries. On desktop this creates a
  wall of text; on mobile the page becomes an especially long sequence of dense
  cards before the reader can confidently orient themselves.
- Why it matters: The current audience skews older. A landing page that feels
  like work to scan undermines the whole point of the reshaped shell, even when
  the site is technically complete.
- Follow-up: [Story 006](../stories/story-006-whole-book-landing-scannability-and-page-label-clarity.md)

### 2. Standalone page and image entries still read like placeholders

- Type: Trust
- What happened: The `Pages & Images` section surfaces labels such as
  `Image 1`, `Page i`, `Image 3`, and the corresponding page title still reads
  `Image 1 — Onward to the Unknown`.
- Why it matters: Those labels make the site feel like a processing artifact
  instead of a careful family archive. Readers should not have to infer whether
  an entry is a cover page, front matter, or a photo plate from a generic
  placeholder name.
- Follow-up: [Story 006](../stories/story-006-whole-book-landing-scannability-and-page-label-clarity.md)

### 3. Representative reading pages are already on the right track

- Type: Functional
- What happened: The family-story page (`chapter-009.html`) reads calmly on
  desktop and mobile, the previous / contents / next navigation remains easy to
  understand, and the page itself stays focused on reading rather than internal
  audit surfaces.
- Why it matters: The follow-up should stay focused on ship-readiness defects,
  not reopen Story 005 wholesale.
- Follow-up: Keep as the baseline to preserve while refining the landing page

## Evidence Summary

- Screenshots:
  - `.runtime/ui-scout-screens/2026-04-10-wb1/index-desktop-top.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1/index-mobile-narrow.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1/chapter-009-desktop-top.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1/chapter-009-mobile-top.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1/page-001-desktop.png`
- Notes:
  - `build/family-site/_internal/omission-audit.json` reports `manifest_entry_count: 33`
    and `status_counts: {"rendered": 33}`
  - `build/family-site/index.html` still exposes generic labels in the
    `Pages & Images` section
- Exact pages checked:
  - `index.html`
  - `chapter-001.html`
  - `chapter-009.html`
  - `page-001.html`

## Next Action

- Build [Story 006](../stories/story-006-whole-book-landing-scannability-and-page-label-clarity.md), then rerun `WB1`
