# UI Scout — 2026-04-11 — `whole-book-reading-surface` — `local` — `mobile-first-class`

**Scenario:** `WB1`
**Date:** 2026-04-11
**Operator:** Codex
**Story:** `n/a`
**Trigger:** validation contract hardening
**Source bundle:** `input/doc-web-html/story206-onward-proof-r10`
**Surface:** `build/family-site/` built through the normal whole-book reading shell
**Environment:** local Playwright browser sweep over the built static files
**Git:** detached `9be3a8a`
**Overall result:** Pass
**Desktop result:** Pass
**Mobile result:** Pass
**Functional reach:** Pass
**UX / trust:** Pass
**Accessibility / readability:** Pass

## Environment Checks

- Build command: `make build-family-site` — Pass
- Desktop viewport: `1280x900`
- Mobile viewport: `390x844`
- Preview / public URL: local Playwright sweep over `build/family-site/*.html`
- Bundle / revision checked: accepted bundle `story206-onward-proof-r10`

## Exact Path Walked

| Viewport | Surface | Route / action | Result |
|---|---|---|---|
| Desktop | Landing | `index.html` | Pass; grouped sections and jump controls stay obvious and calm |
| Desktop | Book chapter | `chapter-001.html` | Pass; no horizontal overflow and reading chrome stays legible |
| Desktop | Family story | `chapter-009.html` | Pass; narrative page remains stable with large previous/contents/next controls |
| Desktop | Page / image entry | `page-001.html` | Pass; the cover page remains reachable and honestly labeled |
| Mobile | Landing | `index.html` | Pass; jump controls stack cleanly and the first card remains legible without route hunting |
| Mobile | Book chapter | `chapter-001.html` | Pass; navigation stays large and text remains readable at phone width |
| Mobile | Family story | `chapter-009.html` | Pass; stacked controls and narrative measure remain calm and easy to use |
| Mobile | Page / image entry | `page-001.html` | Pass; the cover page remains readable and the image renders after an explicit image-ready wait in scripted capture |

## Honest Current Boundary

The whole-book shell still is not the final long-term visual system, but this
pass raises the validation bar around the current website: desktop and mobile
are now co-equal proof surfaces, and the current shell passes that stricter
check on the core reading path. The site still needs future content and
presentation work, but this run did not find a new mobile-only blocker that
should outrank those planned slices.

## Findings

### 1. Mobile now qualifies as a required proof surface rather than a spot-check

- Type: Accessibility
- What happened: the same core WB1 path was walked on desktop and mobile
  instead of treating mobile as a tie-break or narrow afterthought.
- Why it matters: this repo now has an honest validation contract that can
  catch phone-sized regressions before they are normalized into "good enough"
  ship decisions.
- Follow-up: keep this dual-surface contract on every future WB1 run.

### 2. No horizontal overflow appeared on the checked desktop or mobile path

- Type: Functional
- What happened: the landing page, representative non-family chapter, family
  story, and page/image entry all stayed within the viewport at `1280x900` and
  `390x844`.
- Why it matters: older family readers should not need sideways panning or
  hidden route hunting to move through the site.
- Follow-up: none from this pass.

### 3. Mobile navigation remains forgiving on the current reading path

- Type: UX / trust
- What happened: the landing jump controls and previous / contents / next
  buttons stacked cleanly on mobile and remained easy to identify.
- Why it matters: the current site shell continues to support the repo's
  explicit older-reader requirement instead of only looking calm on desktop.
- Follow-up: none from this pass.

## Evidence Summary

- Screenshots:
  - `.runtime/ui-scout-screens/2026-04-11-wb1-mobile-first-class/index-desktop.png`
  - `.runtime/ui-scout-screens/2026-04-11-wb1-mobile-first-class/index-mobile.png`
  - `.runtime/ui-scout-screens/2026-04-11-wb1-mobile-first-class/chapter-009-desktop.png`
  - `.runtime/ui-scout-screens/2026-04-11-wb1-mobile-first-class/chapter-009-mobile.png`
  - `.runtime/ui-scout-screens/2026-04-11-wb1-mobile-first-class/page-001-desktop-full-waited.png`
  - `.runtime/ui-scout-screens/2026-04-11-wb1-mobile-first-class/page-001-mobile-waited.png`
- Metrics:
  - no horizontal overflow on `index.html`, `chapter-001.html`,
    `chapter-009.html`, or `page-001.html` at `1280x900` or `390x844`
  - `index.html` exposes `3` section jump controls on both viewports
  - checked reading pages expose `3` previous / contents / next controls on
    both viewports
- Notes:
  - the first scripted capture of `page-001.html` fired before the large cover
    image had visibly painted, so the kept page-image screenshots were taken
    only after an explicit image-ready wait
- Exact pages checked:
  - `index.html`
  - `chapter-001.html`
  - `chapter-009.html`
  - `page-001.html`

## Next Action

- Treat this dual-surface WB1 pass as the new baseline and require the same
  desktop/mobile proof on future `/validate` close-out work
