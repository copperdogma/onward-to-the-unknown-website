---
title: "NotebookLM Whole-Book And Chapter Video Companions"
status: "Draft"
priority: "Low"
ideal_refs:
  - "1. Canonical Book Experience"
  - "2. Connected Companion Media"
  - "4. Reusable Content Model"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "spec:8"
  - "C2"
  - "C3"
  - "C4"
  - "C5"
  - "C6"
  - "B1"
adr_refs: []
depends_on:
  - "story-002"
  - "story-005"
category_refs:
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "spec:8"
compromise_refs:
  - "C2"
  - "C3"
  - "C4"
  - "C5"
  - "C6"
  - "B1"
input_coverage_refs:
  - "book-core-html"
architecture_domains:
  - "content_model"
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "NotebookLM or comparable AI video-generation workflow over book text and images"
---

# Story 010 — NotebookLM Whole-Book And Chapter Video Companions

**Priority**: Low
**Status**: Draft
**Decision Refs**: `docs/RUNBOOK.md`, `docs/presentation-decisions.md`, `docs/evals/README.md`, `tests/fixtures/formats/_coverage-matrix.json`, none found after search for repo-local ADRs or video-workflow runbooks
**Depends On**: Stories 002 and 005

## Goal

Run a deliberately bounded experiment to see whether NotebookLM or another
approved thin external workflow can generate useful video companions for the
whole book and selected chapters, using authoritative text and book imagery
without losing provenance, so the project can decide whether video deserves to
become a maintained companion surface at all.

## Acceptance Criteria

- [ ] The repo records dated evidence about the current external capability:
      whether NotebookLM actually supports this video workflow now, or what
      alternative tool would be needed for the same experiment.
- [ ] A documented source-packet and image-selection workflow exists for one
      whole-book video pilot and one chapter-level pilot, with provenance and
      review rules.
- [ ] The repo records where pilot outputs, prompts, and metadata should live
      and what conditions would justify linking these videos on the site later,
      while keeping the lane explicitly experimental for now.

## Out of Scope

- Claiming NotebookLM video support exists before it is verified.
- A final public video gallery or polished site UI for videos.
- Producing one video for every chapter before the pilot proves the format is
  worth carrying.
- Treating video as a committed distribution lane before the experiment earns
  it.

## Approach Evaluation

- **Simplification baseline**: A single pilot made from existing whole-book or
  chapter assets may already show whether the format is useful, so test that
  before designing elaborate image-packet tooling.
- **AI-only**: Strong candidate for generation, but weak on source selection,
  prompt provenance, and image rights/lineage unless the workflow is wrapped in
  explicit review rules.
- **Hybrid**: Strongest fit. Reuse authoritative text and image packets from
  the repo, then use the external AI tool only for synthesis.
- **Pure code**: Not realistic for the synthesis itself; code only helps with
  packet prep, metadata, and repeatability.
- **Repo constraints / prior decisions**: There is no current video workflow,
  no video coverage row, and no public site surface for videos. The whole-book
  builder is still the only real website substrate, and the user has explicitly
  classified this lane as experimental for now.
- **Existing patterns to reuse**: Reuse whole-book and per-slice packet logic
  from Story 002 where it helps, plus the current whole-book site and coverage
  accounting patterns from Story 005.
- **Eval**: Verify current tool capability first, then compare one whole-book
  or chapter pilot for usefulness, review burden, and provenance clarity before
  considering broader rollout.

## Tasks

- [ ] Verify the current external capability from official product/docs
      surfaces and record dated evidence about whether NotebookLM supports this
      workflow now.
- [ ] Define the authoritative text and image packets for one whole-book pilot
      and one chapter-level pilot.
- [ ] Document naming, provenance, storage, and human-review rules for video
      outputs and prompts.
- [ ] Run a small pilot and review whether the resulting video is actually
      useful and respectful of the archive material.
- [ ] Record site-linking guidance and the threshold for graduating video from
      experiment to maintained companion surface.
- [ ] Update `tests/fixtures/formats/_coverage-matrix.json` and related docs if
      video becomes a tracked maintained surface.
- [ ] Check whether the chosen workflow makes any ad hoc media-prep notes or
      duplicate source packets redundant; remove them or create a concrete
      follow-up.
- [ ] Run required checks for touched scope:
  - [ ] `make methodology-compile`
  - [ ] `make methodology-check`
  - [ ] Manually inspect the pilot output and its source packets.
  - [ ] If agent tooling changes: `make skills-check`
- [ ] If the pilot establishes a meaningful quality or review gate, update
      `docs/evals/registry.yaml`.
- [ ] Search docs and update any that changed truth because of the chosen video
      workflow.
- [ ] Verify project tenets:
  - [ ] Video outputs remain tied to authoritative text and images.
  - [ ] Provenance is visible for every pilot.
  - [ ] The experiment reduces manual work without becoming a hidden source of
        truth.
  - [ ] The format proves real user value before large-scale rollout.

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

- **Owning module / area**: Companion-media workflow docs, packet preparation,
  and future video metadata surfaces.
- **Methodology reality**: `spec:2` through `spec:6` are `partial`, and
  `spec:8` remains `partial`; the repo has authoritative book content and a
  real site surface, but no verified video companion workflow.
- **Substrate evidence**: Story 005 proved a whole-book source slice and Story
  002 now defines the adjacent packet-oriented podcast line, but there are no
  current video coverage rows, no runbooks, and no output inventory paths in
  the repo yet.
- **Data contracts / schemas**: This story should define packet boundaries,
  prompt/output metadata, and graduation criteria before any schema is added to
  a site-facing companion-media contract.
- **File sizes**: `docs/RUNBOOK.md` (117), `docs/presentation-decisions.md`
  (96), `docs/evals/registry.yaml` (6),
  `tests/fixtures/formats/_coverage-matrix.json` (60).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/RUNBOOK.md`, `docs/presentation-decisions.md`, `docs/evals/README.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`, and
  `tests/fixtures/formats/_coverage-matrix.json`. No repo-local ADRs or
  video-workflow runbooks exist yet.

## Files to Modify

- `tests/fixtures/formats/_coverage-matrix.json` — add or graduate video
  companion coverage honestly if the experiment becomes a tracked surface
  (60 lines)
- `docs/evals/registry.yaml` — record any pilot quality/review gate that
  becomes part of the workflow (6 lines)
- `docs/RUNBOOK.md` — add recurring human workflow steps if the video lane
  becomes maintained (117 lines)
- `docs/presentation-decisions.md` — capture any accepted video-placement rule
  for the site if the pilots justify it (96 lines)

## Redundancy / Removal Targets

- Ad hoc video experiments that are not tied to authoritative source packets.
- Duplicate packet-prep rules that Story 002 or Story 005 already established.
- One-off video links with no provenance or retention rule.

## Notes

- This story stays `Draft` because the critical external capability is still
  unverified and there is no tracked repo surface for videos yet.
- The first task must verify the current product reality before anyone assumes
  NotebookLM can do this.
- This lane is intentionally low-priority and experimental until a pilot proves
  that it adds real value beyond the audio companions.

## Plan

1. Verify the current external capability and capture dated evidence.
2. Define the thinnest honest whole-book and chapter pilot packets.
3. Run a pilot and inspect whether the result is useful enough to keep.
4. Record the storage, provenance, and site-linking rules if the experiment
   survives.

## Work Log

20260411-1109 — action: created story from user request, result: captured
video companions as a distinct experiment with an explicit capability-verifying
first step, evidence: no current video workflow or coverage row exists in the
repo, next step: verify current external tool support before piloting.
20260411-1118 — action: incorporated user decisions, result: lowered the story
priority and made the experimental status explicit instead of leaving video
positioning ambiguous, evidence: user direction in this thread, next step:
keep video behind audio/distribution work until a pilot proves it is worth
carrying.
