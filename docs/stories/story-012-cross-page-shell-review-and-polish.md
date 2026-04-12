---
title: "Cross-Page Shell Review And Polish"
status: "Done"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "2. Connected Companion Media"
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
  - "story-006"
  - "story-007"
  - "story-011"
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
  - "chapter-audio"
  - "full-book-audio"
architecture_domains:
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "current local whole-book static shell plus the first on-site audiobook page"
---

# Story 012 — Cross-Page Shell Review And Polish

**Priority**: High
**Status**: Done
**Decision Refs**: `docs/ideal.md`, `docs/spec.md`, `docs/presentation-decisions.md`, `docs/methodology/state.yaml`, `docs/methodology/graph.json`, `docs/stories/story-006-whole-book-landing-scannability-and-page-label-clarity.md`, `docs/stories/story-007-rolland-alain-memoir-family-story.md`, `docs/stories/story-011-first-on-site-audiobook-listening-surface.md`, none found after search for repo-local ADRs specific to the current shell polish line
**Depends On**: Stories 005, 006, 007, and 011

> If this story is `Blocked`, replace `N/A` in `Blocker Summary`, `Blocker
> Evidence`, and `Unblock Condition` with repo-backed truth, and make the
> visible `## Plan` describe the unblock path or blocker reassessment work
> instead of stale "proceed now" steps. Leave those sections as `N/A`
> otherwise.

## Goal

Review the shared shell across one representative page of each current public page type, capture the resulting UI findings in a durable story, and then tighten the shared builder so the site title and hero headings stay stable on wide screens while the landing-page jump-row icons read as supporting cues instead of oversized primary artwork. This slice should improve the current static website as a coherent shell, not patch a single page in isolation.

## Acceptance Criteria

- [x] A representative review of the current homepage, audiobook page, chapter page, supplement page, and photo/archive page is recorded in the story notes or work log with the concrete shell findings that drove the implementation.
- [x] The shared shell no longer wraps the homepage or audiobook hero heading unnecessarily on wide desktop layouts, while mobile/smaller layouts still allow honest wrapping when needed.
- [x] The homepage jump-row buttons use smaller, calmer icon treatment that stays clearly secondary to the labels, and fresh built-page inspection plus regression tests confirm the updated shell across the reviewed page types.

## Out of Scope

- A full visual redesign or new design system for the whole site.
- Adding the future podcast button or podcast icon treatment.
- Changing book content, audiobook metadata, or source-manifest structure.
- Reworking chapter/article layout beyond the shared shell and button/heading treatment.

## Approach Evaluation

- **Simplification baseline**: A single LLM call could describe what looks off, but it cannot ship a repeatable fix to the shared shell or protect against regressions in the generated HTML/CSS.
- **AI-only**: Weak fit. The work is deterministic shell markup, CSS, and builder-test coverage over already-rendered pages.
- **Hybrid**: Strong fit. Use manual review on real rendered pages to choose the right shell refinements, then encode those refinements deterministically in the builder and stylesheet.
- **Pure code**: Viable once the review findings are explicit. The changes belong in the renderer and tests rather than a new abstraction layer.
- **Repo constraints / prior decisions**: The active campaign explicitly says to refine the existing whole-book shell toward ship-readiness rather than inventing a new frontend substrate. Story 006 already handled landing-page scannability, and Story 011 added the audiobook surface, so this story should polish the shared shell that those stories now expose together.
- **Existing patterns to reuse**: Extend `modules/build_family_site.py`, its existing CSS generation, the current fixture-backed `tests/test_build_family_site.py` coverage, and `docs/presentation-decisions.md`.
- **Eval**: The decisive proof is a rebuilt site, focused builder-test assertions for the heading/icon shell output, and fresh rendered inspection of representative homepage, audiobook, chapter, supplement, and photo/archive pages.

## Tasks

- [x] Record the representative page review findings for the current shell and confirm which fixes belong in the shared builder rather than one-off page overrides.
- [x] Refine the shared heading and navigation CSS/markup so wide-screen hero headings do not wrap unnecessarily and landing jump-row icons read as supporting cues.
- [x] Update or add regression coverage for the homepage and audiobook hero shell plus the landing jump-row icon treatment.
- [x] Rebuild the real site and inspect one representative page of each public type after implementation.
- [x] If this story changes documented format coverage or graduation reality: no coverage-matrix update was needed; methodology graph/story views were refreshed honestly
- [x] Check whether the chosen implementation makes any existing code, helper paths, or docs redundant; no new redundant path was introduced, and the fix stayed in the existing shared shell instead of adding page-specific overrides
- [x] Run required checks for touched scope:
  - [x] Default Python checks: `make test`
  - [x] Default Python lint: `make lint`
  - [x] Rebuild and inspect the real site with `make build-family-site`
  - [x] If agent tooling changed: not needed
- [x] If evals or goldens changed: not needed for this shell-polish slice
- [x] Search all docs and update any related to what we touched
- [x] Verify Central Tenets:
  - [x] T0 — Traceability: page relationships and audio links remain traceable through the existing builder/provenance surfaces
  - [x] T1 — AI-First: confirmed this is deterministic UI plumbing, not a problem to solve with an LLM pipeline
  - [x] T2 — Eval Before Build: the builder-test baseline and rendered review were recorded before and after refining the shell
  - [x] T3 — Fidelity: no source prose or archive content was rewritten; only the shell treatment changed
  - [x] T4 — Modular: shared shell changes stayed in the existing builder/style path instead of page-specific duplication
  - [x] T5 — Inspect Artifacts: representative built pages were visually inspected after the rebuild

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

- **Owning module / area**: The existing whole-book static shell in `modules/build_family_site.py`, its CSS output, and the fixture-backed shell regression tests.
- **Methodology reality**: This is a `spec:3` / `spec:5` / `spec:7` site-experience story on a `partial` substrate inside the active `bootstrap-canon-and-shell` campaign. Relevant coverage rows are `book-core-html`, `chapter-audio`, and `full-book-audio`; this story does not change their readiness state, but it does change how those already-published surfaces present to readers.
- **Substrate evidence**: `make build-family-site` currently emits the homepage, chapter pages, supplement page, photo/archive pages, and `audiobook.html`; Stories 006, 007, and 011 are done; and fresh local rendered inspection in this pass already reproduced the wide-screen audiobook heading wrap and the current landing jump-row icon treatment.
- **Data contracts / schemas**: No schema or manifest change is expected. This is presentation logic in the existing builder.
- **File sizes**: `modules/build_family_site.py` (2816), `tests/test_build_family_site.py` (1056), `docs/presentation-decisions.md` (116), and this story file (127 before fill-in). The two code files are already large, so changes should stay tightly scoped and avoid adding another shell abstraction unless it clearly simplifies the file.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`, `docs/methodology/state.yaml`, `docs/methodology/graph.json`, `docs/presentation-decisions.md`, and Stories 006, 007, and 011. No repo-local ADRs apply to this shell-polish slice.

## Files to Modify

- `docs/stories/story-012-cross-page-shell-review-and-polish.md` — review record, plan, and work log (new file)
- `modules/build_family_site.py` — shared shell heading/icon CSS and any small markup adjustments (2816)
- `tests/test_build_family_site.py` — regressions for the reviewed shell changes (1056)
- `docs/presentation-decisions.md` — record the tightened shell rules if they ship (116)

## Redundancy / Removal Targets

- Per-page shell exceptions that would otherwise keep piling up around the homepage and audiobook hero.
- Oversized or overly assertive jump-row icon treatment if a calmer shared rule can replace it.

## Notes

- This is a new story rather than a reopen of Story 011 because the validation boundary is broader than the audiobook surface: it covers the shared shell across homepage, audiobook, chapter, supplement, and photo/archive page types.
- Representative review findings captured during story creation:
  - Homepage: the landing jump-row icon treatment reads heavier than necessary for secondary navigation.
  - Audiobook page: the hero heading is capped too narrowly and wraps awkwardly on a wide desktop layout.
  - Chapter page: shared shell and page-nav pattern remain usable; no new structural issue surfaced beyond carrying the shared shell rules cleanly.
  - Supplement page: the current wrapper and listening panel read cleanly; no new supplement-specific fix is needed.
  - Photo/archive page: the current page shell and media treatment read cleanly; no new page-type-specific fix is needed.
- The current honest move is to improve the shared shell, not to open separate one-page stories for each surface.

## Plan

### Eval-First Gate

- **Success eval**:
  - focused `tests/test_build_family_site.py` assertions for the landing jump-row shell and the hero heading CSS treatment
  - `make build-family-site` succeeds and the rebuilt pages render the updated shell
  - fresh rendered inspection of representative homepage, audiobook, chapter, supplement, and photo/archive pages shows the shared shell is calmer and more stable
- **Baseline now**:
  - `make build-family-site` passes on 2026-04-12 and emits the full current site bundle
  - fresh desktop inspection in this pass shows the homepage jump-row icons are still stronger than necessary and `audiobook.html` wraps `Onward to the Unknown Audiobook` across three lines on a wide layout
  - representative chapter, supplement, and photo/archive pages do not show a distinct page-type-specific defect beyond the shared shell treatment
- **Candidate approaches**:
  - page-specific overrides: reject unless exploration proves the shared shell cannot express the right behavior
  - shared builder/style refinement: preferred because the issues come from shared heading and nav patterns
  - larger redesign: out of scope for this story

### Task Plan

1. **Anchor the review findings in the story record** (`XS`)
   - Files: `docs/stories/story-012-cross-page-shell-review-and-polish.md`
   - Preserve the representative page audit findings, the page types inspected, and the scope boundary for this polish pass.
   - Done looks like: a future session can see exactly why the story exists and which pages were reviewed.

2. **Tighten the shared shell styles/markup** (`S`)
   - Files: `modules/build_family_site.py`
   - Refine the landing jump-row icon sizing/weight and the hero-heading rules so wide-screen titles stay on one line when space allows, without forcing the same behavior on narrow layouts.
   - Done looks like: homepage jump-row buttons feel calmer, and the audiobook/home hero headings no longer wrap unnecessarily on desktop.

3. **Lock the shell behavior with tests** (`S`)
   - Files: `tests/test_build_family_site.py`
   - Add or update assertions for the relevant CSS/HTML so the heading/icon treatment does not regress quietly.
   - Done looks like: the fixture-backed builder test fails if the reviewed shell rules disappear.

4. **Refresh the rendered proof and docs** (`XS`)
   - Files: `docs/presentation-decisions.md`, `docs/stories/story-012-cross-page-shell-review-and-polish.md`
   - Rebuild the real site, inspect representative pages again, and record the shipped shell decision.
   - Done looks like: the story work log and presentation decisions match the implemented reality.

## Work Log

20260412-0937 — story creation: reviewed representative homepage, audiobook, chapter, supplement, and photo/archive pages; confirmed this is a new shared-shell polish slice rather than a Story 011 reopen because the validation boundary now spans multiple page types, evidence from fresh local build plus rendered inspection, next step is shared builder refinement.
20260412-0941 — implementation start: promoted the story from Pending to In Progress before editing code so the execution record matches the actual build pass, evidence in this story file plus regenerated methodology views to follow, next step is the shared shell CSS/markup patch.
20260412-0944 — shell refinement: updated `modules/build_family_site.py` so the homepage and audiobook hero headings use explicit wide-screen rules and the landing jump-row icons render smaller and quieter, evidence in the shared CSS emitted from the builder and no new page-specific override path added, next step is regression coverage plus a rebuilt bundle.
20260412-0946 — regression coverage: expanded `tests/test_build_family_site.py` to assert the audiobook hero shell and the new jump-row/icon CSS hooks, evidence `python -m pytest tests/test_build_family_site.py -q` passed with `21 passed` and `python -m ruff check modules/build_family_site.py tests/test_build_family_site.py` passed cleanly, next step is full rebuild and wider verification.
20260412-0949 — rendered verification: rebuilt the full site and inspected representative homepage, opening page, chapter page, supplement page, photo/archive page, and audiobook page on desktop with fresh local screenshots; also verified homepage and audiobook mobile layouts with Playwright at `390x844`, evidence `make build-family-site`, `make methodology-compile`, `make methodology-check`, `make test`, and `make lint` all passed plus fresh screenshot proof from `/tmp/story012-*.png` and Playwright mobile captures, next step is `/validate`.
20260412-0956 — follow-up shell tuning: user feedback showed the landing jump-row icons had been reduced too far, so the shared jump-row icon rule was nudged from `0.9rem` to `1rem` with slightly stronger opacity and the stylesheet regression assertion was tightened to the exact jump-row icon size block, evidence in `modules/build_family_site.py` and `tests/test_build_family_site.py`, next step is rebuild plus fresh visual check and then resume validation.
20260412-0959 — section-header icon alignment: reused the existing audiobook/book SVGs in the homepage section headers so the audiobook overview and the grouped book sections share the same icon language as the jump-row, evidence in `modules/build_family_site.py` plus expanded landing-page assertions in `tests/test_build_family_site.py`, next step is rebuild and rendered verification of the homepage header row and audiobook overview panel.
20260412-1003 — section-header sizing pass: after the first rebuilt screenshot the shared section-header icon treatment read a bit undersized against the larger panel headings, so the section-title icon size was lifted to `1.15rem` while leaving the jump-row icons at `1rem`, evidence in `modules/build_family_site.py`, next step is rerun the focused checks and re-inspect the homepage panel.
20260412-1008 — icon rebalance loop: a fresh homepage screenshot still showed both icon treatments reading too timidly because the glyph artwork sits small inside its viewbox, so the jump-row icons were increased to `1.25rem` and the section-title icons to `1.4rem` before another rebuild/screenshot pass, evidence in `modules/build_family_site.py` and the paired stylesheet assertion in `tests/test_build_family_site.py`, next step is focused verification plus a new screenshot to decide whether another iteration is needed.
20260412-1011 — icon loop stop: reran the focused tests/build and captured a fresh homepage screenshot after the larger icon pass; the jump-row icons now read clearly without overpowering the labels and the section-header icons have enough weight to match the panel headings, evidence `python -m pytest tests/test_build_family_site.py -q`, `python -m ruff check modules/build_family_site.py tests/test_build_family_site.py`, `make build-family-site`, and `/tmp/story012-icons-pass2.png`, next step is user review and then resume `/validate` on the updated slice.
20260412-1015 — explicit ratio tweak: user requested exact sizing ratios, so the jump-row icons were increased by 10% from `1.25rem` to `1.375rem` and the homepage section-header icons were doubled from `1.4rem` to `2.8rem`, with the focused stylesheet assertions updated to match, evidence in `modules/build_family_site.py` and `tests/test_build_family_site.py`, next step is rebuild plus a fresh homepage screenshot from the new numbers.
20260412-1027 — story close-out: revalidated the shipped shell-polish slice against the final icon sizes, marked the workflow gates complete, and promoted Story 012 to Done with refreshed generated views and changelog coverage, evidence `make test`, `make lint`, `make build-family-site`, `make methodology-compile`, and `make methodology-check` on the current tip, next step is `/check-in-diff`.
