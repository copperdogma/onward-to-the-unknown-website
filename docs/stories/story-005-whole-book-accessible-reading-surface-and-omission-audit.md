---
title: "Whole-Book Accessible Reading Surface And Omission Audit"
status: "Pending"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "3. Trustworthy Source Lineage"
  - "4. Reusable Content Model"
  - "5. Accessible Family Archive"
spec_refs:
  - "spec:1"
  - "spec:2"
  - "spec:3"
  - "spec:5"
  - "spec:7"
  - "C1"
  - "C2"
  - "C3"
  - "C5"
  - "C7"
adr_refs: []
depends_on:
  - "story-004"
category_refs:
  - "spec:1"
  - "spec:2"
  - "spec:3"
  - "spec:5"
  - "spec:7"
compromise_refs:
  - "C1"
  - "C2"
  - "C3"
  - "C5"
  - "C7"
input_coverage_refs:
  - "book-core-html"
architecture_domains:
  - "content_model"
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "local staged website snapshot in input/ plus Story 004 family-site builder"
---

# Story 005 — Whole-Book Accessible Reading Surface And Omission Audit

**Priority**: High
**Status**: Pending
**Decision Refs**: `docs/ideal.md`, `docs/spec.md`, `docs/input-contract.md`, `docs/presentation-decisions.md`, `docs/runbooks/golden-build.md`, `docs/decisions/README.md`, none found after search for repo-local ADRs
**Depends On**: Story 004

## Goal

Extend the first local family-site slice into a whole-book local reading surface
that makes the rest of the staged book materially accessible on the web and
adds an explicit omission-audit artifact, so every source entry in the current
`input/` bundle is either rendered, intentionally deferred with a reason, or
clearly linked from the local site rather than silently disappearing.

## Acceptance Criteria

- [ ] A checked-in omission-audit artifact accounts for every current
      `manifest.json` entry and marks it as rendered, intentionally deferred,
      or otherwise surfaced with a documented rationale.
- [ ] The local build produces a whole-book reading surface that exposes the
      family run, the non-family chapter run, and the standalone page/image
      entries through explicit, accessible navigation rather than leaving them
      hidden in the raw input export.
- [ ] Any source material not yet fully reshaped into the new shell is still
      reachable and labeled as an intentional deferral, not an accidental loss.
- [ ] The expanded build path, presentation decisions, and methodology truth
      surfaces are updated honestly for the whole-book slice.

## Out of Scope

- Final visual-system polish for every book surface.
- Companion audio, podcast, or scan embedding beyond link placeholders or
  intentional deferral notes.
- DreamHost deployment changes beyond reusing the existing Story 001 substrate.
- Replacing the staged HTML bundle with a new upstream export format.

## Approach Evaluation

- **Simplification baseline**: A single LLM call is not an honest solution
  because the work needs repeatable manifest coverage accounting and a
  deterministic local site build.
- **AI-only**: Weak fit. AI can help reason about grouping or labeling, but it
  should not be the source of truth for whether an entry is present or omitted.
- **Hybrid**: Reasonable for drafting omission labels or section-grouping
  options while keeping the audit artifact and builder deterministic.
- **Pure code**: Strong fit for manifest-driven coverage accounting, accessible
  navigation generation, and omission-report output.
- **Repo constraints / prior decisions**: The ideal and `spec:3` now explicitly
  require that subsection views not accidentally make book content disappear.
  Story 004 proved the family-slice substrate but also narrowed the current
  visible reading surface on purpose.
- **Existing patterns to reuse**: Extend `modules/build_family_site.py`,
  `docs/presentation-decisions.md`, and the Story 004 test/build/doc surfaces
  instead of inventing a separate runtime.
- **Eval**: The decisive proof is a built local slice plus an artifact that can
  be checked against the manifest to show every entry is accounted for.

## Tasks

- [ ] Inspect the current staged manifest and Story 004 output, then define the
      omission-audit shape for whole-book coverage.
- [ ] Extend the local builder so the local site exposes the whole book through
      accessible section or entry-point navigation rather than a family-only
      landing page.
- [ ] Decide and document how front matter, non-family chapters, and
      standalone page/image entries appear in the reshaped local site.
- [ ] Emit a repeatable omission-audit artifact that accounts for every source
      entry in the bundle.
- [ ] Add or extend fixture-backed tests to cover whole-book accounting and at
      least one representative non-family or standalone page surface.
- [ ] Update repo docs and runbooks for the expanded local whole-book surface.
- [ ] Update `tests/fixtures/formats/_coverage-matrix.json` and any relevant
      methodology docs if shipped whole-book coverage changes documented reality.
- [ ] Check whether the implementation makes any family-slice-only assumptions
      or temporary notes redundant; remove them or create a concrete follow-up.
- [ ] Run required checks for touched scope:
  - [ ] `make test`
  - [ ] `make lint`
  - [ ] `make build-family-site`
  - [ ] `make methodology-compile`
  - [ ] `make methodology-check`
  - [ ] Inspect the local output manually on desktop and mobile widths
- [ ] Confirm whether this story adds a real measured eval surface; update
      `docs/evals/registry.yaml` only if it does.
- [ ] Search docs and update any related to the whole-book build and omission
      rules.
- [ ] Verify project tenets:
  - [ ] Structure before chrome: whole-book routing still follows the source
        shape instead of hiding it behind decoration.
  - [ ] No silent losses: every source entry is accounted for explicitly.
  - [ ] Accessibility remains explicit across desktop and mobile.
  - [ ] Provenance stays visible and inspectable for reshaped surfaces.

## Workflow Gates

- [ ] Build complete: implementation finished, required checks run, and summary
      shared
- [ ] Validation complete or explicitly skipped by user
- [ ] Story marked done via `/mark-story-done`

## Blocker Summary

N/A

## Blocker Evidence

N/A

## Unblock Condition

N/A

## Architectural Fit

- **Owning module / area**: The existing local static builder and its
  supporting documentation.
- **Methodology reality**: `spec:2`, `spec:3`, `spec:5`, and `spec:7` are now
  `partial`; this story advances them by expanding the first real rendering
  slice from a family subsection to a whole-book accessible surface.
- **Substrate evidence**: Story 004 proved a real local builder, documented the
  `input/` bundle contract, and established a fixture-backed proof path. The
  staged source bundle and manifest already exist locally.
- **Data contracts / schemas**: The likely new contract is a small
  omission-audit artifact plus any additional section/grouping metadata the
  builder needs to emit. Keep that layer thin and derived from the manifest.
- **File sizes**: `modules/build_family_site.py` is already a non-trivial file,
  so this story should watch for growth and split template/data helpers if the
  builder becomes hard to review.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`,
  `docs/presentation-decisions.md`, and `docs/decisions/README.md`. No
  repo-local ADRs exist yet.

## Files to Modify

- `modules/build_family_site.py` — extend the builder from family-only output
  to whole-book coverage plus omission accounting
- `scripts/build_family_site.py` — CLI flags or command-surface updates if
  needed
- `tests/test_build_family_site.py` — broaden proof to cover whole-book
  accounting and representative non-family/page-entry rendering
- `tests/fixtures/family_site_minimal/` — extend fixture coverage if needed
- `docs/presentation-decisions.md` — record whole-book presentation and
  deferral rules
- `docs/input-contract.md` — update if the builder depends on additional
  manifest fields or audit assumptions
- `README.md` — document the expanded whole-book build surface
- `docs/RUNBOOK.md` — update local build/inspection instructions
- `docs/runbooks/golden-build.md` — update the golden inspection points for the
  whole-book slice
- `tests/fixtures/formats/_coverage-matrix.json` — graduation reality if the
  local slice broadens beyond the family run
- `docs/methodology/state.yaml` — substrate notes if whole-book coverage
  changes category reality

## Redundancy / Removal Targets

- Family-slice-only assumptions in the builder or docs that become false once
  the local site covers the whole book.
- Temporary omission notes that are superseded by a real omission-audit
  artifact.

## Notes

- This is a new story rather than a reopen of Story 004 because Story 004 now
  has a coherent shipped validation surface: the first family-story slice.
  Whole-book coverage and omission accounting are a broader, distinct success
  surface.
- The user explicitly clarified that the project is meant to make the entire
  book accessible on the web and that any loss of material must be intentional.

## Plan

Written during `/create-story`. The first honest move in `/build-story` should
be to compare the current manifest entry list to the Story 004 output and pick
the thinnest extension that proves whole-book accessibility without silently
dropping front matter, non-family chapters, or standalone page/image entries.

## Work Log

20260410-1738 — action: story created as the explicit follow-up to Story 004,
result: preserved the family-slice validation boundary while packaging the next
whole-book accessibility and omission-accounting slice as its own buildable
story, evidence: user instruction after validation plus the new preservation
rule in `docs/ideal.md` and `docs/spec.md`, next step: run `/build-story` on
this file when ready to expand the local site beyond the family run.
