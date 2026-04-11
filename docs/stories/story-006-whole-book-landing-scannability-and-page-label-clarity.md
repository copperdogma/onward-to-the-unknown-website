---
title: "Whole-Book Landing Scannability And Page Label Clarity"
status: "Done"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "5. Accessible Family Archive"
spec_refs:
  - "spec:3"
  - "spec:5"
  - "spec:7"
  - "C3"
  - "C5"
  - "C7"
adr_refs: []
depends_on:
  - "story-005"
category_refs:
  - "spec:3"
  - "spec:5"
  - "spec:7"
compromise_refs:
  - "C3"
  - "C5"
  - "C7"
input_coverage_refs:
  - "book-core-html"
architecture_domains:
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "Story 005 whole-book reading surface built from the staged input bundle"
---

# Story 006 — Whole-Book Landing Scannability And Page Label Clarity

**Priority**: High
**Status**: Done
**Decision Refs**: `docs/ideal.md`, `docs/spec.md`, `docs/presentation-decisions.md`, `docs/ui-scout.md`, `docs/ui-scout/2026-04-10-whole-book-local.md`, `docs/runbooks/whole-book-ui-manual-walkthrough.md`, `docs/stories/story-005-whole-book-accessible-reading-surface-and-omission-audit.md`, `docs/decisions/README.md`, none found after search for repo-local ADRs
**Depends On**: Story 005

> If this story is `Blocked`, replace `N/A` in `Blocker Summary`, `Blocker
> Evidence`, and `Unblock Condition` with repo-backed truth, and make the
> visible `## Plan` describe the unblock path or blocker reassessment work
> instead of stale "proceed now" steps. Leave those sections as `N/A`
> otherwise.

## Goal

Refine the current whole-book reading surface so the landing page is easier to
scan and the standalone page/image entries read like trustworthy book surfaces
instead of generic placeholders. The first WB1 UI scout proved the whole-book
shell works, but it also showed that the public-facing experience is still too
dense and ambiguous to count as ready to ship for older family readers.

## Acceptance Criteria

- [x] The landing page is materially easier to scan on desktop and mobile,
      with less preview-text density and clearer first-pass section rhythm.
- [x] Standalone page/image entries no longer surface to readers as vague
      labels like `Image 1` or `Page i` when clearer reader-facing labels can
      be derived or supplied honestly.
- [x] A fresh WB1 walkthrough of the landing page, one representative family
      story, and one representative page/image entry confirms this slice
      closes the current top scout findings or narrows them to a smaller
      follow-up.

## Out of Scope

- Final visual-system redesign for the entire site.
- Companion audio, podcast, or scan embedding.
- A new canonical data-model layer or runtime migration.
- Rewriting chapter prose or changing the whole-book omission-audit contract.

## Approach Evaluation

- **Simplification baseline**: A single LLM call can suggest shorter labels or
  calmer copy, but it cannot by itself make the shipped shell repeatably less
  dense or guarantee that page/image labeling stays consistent across builds.
- **AI-only**: Weak fit for the public surface. AI can help propose label copy,
  but the actual ship-readiness problems are persistent UI behavior and reader
  scanning burden.
- **Hybrid**: Strong fit. Use manual editorial judgment for the right labels and
  reading priorities, then encode the chosen shell changes and rerun the scout.
- **Pure code**: Reasonable for summary-length limits, card rhythm, and label
  derivation once the human editorial choices are clear.
- **Repo constraints / prior decisions**: The new triage posture and UI-scout
  lane explicitly prioritize manual site refinement on the real whole-book
  shell. Story 005 already proved the shell and omission accounting; this story
  should improve that surfaced site rather than inventing another abstraction.
- **Existing patterns to reuse**: Extend `modules/build_family_site.py`, the
  Story 005 build/test path, `docs/presentation-decisions.md`, and the new
  WB1 UI-scout lane.
- **Eval**: The decisive proof is a rebuilt site plus a fresh WB1 walkthrough
  with rendered screenshots of the landing page, one representative family
  story, and one representative page/image entry.

## Tasks

- [x] Reproduce the WB1 scout findings in the current shell and choose the
      smallest changes that materially improve landing-page scanning without
      hiding content.
- [x] Reduce landing-page scan fatigue by tightening card summaries, spacing,
      or other whole-book index presentation choices in the current shell.
- [x] Replace or augment generic page/image labels with clearer reader-facing
      titles where the source or a small amount of editorial wiring supports
      that honestly.
- [x] Update fixture-backed tests if the rendered labels or landing-page output
      expectations change.
- [x] Rerun the WB1 walkthrough after implementation and update
      `docs/ui-scout.md`, `docs/ui-scout/`, and `docs/methodology/state.yaml`
      honestly.
- [x] If this story changes documented format coverage or graduation reality: no coverage-matrix update was needed; the UI-scout state and report surfaces were refreshed honestly
- [x] Check whether the chosen implementation makes any existing code, helper paths, or docs redundant; removed the public shell's dependence on raw placeholder page titles and the redundant title-prefix card summaries without adding a follow-up cleanup story
- [x] Run required checks for touched scope:
  - [x] `make test`
  - [x] `make lint`
  - [x] `make build-family-site`
  - [x] Manually inspect the rebuilt shell on desktop and mobile widths
  - [x] If agent tooling changed: not needed
- [x] If evals or goldens changed: not needed; no eval or golden surface changed
- [x] Search all docs and update any related to what we touched
- [x] Verify project tenets:
  - [x] Structure before chrome: page readability improves without hiding the
        source book structure.
  - [x] Accessibility is explicit: older-reader scanning and hit-target
        clarity improve on real pages.
  - [x] No silent losses: all entries remain reachable and honestly labeled.
  - [x] Provenance remains inspectable through internal maintenance surfaces.

## Workflow Gates

- [x] Build complete: implementation finished, required checks run, and summary shared
- [x] Validation complete or explicitly skipped by user
- [x] Story marked done via `/mark-story-done`

## Blocker Summary

N/A

## Blocker Evidence

N/A

## Unblock Condition

N/A

## Architectural Fit

- **Owning module / area**: The current whole-book builder, its fixture-backed
  tests, and the reader-facing presentation docs.
- **Methodology reality**: This is a `spec:3` / `spec:5` / `spec:7` site
  experience story on a `partial` substrate. The active campaign now treats the
  whole-book shell as the working website, and the first `WB1` UI scout found
  ship-readiness issues worth a focused follow-up. Coverage row
  `book-core-html` remains `partial` and is the relevant input surface.
- **Substrate evidence**: `make build-family-site` now renders all `33`
  manifest entries, `build/family-site/_internal/omission-audit.json` reports
  `{"rendered": 33}`, Story 005 is done, and the first UI-scout screenshots
  show both the existing shell strengths and the current density/labeling
  issues.
- **Data contracts / schemas**: No cross-artifact schema change is required.
  This story should prefer thin label or summary logic inside the existing
  builder over introducing a new canonical data layer.
- **File sizes**: `modules/build_family_site.py` (850), `tests/test_build_family_site.py` (121), `docs/presentation-decisions.md` (64), `docs/ui-scout.md` (36), `docs/runbooks/whole-book-ui-manual-walkthrough.md` (81), `README.md` (105), `docs/RUNBOOK.md` (117).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/presentation-decisions.md`, `docs/ui-scout.md`,
  `docs/ui-scout/2026-04-10-whole-book-local.md`,
  `docs/runbooks/whole-book-ui-manual-walkthrough.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, and Story 005. No repo-local
  ADRs apply yet.

## Files to Modify

- `modules/build_family_site.py` — tighten landing-page summaries and improve
  reader-facing page/image labels (850)
- `tests/test_build_family_site.py` — assert the new landing/page label output
  and any summary changes that deserve coverage (121)
- `docs/presentation-decisions.md` — record the refined landing and page-label
  choices if they ship (64)
- `docs/ui-scout.md` — refresh the WB1 index after the rerun (36)
- `docs/ui-scout/` — add the post-fix rerun report (new file)
- `README.md` — update current-state wording if the refined shell changes what
  we claim is ready (105)
- `docs/RUNBOOK.md` — update the operational truth if the walkthrough surface
  changes materially (117)

## Redundancy / Removal Targets

- Overlong landing-page excerpts that make first-pass scanning harder than it
  needs to be.
- Generic page/image labels like `Image 1` and `Page i` when a clearer
  reader-facing label can be shown honestly.

## Notes

- This is a new story rather than a reopen of Story 005 because Story 005
  shipped the whole-book shell and omission audit successfully. The first WB1
  scout surfaced a distinct public-readiness problem line on top of that now
  real website.
- The current recommendation is manual refinement of the actual surfaced site,
  not a new canonical-model project.

## Plan

### Eval-First Gate

- **Success eval**: the smallest honest proof is:
  - fixture tests still pass and gain assertions for the refined reader-facing
    page/image labels and shorter landing-card summaries
  - a rebuilt real bundle still renders all `33` entries
  - a rerun WB1 scout shows the landing page is easier to scan and the
    `Pages & Images` lane no longer reads like placeholder internal output
- **Baseline now**:
  - `python -m pytest tests/test_build_family_site.py -q` passes with `3` tests
    on 2026-04-10
  - the current real bundle renders `33` story cards
  - current summary baseline from the real bundle is `191.8` average characters
    and `220` max characters
  - current page-entry titles are still `Image 1`, `Page i`, `Image 3`,
    `Page iii`, `Image 5`, `Page v`, `Image 7`, `Page vii`, `Page viii`
- **Candidate approaches**:
  - AI-only: reject; it can suggest labels but not enforce repeatable rendered
    output
  - Hybrid: preferred; use human editorial judgment to choose honest label
    derivation rules, then encode them in the builder
  - Pure code: viable only for the final rendering logic once the editorial
    rule is chosen

### Task Plan

1. **Anchor the refinement to the current shell** (`XS`)
   - Files: `docs/stories/story-006-whole-book-landing-scannability-and-page-label-clarity.md`
   - Record the exploration baseline, exact files touched, and the rendering
     seam to modify.
   - Done looks like: the story cites the real builder/test/doc surfaces and
     the current WB1 metrics instead of generic intent.

2. **Reduce landing-page scan fatigue in the renderer** (`S`)
   - Files: `modules/build_family_site.py`
   - Add a tighter landing-card summary rule for the whole-book index while
     preserving full detail on entry pages.
   - Prefer a small rendering-layer change such as a lower excerpt limit and,
     if needed, slightly calmer section/card rhythm instead of reworking the
     whole shell.
   - Done looks like: the landing page remains grouped and complete, but the
     first scan is materially less text-heavy on desktop and mobile.

3. **Replace placeholder-like page/image labels with reader-facing display labels** (`S`)
   - Files: `modules/build_family_site.py`
   - Derive or supply a reader-facing display label for page/image entries from
     article headings, visible text, or image alt/caption cues where those are
     already present.
   - Keep the manifest title as provenance truth in internal artifacts unless
     evidence shows the source title itself should change; use a separate
     display label in the public shell if needed.
   - Done looks like: entry cards, page `<title>`, and previous/next navigation
     no longer expose generic labels such as `Image 1` when a clearer label can
     be shown honestly.

4. **Broaden the fixture proof** (`XS`)
   - Files: `tests/test_build_family_site.py`
   - Update the fixture assertions to cover:
     - the revised landing-page summary behavior
     - the refined page/image labels
     - no regression in omission-audit or navigation proof
   - Done looks like: the new rendering behavior is locked by tests, not just
     by manual inspection.

5. **Refresh the UI-scout truth surfaces after implementation** (`XS`)
   - Files: `docs/ui-scout.md`, `docs/ui-scout/`, `docs/methodology/state.yaml`
   - Rebuild the real shell, rerun WB1, record screenshots, and update the
     freshness state honestly.
   - Done looks like: either WB1 passes or the remaining gap is narrowed to one
     smaller follow-up.

6. **Update only the docs whose truth actually changes** (`XS`)
   - Files: `docs/presentation-decisions.md`, optionally `README.md`,
     optionally `docs/RUNBOOK.md`
   - Record the refined landing and display-label decisions if they ship.
   - Done looks like: repo docs reflect the real rendered behavior without
     claiming more polish than was actually verified.

### Impact Analysis

- Primary blast radius:
  - `modules/build_family_site.py` because it owns summary generation, landing
    cards, page titles, and nav labels
  - `tests/test_build_family_site.py` because current assertions hard-code
    `Image 1` in the fixture output
- Files at risk:
  - `docs/presentation-decisions.md` if the refinement changes a previously
    implicit rule for page/image labeling
  - WB1 scout docs/state because the rerun result may stay `issues_found`
- What should not change:
  - manifest ordering
  - whole-entry reachability
  - omission-audit accounting
  - the calm, working chapter-page layout already seen in `chapter-009.html`

### Structural Health Notes

- `modules/build_family_site.py` is already `850` lines, so keep the change
  tight. Prefer one or two small helper functions for display-label derivation
  and summary limits rather than spreading new conditionals throughout the file.
- No schema or coverage-matrix change is expected if this stays a pure
  rendering refinement.
- No large scope expansion is needed. The only small folded-in delta is making
  the public display label distinct from provenance truth when necessary.

### Human-Approval Notes

- Recommended rendering rule: preserve source titles in internal provenance /
  omission surfaces, but introduce a reader-facing display label for public
  pages and navigation when the manifest title is clearly placeholder-like.
- No blocker is present. The substrate is fully verified in code, tests, real
  build output, and the first WB1 scout.

## Work Log

20260410-1736 — action: story created from the first WB1 UI scout, result:
captured the top ship-readiness follow-up as a focused refinement slice,
evidence: `docs/ui-scout/2026-04-10-whole-book-local.md`, local screenshots
under `.runtime/ui-scout-screens/2026-04-10-wb1/`, next step: build the
smallest landing-page and page-label changes that clear those findings.
20260410-1745 — action: build-story exploration, result: verified Story 006 is
honestly buildable on the existing whole-book shell and does not need a new
prerequisite story, evidence: `docs/ideal.md`, `docs/spec.md` `spec:3`,
`spec:5`, `spec:7`, `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
`tests/fixtures/formats/_coverage-matrix.json`, Story 005, WB1 scout report,
`modules/build_family_site.py`, `scripts/build_family_site.py`,
`tests/test_build_family_site.py`, and `docs/decisions/README.md`, next step:
use the rendering layer to shorten landing-card summaries and add reader-facing
page/image display labels while keeping provenance truth intact.
20260410-1745 — action: eval-first baseline, result: confirmed the current
builder proof passes but the ship-readiness defects are still measurable,
evidence: fresh `python -m pytest tests/test_build_family_site.py -q` (`3`
tests passing), fresh real-bundle build metrics showing `33` story cards,
summary baseline `191.8` average / `220` max characters, and page-entry titles
still exposed as `Image 1`, `Page i`, `Image 3`, `Page iii`, `Image 5`,
`Page v`, `Image 7`, `Page vii`, `Page viii`, next step: present the plan and
wait for approval before writing implementation code.
20260410-1821 — action: implementation started after approval, result:
promoted Story 006 to `In Progress` before touching code so the story status
matches reality, evidence: this story file and the pending methodology
regeneration, next step: patch the builder to shorten landing-card summaries,
separate public display labels from source titles, then rerun the WB1 proof.
20260410-1830 — action: implemented and verified the landing-summary and
display-label refinement, result: the builder now strips repeated title text
from landing-card excerpts, caps the summary burden more tightly, derives
reader-facing page/image labels from page content or thin honest fallbacks, and
avoids duplicate browser titles on cover-like pages, evidence:
`modules/build_family_site.py`, `tests/test_build_family_site.py`,
`docs/presentation-decisions.md`, `docs/ui-scout.md`,
`docs/ui-scout/2026-04-10-whole-book-local-story-006-rerun.md`,
`docs/methodology/state.yaml`, fresh `make test`, fresh `make lint`, fresh
`make build-family-site`, fresh `make methodology-compile`, fresh
`make methodology-check`, fresh `git diff --check`, and the new screenshots
under `.runtime/ui-scout-screens/2026-04-10-wb1-story-006/`, next step:
recommend `/validate`, then `/mark-story-done` if the user accepts the slice.
20260410-2141 — action: close-out validation and story completion, result:
confirmed Story 006 is complete, marked it `Done`, and prepared it for git
check-in, evidence: fresh `python -m pytest tests/`, fresh `python -m ruff
check modules/ tests/`, fresh `make build-family-site`, fresh validation of
the rerun WB1 report and screenshot set, and no repo-local ADR blockers under
`docs/decisions/`, next step: `/check-in-diff`.
