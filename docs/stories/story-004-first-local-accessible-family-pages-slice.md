---
title: "First Local Accessible Family-Pages Slice"
status: "Done"
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
**Status**: Done
**Decision Refs**: `docs/infrastructure.md`, `README.md`, `docs/RUNBOOK.md`, `docs/runbooks/golden-build.md`, `docs/decisions/README.md`, none found after search for repo-local ADRs
**Depends On**: Story 001

## Goal

Build the first local, static-export-first website slice from the verified
`input/` bundle, using the current input website as the presentation baseline
while preserving each family page as a whole page in the first pass and making
the result materially more accessible for older desktop/mobile readers.

## Acceptance Criteria

- [x] A checked-in doc explains the actual local `input/` bundle contract,
      including `manifest.json`, chapter HTML, page HTML, images, and
      provenance JSONL.
- [x] The repo records the first presentation decisions for the imported site,
      explicitly preserving family pages as whole pages unless a later story
      changes that.
- [x] One real local family-site slice renders from the current `input/`
      bundle with a family landing page plus whole-page family chapters, larger
      type, larger hit targets, clear navigation, and visible provenance cues
      for older readers.
- [x] The local build path is repeatable and documented, even if final design
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

- [x] Inspect the current input website and document the `input/` bundle
      contract in a checked-in doc.
- [x] Record the first presentation decisions, including that family pages stay
      whole pages in this pass.
- [x] Create a minimal static-export build path from the verified `input/`
      source bundle.
- [x] Render the first local family subsection as a landing page plus whole-page
      family stories with larger type, larger tap targets, clear nav, and
      provenance cues.
- [x] Add a repeatable local preview/build command and update repo docs.
- [x] Replace the placeholder truth in `docs/runbooks/golden-build.md` with the
      first real local render/build path if this story lands it.
- [x] Update `tests/fixtures/formats/_coverage-matrix.json` and any relevant
      methodology docs if the local site slice changes documented reality.
- [x] Check whether the implementation makes any provisional notes or throwaway
      adapter logic redundant; remove them or create a concrete follow-up.
- [x] Run required checks for touched scope:
  - [x] `make methodology-compile`
  - [x] `make methodology-check`
  - [x] Run the chosen local build/export command once it exists.
  - [x] Inspect the local output manually on desktop and mobile widths.
  - [ ] If agent tooling changes:
    - [ ] `scripts/sync-agent-skills.sh`
    - [ ] `scripts/sync-agent-skills.sh --check`
    - [ ] `make skills-check`
- [x] Confirm whether this slice adds a real measured eval surface; leave
      `docs/evals/registry.yaml` unchanged if not.
- [x] Search docs and update any that changed truth because of the chosen
      local build and presentation path.
- [x] Verify project tenets:
  - [x] Structure before chrome: the content shape remains primary.
  - [x] Family pages stay whole pages in this pass.
  - [x] Accessibility is explicit: larger targets and older-reader usability
        are requirements, not polish.
  - [x] Provenance remains visible and inspectable.

## Workflow Gates

- [x] Build complete: implementation finished, required checks run, and summary
      shared
- [x] Validation complete or explicitly skipped by user
- [x] Story marked done via `/mark-story-done`

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

- `.gitignore` — keep the real staged `input/` bundle ignored while allowing
  committed builder fixtures under `tests/fixtures/**/input/`
- `docs/input-contract.md` — real local input bundle contract
- `docs/presentation-decisions.md` — first checked-in presentation choices for
  the family-site slice
- `README.md` — local build/runtime truth once chosen
- `docs/RUNBOOK.md` — local build and preview commands
- `docs/runbooks/golden-build.md` — replace the current placeholder once the
  first local render path exists
- `Makefile` — add local build/preview plus repo-level test and lint targets
- `tests/fixtures/formats/_coverage-matrix.json` — update intake/site-slice
  truth if needed
- `modules/build_family_site.py` — thin builder implementation for the local
  family-site slice
- `scripts/build_family_site.py` — thin local static builder for the family-site
  slice
- `tests/test_build_family_site.py` — fixture-backed build proof for the slice
- `tests/fixtures/family_site_minimal/` — minimal committed fixture for the
  local builder
- `AGENTS.md` — current repo reality and core-doc references for the new local
  build surface
- Static template/style files TBD once the smallest path is chosen

## Redundancy / Removal Targets

- Assumptions copied from the raw input site that do not survive the first
  local accessible slice.
- Throwaway local build notes once the build command and docs exist.

## Notes

- This story intentionally separates site crafting from the hosting substrate
  already completed in Story 001.
- The first pass should preserve the integrity of family pages rather than
  atomizing them.
- This family-focused slice is a deliberate subsection, not a claim that the
  rest of the book can disappear; anything not carried into a reshaped surface
  needs to be intentionally deferred and documented.

## Plan

### Eval-First Gate

- **Success eval**: add one fixture-backed build test that proves the local
  builder can read a minimal manifest plus chapter/page HTML, emit a family
  landing page and one whole-page family chapter, preserve block ids and image
  references, and surface provenance summary text.
- **Baseline now**:
  - `docs/input-contract.md` does not exist.
  - No local site build command exists in `Makefile`.
  - `make test` currently fails with `No rule to make target 'test'`.
  - `make lint` currently fails with `No rule to make target 'lint'`.
  - `docs/runbooks/golden-build.md` still states there is no rendered site
    path.
- **Candidate approaches**:
  - AI-only: reject for the render path; it would be opaque and unstable for a
    deterministic archive surface.
  - Hybrid: useful for documenting the intake contract and presentation
    tradeoffs, but the actual build/render path should remain explicit code.
  - Pure code: simplest for the builder itself, with AI only helping reason
    about presentation choices.

### Scope Delta Folded In

- Render the first **family subsection** rather than a single isolated page.
  Once a builder exists, looping across the explicit family sequence is a small
  coherent delta and is the honest way to prove the “whole family pages”
  decision.
- Add repo-level `make test` and `make lint` targets in the same pass so the
  story’s new code can be validated through a stable project command surface.
- Replace the placeholder `docs/runbooks/golden-build.md` text because this
  story, if shipped, will invalidate it.

### Implementation Order

1. **Document intake and editorial decisions** (`XS`)
   - Files: `docs/input-contract.md`, `docs/presentation-decisions.md`
   - Capture the real bundle shape: manifest metadata, entry ordering, chapter
     and page HTML conventions, image folder usage, provenance JSONL schema
     cues, and the current run id `story206-onward-proof-r10`.
   - Record the first presentation decisions:
     - preserve family stories as whole pages in this pass
     - treat the family-story subsection as the first reshaped surface
     - keep front matter and standalone image pages out of the family landing
       page for now
     - keep provenance visible on every rendered family page
   - Done looks like: a future session could understand the bundle and the
     first presentation stance without reopening the raw HTML.

2. **Add the thin local family-site builder** (`M`)
   - Files: `scripts/build_family_site.py`, one small checked-in style/template
     surface (exact file TBD), possibly `Makefile`
   - Use explicit static generation, not a framework.
   - Source resolution order should be:
     - `--source`
     - `ONWARD_INPUT_SOURCE_DIR`
     - existing `DREAMHOST_DEPLOY_SOURCE_DIR` as a compatibility fallback
   - Output to a local ignored build directory such as `build/family-site/`.
   - Parse `manifest.json`, preserve the family sequence explicitly, extract
     each source page’s `<article>` content, and emit:
     - a family landing page
     - whole-page family chapter pages
     - copied supporting images
     - copied raw provenance JSONL plus a visible per-page provenance summary
   - Accessibility floor for the generated pages:
     - larger default body type
     - large previous/next/home targets
     - clearer section spacing and table handling
     - obvious “where this came from” panel
   - Done looks like: one command produces a browsable local family-site slice
     from the current bundle without editing the source export by hand.

3. **Add repeatable validation and preview commands** (`S`)
   - Files: `Makefile`, `tests/test_build_family_site.py`,
     `tests/fixtures/family_site_minimal/`
   - Add `make test` and `make lint` as stable repo commands.
   - Add a build command such as `make build-family-site`.
   - Document the preview command in repo docs; add a `make preview-family-site`
     target only if it stays thin and honest.
   - Fixture test should verify:
     - builder reads manifest and source HTML
     - generated output includes landing and family page files
     - block ids survive into rendered content
     - provenance summary text is present
   - Done looks like: the build is not just manual inspection; it has one
     repeatable committed proof.

4. **Update truth surfaces after the first real local render path exists** (`S`)
   - Files: `README.md`, `docs/RUNBOOK.md`, `docs/runbooks/golden-build.md`,
     `tests/fixtures/formats/_coverage-matrix.json`, and likely
     `docs/methodology/state.yaml`
   - Replace the current “no rendered site yet” placeholder in the golden-build
     runbook with the actual local build command and inspection points.
   - Move the relevant format/methodology surfaces from “planned/missing” to
     the honest partial state that the first local slice proves.
   - Done looks like: repo docs no longer describe this area as nonexistent.

### Impact Analysis

- **Files likely to change**: the story’s listed docs, `Makefile`, a new local
  build script, and one new builder test fixture/test pair.
- **Files at risk**: `README.md`, `docs/RUNBOOK.md`, and
  `docs/runbooks/golden-build.md` can easily drift if the command names or
  output directory change late.
- **Substrate verified**:
  - Story 001 already proved deploy and hosting.
  - The input bundle exists locally and contains 24 chapter entries, 9 page
    entries, an `images/` directory, and `provenance/blocks.jsonl`.
  - Raw HTML already preserves block ids and image references, so the first
    local builder can stay thin.
- **Substrate missing**:
  - no runtime/build code
  - no intake contract doc
  - no family-slice presentation doc
  - no local build command
  - no repo-level `make test` / `make lint`
- **Redundancy plan**: avoid inventing a second opaque content transform. The
  first builder should adapt the staged export as directly as possible and
  delete any placeholder docs it makes false.
- **Human-approval blocker**: none beyond agreement with the small scope
  expansions above.

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
20260410-1509 — action: build-story exploration, result: verified Story 004 is
honestly buildable against the current repo and local bundle; reviewed
`docs/ideal.md`, `docs/spec.md`, `docs/methodology/state.yaml`,
`docs/methodology/graph.json`, `tests/fixtures/formats/_coverage-matrix.json`,
`docs/infrastructure.md`, `docs/runbooks/golden-build.md`, `README.md`, and
dependency Story 001; confirmed no repo-local ADRs exist beyond
`docs/decisions/README.md`; inspected the staged bundle at
`/Users/cam/Documents/Projects/onward-to-the-unknown-website/input/doc-web-html/story206-onward-proof-r10`
and found `manifest.json`, 24 chapter pages, 9 standalone page entries,
`images/`, and 525 provenance rows with preserved `blk-*` ids; identified the
main substrate gap as “no local builder/runtime at all,” not missing source
data; found that `make test` and `make lint` currently fail because no such
targets exist and that `docs/runbooks/golden-build.md` will become false once
this story lands; noted the current input site’s accessibility issues
(duplicated inline CSS, `0.9rem` nav text, small link targets, no visible
provenance surface, and a contents page that mixes standalone page entries with
chapters), evidence: current-pass file reads and `make test` / `make lint`
failures, next step: present the implementation plan and wait for approval
before writing code.
20260410-1517 — action: implementation start, result: user approved the build
plan and the story was promoted from `Pending` to `In Progress` so the story
index matches reality before code changes, evidence: this updated story record,
next step: build the thin local family-site generator, fixture proof, and local
build commands.
20260410-1649 — action: implementation and proof, result: added
`docs/input-contract.md` and `docs/presentation-decisions.md`; built the thin
local generator in `modules/build_family_site.py` with the script entrypoint in
`scripts/build_family_site.py`; added fixture-backed proof in
`tests/test_build_family_site.py` plus a `.gitignore` carve-out so the committed
fixture under `tests/fixtures/**/input/` is not swallowed by the repo-wide
`input/` ignore rule; added `make test`, `make lint`, `make build-family-site`,
and `make preview-family-site`; replaced the placeholder golden-build runbook;
updated README, RUNBOOK, AGENTS, methodology state, coverage matrix, and
generated story surfaces to reflect the first real local render path, evidence:
`make test`, `make lint`, `make build-family-site
SOURCE=/Users/cam/Documents/Projects/onward-to-the-unknown-website/input/doc-web-html/story206-onward-proof-r10`,
`make methodology-compile`, `make methodology-check`, and manual desktop/mobile
inspection of the generated slice at `build/family-site/` using captured
screenshots under `build/inspection/`, next step: run `/validate` before
marking the story done.
20260410-1703 — action: preservation-rule clarification, result: tightened the
ideal/spec/presentation surfaces so the project explicitly aims to make the
entire book accessible on the web and treats any omitted source material as an
intentional, documented deferral rather than accidental loss, evidence: updates
to `docs/ideal.md`, `docs/spec.md`, `docs/presentation-decisions.md`, and this
story note, next step: carry that rule forward when reshaping non-family
sections.
20260410-1748 — action: story closed via `/mark-story-done`, result: Story 004
is complete and validated as the first local family-story slice; the remaining
whole-book accessibility and omission-accounting work was split explicitly into
Story 005, evidence: fresh `python -m pytest tests/`, fresh
`python -m ruff check modules/ tests/`, fresh `make build-family-site
SOURCE=/Users/cam/Documents/Projects/onward-to-the-unknown-website/input/doc-web-html/story206-onward-proof-r10`,
fresh `make methodology-compile`, fresh `make methodology-check`, and the new
follow-up at `docs/stories/story-005-whole-book-accessible-reading-surface-and-omission-audit.md`,
next step: `/check-in-diff`
