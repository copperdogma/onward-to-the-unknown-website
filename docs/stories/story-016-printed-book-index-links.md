---
title: "Printed Book Index Links"
status: "Done"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "3. Trustworthy Source Lineage"
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
  - "story-012"
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
legacy_system: "page-008 printed index rendered as readable text without links to the target chapter pages"
---

# Story 016 - Printed Book Index Links

**Priority**: High
**Status**: Done
**Decision Refs**: `docs/ideal.md`, `docs/spec.md`, `docs/presentation-decisions.md`, `docs/methodology/state.yaml`, `docs/methodology/graph.json`, `tests/fixtures/formats/_coverage-matrix.json`; no repo-local ADRs exist in `docs/decisions/` for this navigation refinement
**Depends On**: Stories 005, 006, and 012

> If this story is `Blocked`, replace `N/A` in `Blocker Summary`, `Blocker
> Evidence`, and `Unblock Condition` with repo-backed truth, and make the
> visible `## Plan` describe the unblock path or blocker reassessment work
> instead of stale "proceed now" steps. Leave those sections as `N/A`
> otherwise.

## Goal

Make the printed book index on `page-008.html` act like a real navigational surface in the generated family site. The source page lists top-level sections and family-branch rows with printed page numbers; the website should link those labels and page numbers to the actual rendered chapter pages while preserving source text and avoiding broad redesign.

## Acceptance Criteria

- [x] The generated `page-008.html` links each top printed-index row to the actual chapter page represented by its printed page number.
- [x] The child/family-branch summary table on `page-008.html` links each family name and page number to the intended chapter page, including OCR/name quirks such as `Wilfred` pointing to Wilfrid's chapter.
- [x] Fresh checks confirm no other source or built page contains an unlinked index-like dot-leader surface that should be linked in this same slice.

## Out of Scope

- Building person-level anchors inside genealogy tables.
- Changing the source manifest or upstream staged HTML.
- Redesigning the printed index page beyond turning existing index entries into links.
- Publishing or deploying the generated site.

## Approach Evaluation

- **Simplification baseline**: A one-off manual edit to generated HTML would fix the current output once, but it would be lost on the next `make build-family-site`.
- **AI-only**: Weak fit. The correct targets come from the repo's manifest and builder output, not an opaque rewrite of the page.
- **Hybrid**: Useful for reviewing the index shape and odd OCR cases, but the shipped behavior needs deterministic builder logic.
- **Pure code**: Strong fit. This is presentation plumbing in the existing family-site builder plus regression coverage.
- **Repo constraints / prior decisions**: `docs/presentation-decisions.md` says the raw staged export is the fidelity baseline and the local builder should reshape presentation without rewriting underlying chapter content. `spec:3`, `spec:5`, and `spec:7` all favor clearer navigation and accessible reader controls on the current whole-book shell.
- **Existing patterns to reuse**: Extend `modules/build_family_site.py` where `page-008` already has a dedicated cleanup pass, and add focused assertions in `tests/test_build_family_site.py`.
- **Eval**: The decisive proof is a rebuilt family site, tests that fail if the index links disappear, source/built scans for other index-like dot leaders, and a browser click from `page-008.html` to a target chapter.

## Tasks

- [x] Confirm the current `page-008.html` source structure and target chapter mapping from the staged manifest.
- [x] Extend the existing `page-008` cleanup pass to link top index rows by printed page and link child rows by label/target mapping where OCR page numbers are not enough.
- [x] Add regression coverage for linked top rows, linked child rows, and the unlinked total row.
- [x] Rebuild the real family site and inspect generated `page-008.html`.
- [x] If this story changes documented format coverage or graduation reality: no coverage-matrix update was needed because the `book-core-html` surface remains partial and this only improves the current presentation layer.
- [x] Check whether the chosen implementation makes any existing code, helper paths, or docs redundant; no redundant path was introduced, and the fix reused the existing `page-008` cleanup seam.
- [x] Run required checks for touched scope:
  - [x] Default Python checks: `make test`
  - [x] Default Python lint: `make lint`
  - [x] Rebuild and inspect the real site with `make build-family-site`
  - [x] If pipeline behavior changed: not applicable
  - [x] If agent tooling changed: not applicable
- [x] If evals or goldens changed: not applicable
- [x] Search all docs and update any related to what we touched; this story records the change, and no separate presentation decision was needed for this narrow index-link behavior.
- [x] Verify Central Tenets:
  - [x] T0 - Traceability: links derive from manifest entry paths, printed-page metadata, and explicit source-label mappings for the printed index page.
  - [x] T1 - AI-First: this is deterministic navigation wiring, not an LLM transform.
  - [x] T2 - Eval Before Build: the source index and existing builder seam were inspected before encoding the fix; regression tests now protect it.
  - [x] T3 - Fidelity: source text remains intact except for removing OCR dot leaders from the reader-facing index presentation.
  - [x] T4 - Modular: behavior stays in the existing family-site builder and does not add a second index renderer.
  - [x] T5 - Inspect Artifacts: rebuilt HTML and local HTTP browser navigation were inspected after the build.

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

- **Owning module / area**: The existing whole-book family-site builder in `modules/build_family_site.py`, specifically the `page-008` index cleanup path.
- **Methodology reality**: This is a `spec:3` / `spec:5` / `spec:7` site-experience refinement inside the active `bootstrap-canon-and-shell` campaign. The relevant coverage row is `book-core-html`, which remains `partial`.
- **Substrate evidence**: `input/doc-web-html/story206-onward-proof-r10/manifest.json` has printed-page metadata and entry paths for the target chapters; `modules/build_family_site.py` already reshapes `page-008`; `make build-family-site` emits the real site output.
- **Data contracts / schemas**: No schema or manifest contract changes.
- **File sizes**: `modules/build_family_site.py` (4977), `tests/test_build_family_site.py` (1877), and this story file (new). The code files are already large, so the change stays localized to the existing page cleanup path and a focused regression test.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`, `docs/presentation-decisions.md`, `docs/methodology/state.yaml`, `docs/methodology/graph.json`, `tests/fixtures/formats/_coverage-matrix.json`, and `docs/decisions/README.md`. No repo-local ADR applies because this is a narrow presentation/navigation refinement in the existing shell.

## Files to Modify

- `modules/build_family_site.py` - add deterministic printed-index target mapping and link rendering in the existing `page-008` cleanup pass (4977)
- `tests/test_build_family_site.py` - add focused regression coverage for printed-index links (1877)
- `docs/stories/story-016-printed-book-index-links.md` - package and close the completed slice (new)
- `docs/stories.md` and `docs/methodology/graph.json` - generated methodology views after compile
- `CHANGELOG.md` - closeout entry

## Redundancy / Removal Targets

- No existing helper or docs path becomes redundant. The page-specific cleanup already existed; this story only teaches it to emit links.

## Notes

- A new story is honest instead of reopening Story 012 because the older story is already closed and covered shared shell polish, while this request is a distinct printed-index navigation bug on a specific book page.
- The user asked for the live public page to be hyperlinked, but this story only changes the repo and generated local output; deployment is not part of this finish-and-push flow unless requested separately.

## Plan

1. Inspect the current source and built `page-008.html`, plus the manifest target pages.
2. Add deterministic link generation in the existing `clean_index_paragraphs()` path.
3. Add regression coverage for both list and table entries.
4. Rebuild, run checks, scan for other index-like dot-leader pages, and browser-test representative navigation.
5. Close the story through `/mark-story-done`, then land through `/check-in-diff`.

## Work Log

20260517-1448 - story creation: packaged the completed user-requested printed-index link fix as a new Story 016 because no open story owned the work and Story 012 was already done, evidence current story/status sweep and reviewed `docs/ideal.md`, `docs/spec.md`, `docs/presentation-decisions.md`, `docs/methodology/state.yaml`, `docs/methodology/graph.json`, `tests/fixtures/formats/_coverage-matrix.json`, and `docs/decisions/README.md`, next step: compile methodology views.
20260517-1453 - implementation and validation: linked the `page-008` top index rows and child summary table through the existing builder cleanup path, added focused regression coverage, rebuilt the family site, scanned the built/source pages for other index-like dot leaders, and verified local HTTP navigation from `page-008.html` `Josephine` to `chapter-012.html`, evidence `python -m pytest tests/test_build_family_site.py -q`, `python -m ruff check modules/build_family_site.py tests/test_build_family_site.py`, `make build-family-site`, `make test`, `make lint`, generated HTML scans, internal-link parser, and Browser check at `http://127.0.0.1:4173/page-008.html`, next step: `/mark-story-done`.
20260517-1459 - close-out: marked Story 016 done after fresh current-state evidence confirmed all acceptance criteria, tasks, workflow gates, tenet checks, and project checks; evidence `make test`, `make lint`, `make build-family-site`, and `make methodology-check` all passed on the current branch, next step: `/check-in-diff`.
