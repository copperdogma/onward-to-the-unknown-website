---
title: "Audiobook And Podcast Distribution Scout And Elder-Friendly Listening"
status: "Done"
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
  - "chapter-podcasts"
  - "full-book-podcast"
architecture_domains:
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "manual audiobook and podcast link placement plus off-site audio-platform research"
---

# Story 009 — Audiobook And Podcast Distribution Scout And Elder-Friendly Listening

**Priority**: Medium
**Status**: Done
**Decision Refs**: `docs/scout.md`, `docs/scout/scout-002-audiobook-distribution-and-elder-friendly-listening.md`, `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`, `tests/fixtures/formats/_coverage-matrix.json`, `docs/stories/story-011-first-on-site-audiobook-listening-surface.md`, `docs/stories/story-014-first-on-site-podcast-listening-surface.md`, none found after search for repo-local ADRs or prior combined audio-distribution scout docs
**Depends On**: Stories 005 and 006

## Goal

Scout the current audiobook and podcast distribution options for this family
project, covering both the already-shipped on-site listening paths and any
off-site publishing or discovery lanes, so the repo has one date-stamped plan
for how a family member can easily find, play, download, or subscribe to the
audio using services they already know without charging anyone, adding paid
hosting, or forcing avoidable account friction.

## Acceptance Criteria

- [x] A dated scout report compares the current on-site audiobook and podcast
      listening patterns against off-site publishing or discovery lanes using
      current primary sources, limited to options that do not charge family
      listeners and do not require recurring hosting fees for this project.
- [x] The report identifies the top external services or apps family listeners
      may already use for podcasts or audiobooks, explains whether this project
      can realistically appear there under the no-fee constraint, and
      distinguishes true publishing lanes from optional duplicates or simple
      link targets.
- [x] The report recommends a first combined audio-distribution plan covering
      what should remain site-hosted, what external duplication is worth
      pursuing if any, what account setup is acceptable, what older-reader copy
      the site should use, and what metadata, feed, or packaging work a
      follow-on implementation story must own.

## Out of Scope

- Generating audiobook or podcast audio.
- Submitting to directories, publishing feeds, or opening platform accounts
  during this story.
- Implementing the final feed generator, external publishing lane, or richer
  site episode and track UI beyond the already-shipped simple on-site player
  surfaces.
- Paid monetization, commercial storefront strategy, or any plan that depends
  on family listeners buying access.

## Approach Evaluation

- **Simplification baseline**: The current site-hosted audiobook and podcast
  pages with large browser play/download actions may already be the best family
  listening lane, so use that as the comparison baseline instead of assuming an
  external app must win.
- **AI-only**: Weak fit. Feed rules, hosting constraints, and directory
  submission requirements need primary-source verification with dates.
- **Hybrid**: Useful for synthesizing or ranking the research after official
  docs are gathered, but not as the primary evidence source.
- **Pure code**: Not relevant for the scout itself beyond inspecting the
  current static-site constraints.
- **Repo constraints / prior decisions**: The repo has a static DreamHost
  deploy path, a whole-book reading surface, and first on-site audiobook and
  podcast player surfaces built from repo-owned MP3 assets, but it still has
  no external feed or directory substrate. The user has decided this lane is
  for family use with no charging and no paid hosting, while account setup is
  acceptable if it materially reduces listener friction.
- **Existing patterns to reuse**: Use the scout index, infrastructure truth,
  Story 008's dated audiobook scout, and the current whole-book audio surfaces.
  Stories 002 and 003 own generation, not distribution.
- **Eval**: The deciding proof is a dated scout document with cited lanes, an
  explicit yes/no fit matrix for the no-fee constraint, older-reader tradeoffs,
  and a bounded follow-up story or decision.

## Tasks

- [x] Rebuild the current site locally and inspect the generated audiobook,
      podcast, homepage, and representative chapter surfaces so the scout
      compares against fresh repo artifacts instead of stale assumptions.
- [x] Research current audiobook and podcast distribution options from official
      or primary sources and date-stamp the findings.
- [x] Compare the already-shipped on-site audiobook and podcast listening
      patterns for the current site, treating browser play/download as the
      baseline rather than assuming an external app is automatically better.
- [x] Identify the top consumer apps or services family listeners are most
      likely to already use, then classify each as a viable free publishing
      lane, viable optional duplicate, listener-only destination, or not
      compatible with the no-fee and no-charge constraint.
- [x] Evaluate whether any audiobook-specific lane is actually better than the
      current site-hosted MP3 flow for this audience, or whether the site plus
      podcast-style distribution already covers the honest need.
- [x] Recommend plain-language copy and interaction patterns that help an
      80+ relative choose between "listen here", "download", and "open in the
      app you already use."
- [x] Reject any lane that requires family listeners to buy access, create a
      paid subscription, or depends on the project taking on recurring hosting
      fees as the primary path.
- [x] Record required feed metadata, audio packaging assumptions, acceptable
      account-setup steps, and any blockers around public indexing or rights
      statements.
- [x] Add the dated scout report to `docs/scout/` and link it from
      `docs/scout.md`.
- [x] Update `docs/presentation-decisions.md`, `docs/infrastructure.md`, or
      `docs/RUNBOOK.md` if the research changes repo truth about likely audio
      delivery.
- [x] Check whether prior temporary notes or split audiobook/podcast scout
      assumptions become redundant; remove them or create a concrete follow-up.
- [x] Run required checks for touched scope:
  - [x] `make methodology-compile`
  - [x] `make methodology-check`
  - [x] Manually review the scout report for plain-language clarity aimed at
        older readers.
- [x] No new standing review gate was warranted for
      `docs/evals/registry.yaml`; leaving the eval registry unchanged is the
      honest outcome for this documentation-only scout.
- [x] Search docs and update any related to audiobook or podcast delivery and
      listening guidance.
- [x] Verify project tenets:
  - [x] Recommendations are grounded in current primary sources.
  - [x] Older-reader usability is explicit, not assumed.
  - [x] On-site and off-site lanes stay compatible with provenance-aware site
        linking.
  - [x] The next implementation slice can proceed without redoing the scout.

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

- **Owning module / area**: Scout documentation, listening-surface planning,
  and infrastructure-aware audio delivery guidance.
- **Methodology reality**: `spec:3` through `spec:7` are `partial`; the
  whole-book site plus the first on-site audiobook and podcast surfaces now
  exist, but no combined external audio lane has been chosen.
- **Substrate evidence**: `docs/infrastructure.md` documents a static DreamHost
  path, Story 011 adds the repo-owned audiobook manifest plus `audiobook.html`
  and page-level listening panels, Story 014 adds the repo-owned
  `podcast/manifest.json` plus `podcast.html` and page-level episode panels,
  and the coverage matrix now marks all four audio surfaces as `partial` with
  site-hosted MP3 delivery as the current recommended first lane. User
  direction in this thread narrows the target to family-first, no-charge
  delivery with no paid hosting fees, while account setup remains acceptable.
- **Data contracts / schemas**: The likely follow-on need is companion-media
  metadata for track and episode labels, feed URLs, platform references, and
  optional "open in app" links, but this story should only define the
  requirement matrix, not commit a schema.
- **File sizes**: `docs/scout.md` (10), `docs/presentation-decisions.md` (172),
  `docs/infrastructure.md` (118), `docs/RUNBOOK.md` (255),
  `docs/stories/story-011-first-on-site-audiobook-listening-surface.md` (405),
  `docs/stories/story-014-first-on-site-podcast-listening-surface.md` (385),
  and `tests/fixtures/formats/_coverage-matrix.json` (60).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, `docs/scout.md`, Story 008,
  Story 011, and Story 014. No repo-local ADRs or prior combined
  audio-distribution scout docs exist yet.

## Files to Modify

- `docs/stories/story-009-audiobook-and-podcast-distribution-scout-and-elder-friendly-listening.md`
  — maintain the combined research scope, work log, and status (444 lines)
- `docs/scout.md` — index the new expedition and keep its status visible
  (10 lines)
- `docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`
  — dated scout report with primary-source findings (286 lines)
- `docs/presentation-decisions.md` — record accepted audio-discovery
  recommendations if the scout settles them (172 lines)
- `docs/infrastructure.md` — note hosting or feed-delivery constraints if they
  affect the recommendation (118 lines)
- `docs/RUNBOOK.md` — capture any recurring operating guidance that becomes
  part of the plan (255 lines)

## Redundancy / Removal Targets

- Split assumptions that audiobook and podcast distribution must be researched
  as separate next-step stories when the user-facing decision is shared.
- Scattered notes about external audio delivery that are not anchored to a
  dated scout report.
- Assumptions that syndication is automatically the best experience for older
  family readers or listeners.
- Any plan that assumes family listeners should buy access or create paid
  accounts.
- Future player, feed, or app-platform ideas that are not tied to a concrete
  older-reader distribution plan.

## Notes

- Expanding the existing Story 009 is the honest move. Story 008 already
  records a dated audiobook-only scout, and the user explicitly asked for one
  combined next-step research story rather than a duplicate ID. This remains
  the same subsystem, validation boundary, and success surface.
- Story 011 and Story 014 now supply the on-site listening baseline this scout
  should evaluate against external feed, directory, or audiobook-platform
  options instead of inventing a hypothetical local player surface.
- Any recommendation that depends on current third-party hosting, directory, or
  platform rules must be date-stamped and sourced, because those surfaces
  change often.
- The decision boundary is now narrower: optimize for family access, no
  charging ever, no paid hosting fees, and the simplest browser, download, or
  familiar-app path before considering public-audience distribution norms.
- If no audiobook-specific platform honestly fits the constraints, the scout
  should say so plainly rather than manufacturing symmetry between audiobook
  and podcast distribution.

## Plan

### Eval-First Gate

- **Success eval**:
  - `docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`
    exists with dated primary-source citations and an explicit fit matrix for
    the no-charge and no-paid-hosting constraint.
  - The scout compares the current on-site audiobook and podcast surfaces
    against the strongest plausible external lanes instead of discussing
    hypothetical local UX.
  - `docs/scout.md`, `docs/presentation-decisions.md`,
    `docs/infrastructure.md`, and `docs/RUNBOOK.md` reflect one combined
    audio-distribution recommendation where warranted.
  - `make methodology-compile` and `make methodology-check` pass after the doc
    updates.
- **Baseline now**:
  - `python -m pytest tests/test_build_family_site.py -q` passes with `25`
    tests on 2026-04-18, confirming the audiobook/podcast build seams already
    exist.
  - `make build-family-site` rebuilt the current local surface on 2026-04-18
    and emitted `build/family-site/index.html`,
    `build/family-site/audiobook.html`, `build/family-site/podcast.html`,
    representative chapter pages, and
    `build/family-site/_internal/omission-audit.json`.
  - The new combined scout document is still missing, and no current truth doc
    yet mentions Scout 003 by name.
- **Candidate approaches**:
  - AI-only synthesis without browsing: reject because provider rules,
    directory requirements, and pricing/hosting terms are time-sensitive.
  - Hybrid primary-source research plus repo documentation updates: preferred.
    Use current official docs as evidence, then record the repo-facing
    recommendation and follow-up slice.
  - Pure code: not the solution. Code inspection only establishes the current
    on-site baseline.

### Task Plan

1. **Anchor the on-site baseline** — effort `S`
   - Files: `docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`
     (new), `docs/stories/story-009-audiobook-and-podcast-distribution-scout-and-elder-friendly-listening.md`
   - Use `audiobook/manifest.json`, `podcast/manifest.json`,
     `modules/build_family_site.py`, `docs/presentation-decisions.md`,
     `docs/infrastructure.md`, `docs/RUNBOOK.md`, and the rebuilt
     `build/family-site/` artifacts to capture what the repo already ships.
   - Done looks like: the scout states the real browser play/download baseline,
     the no-app/no-account path, and the fact that the website is already a
     viable family listening lane for both audio surfaces.

2. **Research current external audiobook and podcast lanes** — effort `M`
   - Files: `docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`
   - Use current primary sources only. Start with the highest-likelihood family
     destinations and publishing lanes: audiobook-specific options that can
     accept existing narrated files if any, plus major podcast ecosystems and
     the directories/apps older relatives are most likely to recognize.
   - Classify each option as one of: viable first lane, viable secondary
     duplicate, listener-only destination that still needs an RSS host, or not
     compatible with the project constraints.
   - Done looks like: the scout has a dated comparison table with clear yes/no
     reasoning on cost, hosting burden, account friction, and whether the lane
     preserves the repo-owned audio files.

3. **Write the combined recommendation and follow-up slice** — effort `S`
   - Files: `docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`,
     `docs/presentation-decisions.md`, `docs/infrastructure.md`,
     `docs/RUNBOOK.md`, `docs/scout.md`
   - Recommend what remains canonical on the site, what external duplication is
     worth pursuing if any, what plain-language copy should appear for older
     relatives, and what a later implementation story would need to own.
   - Done looks like: the repo has one combined recommendation, one list of
     required metadata/feed/packaging prerequisites, and an honest statement
     about whether audiobook-specific external distribution is actually worth
     the friction.

4. **Compile truth surfaces and verify** — effort `XS`
   - Files: touched docs above plus this story file
   - Run `make methodology-compile` and `make methodology-check`, then do a
     manual plain-language pass on the new scout.
   - Done looks like: generated story/index surfaces are fresh, the story work
     log captures the implementation evidence, and the story is ready for a
     later `/validate` pass without hidden context.

### Impact Analysis

- **Tests affected**: no product code change is planned; the relevant proof is
  documentation completeness plus methodology compile/check. The existing
  builder test pass is only a baseline substrate check.
- **What could break**: stale generated methodology artifacts, overclaiming a
  platform lane that does not meet the no-fee constraint, or drifting from the
  site-first family-access baseline already recorded in repo truth.
- **Expected coverage/state movement**: no coverage-matrix status change is
  expected because the repo already ships the on-site audio surfaces as
  `partial`. This story should refine recommendation truth, not claim a new
  runtime surface.

### Structural Health Notes

- This should stay a docs-only slice. If research starts demanding feed
  generators, schema changes, or platform account setup, that becomes a
  follow-on implementation story rather than silent scope creep here.
- `docs/scout/scout-002-audiobook-distribution-and-elder-friendly-listening.md`
  remains useful evidence, but this story may make some of its forward-looking
  assumptions redundant. Prefer superseding notes in current truth docs rather
  than editing history out of the prior scout.

### Scope Adjustments Discovered During Exploration

- Small expansion folded in: rebuild and inspect the current local audio
  surfaces as part of the scout baseline. The worktree did not already contain
  `build/family-site/`, so fresh local artifact proof is necessary to keep the
  comparison honest.
- No larger scope expansion is needed before implementation. The existing doc
  and build substrate is sufficient for the combined research slice.

### Human-Approval Blockers

- None discovered in repo substrate.
- If current official sources show that every realistic external lane requires
  paid hosting, pricing, or a commercial purchase flow, the honest output will
  be a stronger site-first recommendation rather than forcing an external plan.

## Work Log

20260411-1108 — action: created story from user request, result: captured the
podcast distribution scout as separate from NotebookLM podcast generation,
evidence: Story 002 already covers generation while the repo had no feed or
distribution guidance, next step: compare the simplest on-site family
listening flow against free off-site lanes.
20260411-1118 — action: incorporated early user decisions, result: narrowed
the scout toward family-first, no-charge delivery with simple browser access as
the evaluation baseline, evidence: user direction in that thread, next step:
keep external lanes optional unless they materially reduce listener friction.
20260418-2101 — action: broadened the pending story into a combined audiobook
and podcast distribution scout, result: kept one active research story for the
shared audio-consumption decision instead of minting a duplicate ID, evidence:
Story 008 already records the audiobook-only scout and the user requested one
combined next-step story, next step: produce a single dated scout report that
refreshes audiobook assumptions and evaluates podcast lanes against the same
no-fee, older-reader constraints.
20260418-2109 — exploration: verified the story is honestly buildable on the
current repo substrate and rewrote the plan around fresh local evidence,
result: confirmed `audiobook/manifest.json` and `podcast/manifest.json` are
real repo seams, `modules/build_family_site.py` publishes `audiobook.html`,
`podcast.html`, and page-level audio panels, `python -m pytest
tests/test_build_family_site.py -q` passed with `25` tests, and `make
build-family-site` freshly rebuilt the local surface plus omission audit on
this pass; also confirmed the new combined scout doc is still missing and no
repo-local ADRs apply, evidence: `docs/scout/scout-002-audiobook-distribution-and-elder-friendly-listening.md`,
`docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`,
Stories 005, 006, 008, 011, and 014, plus fresh build output under
`build/family-site/`, next step: run current official-source research for the
combined audio lanes, then update the scout and truth docs with one dated
recommendation.
20260418-2129 — implementation: completed the combined audio-distribution
scout and updated the repo truth surfaces around it, result: added
`docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`
with current official-source comparisons, kept the website as the canonical
audio home, recommended a self-hosted podcast RSS feed with Apple Podcasts
first and Spotify second as the only worthwhile first external duplicate, and
explicitly deprioritized audiobook-platform storefront work under the current
no-charge constraint; also updated `docs/scout.md`,
`docs/presentation-decisions.md`, `docs/infrastructure.md`, and
`docs/RUNBOOK.md`, evidence: fresh `make test`, `make lint`,
`make build-family-site`, `make methodology-compile`, and
`make methodology-check`, plus manual review of Scout 003 for older-reader
clarity, next step: run `/validate` on Story 009 and then decide whether to
open a follow-up implementation story for the public podcast RSS feed.
20260418-2141 — follow-up planning: created Story 015 for the public podcast
RSS feed and app-link implementation slice, result: the scout now hands off to
one concrete buildable story instead of leaving the RSS recommendation as only
an abstract next step, evidence:
`docs/stories/story-015-public-podcast-rss-feed-and-app-links.md`, next step:
finish validation and then close Story 009 honestly.
20260418-2201 — close-out: marked Story 009 done after fresh validation,
result: the combined audio-distribution scout is now closed with the website as
the canonical audiobook and podcast home, a self-hosted podcast RSS feed split
into Story 015 as the concrete follow-up, and no separate audiobook-platform
implementation required at this stage, evidence: fresh `python -m pytest
tests/`, `python -m ruff check modules/ tests/`, `make build-family-site`,
`make methodology-compile`, and `make methodology-check`, plus validated Scout
003 and Story 015 handoff, next step: `/check-in-diff`.
