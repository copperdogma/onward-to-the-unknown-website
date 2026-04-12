---
title: "Audiobook Distribution Scout And Elder-Friendly Listening"
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
architecture_domains:
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "manual audiobook link placement plus off-site audiobook platform research"
---

# Story 008 — Audiobook Distribution Scout And Elder-Friendly Listening

**Priority**: Medium
**Status**: Done
**Decision Refs**: `docs/scout.md`, `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`, `tests/fixtures/formats/_coverage-matrix.json`, none found after search for repo-local ADRs or audiobook-distribution scout docs
**Depends On**: Stories 005 and 006

## Goal

Scout the current audiobook-distribution options for this family project,
covering both on-site listening entry points and off-site publishing lanes, so
the repo has a date-stamped recommendation for the easiest elder-friendly way
to let family members listen to a page, listen to the whole book, and find or
download the audiobook without confusion, paywalls, or unnecessary accounts.

## Acceptance Criteria

- [x] A dated scout report compares on-site audiobook entry points and off-site
      audiobook distribution lanes using current primary sources, limited to
      free or effectively no-cost options that fit this family project.
- [x] The report recommends a first publishing lane and a first website
      listening pattern, with specific notes about how an 80+ reader would find
      it, what explanatory copy the site should use, and what metadata/assets
      each lane requires.
- [x] The repo records any follow-up implementation, hosting, or rights
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
  deploy path, a thin whole-book reading surface, and a first on-site
  audiobook page plus page-level listening panels. The remaining gap is the
  off-site lane decision and the dated primary-source comparison behind it.
  The user has decided this lane is for family use with no charging.
- **Existing patterns to reuse**: Use the scout index, infrastructure truth,
  and current whole-book surface as the planning substrate. Story 003 owns
  generation, not distribution.
- **Eval**: The decisive proof is a dated scout document with cited lanes,
  chosen recommendation, and a clear follow-up implementation slice.

## Tasks

- [x] Research current audiobook distribution options from official or primary
      sources and date-stamp the findings.
- [x] Compare on-site listening patterns for the current site, including a
      top-of-page "listen to this page" affordance, a whole-book listen entry
      point, and simple download/open options.
- [x] Evaluate off-site audiobook lanes, including free or low-cost options,
      onboarding friction, discoverability, and how the site would link family
      members into those experiences without pushing them through a purchase
      flow.
- [x] Recommend elder-friendly copy and interaction patterns for audiobook
      discovery on the site.
- [x] Reject any lane that requires charging family members or depends on a
      commercial storefront as the primary access path.
- [x] Record required metadata, file formats, hosting assumptions, and open
      rights or workflow questions for the recommended lane.
- [x] Add the dated scout report to `docs/scout/` and link it from
      `docs/scout.md`.
- [x] Update `docs/presentation-decisions.md`, `docs/infrastructure.md`, or
      `docs/RUNBOOK.md` if the research changes repo truth about likely
      audiobook delivery.
- [x] Check whether the chosen recommendation makes any temporary notes or
      assumptions redundant; remove them or create a concrete follow-up.
- [x] Run required checks for touched scope:
  - [x] `make methodology-compile`
  - [x] `make methodology-check`
  - [x] Manually review the scout report for plain-language clarity aimed at
        older readers.
- [x] No new standing review gate was warranted for `docs/evals/registry.yaml`;
      leaving the eval registry unchanged is the honest outcome for this
      documentation-only scout.
- [x] Search docs and update any related to audiobook delivery or listening
      guidance.
- [x] Verify project tenets:
  - [x] Recommendations are grounded in current primary sources.
  - [x] Older-reader usability is explicit, not implicit.
  - [x] On-site and off-site lanes preserve honest provenance and expectations.
  - [x] The next implementation slice can start without redoing the research.

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
  and infrastructure-aware delivery guidance.
- **Methodology reality**: `spec:3` through `spec:7` are `partial`; the
  whole-book site exists, the first on-site audiobook surfaces are now
  `partial`, and no off-site publishing lane has been chosen.
- **Substrate evidence**: `docs/infrastructure.md` documents a static DreamHost
  path, `docs/presentation-decisions.md` now records the first on-site
  audiobook pattern, and the coverage matrix now marks chapter/full-book
  audiobook surfaces as `partial`. User direction in this thread narrows the
  target to family-first, no-charge delivery.
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

### Eval-First Gate

- **Success eval**:
  - a dated scout report exists under `docs/scout/` with current primary-source
    citations for each compared lane
  - the report compares the real on-site listening surface already shipped in
    this repo against the strongest free or effectively no-cost off-site lanes
  - the report ends with one recommended first lane, one recommended on-site
    listening pattern, required metadata/assets, and explicit older-reader copy
    guidance
  - touched truth surfaces compile and check cleanly with
    `make methodology-compile` and `make methodology-check`
- **Baseline now**:
  - the repo has a real on-site audiobook surface through
    `audiobook/manifest.json`, `build/family-site/audiobook.html`, and
    chapter-level listening panels in `modules/build_family_site.py`
  - `docs/scout.md` has no audiobook-distribution scout entry yet
  - `tests/fixtures/formats/_coverage-matrix.json` still describes off-site
    audiobook distribution as unresolved future work
  - no repo-local ADR or eval entry currently captures the audiobook lane
    decision
- **Candidate approaches**:
  - AI-only synthesis without browsing: reject, because provider rules,
    pricing, and publish surfaces are time-sensitive and require primary-source
    verification
  - hybrid research + repo documentation update: preferred; use current vendor
    docs as evidence, then record the recommendation in repo truth surfaces
  - pure code: not the main solution; code inspection is only needed to
    confirm the current on-site listening substrate

### Task Plan

1. **Capture the scout evidence and recommendation** (`S`)
   - Files: `docs/scout/scout-002-audiobook-distribution-and-elder-friendly-listening.md`,
     `docs/scout.md`
   - Gather current primary-source evidence for the candidate lanes, including
     the shipped on-site browser/download flow and the external options that
     were already named in project notes.
   - Done looks like: one dated scout report compares lane friction, costs,
     account requirements, embeddability/linking, and family-reader fit, then
     recommends the first lane unambiguously.

2. **Refresh the project truth surfaces** (`XS`)
   - Files: `docs/presentation-decisions.md`, `docs/infrastructure.md`,
     `docs/RUNBOOK.md`
   - Record only the repo truths that the scout actually settles: likely the
     preferred first listening/discovery pattern, the preferred first publish
     lane, and any hosting or operator constraints that matter for later build
     work.
   - Done looks like: no core doc still implies that audiobook distribution is
     entirely undecided where this story now establishes a recommendation.

3. **Keep methodology and follow-up hooks honest** (`XS`)
   - Files: this story file, `docs/evals/registry.yaml` only if the scout
     defines a standing gate
   - Update the work log with exploration/implementation evidence, and only add
     an eval registry entry if the scout introduces a recurring verification
     rule that future stories should rerun.
   - Done looks like: the next story can build or reject the lane without
     repeating the research, and no fake eval completeness is added.

4. **Verify the touched scope** (`XS`)
   - Run: `make methodology-compile`, `make methodology-check`
   - Inspect: the new scout report for plain-language clarity and the updated
     truth docs for consistency with the shipped on-site audiobook surface
   - Done looks like: the repo compiles cleanly and the recommendation reads as
     a family-facing access plan rather than maintainer shorthand.

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
20260411-1828 — action: recorded related implementation progress, result:
Story 011 now owns the first on-site audiobook page and chapter-level listening
panels, evidence: repo-local `audiobook/manifest.json`, builder/test updates,
and coverage rows moving from `planned` to `partial`, next step: keep this
story focused on dated off-site distribution research and family-friendly link
copy instead of reopening the already-started on-site build slice.
20260412-1308 — exploration: verified Ideal/spec alignment against
`docs/ideal.md`, `docs/spec.md`, `docs/methodology/state.yaml`, and
`docs/methodology/graph.json`; no repo-local ADR applies. Read dependency
stories `story-005` and `story-006`, the current audiobook implementation in
`story-011`, coverage rows `chapter-audio` and `full-book-audio`, and the live
repo truth surfaces in `docs/presentation-decisions.md`,
`docs/infrastructure.md`, `docs/RUNBOOK.md`, `README.md`, and
`docs/runbooks/elevenlabs-audiobook.md`. Traced the actual on-site listening
substrate through `modules/build_family_site.py`, `audiobook/manifest.json`,
and the existing audiobook build commands; confirmed the story is buildable,
not blocked, because the on-site browser/download flow is already real and the
remaining gap is dated primary-source comparison plus recommendation capture.
Files likely to change: the new scout report, `docs/scout.md`, and whichever of
the presentation/infrastructure/runbook docs the research materially settles.
Files at risk are documentation-only; no code or schema change is currently
required. Next step: present the plan for approval, then perform the research
and truth-surface updates.
20260412-1517 — implementation: completed the dated scout and truth-surface
refresh for audiobook delivery. Added
`docs/scout/scout-002-audiobook-distribution-and-elder-friendly-listening.md`
and indexed it from `docs/scout.md`; updated
`docs/presentation-decisions.md`, `docs/infrastructure.md`, and
`docs/RUNBOOK.md` to record the settled recommendation that the site-hosted
MP3 flow is the first family listening lane and that external platforms remain
secondary duplicates at most. Primary-source evidence gathered in this pass:
ElevenReader Publishing is free but does not accept external audio uploads and
generates narration on demand inside the product; Spotify direct upload is
free, non-exclusive, and supports ElevenLabs digital voice narration but adds
purchase/account/app friction; Voices by INaudio is a retail/library
distribution path with pricing, payout, and go-live overhead; Audio Native and
ElevenLabs Video do not solve this story's distribution problem. Verification
in this pass: `make methodology-compile`, `make methodology-check`, and manual
review of the new scout for plain-language clarity. `docs/evals/registry.yaml`
was intentionally left unchanged because this story did not create a recurring
measured gate. Next step: `/validate`.
20260412-1534 — validation repair: aligned
`tests/fixtures/formats/_coverage-matrix.json` with the newly landed scout so
the canonical planning truth no longer says the audiobook distribution lane is
unresolved after this story's recommendation. Fresh verification in this pass:
`make methodology-compile`, `make methodology-check`, and `git diff --check`.
Result: generated methodology views now match the updated audiobook lane
recommendation, the story's validation gate is complete, and the only
remaining close-out step is `/mark-story-done`.
20260412-1540 — close-out: marked Story 008 done after fresh completion
evidence confirmed the scout, truth-surface updates, and validation suite on
the current tip. Close-out verification in this pass: `python -m pytest tests/`
(`39 passed`), `python -m ruff check modules/ tests/`, `make methodology-compile`,
`make methodology-check`, and `git diff --check`. Result: the story status,
workflow gates, coverage-matrix truth, generated methodology views, and
changelog are now aligned with the shipped audiobook-distribution recommendation.
Next step: `/check-in-diff`.
