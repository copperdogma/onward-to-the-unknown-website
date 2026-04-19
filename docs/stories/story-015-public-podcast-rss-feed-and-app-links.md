---
title: "Public Podcast RSS Feed And App Links"
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
**Status**: Done
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

- [x] `make build-family-site` emits one public podcast RSS XML file in the
      published output using repo-owned podcast metadata and enclosure URLs
      pointing at the site-hosted MP3 files, with stable channel categories,
      ASCII-safe public enclosure URLs, and item fields sufficient for later
      Apple Podcasts submission and Spotify claim.
- [x] The generated site exposes a clear older-reader `Podcast RSS Feed` action
      on the podcast surface, keeps website play/download as the default path,
      and supports optional `Listen in Apple Podcasts` and `Listen in Spotify`
      links only when repo-owned metadata explicitly provides those URLs.
- [x] Regression tests cover the podcast-manifest feed seam, generated RSS XML,
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

- [x] Measure the deterministic baseline: inspect whether the current
      `podcast/manifest.json` already contains enough feed-ready metadata and
      record the smallest schema expansion needed for stable RSS output and
      future optional Apple/Spotify links.
- [x] Extend the repo-owned podcast metadata and local family-site builder so
      `make build-family-site` emits one public RSS feed with stable show
      metadata, item metadata, Apple-safe category metadata, ASCII-safe public
      enclosure URLs, GUIDs, publish dates, and a repo-owned square show-cover
      artwork/reference path suitable for later manual directory submission.
- [x] Add a clear `Podcast RSS Feed` action to the generated podcast surface
      and optionally render `Listen in Apple Podcasts` or `Listen in Spotify`
      actions only when those URLs are present in repo-owned metadata.
- [x] Add or update regression tests for podcast feed generation, manifest
      validation, and rendered HTML link surfaces.
- [x] If this story changes documented format coverage or graduation reality:
      update `tests/fixtures/formats/_coverage-matrix.json` and any relevant
      methodology state honestly.
- [x] Check whether the chosen implementation makes any existing code, helper paths, or docs redundant; remove them or create a concrete follow-up
- [x] Run required checks for touched scope:
  - [x] Default Python checks: `make test`
  - [x] Default Python lint: `make lint`
  - [x] Rebuild the real site with `make build-family-site` and inspect the
        generated podcast page, RSS XML file, and a representative chapter page
  - [x] Methodology views: `make methodology-compile` and
        `make methodology-check`
- [x] If evals or goldens changed: not expected for this story
- [x] Search all docs and update any related to what we touched
- [x] Verify Central Tenets:
  - [x] T0 — Traceability: every feed item stays tied to a repo-owned MP3 file
        and its existing source reference in `podcast/manifest.json`
  - [x] T1 — AI-First: confirmed feed emission and app-link rendering are
        deterministic plumbing, not a job for a one-off LLM call
  - [x] T2 — Eval Before Build: baseline metadata gaps are measured before
        adding feed logic
  - [x] T3 — Fidelity: the story does not alter audio content; it only exposes
        existing files through a new public metadata surface
  - [x] T4 — Modular: RSS fields and optional platform links come from
        manifest-driven metadata, not hardcoded page or feed entries
  - [x] T5 — Inspect Artifacts: manually inspect the emitted RSS XML and the
        generated site handoff surface after the build

## Workflow Gates

- [x] Build complete: implementation finished, required checks run, and summary shared
- [x] Validation complete or explicitly skipped by user
- [x] Story marked done via `/mark-story-done`

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
  The site-hosted podcast surface remains canonical, and the repo now also
  emits one public RSS feed plus a metadata-driven podcast-page handoff for
  listeners who already use an app.
- **Substrate evidence**: `podcast/manifest.json` already maps the full-book
  episode and chapter episodes to repo-owned MP3 files; `modules/build_family_site.py`
  already emits `podcast.html`, `podcast/feed.xml`, repo-owned podcast assets,
  and page-level podcast panels; fresh local build output exists under
  `build/family-site/`; `docs/infrastructure.md` records that the DreamHost
  static deploy path can publish that XML feed beside the MP3 files.
- **Data contracts / schemas**: `podcast/manifest.json` now carries top-level
  feed metadata such as description, site URL, public contact email, artwork
  reference, feed path, Apple category values, and optional platform listing
  URLs, plus per-item publish dates and stable public audio output paths. Item
  summaries and GUIDs are derived deterministically from repo-owned metadata;
  no cross-repo schema or `schemas.py` surface exists today, so the contract
  remains repo-local and inspectable.
- **File sizes**: `modules/build_family_site.py` (4761 lines),
  `tests/test_build_family_site.py` (1748 lines), `podcast/manifest.json`
  (242 lines), `docs/presentation-decisions.md` (175 lines),
  `docs/infrastructure.md` (122 lines), `docs/RUNBOOK.md` (270 lines),
  `tests/fixtures/formats/_coverage-matrix.json` (60 lines), and
  `docs/stories/story-015-public-podcast-rss-feed-and-app-links.md`
  (436 lines). The builder and test files are already large, so prefer small,
  well-localized changes.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, `docs/scout/scout-003-audiobook-and-podcast-distribution-and-elder-friendly-listening.md`,
  `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`,
  Story 009, and Story 014. No repo-local ADRs or prior RSS implementation
  docs exist for this lane.

## Files to Modify

- `docs/stories/story-015-public-podcast-rss-feed-and-app-links.md` — story
  execution record and work log
- `podcast/manifest.json` — feed-ready show metadata, publish dates, category
  metadata, stable public audio paths, artwork reference path, and optional
  external-listing URLs (242 lines)
- `modules/build_family_site.py` — public podcast RSS XML emission and the
  on-site RSS/app-link handoff surface (4761 lines)
- `tests/test_build_family_site.py` — feed generation, manifest validation, and
  rendered listener handoff link coverage (1748 lines)
- `docs/presentation-decisions.md` — shipped site-canonical plus RSS handoff
  pattern (175 lines)
- `docs/infrastructure.md` — feed-output and hosting truth for the static
  deploy path (122 lines)
- `docs/RUNBOOK.md` — build inspection and manual submission handoff guidance
  for the feed (270 lines)
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

### Eval-First Gate

- **Success eval**: Extend the builder regression surface so a fixture-backed
  build emits one podcast RSS XML file, parse that XML in tests, and assert
  stable channel fields, item GUIDs, enclosure URLs, publish dates, and the
  older-reader `Podcast RSS Feed` action on `podcast.html`. Optional Apple
  Podcasts and Spotify links should render only when the manifest provides
  them.
- **Baseline now**: Fresh `make build-family-site` emits `podcast.html`,
  podcast MP3 files, and `_internal/podcast/manifest.json`, but no public RSS
  XML file. A direct grep of the built `podcast.html` found no RSS, Apple
  Podcasts, or Spotify handoff copy. `rg` across the builder, tests, and
  manifest found no existing feed-generation, enclosure, or GUID logic, so the
  baseline feed output and feed-specific regression count are both effectively
  zero.
- **Approach decision**: This remains deterministic plumbing, so pure code is
  still the right path. No AI comparison work is warranted beyond the existing
  story rationale.

### Task Plan

1. **Expand the podcast manifest contract** (`S`)
   - Files: `podcast/manifest.json`, `tests/test_build_family_site.py`
   - Add the smallest repo-owned metadata seam needed for one honest public
     feed: show description/subtitle text, canonical site/feed path inputs,
     public contact email, artwork/reference path, optional Apple/Spotify
     listing URLs, item summaries, publish dates, and stable GUID inputs.
   - Done looks like: the manifest can describe one public feed without any
     hardcoded site HTML or builder constants beyond predictable defaults.
2. **Emit the public RSS feed from the builder** (`M`)
   - Files: `modules/build_family_site.py`, `podcast/manifest.json`
   - Extend podcast loading/build output so the site build writes one public
     RSS XML file beside the existing podcast assets and uses site-hosted MP3
     URLs for enclosures. Reuse existing podcast asset-copy and render wiring
     instead of adding a parallel content path.
   - Done looks like: a local build produces one inspectable feed file with
     stable channel and item metadata derived from repo-owned inputs.
3. **Expose the listener handoff on the site** (`S`)
   - Files: `modules/build_family_site.py`, `tests/test_build_family_site.py`
   - Add a clear `Podcast RSS Feed` action on the podcast page while keeping
     browser play and direct MP3 download visually primary. Render Apple and
     Spotify buttons only when the manifest supplies those URLs.
   - Done looks like: the page helps podcast-app users without shifting the
     canonical listening path away from the website.
4. **Add regression coverage for XML and HTML seams** (`S`)
   - Files: `tests/test_build_family_site.py`
   - Extend the current fixture helpers and podcast-page tests to assert feed
     output, channel metadata, enclosure URLs, stable IDs, and conditional
     HTML action rendering.
   - Done looks like: the feed seam is locked down well enough that metadata or
     rendering regressions fail fast.
5. **Update repo truth surfaces** (`S`)
   - Files: `docs/presentation-decisions.md`, `docs/infrastructure.md`,
     `docs/RUNBOOK.md`, `tests/fixtures/formats/_coverage-matrix.json`,
     `docs/stories/story-015-public-podcast-rss-feed-and-app-links.md`
   - Move the public feed from planned to shipped reality if implementation
     succeeds, and document the manual follow-on lane for later Apple/Spotify
     submission without pretending those listings already exist.
   - Done looks like: docs and coverage surfaces describe the feed as a repo
     output and keep the site-first listening rule intact.

### Impact Analysis

- **Primary files likely to change**: `podcast/manifest.json`,
  `modules/build_family_site.py`, `tests/test_build_family_site.py`, and the
  related docs truth surfaces already named in this story.
- **Files at risk**: podcast page rendering, chapter-level podcast panels,
  public podcast asset paths, and any tests that assume the current manifest
  shape or current podcast page action set.
- **Expected checks**: `make test`, `make lint`, `make build-family-site`,
  `make methodology-compile`, and `make methodology-check`.
- **Coverage/state movement**: `chapter-podcasts` and `full-book-podcast`
  should remain the relevant rows, but their notes may need to reflect the feed
  as shipped repo-owned output rather than only on-site playback.

### Structural Health Notes

- `modules/build_family_site.py` and `tests/test_build_family_site.py` are
  already large, so the change should stay localized to the existing podcast
  load/copy/render path rather than introduce a new subsystem.
- No repo-local ADR currently governs this seam. The manifest-driven,
  repo-owned contract remains the right boundary for this implementation.
- No generalized site-base-URL config seam was found during exploration. If the
  builder needs one to emit honest absolute enclosure URLs, that is a small
  tightly coupled delta and should be absorbed here rather than deferred.

### Scope Adjustments Folded Into This Story

- Exploration confirmed one small, coherent scope delta that should stay inside
  this story: add an explicit repo-owned feed artwork/reference path rather
  than leaving artwork as an undocumented assumption.
- Optional Apple Podcasts and Spotify buttons are already in scope, but they
  should stay metadata-driven and absent by default until real listing URLs
  exist.

### Human-Approval Notes

- No blocker was found that makes the story unbuildable. The current substrate
  is sufficient, and the missing feed seam is bounded.
- The only likely content decision during implementation is whether an existing
  repo-owned image can honestly serve as feed artwork or whether a bounded
  derived asset/reference needs to be added.

## Work Log

20260418-2141 — action: created follow-up implementation story from Story 009,
result: captured the public podcast RSS feed as a separate buildable slice
instead of leaving it as an abstract recommendation, evidence: Scout 003
recommends one self-hosted feed while current repo output still has no RSS XML
or app-link handoff, next step: implement the feed and site handoff without
replacing the website as the canonical audio home.

20260418-2211 — action: completed Story 015 exploration and substrate check,
result: confirmed the story remains honestly buildable without new prerequisite
stories, evidence: reviewed `docs/ideal.md`, `docs/spec.md`,
`docs/methodology/state.yaml`, `docs/methodology/graph.json`,
`tests/fixtures/formats/_coverage-matrix.json`, Story 009, Story 014,
`docs/presentation-decisions.md`, `docs/infrastructure.md`, and `docs/RUNBOOK.md`;
searched `docs/decisions/` and found no repo-local ADR governing podcast RSS;
verified `podcast/manifest.json` already maps repo-owned MP3s, `modules/build_family_site.py`
already loads the podcast catalog and renders `podcast.html`, `make build-family-site`
freshly emitted the podcast page plus MP3 assets, and greps of the builder,
tests, manifest, and built `podcast.html` found no existing public feed XML,
RSS action, Apple Podcasts link, Spotify link, or feed-generation logic; reused
patterns identified in `write_fixture_podcast_manifest` and the existing
podcast-page assertions in `tests/test_build_family_site.py`, next step: wait
for human approval, then extend the manifest, builder, tests, and truth docs
in one implementation pass, including the small coherent delta of explicit
feed-art/reference metadata.

20260418-2249 — action: implemented the repo-owned podcast RSS lane and reader
handoff, result: `modules/build_family_site.py` now emits `podcast/feed.xml`
with stable channel and item metadata plus enclosure URLs, copies a repo-owned
feed-art image into the published payload, and renders a `Use a Podcast App`
panel with a `Podcast RSS Feed` action and metadata-driven Apple/Spotify links;
`podcast/manifest.json` now records the public feed metadata and per-item
publish dates; `tests/test_build_family_site.py` now parses fixture-backed feed
XML and verifies both presence and absence cases for platform buttons; docs and
coverage notes now describe the feed as a shipped repo output, evidence:
`make test`, `make lint`, `make build-family-site`, `make methodology-compile`,
and `make methodology-check` all passed; manual inspection confirmed
`build/family-site/podcast/feed.xml`, `build/family-site/podcast/feed-art.png`,
`build/family-site/podcast.html`, and representative chapter output still
render cleanly, next step: run `/validate` on Story 015 before closing it.

20260418-2308 — action: closed the Apple-compatibility gaps found in
validation, result: `podcast/manifest.json` now declares at least one
Apple-safe category plus stable ASCII public output paths for every published
podcast MP3, the builder validates and emits those fields into the real feed,
and the published chapter/podcast pages now reuse the same clean public paths
instead of leaking raw generator filenames, evidence: targeted podcast tests
pass with fixture source filenames that include spaces and apostrophes while
the emitted feed/channel uses `itunes:category`, `xmlns:content`, and clean
`podcast/tracks/*.mp3` URLs; a fresh `make build-family-site` emits
`build/family-site/podcast/feed.xml` with `Society &amp; Culture` and clean
enclosures such as `podcast/tracks/05-alma-marie-lheureux-alain.mp3`, next
step: rerun the full required checks and re-validate Story 015.

20260418-2332 — action: fixed the remaining Apple show-cover gap, result: the
repo now carries a square 3000x3000 `podcast/feed-art.png` asset, the manifest
points at that asset instead of the portrait book-page image, the builder now
rejects non-square or out-of-range show-cover artwork during podcast catalog
load, and regression tests cover both the valid square-art case and a
non-square rejection path, evidence: fresh `sips` inspection reported
`3000 x 3000` for `podcast/feed-art.png`; `make test`, `make lint`,
`make build-family-site`, `make methodology-compile`, and
`make methodology-check` all passed; the built feed now points at
`https://onward.copper-dog.com/podcast/feed-art.png`, next step: re-run
`/validate` and close Story 015 if no other submission-grade gaps remain.

20260418-2356 — action: completed fresh close-out validation and marked Story
015 done, result: the repo-owned podcast RSS feed now has current Apple-safe
category and show-cover metadata, stable ASCII enclosure URLs, a square
3000x3000 non-alpha feed-art asset, and the older-reader site handoff remains
intact; Story 015 status, workflow gates, generated story views, and changelog
can now reflect the shipped state, evidence: fresh `make test`, `make lint`,
`make build-family-site`, `make methodology-compile`, and
`make methodology-check` all passed; fresh `sips` inspection reported
`3000 x 3000` and `hasAlpha: no` for both `podcast/feed-art.png` and
`build/family-site/podcast/feed-art.png`; fresh artifact inspection confirmed
`build/family-site/podcast/feed.xml` includes `xmlns:content`,
`itunes:category text="Society &amp; Culture"`, and
`https://onward.copper-dog.com/podcast/feed-art.png`; current Apple support
docs for `Podcast RSS feed requirements`, `Show Cover`, and `Validate your
podcast RSS feed` still describe the relevant RSS, artwork, and validation
requirements, while current Spotify support docs confirm RSS email ownership
verification and later feed-link updates for claiming or host changes, next
step: `/check-in-diff`.

20260419-0007 — action: added a dedicated manual submission runbook, result:
the repo now has one concrete operator guide for getting the shipped podcast
feed onto Apple Podcasts and Spotify and then wiring the resulting listing URLs
back into `podcast/manifest.json`, evidence:
`docs/runbooks/podcast-apple-and-spotify-submission.md` now records the exact
public feed URL, Apple Podcasts Connect steps, Spotify for Creators claim
steps, email-verification fallback, and the follow-up rebuild/redeploy loop;
`docs/RUNBOOK.md` now points at that guide for account-side submission work,
next step: `/check-in-diff`.
