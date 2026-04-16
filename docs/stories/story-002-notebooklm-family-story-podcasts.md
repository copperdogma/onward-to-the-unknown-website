---
title: "NotebookLM Whole-Book And Chapter Podcasts"
status: "Draft"
priority: "Medium"
ideal_refs:
  - "1. Canonical Book Experience"
  - "2. Connected Companion Media"
  - "4. Reusable Content Model"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:1"
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:6"
  - "spec:8"
  - "C1"
  - "C2"
  - "C3"
  - "C4"
  - "C6"
  - "B1"
adr_refs: []
depends_on:
  - "story-005"
category_refs:
  - "spec:1"
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:6"
  - "spec:8"
compromise_refs:
  - "C1"
  - "C2"
  - "C3"
  - "C4"
  - "C6"
  - "B1"
input_coverage_refs:
  - "book-core-html"
  - "chapter-podcasts"
  - "full-book-podcast"
architecture_domains:
  - "content_model"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "Google NotebookLM workflow over staged archive materials"
---

# Story 002 — NotebookLM Whole-Book And Chapter Podcasts

**Priority**: Medium
**Status**: Draft
**Decision Refs**: `docs/evals/README.md`, `docs/input-contract.md`, `docs/RUNBOOK.md`, `tests/fixtures/formats/_coverage-matrix.json`, none found after search for repo-local ADRs or NotebookLM runbooks
**Depends On**: Story 005

## Goal

Create a repeatable, provenance-aware NotebookLM workflow that can generate one
podcast for the whole book and one podcast per chapter from authoritative
source packets, without turning the process into a set of opaque one-off
uploads that drift from the repo's source truth.

## Acceptance Criteria

- [ ] A documented source-prep workflow exists for creating one whole-book
      NotebookLM podcast from authoritative staged or canonical source
      materials.
- [ ] Reliable per-chapter source packets are defined with naming, lineage, and
      review rules so one podcast can be generated for each chapter without ad
      hoc selection.
- [ ] The repo records where generated podcast outputs, prompts, and metadata
      should live so the site can later link to them with inspectable
      provenance.

## Out of Scope

- Building the public website runtime itself.
- ElevenLabs audiobook production or distribution.
- Final podcast hosting or player UI beyond the metadata needed for future site
  integration.

## Approach Evaluation

- **Simplification baseline**: A single NotebookLM upload may already be good
  enough for the whole-book pilot, so the first task should measure that before
  inventing elaborate prep tooling.
- **AI-only**: Viable for draft audio generation, but weak on repeatability,
  source packaging, and provenance unless the surrounding workflow is explicit.
- **Hybrid**: Strongest fit. Use canonical source packets, naming conventions,
  and lightweight docs/scripts around NotebookLM's generation surface.
- **Pure code**: Not realistic for the generation step because the core
  capability lives in an external AI product.
- **Repo constraints / prior decisions**: There is no existing NotebookLM
  workflow, no packet-generation rule for whole-book versus chapter variants,
  and no output inventory path in the repo yet. The whole-book site slice
  should shape the packet boundaries instead of every audio workflow inventing
  its own format.
- **Existing patterns to reuse**: Story 005 established the authoritative
  whole-book source slice. Coverage rows already acknowledge chapter and
  full-book podcast surfaces, and the audiobook script corpus now offers a
  chapter-aligned fallback source lane when that is the clearest packet.
- **Eval**: Pilot the whole-book workflow and one representative chapter
  packet. Compare repeatability, source lineage, and manual review burden
  before scaling to the full set.

## Tasks

- [ ] Define how whole-book and per-chapter source packets will be derived from
      the staged source snapshot or canonical site data.
- [ ] Run a small baseline NotebookLM experiment on the whole-book corpus
      before building extra prep or packaging logic.
- [ ] Document naming, provenance, storage, and human-review rules for
      generated podcasts.
- [ ] Generate the whole-book podcast and one podcast per chapter once the
      source packets are ready.
- [ ] Record links and metadata for generated podcasts so they can become
      inspectable companion media on the site.
- [ ] Update `tests/fixtures/formats/_coverage-matrix.json` and any related
      docs if these podcast surfaces move from planned to real.
- [ ] Remove or avoid ad hoc source-packet notes if canonical slices can drive
      the workflow directly.
- [ ] Run required checks for touched scope:
  - [ ] `make methodology-compile`
  - [ ] `make methodology-check`
  - [ ] Manually inspect the source packets used for the pilot.
  - [ ] Manually review the pilot podcast outputs before scaling up.
  - [ ] If agent tooling changes: `make skills-check`
- [ ] If the pilot establishes a meaningful quality or review gate, update
      `docs/evals/registry.yaml`.
- [ ] Search docs and update any that changed truth because of the chosen
      NotebookLM workflow.
- [ ] Verify project tenets:
  - [ ] Companion media remains tied to authoritative source packets.
  - [ ] Provenance is visible for every generated podcast.
  - [ ] AI usage reduces drudgery without becoming a hidden source of truth.
  - [ ] The workflow can be resumed after a long gap without relying on memory.

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

- **Owning module / area**: Companion-media workflow docs, source-packet
  packaging, and future podcast metadata surfaces.
- **Methodology reality**: `spec:1`, `spec:2`, `spec:3`, `spec:4`, and
  `spec:6` are `partial`, while `spec:8` remains `partial`; all relevant
  compromises are still in `climb` except `B1`, which remains in `hold`.
- **Substrate evidence**: Story 005 proved a real whole-book source slice and
  coverage rows for podcast surfaces exist, but there are no packet rules, no
  NotebookLM workflow docs, and no recorded outputs in the repo yet.
- **Data contracts / schemas**: This story should define packet boundaries,
  naming, prompt/provenance metadata, and output-recording rules rather than
  inventing per-run conventions.
- **File sizes**: `docs/RUNBOOK.md` (117), `docs/evals/registry.yaml` (6),
  `tests/fixtures/formats/_coverage-matrix.json` (60), packet/output docs TBD.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/input-contract.md`, `docs/evals/README.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, and `docs/RUNBOOK.md`. No
  repo-local ADRs or NotebookLM-specific runbooks exist yet.

## Files to Modify

- `tests/fixtures/formats/_coverage-matrix.json` — update podcast surface truth
  when whole-book and per-chapter outputs become real (60 lines)
- `docs/evals/registry.yaml` — record any baseline/pilot quality checks that
  become part of the workflow (6 lines)
- `docs/RUNBOOK.md` — add recurring human workflow steps if this becomes a
  maintained operational path (117 lines)
- Packet and output inventory docs/paths TBD once the storage shape is chosen

## Redundancy / Removal Targets

- Ad hoc NotebookLM notebook naming that is not anchored to whole-book or
  chapter identities.
- Separate manual packet notes if canonical source slices can generate the same
  inputs.
- One-off podcast link lists that are not tied back to source lineage.

## Notes

- No new story was created for the user's 2026-04-11 request because this is
  the same subsystem, validation boundary, and success surface as the existing
  NotebookLM podcast story; the honest move is to broaden this story's scope.
- The whole-book pilot should happen before per-chapter scaling unless the
  baseline proves that the broader corpus fails badly.
- The scoped output set now follows the machine-readable coverage truth and the
  active rollout: one whole-book podcast and one podcast per chapter where an
  episode exists.

## Plan

1. Establish what the authoritative whole-book corpus and per-chapter
   packets are.
2. Pilot the whole-book NotebookLM workflow with minimal tooling.
3. Lock naming, provenance, and storage rules.
4. Scale to one podcast per chapter and record the outputs for later site
   integration.

## Work Log

20260410-1243 — action: created story from inbox items 1 and 2, result:
captured the NotebookLM overall-plus-per-family podcast line as one workflow,
evidence: `docs/inbox.md` and coverage rows for podcast surfaces, next step:
measure the overall-corpus baseline before automating packet preparation.
20260411-1105 — action: clarified scope instead of minting a duplicate story,
result: broadened the story from a family-story aggregate podcast to a whole-
book podcast plus one per family story, evidence: user request in this thread
and existing Story 005 whole-book substrate, next step: keep the first pilot on
the whole-book corpus.
20260411-1119 — action: captured remaining scope decision, result: ruled out a
per-chapter podcast rollout for this story line, evidence: user direction in
this thread, next step: keep the packet model centered on the family-story run.
20260412-1600 — action: realigned the generation story with the current asset
rollout, result: renamed the story from family-story podcasts to chapter
podcasts because the first shipped companion episode targets `chapter-002` and
the coverage matrix already uses `chapter-podcasts`, evidence: user-provided
NotebookLM exports in `/Users/cam/Documents/Projects/onward-to-the-unknown-website/podcast/`
plus `tests/fixtures/formats/_coverage-matrix.json`, next step: keep the
workflow docs and output inventory centered on whole-book plus per-chapter
episodes.
