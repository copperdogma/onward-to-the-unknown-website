# UI Scout — 2026-04-10 — `whole-book-reading-surface` — `local` — `story-006-rerun`

**Scenario:** `WB1`
**Date:** 2026-04-10
**Operator:** Codex
**Story:** `Story 006`
**Trigger:** post-implementation rerun
**Source bundle:** `input/doc-web-html/story206-onward-proof-r10`
**Surface:** `build/family-site/` built through the normal whole-book reading shell
**Environment:** local preview at `http://127.0.0.1:4173`
**Git:** detached `5a4251c`
**Overall result:** Pass
**Functional reach:** Pass
**UX / trust:** Pass
**Accessibility / readability:** Pass

## Environment Checks

- Build command: `make build-family-site` — Pass
- Preview / public URL: `python -m http.server 4173 --directory build/family-site` — Pass
- Bundle / revision checked: accepted bundle `story206-onward-proof-r10`

## Exact Path Walked

| Surface | Route / action | Result |
|---|---|---|
| Landing | `index.html` | Pass; the card grid is still large, but first-pass scanning is materially calmer on desktop and mobile |
| Family story | `chapter-009.html` | Pass; previously good reading-page behavior stayed intact |
| Page / image entry | `page-001.html` | Pass; reader-facing labeling now feels intentional rather than placeholder-like |
| Mobile spot-check | `index.html`, `chapter-009.html`, and `page-001.html` at narrow viewport | Pass; stacked navigation remains easy to operate and the landing page is easier to orient within |

## Honest Current Boundary

The whole-book shell still is not the final full-site visual system, but this
slice clears the two top blocking findings from the first WB1 scout. The
landing page now scans more comfortably because card summaries are shorter and
start with actual entry content instead of repeating the title. The
`Pages & Images` lane now reads like a careful reader-facing surface rather
than a manifest dump because placeholder labels have been replaced with honest
display titles derived from page content or thin fallback wording.

## Findings

### 1. Landing-page scan burden is materially lower

- Type: Accessibility
- What changed: Card excerpts are shorter, and repeated title text is no longer
  duplicated at the top of each summary.
- Why it matters: The whole-book landing page still contains a lot of material,
  but it no longer feels like a solid wall of redundant text before a reader
  can orient themselves.
- Evidence: summary baseline moved from `191.8` average / `220` max characters
  to `136.6` average / `175` max characters across the real bundle.

### 2. `Pages & Images` now uses trustworthy reader-facing labels

- Type: Trust
- What changed: The landing page no longer shows raw labels such as `Image 1`
  or `Page i`. The current card titles now read as `Onward to the Unknown`,
  `Illustration page 3`, `Cover Illustration by Louise (L’Heureux) Aubichon`,
  `L'Heureux Family`, `Acknowledgement`, `Index`, and `Introduction and Dedication`.
- Why it matters: The section now reads like a deliberate archive surface
  instead of internal processing output.
- Evidence: `build/family-site/index.html` contains no remaining card titles
  matching `Image N` or `Page roman`.

### 3. Representative reading pages stayed stable through the refinement

- Type: Functional
- What changed: `chapter-009.html` and `page-001.html` still render calmly on
  desktop and mobile, and the previous / contents / next navigation remains
  easy to operate.
- Why it matters: This story improved the public shell without reopening Story
  005 or disturbing the reading-page substrate that was already working.
- Evidence: screenshots for `chapter-009.html` and `page-001.html` remain
  visually coherent at both checked widths.

## Evidence Summary

- Screenshots:
  - `.runtime/ui-scout-screens/2026-04-10-wb1-story-006/index-desktop-top.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1-story-006/index-desktop-full.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1-story-006/index-mobile-top.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1-story-006/chapter-009-desktop-top.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1-story-006/chapter-009-mobile-top.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1-story-006/page-001-desktop-top.png`
  - `.runtime/ui-scout-screens/2026-04-10-wb1-story-006/page-001-mobile-top.png`
- Notes:
  - `build/family-site/_internal/omission-audit.json` reports `manifest_entry_count: 33`
    and `status_counts: {"rendered": 33}`
  - narrow fixture tests now cover the public display-title seam and the
    summary-prefix stripping rule
- Exact pages checked:
  - `index.html`
  - `chapter-009.html`
  - `page-001.html`

## Next Action

- Run `/validate` on [Story 006](../stories/story-006-whole-book-landing-scannability-and-page-label-clarity.md), then mark it done if the broader repo checks stay green
