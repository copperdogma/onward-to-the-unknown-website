---
title: "Podcast Distribution Scout And Elder-Friendly Listening"
status: "Pending"
priority: "Medium"
ideal_refs:
  - "2. Connected Companion Media"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:3"
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "spec:7"
  - "C3"
  - "C4"
  - "C5"
  - "C6"
  - "C7"
adr_refs: []
depends_on:
  - "story-005"
  - "story-006"
category_refs:
  - "spec:3"
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "spec:7"
compromise_refs:
  - "C3"
  - "C4"
  - "C5"
  - "C6"
  - "C7"
input_coverage_refs:
  - "chapter-podcasts"
  - "full-book-podcast"
architecture_domains:
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "manual podcast link placement plus off-site podcast-hosting and directory research"
---

# Story 009 — Podcast Distribution Scout And Elder-Friendly Listening

**Priority**: Medium
**Status**: Pending
**Decision Refs**: `docs/scout.md`, `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`, `tests/fixtures/formats/_coverage-matrix.json`, none found after search for repo-local ADRs or podcast-distribution scout docs
**Depends On**: Stories 005 and 006

## Goal

Scout the current podcast-distribution options for this family project,
covering both on-site listening paths and off-site podcast publishing lanes, so
the repo has a date-stamped plan for how a family member can easily find, play,
or subscribe to a whole-book podcast and any chapter podcast episodes
without paywalls, commercial friction, or avoidable account setup.

## Acceptance Criteria

- [ ] A dated scout report compares on-site podcast listening patterns and
      off-site hosting/directory lanes using current primary sources, limited
      to free or effectively no-cost options suitable for this family archive.
- [ ] The report recommends a first podcast distribution lane and a first site
      listening/discovery pattern, with explicit older-reader guidance and the
      asset, feed, or metadata requirements for each option.
- [ ] The repo records a clear follow-up implementation slice for feed hosting,
      external linking, or richer episode placement beyond the current on-site
      baseline without pretending the scout alone ships those surfaces.

## Out of Scope

- Generating the podcast audio itself.
- Submitting the show to directories or publishing a feed during this story.
- Implementing the final feed generator, off-site publishing lane, or richer
  site episode UI beyond the already-shipped simple on-site player surface.
- Paid podcast monetization or commercial audience-growth strategy.

## Approach Evaluation

- **Simplification baseline**: A clear on-site page with large play/download
  actions for a whole-book episode and a simple chapter episode list may
  already outperform more complex syndication for the intended audience, so use
  that as the comparison baseline.
- **AI-only**: Weak fit. Feed rules, hosting constraints, and directory
  submission requirements need primary-source verification with dates.
- **Hybrid**: Useful for synthesizing or ranking the research after official
  docs are gathered, but not as the primary evidence source.
- **Pure code**: Not relevant for the scout itself beyond inspecting the
  current static-site constraints.
- **Repo constraints / prior decisions**: The repo has a static deploy path, a
  whole-book reading surface, and a first on-site podcast player surface built
  from repo-owned MP3 assets, but it still has no current feed or external
  directory substrate. The user has decided this lane is for family use with
  no charging.
- **Existing patterns to reuse**: Use the scout index, infrastructure truth,
  and the current whole-book surface. Story 002 owns generation, not
  distribution.
- **Eval**: The deciding proof is a dated scout document with cited lanes,
  older-reader tradeoffs, and a bounded follow-up story or decision.

## Tasks

- [ ] Research current podcast hosting, feed, and directory options from
      official or primary sources and date-stamp the findings.
- [ ] Compare on-site podcast listening patterns for the current site,
      including large play/download actions, a whole-book podcast surface, and
      episode-level discovery for chapter podcasts.
- [ ] Evaluate off-site podcast lanes, including free or low-cost hosting,
      directory visibility, subscription friction, and how the site would link
      or explain those experiences to older readers without sending them into a
      purchase flow.
- [ ] Recommend plain-language copy and interaction patterns for podcast
      discovery, listening, and subscription.
- [ ] Reject any lane that requires charging family members or depends on a
      commercial storefront as the primary access path.
- [ ] Record required feed metadata, audio packaging assumptions, and any
      blockers around hosting or public indexing.
- [ ] Add the dated scout report to `docs/scout/` and link it from
      `docs/scout.md`.
- [ ] Update `docs/presentation-decisions.md`, `docs/infrastructure.md`, or
      `docs/RUNBOOK.md` if the research changes repo truth about likely podcast
      delivery.
- [ ] Check whether the chosen recommendation makes any temporary notes or
      assumptions redundant; remove them or create a concrete follow-up.
- [ ] Run required checks for touched scope:
  - [ ] `make methodology-compile`
  - [ ] `make methodology-check`
  - [ ] Manually review the scout report for plain-language clarity aimed at
        older readers.
- [ ] If the scout establishes a standing review gate for future podcast
      publishing, update `docs/evals/registry.yaml`.
- [ ] Search docs and update any related to podcast delivery or listening
      guidance.
- [ ] Verify project tenets:
  - [ ] Recommendations are grounded in current primary sources.
  - [ ] Older-reader usability is explicit, not assumed.
  - [ ] On-site and off-site lanes stay compatible with provenance-aware site
        linking.
  - [ ] The next implementation slice can proceed without redoing the scout.

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

- **Owning module / area**: Scout documentation, listening-surface planning,
  and infrastructure-aware podcast delivery guidance.
- **Methodology reality**: `spec:3` through `spec:7` are `partial`; the
  whole-book site and the first on-site podcast surface now exist, but no feed
  or external lane has been chosen.
- **Substrate evidence**: `docs/infrastructure.md` documents a static DreamHost
  path, Story 014 now adds a repo-owned `podcast/manifest.json` plus
  `podcast.html` and page-level episode panels, and the coverage matrix now
  marks chapter/full-book podcast surfaces as `partial`. User direction in this
  thread narrows the target to family-first, no-charge delivery.
- **Data contracts / schemas**: The likely follow-on need is companion-media
  metadata for episode labels, feed URLs, and off-site references, but this
  story should only define the requirement matrix, not implement the schema.
- **File sizes**: `docs/scout.md` (8), `docs/presentation-decisions.md` (96),
  `docs/infrastructure.md` (105), `docs/RUNBOOK.md` (117),
  `tests/fixtures/formats/_coverage-matrix.json` (60).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, and `docs/scout.md`. No
  repo-local ADRs or prior podcast-distribution scout docs exist yet.

## Files to Modify

- `docs/scout.md` — index the new expedition and keep its status visible
  (8 lines)
- `docs/scout/scout-003-podcast-distribution-and-elder-friendly-listening.md`
  — dated scout report with primary-source findings (new file)
- `docs/presentation-decisions.md` — record accepted on-site podcast discovery
  recommendations if the scout settles them (96 lines)
- `docs/infrastructure.md` — note hosting or feed-delivery constraints if they
  affect the recommendation (105 lines)
- `docs/RUNBOOK.md` — capture any recurring operating guidance that becomes
  part of the plan (117 lines)

## Redundancy / Removal Targets

- Scattered notes about podcast delivery that are not anchored to a dated scout
  report.
- Assumptions that syndication is automatically the best experience for older
  family readers/listeners.
- Any plan that assumes family listeners should buy access or create paid
  accounts.
- Future player/feed ideas that are not tied to a concrete distribution plan.

## Notes

- This is a new story rather than a reopen of Story 002 because generation and
  distribution are distinct validation boundaries. NotebookLM output can exist
  before the project decides where or how to publish it.
- Story 014 now supplies the on-site listening baseline this scout should
  evaluate against external feed or directory options, rather than inventing a
  hypothetical local player surface.
- Any recommendation that depends on current third-party hosting or directory
  rules must be date-stamped and sourced, because those surfaces change often.
- The decision boundary is now narrower: optimize for family access, no charge,
  and the simplest browser/play/download flow before considering public-audience
  podcast norms.

## Plan

1. Gather current official-source evidence for podcast hosting and discovery
   lanes.
2. Compare the simplest on-site listening pattern against off-site syndication.
3. Recommend the first lane and the site copy needed for older readers.
4. Record the follow-up build slice and any unresolved feed/hosting questions.

## Work Log

20260411-1108 — action: created story from user request, result: captured
podcast distribution as a separate scout from NotebookLM podcast generation,
evidence: Story 002 already covers generation while the repo has no feed or
podcast distribution guidance, next step: produce a dated scout report with a
clear first-lane recommendation.
20260411-1118 — action: incorporated user decisions, result: narrowed the
scout to family-first, no-charge podcast delivery with simple browser access as
the default evaluation frame, evidence: user direction in this thread, next
step: compare the simplest on-site family listening flow against free off-site
podcast lanes.
