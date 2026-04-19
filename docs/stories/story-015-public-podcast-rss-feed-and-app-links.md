---
title: "Public Podcast RSS Feed And App Links"
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
  - "story-009"
  - "story-014"
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
  - "content_model"
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "site-hosted podcast pages with no public RSS feed, no platform-link handoff, and no repo-owned external subscription metadata"
---

# Story 015 — Public Podcast RSS Feed And App Links

**Priority**: Medium
**Status**: Pending
**Decision Refs**: `docs/scout.md`, `docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`, `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`, `tests/fixtures/formats/_coverage-matrix.json`, `docs/stories/story-009-audiobook-and-podcast-distribution-scout-and-elder-friendly-listening.md`, `docs/stories/story-014-first-on-site-podcast-listening-surface.md`, none found after search for repo-local ADRs or prior RSS implementation docs
**Depends On**: Stories 009 and 014

> If this story is `Blocked`, replace `N/A` in `Blocker Summary`, `Blocker
> Evidence`, and `Unblock Condition` with repo-backed truth, and make the
> visible `## Plan` describe the unblock path or blocker reassessment work
> instead of stale "proceed now" steps. Leave those sections as `N/A`
> otherwise.

## Goal

Emit one public podcast RSS feed from the repo-owned podcast metadata and
site-hosted MP3 files, then surface a plain-language listener handoff on the
website so relatives who already use podcast apps can add or follow the show
without replacing the website as the canonical audio home. The site must keep
"listen here" and direct MP3 download as the family-default path, while the
RSS feed and any future Apple Podcasts or Spotify links remain optional helper
lanes for people who already use those apps.

## Acceptance Criteria

- [ ] `make build-family-site` emits one public podcast RSS XML file in the
      published output using repo-owned podcast metadata and enclosure URLs
      pointing at the site-hosted MP3 files, with stable channel and item
      fields sufficient for later Apple Podcasts submission and Spotify claim.
- [ ] The generated site exposes a clear older-reader `Podcast RSS Feed` action
      on the podcast surface, keeps website play/download as the default path,
      and supports optional `Listen in Apple Podcasts` and `Listen in Spotify`
      links only when repo-owned metadata explicitly provides those URLs.
- [ ] Regression tests cover the podcast-manifest feed seam, generated RSS XML,
      and rendered HTML link surfaces, and the related docs plus coverage notes
      describe the feed as a shipped repo-owned output rather than a future
      idea.

## Out of Scope

- Actually submitting the feed to Apple Podcasts or claiming it on Spotify.
- Opening or managing external platform accounts, payment profiles, analytics,
  or listener metrics.
- Changing the audiobook distribution lane or adding an audiobook storefront.
- Building a custom podcast player, transcript pipeline, or audio-processing
  workflow beyond the current repo-owned MP3 set.

## Approach Evaluation

- **Simplification baseline**: The current site-hosted podcast page plus a
  visible RSS URL may already solve the real family-app handoff need without
  adding multi-feed or platform-specific complexity. First task should measure
  whether the current `podcast/manifest.json` already contains enough metadata
  to emit one honest public feed with only a small schema expansion.
- **AI-only**: Poor fit. RSS XML, enclosure URLs, stable GUIDs, and optional
  app-link rendering need deterministic build output and regression coverage.
- **Hybrid**: Low value for the core implementation. Human-curated metadata and
  deterministic rendering are simpler and more inspectable than LLM-generated
  feed content, though AI could help brainstorm copy later if needed.
- **Pure code**: Best likely fit. This is a bounded static-build and metadata
  extension on top of an already-shipped on-site podcast surface.
- **Repo constraints / prior decisions**: Scout 003 recommends one self-hosted
  podcast RSS feed as the only worthwhile first external duplicate and keeps
  the website canonical. `docs/infrastructure.md` already records that the
  DreamHost static deploy path can host the feed XML beside the current MP3
  files. No paid host, no listener charge, and no app requirement remain firm
  constraints.
- **Existing patterns to reuse**: Extend `podcast/manifest.json` and
  `modules/build_family_site.py`, reuse the existing podcast page and audio
  action patterns from Story 014, and keep external-link rendering driven by
  repo-owned metadata rather than hardcoded HTML.
- **Eval**: The winning implementation should pass a builder regression that
  parses the emitted feed XML, verifies enclosure URLs and stable metadata, and
  confirms the rendered podcast page exposes the RSS handoff without weakening
  the site-first listening path.

## Tasks

- [ ] Measure the deterministic baseline: inspect whether the current
      `podcast/manifest.json` already contains enough feed-ready metadata and
      record the smallest schema expansion needed for stable RSS output and
      future optional Apple/Spotify links.
- [ ] Extend the repo-owned podcast metadata and local family-site builder so
      `make build-family-site` emits one public RSS feed with stable show
      metadata, item metadata, enclosure URLs, GUIDs, publish dates, and a
      repo-owned artwork/reference path suitable for later manual directory
      submission.
- [ ] Add a clear `Podcast RSS Feed` action to the generated podcast surface
      and optionally render `Listen in Apple Podcasts` or `Listen in Spotify`
      actions only when those URLs are present in repo-owned metadata.
- [ ] Add or update regression tests for podcast feed generation, manifest
      validation, and rendered HTML link surfaces.
- [ ] If this story changes documented format coverage or graduation reality:
      update `tests/fixtures/formats/_coverage-matrix.json` and any relevant
      methodology state honestly.
- [ ] Check whether the chosen implementation makes any existing code, helper paths, or docs redundant; remove them or create a concrete follow-up
- [ ] Run required checks for touched scope:
  - [ ] Default Python checks: `make test`
  - [ ] Default Python lint: `make lint`
  - [ ] Rebuild the real site with `make build-family-site` and inspect the
        generated podcast page, RSS XML file, and a representative chapter page
  - [ ] Methodology views: `make methodology-compile` and
        `make methodology-check`
- [ ] If evals or goldens changed: not expected for this story
- [ ] Search all docs and update any related to what we touched
- [ ] Verify Central Tenets:
  - [ ] T0 — Traceability: every feed item stays tied to a repo-owned MP3 file
        and its existing source reference in `podcast/manifest.json`
  - [ ] T1 — AI-First: confirmed feed emission and app-link rendering are
        deterministic plumbing, not a job for a one-off LLM call
  - [ ] T2 — Eval Before Build: baseline metadata gaps are measured before
        adding feed logic
  - [ ] T3 — Fidelity: the story does not alter audio content; it only exposes
        existing files through a new public metadata surface
  - [ ] T4 — Modular: RSS fields and optional platform links come from
        manifest-driven metadata, not hardcoded page or feed entries
  - [ ] T5 — Inspect Artifacts: manually inspect the emitted RSS XML and the
        generated site handoff surface after the build

## Workflow Gates

- [ ] Build complete: implementation finished, required checks run, and summary shared
- [ ] Validation complete or explicitly skipped by user
- [ ] Story marked done via `/mark-story-done`

## Blocker Summary

N/A

## Blocker Evidence

N/A

## Unblock Condition

N/A

## Architectural Fit

- **Owning module / area**: Local whole-book static builder, repo-owned
  podcast metadata, public feed output, and podcast-page listener handoff UI.
- **Methodology reality**: `spec:3` through `spec:7` remain `partial`.
  `chapter-podcasts` and `full-book-podcast` are the relevant coverage rows.
  The site-hosted podcast surface already exists, but no public RSS feed or
  app-link handoff exists in repo output yet. This story adds that external
  duplicate seam while keeping the website canonical.
- **Substrate evidence**: `podcast/manifest.json` already maps the full-book
  episode and chapter episodes to repo-owned MP3 files; `modules/build_family_site.py`
  already emits `podcast.html` and page-level podcast panels; fresh local build
  output exists under `build/family-site/`; `docs/infrastructure.md` records
  that the DreamHost static deploy path can host a feed XML file beside the MP3
  files. `rg` found no current RSS or feed-generation logic in the builder or
  manifest beyond documentation references, so the missing seam is real.
- **Data contracts / schemas**: Likely expand `podcast/manifest.json` with
  top-level show metadata such as description, site URL, public contact email,
  artwork reference, and optional platform listing URLs, plus per-item publish
  dates, summaries, and stable GUID inputs. No cross-repo schema or `schemas.py`
  surface exists today; keep the contract repo-local and inspectable.
- **File sizes**: `modules/build_family_site.py` (4288 lines),
  `tests/test_build_family_site.py` (1485 lines), `podcast/manifest.json`
  (188 lines), `docs/presentation-decisions.md` (172 lines),
  `docs/infrastructure.md` (118 lines), `docs/RUNBOOK.md` (255 lines),
  `tests/fixtures/formats/_coverage-matrix.json` (60 lines), and
  `docs/stories/story-015-public-podcast-rss-feed-and-app-links.md`
  (281 lines). The builder and test files are already large, so prefer small,
  well-localized changes.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, `docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`,
  `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`,
  Story 009, and Story 014. No repo-local ADRs or prior RSS implementation
  docs exist for this lane.

## Files to Modify

- `docs/stories/story-015-public-podcast-rss-feed-and-app-links.md` — story
  execution record and work log (281 lines)
- `podcast/manifest.json` — add feed-ready show and item metadata plus
  optional external-listing URLs (188 lines)
- `modules/build_family_site.py` — emit public podcast RSS XML and render the
  on-site RSS/app-link handoff surface (4288 lines)
- `tests/test_build_family_site.py` — cover feed generation and rendered
  listener handoff links (1485 lines)
- `docs/presentation-decisions.md` — record the shipped site-canonical plus RSS
  handoff pattern (172 lines)
- `docs/infrastructure.md` — record feed-output and hosting truth for the
  static deploy path (118 lines)
- `docs/RUNBOOK.md` — capture build inspection and manual submission handoff
  guidance for the feed (255 lines)
- `tests/fixtures/formats/_coverage-matrix.json` — update podcast-surface notes
  if the feed ships as repo-owned output (60 lines)

## Redundancy / Removal Targets

- Any docs that still describe a public podcast RSS feed as purely future work
  after this story ships.
- Any duplicated helper copy that tells relatives to manually discover the feed
  URL outside the podcast surface when the site can expose it directly.
- Any hardcoded HTML path for external app buttons; platform links should come
  from repo-owned metadata or not render at all.

## Notes

- This is a new story rather than a reopen of Story 009 because Story 009
  validated the research and recommendation surface, while this story changes
  build output, metadata, and reader-facing site UI.
- Keep the website as the canonical audio home. The feed is an optional
  duplicate for listeners who already use podcast apps, not a replacement for
  browser play/download.
- If Apple Podcasts or Spotify listing URLs do not exist yet, the story should
  still succeed with a public feed URL and a repo-owned metadata seam for those
  future links rather than inventing fake platform buttons.
- Feed artwork may need to reuse an existing repo-owned image or add a bounded
  derived asset if no current file honestly fits Apple-compatible feed art
  requirements.

## Plan

1. Inspect the current podcast manifest and identify the minimum additional
   metadata needed for one honest public feed.
2. Extend the builder to emit that feed and expose a visible RSS handoff on the
   podcast surface without weakening the current site-first listening flow.
3. Add regression tests that parse the feed XML and verify the rendered HTML
   actions.
4. Update docs and coverage truth so the repo no longer treats the feed as a
   hypothetical future lane once it ships.

## Work Log

20260418-2141 — action: created follow-up implementation story from Story 009,
result: captured the public podcast RSS feed as a separate buildable slice
instead of leaving it as an abstract recommendation, evidence: Scout 003
recommends one self-hosted feed while current repo output still has no RSS XML
or app-link handoff, next step: implement the feed and site handoff without
replacing the website as the canonical audio home.
