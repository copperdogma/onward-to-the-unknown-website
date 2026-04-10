---
title: "ElevenLabs Full Audiobook"
status: "Draft"
priority: "Medium"
ideal_refs:
  - "2. Connected Companion Media"
  - "4. Reusable Content Model"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:2"
  - "spec:4"
  - "spec:6"
  - "spec:8"
  - "C2"
  - "C4"
  - "C6"
  - "B1"
adr_refs: []
depends_on:
  - "story-001"
category_refs:
  - "spec:2"
  - "spec:4"
  - "spec:6"
  - "spec:8"
compromise_refs:
  - "C2"
  - "C4"
  - "C6"
  - "B1"
input_coverage_refs:
  - "book-core-html"
  - "chapter-audio"
  - "full-book-audio"
architecture_domains:
  - "content_model"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "ElevenLabs audiobook workflow over authoritative book text"
---

# Story 003 — ElevenLabs Full Audiobook

**Priority**: Medium
**Status**: Draft
**Decision Refs**: `docs/inbox.md`, `docs/evals/README.md`, `tests/fixtures/formats/_coverage-matrix.json`, none found after search for repo-local ADRs or audiobook runbooks
**Depends On**: Story 001 or equivalent authoritative text/canonicalization work

## Goal

Produce a repeatable full-book audiobook workflow using ElevenLabs from the
authoritative book text, with documented chapter boundaries, voice/settings
choices, and provenance so the resulting audio can be linked as first-class
companion media rather than treated as a detached side project.

## Acceptance Criteria

- [ ] The authoritative audiobook-ready text and chapter boundaries are defined
      from the staged or canonical source material.
- [ ] The ElevenLabs workflow is documented well enough to rerun, including the
      chosen voice/model settings, chunking strategy, and any manual review
      steps.
- [ ] The repo records where the resulting audiobook assets and metadata live so
      the site can later publish them with inspectable lineage.

## Out of Scope

- NotebookLM podcast generation.
- Final site player UI beyond the metadata needed for future linking.
- Studio-quality mastering or post-production beyond the first honest pass.

## Approach Evaluation

- **Simplification baseline**: A single-chapter ElevenLabs pilot may already be
  sufficient to judge voice quality, pacing, and cost before any chunking or
  helper tooling is built.
- **AI-only**: Strong for the synthesis step itself, but weak on authoritative
  text prep, chapter boundaries, and output provenance unless the workflow is
  documented around it.
- **Hybrid**: Strongest fit. Use explicit text preparation and metadata rules,
  then rely on ElevenLabs for the actual audio generation.
- **Pure code**: Not sufficient because the core synthesis capability is
  external; code only helps with chunking, metadata, and repeatability.
- **Repo constraints / prior decisions**: There is no verified audiobook-ready
  text export, no chosen voice/settings, and no runbook for storing or linking
  the outputs yet.
- **Existing patterns to reuse**: Coverage rows already acknowledge chapter and
  full-book audio surfaces. Story 001 should establish the authoritative text
  and chapter structure this workflow consumes.
- **Eval**: Pilot one chapter first. Compare quality, review burden, chapter
  boundary handling, and cost before running the full book.

## Tasks

- [ ] Extract and verify the authoritative full-book text and chapter
      boundaries from the staged source snapshot or canonical site data.
- [ ] Run a one-chapter ElevenLabs baseline to measure voice quality, pacing,
      cost, and workflow friction.
- [ ] Decide whether the maintained output shape should be chapter files, a
      full-book file, or both, and document the naming/provenance rules.
- [ ] Generate the audiobook assets once text prep and baseline review are
      complete.
- [ ] Record links and metadata for the resulting audio so the site can publish
      it as companion media later.
- [ ] Update `tests/fixtures/formats/_coverage-matrix.json` and related docs if
      audiobook surfaces move from planned to real.
- [ ] Remove or avoid temporary copied text files if canonical chapter data can
      drive the workflow directly.
- [ ] Run required checks for touched scope:
  - [ ] `make methodology-compile`
  - [ ] `make methodology-check`
  - [ ] Manually review the prepared text for at least one pilot chapter.
  - [ ] Manually listen to the pilot output before scaling up.
  - [ ] If agent tooling changes: `make skills-check`
- [ ] If the pilot establishes a meaningful quality or review gate, update
      `docs/evals/registry.yaml`.
- [ ] Search docs and update any that changed truth because of the chosen
      ElevenLabs workflow.
- [ ] Verify project tenets:
  - [ ] Audiobook outputs remain tied to authoritative book text.
  - [ ] Chapter boundaries and filenames are inspectable and repeatable.
  - [ ] AI usage reduces manual narration work without hiding workflow truth.
  - [ ] The workflow can be resumed after a long gap from repo docs alone.

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

- **Owning module / area**: Audiobook source prep, metadata rules, and future
  audio companion publishing surfaces.
- **Methodology reality**: `spec:2` is `missing`, `spec:4` and `spec:6` are
  `partial`, and `spec:8` is `partial`; `C2`, `C4`, and `C6` remain in
  `climb`, while `B1` remains in `hold`.
- **Substrate evidence**: Coverage rows for chapter and full-book audio exist,
  but there is no canonical audiobook-ready text export, no ElevenLabs workflow
  doc, and no audio output inventory in the repo yet.
- **Data contracts / schemas**: This story should define the text-export,
  chapter-boundary, naming, and provenance rules needed to generate audiobook
  assets repeatably.
- **File sizes**: `docs/RUNBOOK.md` (21), `docs/evals/registry.yaml` (6),
  `tests/fixtures/formats/_coverage-matrix.json` (60), output inventory docs
  TBD once the storage shape is chosen.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/evals/README.md`, `docs/methodology/state.yaml`,
  `docs/methodology/graph.json`, `tests/fixtures/formats/_coverage-matrix.json`,
  and `docs/inbox.md`. No repo-local ADRs or audiobook-specific runbooks exist
  yet.

## Files to Modify

- `tests/fixtures/formats/_coverage-matrix.json` — update audio surface truth
  when chapter/full-book audiobook outputs become real (60 lines)
- `docs/evals/registry.yaml` — record any baseline/pilot quality checks that
  become part of the workflow (6 lines)
- `docs/RUNBOOK.md` — add recurring audiobook workflow steps if this becomes a
  maintained operational path (21 lines)
- Text-prep and output inventory docs/paths TBD once the workflow shape is
  chosen

## Redundancy / Removal Targets

- Temporary copied text exports that drift from the authoritative source.
- Manual filename conventions that are not anchored to chapter identity.
- One-off audiobook link lists that are not tied back to the source text and
  generation settings.

## Notes

- A one-chapter pilot should happen before any full-book run to avoid paying
  full-run cost on a bad voice or chunking strategy.
- This story should reuse the canonical text shape from Story 001 rather than
  fork a second text-prep pipeline unless the evidence says that is necessary.

## Plan

1. Establish the authoritative text and chapter-boundary export the audiobook
   will consume.
2. Pilot one chapter in ElevenLabs and review the result.
3. Lock the output shape, naming, and provenance rules.
4. Scale to the full audiobook and record the resulting assets for later site
   integration.

## Work Log

20260410-1243 — action: created story from inbox item 3, result: captured the
ElevenLabs audiobook line as a separate workflow with shared upstream
dependencies, evidence: `docs/inbox.md` and audio coverage rows, next step:
pilot one chapter before committing to a full-book generation path.
