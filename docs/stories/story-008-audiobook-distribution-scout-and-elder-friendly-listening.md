---
title: "Audiobook Distribution Scout And Elder-Friendly Listening"
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
  - "chapter-audio"
  - "full-book-audio"
architecture_domains:
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "manual audiobook link placement plus off-site audiobook platform research"
---

# Story 008 — Audiobook Distribution Scout And Elder-Friendly Listening

**Priority**: Medium
**Status**: Pending
**Decision Refs**: `docs/scout.md`, `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`, `tests/fixtures/formats/_coverage-matrix.json`, none found after search for repo-local ADRs or audiobook-distribution scout docs
**Depends On**: Stories 005 and 006

## Goal

Scout the current audiobook-distribution options for this family project,
covering both on-site listening entry points and off-site publishing lanes, so
the repo has a date-stamped recommendation for the easiest elder-friendly way
to let family members listen to a page, listen to the whole book, and find or
download the audiobook without confusion, paywalls, or unnecessary accounts.

## Acceptance Criteria

- [ ] A dated scout report compares on-site audiobook entry points and off-site
      audiobook distribution lanes using current primary sources, limited to
      free or effectively no-cost options that fit this family project.
- [ ] The report recommends a first publishing lane and a first website
      listening pattern, with specific notes about how an 80+ reader would find
      it, what explanatory copy the site should use, and what metadata/assets
      each lane requires.
- [ ] The repo records any follow-up implementation, hosting, or rights
      questions clearly enough that the next story can build or reject the plan
      without redoing the entire scout from scratch.

## Out of Scope

- Generating the audiobook itself.
- Publishing to any external audiobook service during this story.
- Paid storefront or subscription strategies.
- Implementing the final player UI or whole-book listening surface in code.

## Approach Evaluation

- **Simplification baseline**: A clear on-site whole-book download or browser
  stream with large explanatory copy may already solve most family access
  needs, so compare that against heavier off-site distribution before assuming
  a platform is required.
- **AI-only**: Weak fit. Provider policies, feed requirements, and current
  pricing or free-tier rules need primary-source verification and timestamps.
- **Hybrid**: Useful for synthesizing findings after official-doc research, but
  the source of truth must stay in dated scout notes with links to current
  vendor docs.
- **Pure code**: Not relevant for the scout itself except to inspect current
  site constraints.
- **Repo constraints / prior decisions**: The repo has a static DreamHost
  deploy path, a thin whole-book reading surface, and no audio player or
  distribution runbook yet. Presentation decisions explicitly defer audio
  companion embeds, and the user has decided this lane is for family use with
  no charging.
- **Existing patterns to reuse**: Use the scout index, infrastructure truth,
  and current whole-book surface as the planning substrate. Story 003 owns
  generation, not distribution.
- **Eval**: The decisive proof is a dated scout document with cited lanes,
  chosen recommendation, and a clear follow-up implementation slice.

## Tasks

- [ ] Research current audiobook distribution options from official or primary
      sources and date-stamp the findings.
- [ ] Compare on-site listening patterns for the current site, including a
      top-of-page "listen to this page" affordance, a whole-book listen entry
      point, and simple download/open options.
- [ ] Evaluate off-site audiobook lanes, including free or low-cost options,
      onboarding friction, discoverability, and how the site would link family
      members into those experiences without pushing them through a purchase
      flow.
- [ ] Recommend elder-friendly copy and interaction patterns for audiobook
      discovery on the site.
- [ ] Reject any lane that requires charging family members or depends on a
      commercial storefront as the primary access path.
- [ ] Record required metadata, file formats, hosting assumptions, and open
      rights or workflow questions for the recommended lane.
- [ ] Add the dated scout report to `docs/scout/` and link it from
      `docs/scout.md`.
- [ ] Update `docs/presentation-decisions.md`, `docs/infrastructure.md`, or
      `docs/RUNBOOK.md` if the research changes repo truth about likely
      audiobook delivery.
- [ ] Check whether the chosen recommendation makes any temporary notes or
      assumptions redundant; remove them or create a concrete follow-up.
- [ ] Run required checks for touched scope:
  - [ ] `make methodology-compile`
  - [ ] `make methodology-check`
  - [ ] Manually review the scout report for plain-language clarity aimed at
        older readers.
- [ ] If the scout defines a standing review gate or acceptance criterion for
      future audio publishing, update `docs/evals/registry.yaml`.
- [ ] Search docs and update any related to audiobook delivery or listening
      guidance.
- [ ] Verify project tenets:
  - [ ] Recommendations are grounded in current primary sources.
  - [ ] Older-reader usability is explicit, not implicit.
  - [ ] On-site and off-site lanes preserve honest provenance and expectations.
  - [ ] The next implementation slice can start without redoing the research.

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
  and infrastructure-aware delivery guidance.
- **Methodology reality**: `spec:3` through `spec:7` are `partial`; the
  whole-book site exists, but audiobook surfaces remain `planned` and no
  publishing lane has been chosen.
- **Substrate evidence**: `docs/infrastructure.md` documents a static DreamHost
  path, `docs/presentation-decisions.md` explicitly defers audio embeds, and
  the coverage matrix still marks chapter/full-book audiobook surfaces as
  planned. User direction in this thread narrows the target to family-first,
  no-charge delivery.
- **Data contracts / schemas**: The likely follow-on need is companion-media
  metadata for player labels, download links, and off-site references, but this
  story should only define the requirement matrix, not commit a schema yet.
- **File sizes**: `docs/scout.md` (8), `docs/presentation-decisions.md` (96),
  `docs/infrastructure.md` (105), `docs/RUNBOOK.md` (117),
  `tests/fixtures/formats/_coverage-matrix.json` (60).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, and `docs/scout.md`. No
  repo-local ADRs or prior audiobook-distribution scout docs exist yet.

## Files to Modify

- `docs/scout.md` — index the new expedition and keep its status visible
  (8 lines)
- `docs/scout/scout-002-audiobook-distribution-and-elder-friendly-listening.md`
  — dated scout report with primary-source findings (new file)
- `docs/presentation-decisions.md` — record accepted on-site listening-entry
  recommendations if the scout settles them (96 lines)
- `docs/infrastructure.md` — note hosting or delivery constraints if they
  affect the recommendation (105 lines)
- `docs/RUNBOOK.md` — capture any recurring operating guidance that becomes
  part of the plan (117 lines)

## Redundancy / Removal Targets

- Scattered notes about audiobook delivery that are not anchored to a dated
  scout report.
- Assumptions that an external audiobook platform is automatically better than
  a clear on-site listening surface.
- Any plan that assumes family listeners should buy access or create paid
  accounts.
- Unexplained future UI ideas that are not tied to older-reader needs.

## Notes

- This is a new story rather than a reopen of Story 003 because generation and
  distribution are distinct validation boundaries. Story 003 can succeed while
  distribution remains unresolved.
- Any recommendation that depends on current third-party platform rules must be
  date-stamped and sourced, because that market changes too often to rely on
  memory.
- The decision boundary is now narrower: optimize for family access, no charge,
  and the simplest browser/download flow before considering audiobook-market
  norms.
- User-provided ElevenReader publish UI evidence in this thread shows these
  built-in lanes to validate during the scout: ElevenReader, Spotify, InAudio,
  ElevenLabs Video, and Audio Native. Treat that list as candidate distribution
  surfaces, not as confirmed current policy or final recommendations until
  primary-source research is recorded.

## Plan

1. Gather current official-source evidence for audiobook lanes.
2. Compare the simplest on-site listening pattern against off-site platforms.
3. Recommend the first lane and the site copy needed for older readers.
4. Record the follow-up build slice and any unresolved constraints.

## Work Log

20260411-1108 — action: created story from user request, result: captured
audiobook distribution as a separate scout from audiobook generation, evidence:
Story 003 already covers generation while `docs/presentation-decisions.md`
still defers audio surfaces, next step: produce a dated scout report with a
clear first-lane recommendation.
20260411-1118 — action: incorporated user decisions, result: narrowed the
scout to family-first, no-charge delivery with browser/download simplicity as
the default evaluation frame, evidence: user direction in this thread, next
step: compare the simplest on-site family listening flow against free off-site
lanes.
