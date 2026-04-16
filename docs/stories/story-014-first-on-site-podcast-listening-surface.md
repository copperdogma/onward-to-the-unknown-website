---
title: "First On-Site Podcast Listening Surface"
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
  - "chapter-podcasts"
  - "full-book-podcast"
architecture_domains:
  - "content_model"
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "no on-site podcast surface; NotebookLM exports exist outside the current site build output"
---

# Story 014 — First On-Site Podcast Listening Surface

**Priority**: Medium
**Status**: Done
**Decision Refs**: `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`, `tests/fixtures/formats/_coverage-matrix.json`, `docs/stories/story-002-notebooklm-family-story-podcasts.md`, `docs/stories/story-009-podcast-distribution-scout-and-elder-friendly-listening.md`, `docs/stories/story-011-first-on-site-audiobook-listening-surface.md`, none found after search for repo-local ADRs or prior on-site podcast implementation docs
**Depends On**: Stories 005 and 006

> If this story is `Blocked`, replace `N/A` in `Blocker Summary`, `Blocker
> Evidence`, and `Unblock Condition` with repo-backed truth, and make the
> visible `## Plan` describe the unblock path or blocker reassessment work
> instead of stale "proceed now" steps. Leave those sections as `N/A`
> otherwise.

## Goal

Ship the first honest on-site podcast surface for the current static reading
site by converting the first two NotebookLM `.m4a` exports into repo-owned
`.mp3` assets, recording them in an inspectable podcast manifest, adding a
dedicated whole-book podcast page, and surfacing a simple native-player
"listen to this episode" panel on any chapter with a matching companion
episode. The homepage should also gain a clearer top-level `Book`,
`Audiobook`, and `Podcast` split so the three family listening and reading
lanes are obvious.

## Acceptance Criteria

- [x] A repo-owned podcast manifest defines the current published whole-book
      and chapter episode set, including converted MP3 paths, the shared
      NotebookLM prompt path, the source packet or script path, and the
      rendered entry id when an episode belongs to a surfaced chapter.
- [x] `make build-family-site` copies the referenced podcast MP3 files into the
      static output, emits a dedicated `podcast.html` page, adds a clear
      homepage `Book / Audiobook / Podcast` top-level split, and renders a
      page-level podcast panel wherever the manifest declares a matching
      episode.
- [x] Regression tests cover the podcast manifest seam and generated HTML
      surface, and the related docs plus coverage rows no longer describe the
      podcast surface as purely planned.

## Out of Scope

- Generating any future podcast episodes beyond the currently available
  NotebookLM exports.
- Podcast feed generation, off-site podcast hosting, or directory submission.
- A custom audio player, transcripts, or synchronized text.
- Automating NotebookLM generation beyond recording the current prompt and
  source references.

## Approach Evaluation

- **Simplification baseline**: A dedicated podcast page plus native HTML
  `<audio controls>` and direct MP3 download links may already solve the
  family-access need; test that before inventing feed plumbing or a custom
  player.
- **AI-only**: Not a fit. This is deterministic asset conversion, manifest
  truth, and site wiring around already-generated audio.
- **Hybrid**: Unnecessary for the first slice. Human-curated podcast metadata
  plus deterministic rendering is simpler and more inspectable.
- **Pure code**: Best fit. The job is a bounded static-build extension that can
  reuse the audiobook surface pattern.
- **Repo constraints / prior decisions**: `docs/presentation-decisions.md`
  already prefers simple on-site browser play and download controls for older
  relatives. `docs/infrastructure.md` already proves the DreamHost deploy path
  can publish generated audio assets. Story 009 remains a scout boundary, so
  this story should only implement the on-site baseline rather than decide the
  final off-site lane.
- **Existing patterns to reuse**: Extend `modules/build_family_site.py`, reuse
  the manifest-plus-native-player pattern from Story 011, and keep the
  homepage/site copy reader-facing rather than exposing NotebookLM workflow
  language on the public surface.
- **Eval**: A narrow builder regression using a tiny fake podcast manifest and
  dummy MP3 files should prove the copied assets, homepage split, chapter
  panel, and podcast page without depending on the full real files.

## Tasks

- [x] Add a repo-owned podcast manifest and shared prompt file that record the
      current whole-book episode and chapter episode set with source lineage.
- [x] Convert the provided NotebookLM `.m4a` exports into the repo-owned MP3
      files declared by that manifest.
- [x] Extend the local family-site builder to load the podcast manifest, copy
      the referenced MP3 files into the published bundle, generate a dedicated
      podcast page, add page-level podcast panels for matching rendered
      chapters, and expose a homepage `Book / Audiobook / Podcast` split.
- [x] Update the stylesheet and rendered copy so the podcast controls stay
      legible and easy to use on desktop and mobile, with explicit play and
      download cues for older readers.
- [x] Add or update tests for the podcast manifest seam, copied public assets,
      and generated landing/chapter/podcast HTML.
- [x] If this story changes documented format coverage or graduation reality: update `tests/fixtures/formats/_coverage-matrix.json` and any relevant methodology state honestly
- [x] Check whether the chosen implementation makes any existing code, helper paths, or docs redundant; remove them or create a concrete follow-up
- [x] Run required checks for touched scope:
  - [x] Default Python checks: `make test`
  - [x] Default Python lint: `make lint`
  - [x] Rebuild the real site with `make build-family-site` and inspect the
        generated homepage, podcast page, and representative chapter page
  - [x] Methodology views: `make methodology-compile` and `make methodology-check`
- [x] If evals or goldens changed: not expected for this story
- [x] Search all docs and update any related to what we touched
- [x] Verify Central Tenets:
  - [x] T0 — Traceability: every surfaced episode stays tied to a repo-owned
        MP3 file, the shared NotebookLM prompt, and its source packet or script
  - [x] T1 — AI-First: confirmed this is deterministic plumbing, not a job for
        an LLM
  - [x] T2 — Eval Before Build: builder tests prove the new surface before any
        deploy claim
  - [x] T3 — Fidelity: source content remains unchanged; the story only adds
        companion listening surfaces
  - [x] T4 — Modular: the podcast surface reads from manifest data instead of
        hardcoded episode HTML
  - [x] T5 — Inspect Artifacts: inspect the generated landing, podcast, and
        representative chapter pages after the build

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

- **Owning module / area**: Local whole-book static builder, repo-owned podcast
  metadata/assets, and the docs that describe published listening truth.
- **Methodology reality**: `spec:3` through `spec:7` remain `partial`.
  `chapter-podcasts` and `full-book-podcast` are the relevant coverage rows and
  should move from `planned` to `partial` if this story ships the first on-site
  podcast surface.
- **Substrate evidence**: `modules/build_family_site.py` already renders the
  whole-book shell, source-library page, audiobook page, and page-level
  audiobook panels; `audiobook/manifest.json` proves the repo already uses a
  manifest seam for companion audio; `/Users/cam/Documents/Projects/onward-to-the-unknown-website/podcast/`
  currently contains the two NotebookLM `.m4a` exports plus a shared prompt
  note; `ffprobe` in this pass measured those source durations as `2535.36`
  seconds and `329.65` seconds.
- **Data contracts / schemas**: Introduce a small repo-owned podcast manifest
  under `podcast/` with schema version, shared prompt path, a whole-book
  episode object, and ordered chapter episode rows with optional rendered-entry
  mapping. No cross-repo schema change is needed.
- **File sizes**: `modules/build_family_site.py` (4061 lines),
  `tests/test_build_family_site.py` (1354 lines),
  `docs/stories/story-002-notebooklm-family-story-podcasts.md` (240 lines),
  `docs/stories/story-009-podcast-distribution-scout-and-elder-friendly-listening.md`
  (243 lines), `docs/presentation-decisions.md` (154 lines),
  `docs/infrastructure.md` (114 lines), `docs/RUNBOOK.md` (235 lines),
  `tests/fixtures/formats/_coverage-matrix.json` (60 lines), and
  `docs/methodology/state.yaml` (135 lines).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, `docs/presentation-decisions.md`,
  `docs/infrastructure.md`, `docs/RUNBOOK.md`, Stories 002, 009, and 011, plus
  the external NotebookLM prompt/source export folder. No repo-local ADRs
  specific to on-site podcast delivery exist.

## Files to Modify

- `docs/stories/story-014-first-on-site-podcast-listening-surface.md` — story
  execution record and work log (new file)
- `docs/stories/story-002-notebooklm-family-story-podcasts.md` — align the
  generation story wording with the chapter-based rollout (230 lines)
- `podcast/manifest.json` — canonical on-site podcast inventory (new file)
- `podcast/notebooklm-prompt.md` — shared NotebookLM prompt notes for podcast
  generation (new file)
- `podcast/NotebookLM_Onward_to_the_Unknown/*.mp3` — converted repo-owned
  podcast assets (new files)
- `modules/build_family_site.py` — podcast manifest loading, public asset copy,
  homepage split, podcast-page render, and page-level podcast panels (3664 lines)
- `tests/test_build_family_site.py` — podcast builder regression coverage using
  small fake MP3 fixtures (1189 lines)
- `docs/presentation-decisions.md` — capture the accepted first podcast
  listening pattern (146 lines)
- `docs/infrastructure.md` — record the deploy impact of generated podcast
  assets (113 lines)
- `docs/RUNBOOK.md` — record the podcast-aware build/inspection flow (203 lines)
- `docs/stories/story-009-podcast-distribution-scout-and-elder-friendly-listening.md`
  — keep the distribution scout aligned with the new on-site baseline (238 lines)
- `tests/fixtures/formats/_coverage-matrix.json` — update podcast-surface truth
  (60 lines)

## Redundancy / Removal Targets

- The blanket assumption in docs that podcasts are only planned companion media
  with no on-site listening surface.
- Any future temptation to hardcode podcast MP3 links directly into one-off
  pages instead of keeping them in the manifest.
- The homepage treatment that makes archive/library and audiobook the only
  top-level lanes while the book and podcast surfaces remain implicit.

## Notes

- This is a new story rather than an expansion of Story 002 because generation
  workflow and on-site listening UI are distinct validation boundaries.
- This is also a new story rather than an expansion of Story 009 because Story
  009 is still a scout/documentation boundary, while this story owns the first
  concrete podcast page and page-level player surface.
- The initial repo-owned podcast slice was intentionally small: one whole-book
  episode and one chapter episode. Later work-log entries expand that same
  manifest seam across the full currently available NotebookLM episode set.

## Plan

1. Define the repo-owned podcast manifest, prompt path, and converted MP3 asset
   layout under `podcast/`, mirroring the audiobook seam closely enough to stay
   inspectable without pretending the two surfaces are identical.
2. Extend `modules/build_family_site.py` and `tests/test_build_family_site.py`
   to load the new catalog, copy podcast assets, render `podcast.html`, add
   page-level episode panels, and change the homepage top-level split to
   `Book`, `Audiobook`, and `Podcast`.
3. Update the touched truth docs and coverage rows so the new on-site podcast
   baseline is visible in repo documentation and future scout/generation work
   can build on it honestly.
4. Run the touched validation, rebuild the real site, and inspect the homepage,
   podcast page, and a representative chapter page before handing off.

## Work Log

20260412-1600 — exploration: verified Ideal/spec alignment against
`docs/ideal.md`, `docs/spec.md`, `docs/methodology/state.yaml`,
`docs/methodology/graph.json`, `tests/fixtures/formats/_coverage-matrix.json`,
`docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`,
Stories 002, 009, and 011, and the external NotebookLM export folder. Traced
the current site surface through `modules/build_family_site.py` and
`tests/test_build_family_site.py`. Fresh substrate evidence: the builder
already supports repo-owned audiobook manifests, copied MP3 assets,
`audiobook.html`, and page-level listening panels, but there is no parallel
podcast seam yet. External source evidence for this story now exists in
`/Users/cam/Documents/Projects/onward-to-the-unknown-website/podcast/` with two
NotebookLM `.m4a` exports and a shared prompt note; `ffprobe` measured the
durations as `2535.36` seconds and `329.65` seconds. Next step: add the
repo-owned podcast manifest plus the first on-site podcast surface instead of
stretching the generation or scout stories beyond their current boundaries.
20260412-1600 — implementation: converted the first two NotebookLM podcast
exports into repo-owned MP3 assets under `podcast/`, added
`podcast/manifest.json` plus the shared prompt note, extended
`modules/build_family_site.py` to publish `podcast.html`, page-level podcast
panels, and the homepage `Book / Audiobook / Podcast` split, and updated the
podcast truth docs plus story surfaces. Fresh verification in this pass:
`python -m pytest tests/test_build_family_site.py -q`, `make test`,
`make lint`, `make build-family-site`, `make methodology-compile`, and
`make methodology-check` all passed. Direct artifact inspection confirmed the
generated `build/family-site/index.html` jump row and podcast actions,
`build/family-site/podcast.html` whole-book and episode cards, and
`build/family-site/chapter-002.html` page-level podcast panel with the chapter
episode MP3. Next step: `/validate`.
20260412-1615 — refinement: removed the homepage hero jump-row after direct UI
inspection showed the new `Book / Audiobook / Podcast` buttons only jumped the
reader a negligible distance and added noise above the actual feature panels.
Implementation touched `modules/build_family_site.py`, homepage assertions in
`tests/test_build_family_site.py`, and this story log. Next step: rerun the
touched checks and rebuild the site to confirm the simplified hero still reads
cleanly.
20260413-0000 — content expansion: converted the newly added NotebookLM source
exports for Chapters 03 through 14 into repo-owned MP3 assets under
`podcast/NotebookLM_Onward_to_the_Unknown/` and extended
`podcast/manifest.json` so the current on-site podcast surface now covers the
whole-book episode plus Chapter 02 through Chapter 14. Fresh verification in
this pass: `python -m pytest tests/test_build_family_site.py -q` passed and
`make build-family-site` rebuilt the site successfully. Direct artifact checks
confirmed that `build/family-site/podcast.html` now lists Episodes 03 and 14
with matching chapter links, that the published podcast asset directory now
contains MP3 files 01 through 14, and that `build/family-site/chapter-003.html`,
`chapter-009.html`, and `chapter-014.html` all show the page-level podcast
panel. Next step: add the remaining episodes when their NotebookLM exports are
ready, then rerun the same manifest/build pass.
20260416-1100 — full intake completion: converted the remaining available
NotebookLM source exports for Episodes 15 through 20 into repo-owned MP3
assets under `podcast/NotebookLM_Onward_to_the_Unknown/` and extended
`podcast/manifest.json` so the on-site podcast surface now covers the whole-book
episode plus every currently available chapter and supplement episode through
the Rolland Alain memoir. While validating the expanded set, the earlier
Chapter 03 through 14 target-entry mapping was corrected to match the rendered
chapter ids already established by `audiobook/manifest.json` and the built site
titles, avoiding podcast panels on unrelated reunion/award pages. `docs/inbox.md`
was also checked in this pass and it currently contains no untriaged items, so
there was nothing to triage or land elsewhere. Next step: rerun the
builder/test/methodology checks and inspect the late-chapter and supplement
pages that now carry podcast panels.
20260416-1230 — manual QA refinement: processed the current source-repo inbox
notes into this active story instead of creating a new slice because the issues
were all direct follow-ups to the new audiobook/podcast surfaces. The builder
now renders a top menu for the book/audiobook/podcast lanes, simplifies the
homepage audiobook and podcast panels down to one button each, moves the full
audiobook into its own section above the individual tracks, and converts the
page-level audiobook/podcast blocks into compact disclosures that sit in a
two-up grid when both companions exist. Because the repo still does not contain
`audiobook/ElevenLabs_Onward_to_the_Unknown/full-audiobook.mp3` at that point
in the pass, the audiobook page was updated to keep that top slot visible with
an honest reader-facing note until the full MP3 was regenerated. Next step:
rerun the touched test/build checks and inspect the homepage, audiobook page,
and representative chapter pages to confirm the quieter reading layout.
20260416-1410 — navigation split refinement: changed the site structure so
`index.html` now acts as the landing page for the archive, while a dedicated
`book.html` carries the former reading-surface overview with the `Opening
Pages`, `Family Stories`, and `Closing Archive` sections. The shared site menu
now consistently exposes `Home`, `The Book`, `Archive Sources`, `Audiobook`,
and `Podcast`, with the current lane highlighted on the landing page, the book
page, the listening pages, the archive-sources page, and the individual book
entries. The source-library page is also now emitted even for lean fixture
builds so that the five-link global menu never points at a missing page during
verification. Fresh verification in this pass: `python -m pytest
tests/test_build_family_site.py -q` and `make build-family-site` passed, and
direct artifact inspection confirmed the new menu/link shape on
`build/family-site/index.html`, `book.html`, `archive-sources.html`,
`audiobook.html`, `podcast.html`, and `chapter-002.html`. Next step: rerun the
methodology checks, then hand off unless further layout tweaks are needed.
20260416-1500 — QA and publish refinement: processed the latest browser notes
directly into this same story because they were still narrow fit-and-finish on
the new podcast/book/archive shell rather than a new validation boundary. The
shared five-link menu regained its icons, the archive-sources hero dropped the
redundant `Back to Home` button, `book.html` gained an `Open the Book PDF`
action in the hero, and the source surfaces were simplified to open-first PDF
actions instead of separate download buttons. To support the real build in this
worktree, `input/Onward to the Unknown.pdf` was copied in locally from the
source project so the surfaced book link could resolve during generation.
Fresh verification in this pass: `python -m pytest tests/test_build_family_site.py -q`
and `make build-family-site` passed locally, then the rebuilt bundle was
deployed to DreamHost and verified publicly with `HTTP 200` responses for `/`,
`/book.html`, `/chapter-001.html`, and the published book PDF. Next step:
run the full close-out validation and, if it stays green, mark the story done.
20260416-1512 — close-out: reran the required close-out validation for this
story with `python -m pytest tests/` and `python -m ruff check modules/ tests/`,
both passing fresh in this worktree. Story 014 now closes as the shipped
podcast/listening-shell slice: the repo owns the full current NotebookLM podcast
catalog, the site exposes dedicated `Home`, `The Book`, `Archive Sources`,
`Audiobook`, and `Podcast` lanes with a shared highlighted menu, the book hero
provides an immediate open-the-book path, and the archive/source surfaces now
prefer simple browser-open actions for non-technical family readers. Next step:
`/check-in-diff`.
