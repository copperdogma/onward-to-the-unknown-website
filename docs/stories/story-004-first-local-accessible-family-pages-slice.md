---
title: "First Local Accessible Family-Pages Slice"
status: "Pending"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "2. Connected Companion Media"
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
  - "story-001"
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
legacy_system: "local staged website snapshot in input/"
---

# Story 004 — First Local Accessible Family-Pages Slice

**Priority**: High
**Status**: Pending
**Decision Refs**: `docs/infrastructure.md`, `README.md`, `docs/RUNBOOK.md`, `docs/runbooks/golden-build.md`, `docs/decisions/README.md`, none found after search for repo-local ADRs
**Depends On**: Story 001

## Goal

Build the first local, static-export-first website slice from the verified
`input/` bundle, using the current input website as the presentation baseline
while preserving each family page as a whole page in the first pass and making
the result materially more accessible for older desktop/mobile readers.

## Acceptance Criteria

- [ ] A checked-in doc explains the actual local `input/` bundle contract,
      including `manifest.json`, chapter HTML, page HTML, images, and
      provenance JSONL.
- [ ] The repo records the first presentation decisions for the imported site,
      explicitly preserving family pages as whole pages unless a later story
      changes that.
- [ ] One real local site slice renders from the current `input/` bundle with
      larger type, larger hit targets, clear navigation, and visible provenance
      cues for older readers.
- [ ] The local build path is repeatable and documented, even if final design
      polish is deferred.

## Out of Scope

- Origin-SSL hardening or deploy automation beyond the infrastructure path
  already owned by Story 001.
- Full-site migration of every chapter and archive surface.
- Breaking family pages into smaller fragments.
- NotebookLM podcast generation.
- ElevenLabs audiobook production.

## Approach Evaluation

- **Simplification baseline**: Start from the existing HTML export and improve
  presentation/accessibility before inventing a heavier content pipeline.
- **AI-only**: Weak fit for the actual slice. AI can help summarize the input
  shape and presentation tradeoffs, but the site output should be deterministic
  and inspectable.
- **Hybrid**: Good fit for documenting the input contract and presentation
  choices while keeping the build itself explicit code/templates.
- **Pure code**: Appropriate for the static-export build and local preview path.
- **Repo constraints / prior decisions**: Hosting is already verified on
  DreamHost shared hosting, so the site slice should stay static-export-first.
- **Existing patterns to reuse**: The current input website is the baseline to
  compare against; preserve family pages as whole pages on the first pass.
- **Eval**: Compare the built local slice against the current input website for
  fidelity, navigation clarity, and older-reader accessibility.

## Tasks

- [ ] Inspect the current input website and document the `input/` bundle
      contract in a checked-in doc.
- [ ] Record the first presentation decisions, including that family pages stay
      whole pages in this pass.
- [ ] Create a minimal static-export build path from the verified `input/`
      source bundle.
- [ ] Render one real local family-page slice with larger type, larger tap
      targets, clear nav, and provenance cues.
- [ ] Add a repeatable local preview/build command and update repo docs.
- [ ] Update `tests/fixtures/formats/_coverage-matrix.json` and any relevant
      methodology docs if the local site slice changes documented reality.
- [ ] Check whether the implementation makes any provisional notes or throwaway
      adapter logic redundant; remove them or create a concrete follow-up.
- [ ] Run required checks for touched scope:
  - [ ] `make methodology-compile`
  - [ ] `make methodology-check`
  - [ ] Run the chosen local build/export command once it exists.
  - [ ] Inspect the local output manually on desktop and mobile widths.
  - [ ] If agent tooling changes:
    - [ ] `scripts/sync-agent-skills.sh`
    - [ ] `scripts/sync-agent-skills.sh --check`
    - [ ] `make skills-check`
- [ ] If real measured checks are added for the slice, update
      `docs/evals/registry.yaml`.
- [ ] Search docs and update any that changed truth because of the chosen
      local build and presentation path.
- [ ] Verify project tenets:
  - [ ] Structure before chrome: the content shape remains primary.
  - [ ] Family pages stay whole pages in this pass.
  - [ ] Accessibility is explicit: larger targets and older-reader usability
        are requirements, not polish.
  - [ ] Provenance remains visible and inspectable.

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

- **Owning module / area**: Static build substrate, local site templates, and
  input-contract documentation.
- **Methodology reality**: Story 001 established hosting and deploy substrate;
  this story now creates the first real site/runtime substrate for `spec:2`,
  `spec:3`, `spec:5`, and `spec:7`.
- **Substrate evidence**: Verified `input/` bundle exists; DreamHost deploy path
  exists; no site runtime exists yet, so this story honestly creates it.
- **Data contracts / schemas**: The first checked-in input contract doc and
  build path should stay thin and tied directly to the existing bundle shape.
- **File sizes**: runtime files TBD; keep them small.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, `docs/infrastructure.md`,
  and `README.md`. No repo-local ADRs exist yet.

## Files to Modify

- `docs/input-contract.md` — real local input bundle contract
- `README.md` — local build/runtime truth once chosen
- `docs/RUNBOOK.md` — local build and preview commands
- `tests/fixtures/formats/_coverage-matrix.json` — update intake/site-slice
  truth if needed
- Static build/template files TBD once the smallest path is chosen

## Redundancy / Removal Targets

- Assumptions copied from the raw input site that do not survive the first
  local accessible slice.
- Throwaway local build notes once the build command and docs exist.

## Notes

- This story intentionally separates site crafting from the hosting substrate
  already completed in Story 001.
- The first pass should preserve the integrity of family pages rather than
  atomizing them.

## Plan

Written during `/build-story`.

## Work Log

20260410-1258 — action: story created as follow-up during Story 001 close-out,
result: separated local website crafting from already-completed hosting/DNS
setup, evidence: Story 001 rescope decision, next step: build this story from
the verified `input/` bundle and presentation baseline.
20260410-1320 — action: scope refinement, result: added a thin project-local
`/deploy` skill to this story after confirming this repo does not yet have one
and that Storybook's existing `/deploy` skill is Fly-specific, evidence:
searches under `.agents/skills/` in this repo and
`/Users/cam/Documents/Projects/Storybook/storybook/.agents/skills/deploy/SKILL.md`,
next step: adapt the idea down to static SFTP upload for DreamHost.
20260410-1418 — action: scope correction, result: moved the deploy-skill
requirement back to Story 001 because the user wants the first real upload to
count as infrastructure rather than local site-crafting work, evidence: user
instruction in this thread, next step: keep Story 004 focused on reshaping the
site locally once the deploy path is proven.
