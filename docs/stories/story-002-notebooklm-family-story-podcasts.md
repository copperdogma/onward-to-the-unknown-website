---
title: "NotebookLM Family-Story Podcasts"
status: "Draft"
priority: "Medium"
ideal_refs:
  - "2. Connected Companion Media"
  - "4. Reusable Content Model"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:6"
  - "spec:8"
  - "C2"
  - "C3"
  - "C4"
  - "C6"
  - "B1"
adr_refs: []
depends_on:
  - "story-001"
category_refs:
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:6"
  - "spec:8"
compromise_refs:
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

# Story 002 — NotebookLM Family-Story Podcasts

**Priority**: Medium
**Status**: Draft
**Decision Refs**: `docs/inbox.md`, `docs/evals/README.md`, `tests/fixtures/formats/_coverage-matrix.json`, none found after search for repo-local ADRs or NotebookLM runbooks
**Depends On**: Story 001 or equivalent canonical source-slice work

## Goal

Create a repeatable, provenance-aware NotebookLM workflow that can generate one
overall podcast about the family stories as a whole and one podcast per family
story from authoritative source packets, without turning the process into a set
of opaque one-off uploads.

## Acceptance Criteria

- [ ] A documented source-prep workflow exists for creating one overall
      NotebookLM podcast from authoritative staged or canonical source
      materials.
- [ ] Reliable per-family source packets are defined with naming, lineage, and
      review rules so one podcast can be generated for each family's story.
- [ ] The repo records where generated podcast outputs and metadata should live
      so the site can later link to them with inspectable provenance.

## Out of Scope

- Building the public website runtime itself.
- ElevenLabs audiobook production.
- Final audio hosting or player UI beyond the metadata needed for future site
  integration.

## Approach Evaluation

- **Simplification baseline**: A single NotebookLM upload may already be good
  enough for the overall podcast, so the first task should measure that before
  inventing elaborate prep tooling.
- **AI-only**: Viable for draft audio generation, but weak on repeatability,
  source packaging, and provenance unless the surrounding workflow is explicit.
- **Hybrid**: Strongest fit. Use canonical source packets, naming conventions,
  and lightweight docs/scripts around NotebookLM's generation surface.
- **Pure code**: Not realistic for the generation step because the core
  capability lives in an external AI product.
- **Repo constraints / prior decisions**: There is no existing NotebookLM
  workflow, no family-slice packaging rule, and no output inventory path in the
  repo yet. The content model and site slice work should shape the packet
  boundaries instead of every audio workflow inventing its own format.
- **Existing patterns to reuse**: Coverage rows already acknowledge chapter and
  full-book podcast surfaces. Story 001 should establish the authoritative
  source slices that this workflow reuses.
- **Eval**: Pilot the overall-corpus workflow and one family packet. Compare
  repeatability, source lineage, and manual review burden before scaling to the
  full set.

## Tasks

- [ ] Define how overall and per-family source packets will be derived from the
      staged source snapshot or canonical site data.
- [ ] Run a small baseline NotebookLM experiment on the overall corpus before
      building extra prep or packaging logic.
- [ ] Document naming, provenance, storage, and human-review rules for
      generated podcasts.
- [ ] Generate the overall podcast and one podcast per family story once the
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
- **Methodology reality**: `spec:2` and `spec:3` are `missing`, `spec:4` and
  `spec:6` are `partial`, and `spec:8` is `partial`; all relevant compromises
  are still in `climb` except `B1`, which is in `hold`.
- **Substrate evidence**: Coverage rows for podcast surfaces exist, but there
  are no family packets, no NotebookLM workflow docs, and no recorded outputs
  in the repo yet.
- **Data contracts / schemas**: This story should define packet boundaries,
  naming, provenance metadata, and output-recording rules rather than inventing
  per-run conventions.
- **File sizes**: `docs/RUNBOOK.md` (21), `docs/evals/registry.yaml` (6),
  `tests/fixtures/formats/_coverage-matrix.json` (60), packet/output docs TBD.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/evals/README.md`, `docs/methodology/state.yaml`,
  `docs/methodology/graph.json`, `tests/fixtures/formats/_coverage-matrix.json`,
  and `docs/inbox.md`. No repo-local ADRs or NotebookLM-specific runbooks
  exist yet.

## Files to Modify

- `tests/fixtures/formats/_coverage-matrix.json` — update podcast surface truth
  when overall/per-family outputs become real (60 lines)
- `docs/evals/registry.yaml` — record any baseline/pilot quality checks that
  become part of the workflow (6 lines)
- `docs/RUNBOOK.md` — add recurring human workflow steps if this becomes a
  maintained operational path (21 lines)
- Packet and output inventory docs/paths TBD once the storage shape is chosen

## Redundancy / Removal Targets

- Ad hoc NotebookLM notebook naming that is not anchored to family/story
  identities.
- Separate manual packet notes if canonical source slices can generate the same
  inputs.
- One-off podcast link lists that are not tied back to source lineage.

## Notes

- The overall podcast may be valuable before per-family slicing is complete, so
  the baseline should test that path first.
- Per-family podcasts should wait for authoritative family/story packet rules
  instead of relying on improvised manual selection each time.

## Plan

1. Establish what the authoritative overall corpus and per-family packets are.
2. Pilot the overall NotebookLM workflow with minimal tooling.
3. Lock naming, provenance, and storage rules.
4. Scale to one podcast per family story and record the outputs for later site
   integration.

## Work Log

20260410-1243 — action: created story from inbox items 1 and 2, result:
captured the NotebookLM overall-plus-per-family podcast line as one workflow,
evidence: `docs/inbox.md` and coverage rows for podcast surfaces, next step:
measure the overall-corpus baseline before automating packet preparation.
