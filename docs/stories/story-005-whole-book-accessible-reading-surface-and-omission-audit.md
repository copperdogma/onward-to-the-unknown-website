---
title: "Whole-Book Accessible Reading Surface And Omission Audit"
status: "Done"
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
**Status**: Done
**Decision Refs**: `docs/ideal.md`, `docs/spec.md`, `docs/input-contract.md`, `docs/presentation-decisions.md`, `docs/runbooks/golden-build.md`, `docs/decisions/README.md`, none found after search for repo-local ADRs
**Depends On**: Story 004

## Goal

Extend the first local family-site slice into a whole-book local reading surface
that makes the rest of the staged book materially accessible on the web and
adds an explicit omission-audit artifact, so every source entry in the current
`input/` bundle is either rendered, intentionally deferred with a reason, or
clearly linked from the local site rather than silently disappearing.

## Acceptance Criteria

- [x] A checked-in omission-audit artifact accounts for every current
      `manifest.json` entry and marks it as rendered, intentionally deferred,
      or otherwise surfaced with a documented rationale.
- [x] The local build produces a whole-book reading surface that exposes the
      family run, the non-family chapter run, and the standalone page/image
      entries through explicit, accessible navigation rather than leaving them
      hidden in the raw input export.
- [x] Any source material not yet fully reshaped into the new shell is still
      reachable and labeled as an intentional deferral, not an accidental loss.
- [x] The expanded build path, presentation decisions, and methodology truth
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

- [x] Inspect the current staged manifest and Story 004 output, then define the
      omission-audit shape for whole-book coverage.
- [x] Extend the local builder so the local site exposes the whole book through
      accessible section or entry-point navigation rather than a family-only
      landing page.
- [x] Repair the builder's default source resolution so the documented local
      `input/` bundle builds without hidden env-only setup.
- [x] Decide and document how front matter, non-family chapters, and
      standalone page/image entries appear in the reshaped local site.
- [x] Emit a repeatable omission-audit artifact that accounts for every source
      entry in the bundle.
- [x] Add or extend fixture-backed tests to cover whole-book accounting and at
      least one representative non-family or standalone page surface.
- [x] Update repo docs and runbooks for the expanded local whole-book surface.
- [x] Update `tests/fixtures/formats/_coverage-matrix.json` and any relevant
      methodology docs if shipped whole-book coverage changes documented reality.
- [x] Check whether the implementation makes any family-slice-only assumptions
      or temporary notes redundant; remove them or create a concrete follow-up.
- [x] Run required checks for touched scope:
  - [x] `make test`
  - [x] `make lint`
  - [x] `make build-family-site`
  - [x] `make methodology-compile`
  - [x] `make methodology-check`
  - [x] Inspect the local output manually on desktop and mobile widths
- [x] Confirm whether this story adds a real measured eval surface; update
      `docs/evals/registry.yaml` only if it does.
- [x] Search docs and update any related to the whole-book build and omission
      rules.
- [x] Verify project tenets:
  - [x] Structure before chrome: whole-book routing still follows the source
        shape instead of hiding it behind decoration.
  - [x] No silent losses: every source entry is accounted for explicitly.
  - [x] Accessibility remains explicit across desktop and mobile.
  - [x] Provenance stays inspectable through internal maintenance surfaces.

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
- `Makefile` — add a repeatable omission-audit refresh command
- `docs/presentation-decisions.md` — record whole-book presentation and
  deferral rules
- `docs/input-contract.md` — update if the builder depends on additional
  manifest fields or audit assumptions
- `docs/omission-audit.json` — checked-in omission-audit snapshot for the
  accepted bundle
- `README.md` — document the expanded whole-book build surface
- `docs/RUNBOOK.md` — update local build/inspection instructions
- `docs/runbooks/golden-build.md` — update the golden inspection points for the
  whole-book slice
- `tests/fixtures/formats/_coverage-matrix.json` — graduation reality if the
  local slice broadens beyond the family run
- `docs/methodology/state.yaml` — substrate notes if whole-book coverage
  changes category reality
- `AGENTS.md` — current repo reality and core-doc references for the omission
  audit and whole-book builder

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

### Eval-First Gate

- **Success eval**: extend the fixture-backed builder proof so it covers one
  non-family chapter, one family chapter, and one standalone page entry, then
  assert that the generated site:
  - emits a whole-book landing page with explicit sections for family stories,
    non-family chapters, and standalone page/image entries
  - renders representative chapter and page-entry detail pages with preserved
    block ids and simple reading-page navigation while provenance remains
    inspectable in internal maintenance artifacts
  - writes an omission-audit artifact that accounts for every manifest entry
    with a status and rationale
- **Baseline now**:
  - `make test` passes with `8` tests on 2026-04-10.
  - `make lint` passes on 2026-04-10.
  - `make methodology-compile` and `make methodology-check` pass on
    2026-04-10.
  - `make build-family-site` fails on 2026-04-10 unless `SOURCE=` or an env
    var is provided because `modules/build_family_site.py` does not check the
    documented default bundle path under `input/`.
  - `make build-family-site SOURCE=input/doc-web-html/story206-onward-proof-r10`
    succeeds, but the generated site renders only the `15` family chapters.
  - Current whole-book coverage from the local site is `15 / 33` manifest
    entries rendered, with the other `18 / 33` entries omitted from the local
    surface and no omission-audit artifact checked in.
- **Candidate approaches**:
  - AI-only: reject for the source-of-truth render and omission accounting;
    coverage needs deterministic repeatable output.
  - Hybrid: acceptable only for helping phrase section labels or deferral copy;
    the builder and audit artifact still need to be explicit code.
  - Pure code: simplest honest path for manifest-driven grouping, navigation,
    and omission accounting.

### Scope Delta Folded In

- Repair the builder's default source resolution in the same pass. The docs
  already present `make build-family-site` as a supported path, so leaving the
  default broken would make the whole-book expansion look healthier than it is.
- Expand the fixture from two family chapters to a small mixed manifest slice
  so the acceptance criteria are covered by committed proof rather than live
  bundle inspection alone.
- Add one checked-in omission-audit artifact for the current accepted bundle in
  the repo truth surfaces, not just in ignored build output.

### Implementation Order

1. **Generalize the builder to whole-book entries** (`M`)
   - Files: `modules/build_family_site.py`,
     `scripts/build_family_site.py` only if CLI help or flags need to change
   - Replace the family-only selection flow with manifest-driven grouping that
     keeps source order intact while exposing:
     - family-story run
     - non-family chapter run
     - standalone page/image entries
  - Render both chapter and page entries through the same thin article
    extraction path, preserving block ids, copied images, the internal source
    manifest, and per-entry provenance JSON.
   - Keep the output static-export-first and derived directly from
     `manifest.json`; do not invent a second canonical metadata file just to
     drive navigation.
   - Done looks like: the generated local site has a clear whole-book landing
     page and browsable detail pages for representative entries across the full
     manifest.

2. **Add omission accounting and repair the default build path** (`S`)
   - Files: `modules/build_family_site.py`, likely one new checked-in audit
     artifact under `docs/`
   - Teach source resolution to look at the documented default bundle path
     under `input/doc-web-html/story206-onward-proof-r10` after `--source` and
     env overrides.
   - Emit a repeatable audit artifact that records each manifest entry's
     coverage status, grouping, output path or surfacing mode, and rationale.
   - Keep the audit thin and derived from the manifest plus builder decisions
     so it stays inspectable and easy to regenerate.
   - Done looks like: every manifest entry is explicitly accounted for, and the
     default local command works against the committed accepted bundle.

3. **Strengthen committed proof for whole-book coverage** (`S`)
   - Files: `tests/test_build_family_site.py`,
     `tests/fixtures/family_site_minimal/`
   - Extend the fixture manifest and HTML/provenance payload so tests cover:
     - one non-family chapter
     - one family chapter
     - one standalone page entry
     - omission-audit output
     - default-source handling via an explicit narrow assertion where honest
   - Keep the fixture intentionally small; the point is coverage shape, not a
     second full-book snapshot.
   - Done looks like: the new whole-book behavior is exercised by repeatable
     repo tests instead of only manual inspection.

4. **Update truth surfaces for the expanded slice** (`S`)
   - Files: `docs/presentation-decisions.md`, `docs/input-contract.md`,
     `README.md`, `docs/RUNBOOK.md`, `docs/runbooks/golden-build.md`,
     `tests/fixtures/formats/_coverage-matrix.json`,
     `docs/methodology/state.yaml`
   - Record how front matter, non-family chapters, and standalone page/image
     entries now appear in the local site, and which items are still only
     lightly reshaped versus richly presented.
   - Keep the coverage matrix and methodology notes honest: this story should
     improve `book-core-html` accessibility coverage while likely remaining
     `partial` overall because companion media and the final shell still do not
     exist.
   - Done looks like: docs stop describing the local slice as family-only, and
     the truth surfaces accurately describe the new whole-book boundary.

### Impact Analysis

- **Files likely to change**: `modules/build_family_site.py`,
  `tests/test_build_family_site.py`,
  `tests/fixtures/family_site_minimal/`, `docs/presentation-decisions.md`,
  `docs/input-contract.md`, `README.md`, `docs/RUNBOOK.md`,
  `docs/runbooks/golden-build.md`, `tests/fixtures/formats/_coverage-matrix.json`,
  `docs/methodology/state.yaml`, and one new checked-in omission-audit
  artifact.
- **Files at risk**: `modules/build_family_site.py` is already sizable, so this
  pass should extract or consolidate helper logic if the render branches become
  hard to review. The doc/runbook files are also at risk of drifting if the
  audit path or output labels change late.
- **Relevant graph/state context**:
  - `spec:1`, `spec:2`, `spec:3`, `spec:5`, and `spec:7` are all currently
    `partial`.
  - `book-core-html` remains `partial` in
    `tests/fixtures/formats/_coverage-matrix.json`.
  - `content_model` and `site_experience` are the primary architecture domains
    in play for this story.
- **Substrate verified**:
  - Story 004's builder exists and is fixture-tested.
  - The accepted local bundle contains `33` manifest entries (`24` chapters,
    `9` standalone pages), `images/`, and `provenance/blocks.jsonl`.
  - Both chapter and standalone page HTML files expose `<article>` regions with
    preserved `blk-*` ids and provenance rows.
- **Substrate missing**:
  - no whole-book navigation or grouping in the current local site
  - no omission-audit artifact
  - no default-source resolution for the documented local bundle path
- **Patterns to follow**: keep the builder deterministic, manifest-driven, and
  thin; reuse the current article extraction, provenance copy, and static page
  rendering patterns instead of inventing a separate runtime.
- **Potential redundancy to remove**: family-slice-only copy and landing-page
  assumptions in docs and builder text once the whole-book surface exists.
- **Human-approval blocker**: approval to proceed with the small scope delta
  above, especially the checked-in omission-audit artifact and the default-path
  repair folded into this story.

## Work Log

20260410-1738 — action: story created as the explicit follow-up to Story 004,
result: preserved the family-slice validation boundary while packaging the next
whole-book accessibility and omission-accounting slice as its own buildable
story, evidence: user instruction after validation plus the new preservation
rule in `docs/ideal.md` and `docs/spec.md`, next step: run `/build-story` on
this file when ready to expand the local site beyond the family run.
20260410-1820 — action: build-story exploration, result: verified Story 005 is
honestly buildable on the Story 004 substrate and does close a named Ideal gap
rather than optimizing a compromise in isolation; reviewed `docs/ideal.md`,
`docs/spec.md`, `docs/methodology/state.yaml`,
`docs/methodology/graph.json`, `tests/fixtures/formats/_coverage-matrix.json`,
dependency Story 004, `docs/input-contract.md`,
`docs/presentation-decisions.md`, `docs/runbooks/golden-build.md`, and
`docs/decisions/README.md`; traced the runtime seam from
`scripts/build_family_site.py` into `modules/build_family_site.py`; inspected
the accepted bundle at `input/doc-web-html/story206-onward-proof-r10` and
confirmed `33` manifest entries (`24` chapters, `9` standalone pages), copied
image assets, and provenance coverage for both chapter and page entries;
compared current output to the manifest and found that the builder renders only
the `15` family chapters, hard-rejects non-chapter entry ids, and emits no
omission-audit artifact; baseline evidence from this pass: `make test`,
`make lint`, `make methodology-compile`, and `make methodology-check` all
pass, `make build-family-site` fails without `SOURCE=` because no documented
default bundle path is checked, and `make build-family-site
SOURCE=input/doc-web-html/story206-onward-proof-r10` succeeds but leaves
`18 / 33` manifest entries outside the local surface; files likely to change:
builder module, mixed fixture/test proof, presentation/input/runbook docs,
coverage matrix/state notes, and one checked-in omission-audit artifact; next
step: present the detailed implementation plan and wait for approval before
writing code.
20260410-1826 — action: implementation start, result: user approved the plan
and the story status was promoted from `Pending` to `In Progress` before code
changes so the story record matches reality, evidence: this updated story file,
next step: regenerate methodology surfaces and implement the whole-book builder,
omission-audit artifact, and supporting tests/docs.
20260410-1847 — action: implementation, result: rewrote
`modules/build_family_site.py` from a family-only renderer into a manifest-led
whole-book reading-surface builder; added default-source fallback to the
committed `input/doc-web-html/story206-onward-proof-r10` bundle; rendered all
entry kinds through the same whole-entry path with grouped landing sections,
manifest-order previous/next navigation, per-entry provenance JSON, and an
`omission-audit.json` artifact that accounts for every manifest entry; expanded
the fixture to cover one standalone page, one non-family chapter, and one
family chapter; added `make refresh-omission-audit`; updated the input
contract, presentation decisions, runbooks, coverage matrix, methodology
state/graph, README, AGENTS, and the checked-in `docs/omission-audit.json`
snapshot so repo truth matches the new whole-book slice, evidence:
`make build-family-site` now succeeds without `SOURCE=`, the generated audit
shows `33` manifest entries with `{'rendered': 33}`, and the local output now
includes `page-001.html`, `chapter-001.html`, `chapter-009.html`, and
`chapter-024.html`; that pass still exposed reader-facing provenance and
omission-audit links, which were removed in the later reader-surface revision,
next step: run the full repo checks, record residual risk, and hand off for
validation.
20260410-1854 — action: verification and alignment sweep, result: refreshed the
checked-in audit snapshot with `make refresh-omission-audit`; ran `make test`
(`9` tests passed), `make lint`, `make methodology-compile`, and
`make methodology-check`; confirmed the generated HTML and audit artifact
contain the expected whole-book sections and entry pages via direct file
inspection; ran the `/align` methodology sweep and found no new spec, ADR, or
eval changes warranted beyond the truth-surface updates already made; left the
manual desktop/mobile browser inspection and validation workflow gates open
because they were not performed in this pass, evidence: current-pass command
output plus direct reads of `build/family-site/index.html`,
`build/family-site/page-001.html`, `build/family-site/chapter-001.html`,
`build/family-site/chapter-009.html`, `build/family-site/chapter-024.html`,
and `docs/omission-audit.json`, next step: ask the user to run `/validate` and
complete a real browser check on desktop and mobile widths before marking the
story done.
20260410-1916 — action: reader-surface revision, result: removed the
meta-commentary and provenance/audit chrome from the public HTML in response to
user feedback that the site should read like a real website instead of an
explanation of itself; simplified the landing page to section navigation plus
entry cards, simplified detail pages to previous/contents/next navigation and
article content only, and moved generated audit/provenance/source-manifest
artifacts under `build/family-site/_internal/` while keeping
`docs/omission-audit.json` as the checked-in maintenance snapshot; updated the
fixture proof, presentation decisions, golden-build runbook, and refresh
command to match, evidence: current-pass `make refresh-omission-audit`,
`make test`, `make lint`, `make methodology-compile`, `make methodology-check`,
and direct reads of the rebuilt public HTML showing the removal of
`Visible provenance`, `Omission audit`, and related reader-facing copy, next
step: run a human browser pass to judge whether the simplified reading surface
now feels appropriately editorial instead of internal.
20260410-1949 — action: manual inspection and close-out truth pass, result:
reviewed fresh desktop/mobile screenshots of `index.html` and `chapter-009.html`
and found the grouped landing sections, full-width mobile navigation, table
overflow handling, and article typography acceptable without more CSS changes
for this story; updated the input contract and story wording so provenance is
described as an internal maintenance surface rather than reader-facing chrome;
checked the acceptance criteria, manual-inspection task, accessibility tenet,
and build/validation workflow gates based on this pass, evidence:
fresh Playwright desktop/mobile screenshots of `index.html` and
`chapter-009.html`, plus direct edits to `docs/input-contract.md` and this
story file, next step: rerun the required checks and confirm the story is ready
for `/mark-story-done`.
20260410-2004 — action: mark-story-done close-out, result: confirmed all Story
005 tasks, acceptance criteria, and tenet checks remain satisfied; reran
`python -m pytest tests/`, `python -m ruff check modules/ tests/`,
`make build-family-site`, `make methodology-compile`, and
`make methodology-check`; set the story status to `Done`, checked the final
workflow gate, and prepared the changelog/generated story surfaces for git
landing, evidence: current-pass command output plus this updated story file and
`CHANGELOG.md`, next step: `/check-in-diff`.
