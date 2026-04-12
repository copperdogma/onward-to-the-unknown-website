---
title: "First On-Site Audiobook Listening Surface"
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
  - "story-003"
  - "story-005"
  - "story-006"
  - "story-007"
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
  - "content_model"
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "no on-site audiobook surface; repo-owned MP3 files exist outside the current site build output"
---

# Story 011 — First On-Site Audiobook Listening Surface

**Priority**: Medium
**Status**: Done
**Decision Refs**: `docs/presentation-decisions.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`, `docs/runbooks/elevenlabs-audiobook.md`, `tests/fixtures/formats/_coverage-matrix.json`, `docs/stories/story-003-elevenlabs-full-audiobook.md`, `docs/stories/story-008-audiobook-distribution-scout-and-elder-friendly-listening.md`, none found after search for repo-local ADRs or prior on-site audiobook implementation docs
**Depends On**: Stories 003, 005, 006, and 007

> If this story is `Blocked`, replace `N/A` in `Blocker Summary`, `Blocker
> Evidence`, and `Unblock Condition` with repo-backed truth, and make the
> visible `## Plan` describe the unblock path or blocker reassessment work
> instead of stale "proceed now" steps. Leave those sections as `N/A`
> otherwise.

## Goal

Ship the first honest on-site audiobook surface for the current static reading
site by turning the repo-owned chapter MP3 set into an inspectable audiobook
manifest, copying those assets into the generated bundle, adding a clear
whole-book listening entry point, and surfacing a simple native-player
"listen to this chapter" panel on pages that have matching audio. This slice
also now owns the first merged full-audiobook MP3, built from the chapter set
with fixed silence between tracks so the site can offer one-button full-book
play and download. The result should let older family members start listening
without leaving the site or guessing which file matches which chapter.

## Acceptance Criteria

- [x] A repo-owned audiobook manifest defines the current published track set
      in listening order, including the audio file path, the reviewed script
      source, and the rendered entry id when a track belongs to a surfaced page
      or supplement.
- [x] `make build-family-site` copies the referenced MP3 files into the static
      output, emits a dedicated whole-book audiobook page, and adds a clear
      page-level listening panel everywhere the manifest declares a matching
      track.
- [x] A maintained repo command builds a merged full-audiobook MP3 from the
      ordered chapter track set with `4` seconds of silence between tracks, and
      the site exposes that file for browser play and download.
- [x] Regression tests cover the audiobook manifest seam and the generated HTML
      surface, and the related truth docs and coverage rows no longer describe
      audiobook delivery as purely planned.

## Out of Scope

- Off-site audiobook publishing or platform selection.
- Podcast or video companion work.
- Transcript UI, search, or per-sentence synchronization.
- Any attempt to automate ElevenLabs generation or change the existing script
  corpus.

## Approach Evaluation

- **Simplification baseline**: A dedicated audiobook page plus native HTML
  `<audio controls>` and direct MP3 links may already solve the family-access
  need; test that before inventing a richer player or external dependency.
- **AI-only**: Not a fit. This is static asset wiring, metadata truth, and UI
  plumbing over a known local track set.
- **Hybrid**: Unnecessary for the first slice. Human-authored audiobook
  metadata plus deterministic rendering is simpler and more inspectable.
- **Pure code**: Best fit. The problem is a bounded static-build extension with
  a small canonical manifest and straightforward HTML/CSS output.
- **Repo constraints / prior decisions**: The repo already has a static
  DreamHost deploy path, a thin whole-book shell, supplement support, and a
  completed repo-owned audiobook script corpus. `docs/presentation-decisions.md`
  still defers richer companion-media embedding, so this story should stay
  small and reader-facing rather than inventing a generalized media layer.
- **Existing patterns to reuse**: Extend `modules/build_family_site.py`, reuse
  the supplement metadata pattern for a small audiobook manifest, and follow
  the existing landing-page and page-level navigation treatment rather than
  introducing a second site shell.
- **Eval**: A narrow builder regression using a tiny fake audiobook manifest
  and dummy MP3 files should prove the HTML surface, copied assets, and chapter
  matching without depending on the full real 500 MB audio set.

## Tasks

- [x] Add a repo-owned audiobook manifest that records the current track set,
      listening order, asset paths, and rendered-entry mapping.
- [x] Extend the local family-site builder to load that manifest, copy the
      referenced MP3s into the published bundle, generate a dedicated audiobook
      page, and add page-level listening panels for matching rendered entries.
- [x] Update the stylesheet and rendered copy so the audiobook controls stay
      legible and easy to use on desktop and mobile, with explicit play and
      download cues for older readers.
- [x] Add a maintained full-audiobook build script that concatenates the
      ordered track set with a fixed silence gap and records the merged file in
      the audiobook manifest.
- [x] Add or update tests for the audiobook manifest seam, copied public
      assets, and generated landing/chapter/audiobook HTML.
- [x] If this story changes documented format coverage or graduation reality: update `tests/fixtures/formats/_coverage-matrix.json` and any relevant methodology state honestly
- [x] Check whether the chosen implementation makes any existing code, helper paths, or docs redundant; remove them or create a concrete follow-up
- [x] Run required checks for touched scope:
  - [x] Default Python checks: `make test`
  - [x] Default Python lint: `make lint`
  - [x] Rebuild the real site with `make build-family-site` and inspect the
        generated audiobook surfaces
  - [x] Methodology views: `make methodology-compile` and `make methodology-check`
- [x] If evals or goldens changed: not expected for this story
- [x] Search all docs and update any related to what we touched
- [x] Verify Central Tenets:
  - [x] T0 — Traceability: every track stays tied to a repo-owned audio file,
        a reviewed script file, and the matching rendered page when one exists
  - [x] T1 — AI-First: confirmed this is deterministic plumbing, not a job for
        an LLM
  - [x] T2 — Eval Before Build: builder tests prove the new surface before any
        deploy claim
  - [x] T3 — Fidelity: source content and supplement prose remain unchanged;
        the story only adds companion listening surfaces
- [x] T4 — Modular: the audiobook surface reads from manifest data instead
        of hardcoding track-by-track HTML
  - [x] T5 — Inspect Artifacts: inspect the generated landing, audiobook, and
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

- **Owning module / area**: Local whole-book static builder, repo-owned
  audiobook metadata, and the docs that describe published audio truth.
- **Methodology reality**: `spec:3` through `spec:7` remain `partial`.
  `chapter-audio` and `full-book-audio` are the relevant coverage rows and now
  move from `planned` to `partial` with the first on-site audiobook surface.
- **Substrate evidence**: `modules/build_family_site.py` already renders the
  whole-book shell and supplement page surfaces; `audiobook/script/` already
  provides the reviewed chapter corpus; `audiobook/ElevenLabs_Onward_to_the_Unknown/`
  now contains `21` chapter MP3 files dated 2026-04-11 plus the maintained
  merged `full-audiobook.mp3`; this story adds `audiobook/manifest.json`,
  `modules/build_full_audiobook.py`, generated `audiobook.html`, and
  page-level listening panels.
- **Data contracts / schemas**: Introduce a small repo-owned audiobook manifest
  file under `audiobook/` with schema version, ordered tracks, script/audio
  paths, optional rendered-entry mapping, and the merged full-audiobook asset
  metadata. No cross-repo schema change is needed.
- **File sizes**: `modules/build_family_site.py` (2758 lines),
  `modules/build_full_audiobook.py` (139 lines),
  `scripts/build_full_audiobook.py` (19 lines),
  `tests/test_build_family_site.py` (1044 lines),
  `tests/test_build_full_audiobook.py` (107 lines), `README.md` (145 lines),
  `docs/RUNBOOK.md` (191 lines), `docs/presentation-decisions.md` (116 lines),
  `docs/infrastructure.md` (109 lines),
  `docs/runbooks/elevenlabs-audiobook.md` (115 lines),
  `docs/stories/story-008-audiobook-distribution-scout-and-elder-friendly-listening.md`
  (251 lines), `tests/fixtures/formats/_coverage-matrix.json` (60 lines),
  `audiobook/manifest.json` (159 lines), `Makefile` (63 lines), and this
  story file (334 lines).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, `docs/presentation-decisions.md`,
  `docs/infrastructure.md`, `docs/RUNBOOK.md`,
  `docs/runbooks/elevenlabs-audiobook.md`, `docs/scout.md`, and Stories 003
  and 008. No repo-local ADRs specific to on-site audiobook delivery exist.

## Files to Modify

- `docs/stories/story-011-first-on-site-audiobook-listening-surface.md` —
  story execution record and work log (new file)
- `audiobook/manifest.json` — canonical on-site audiobook track inventory (new file)
- `modules/build_full_audiobook.py` — maintained merged-audiobook build
  command over the manifest track set (new file)
- `scripts/build_full_audiobook.py` — thin CLI wrapper for the maintained full
  audiobook builder (new file)
- `modules/build_family_site.py` — audiobook manifest loading, public asset
  copy, audiobook-page render, page-level listening panels, and full-book
  play/download links (2758 lines)
- `tests/test_build_family_site.py` — audiobook builder regression coverage
  using small fake MP3 fixtures (1044 lines)
- `tests/test_build_full_audiobook.py` — merged-audiobook build regression
  coverage over small synthetic MP3 fixtures (107 lines)
- `README.md` — document the audiobook asset and site-build surface (145 lines)
- `Makefile` — add a maintained full-audiobook build target (63 lines)
- `docs/RUNBOOK.md` — record the audiobook-aware build/inspection flow
  (191 lines)
- `docs/presentation-decisions.md` — capture the accepted first audiobook
  listening pattern (116 lines)
- `docs/infrastructure.md` — record the deploy impact of generated audiobook
  assets (109 lines)
- `docs/runbooks/elevenlabs-audiobook.md` — capture the current asset surface
  now that MP3 files are repo truth (115 lines)
- `docs/stories/story-008-audiobook-distribution-scout-and-elder-friendly-listening.md`
  — keep the distribution scout aligned with the new on-site implementation
  baseline (251 lines)
- `tests/fixtures/formats/_coverage-matrix.json` — update audio-surface truth
  (60 lines)

## Redundancy / Removal Targets

- Ad hoc notes that the audiobook only exists as local files with no repo-owned
  public mapping.
- The blanket assumption in docs that audio embeds are entirely deferred.
- Any future temptation to hardcode MP3 links directly into one-off HTML pages
  instead of keeping them in a manifest.

## Notes

- This is a new story rather than an expansion of Story 008 because Story 008
  is a scout/documentation validation boundary, while this story owns the first
  repo-local implementation of an on-site listening surface.
- The first shipped surface should stay simple: a whole-book audiobook page
  plus chapter-level native players and download links are more honest than a
  custom player without better evidence.
- A merged full-audiobook MP3 is now a small coherent scope expansion rather
  than a new story because it reuses the same manifest, assets, player surface,
  and validation boundary.
- Off-site distribution research still belongs to Story 008.

## Plan

1. Add the audiobook manifest.
   - Files: `audiobook/manifest.json`
   - Record the current `21` track set with stable order, source/script
     references, and rendered-entry ids for chapter and supplement matching.
   - Done looks like: the track inventory exists as a repo-owned artifact
     rather than implicit filename knowledge.
2. Extend the builder.
   - Files: `modules/build_family_site.py`
   - Load the manifest, copy the referenced MP3 files into the generated
     bundle, render a dedicated `audiobook.html` page, and inject a compact
     listening panel into matching rendered entry pages plus a whole-book entry
     point on `index.html`.
   - Impact: touches the published bundle shape and page HTML but should not
     alter article content or omission-audit logic.
   - Done looks like: a built site exposes `audiobook.html`, public MP3 files,
     and chapter/supplement listening panels from manifest data.
3. Add regression coverage.
   - Files: `tests/test_build_family_site.py`
   - Keep existing builder tests opt-out by default, then add a focused
     audiobook fixture that proves asset copy, whole-book page output, and a
     chapter-level panel.
   - Done looks like: test coverage exercises the new surface without copying
     the full real audiobook corpus into every temp build.
4. Update truth docs.
   - Files: `README.md`, `docs/RUNBOOK.md`, `docs/presentation-decisions.md`,
     `tests/fixtures/formats/_coverage-matrix.json`
   - Record the first accepted on-site audiobook pattern and the fact that
     real audio assets now exist in repo truth.
   - Done looks like: docs and coverage no longer describe audiobook delivery
     as only planned.
5. Verify and inspect.
   - Run: `make build-full-audiobook`, `make methodology-compile`,
     `make methodology-check`, `make test`, `make lint`,
     `make build-family-site`
   - Inspect the generated landing page, audiobook page, and a representative
     chapter/supplement page before claiming the surface works.

## Work Log

20260411-1805 — action: created story from newly available audiobook assets,
result: split the first on-site audiobook implementation from the still-pending
distribution scout, evidence: repo now contains `21` MP3 files under
`audiobook/ElevenLabs_Onward_to_the_Unknown/` while Story 008 remains
research-only and explicitly out of scope for player UI, next step: add a
canonical audiobook manifest and wire it into the static builder.
20260411-1851 — action: implemented the first on-site audiobook surface,
result: added `audiobook/manifest.json`, taught `modules/build_family_site.py`
to publish `audiobook.html`, copy `21` MP3 files into the built bundle, and
show page-level listening panels for matching chapters and the memoir
supplement; updated builder regression coverage and repo truth docs, evidence:
fresh `make test`, `make lint`, `make methodology-compile`,
`make methodology-check`, and `make build-family-site` runs plus generated
HTML checks in `build/family-site/index.html`, `build/family-site/audiobook.html`,
`build/family-site/chapter-009.html`, `build/family-site/chapter-024.html`,
and `build/family-site/rolland-alain-memoir-family-story.html`, next step:
run `/validate` and do a fresh browser-level visual pass before marking the
story done.
20260411-1900 — action: refined shared navigation chrome from user feedback,
result: replaced the middle `Contents` control with a home-icon button and
made the top site title link back to `index.html` on entry and audiobook
pages, evidence: fresh `python -m pytest tests/test_build_family_site.py -q`,
`python -m ruff check modules/build_family_site.py tests/test_build_family_site.py`,
and `make build-family-site` runs plus generated HTML checks in
`build/family-site/chapter-009.html`, `build/family-site/chapter-024.html`,
and `build/family-site/audiobook.html`, next step: keep the story in progress
until `/validate` confirms the full surface.
20260411-1908 — action: expanded story scope from user request, result:
folded the merged full-audiobook file into Story 011 instead of minting a new
story because it shares the same manifest, builder, and public listening
surface, evidence: current repo state and user direction in this thread, next
step: add the maintained concat command, generate the file, and surface it in
the site.
20260411-2213 — action: implemented the maintained merged-audiobook path,
result: added `modules/build_full_audiobook.py`, `scripts/build_full_audiobook.py`,
and `make build-full-audiobook`, generated
`audiobook/ElevenLabs_Onward_to_the_Unknown/full-audiobook.mp3` with `4`
seconds of silence between ordered chapter tracks, and exposed that file for
browser play/download on `index.html` and `audiobook.html`, evidence: fresh
`make build-full-audiobook`, `python -m pytest tests/test_build_family_site.py tests/test_build_full_audiobook.py -q`,
`python -m ruff check modules/build_family_site.py modules/build_full_audiobook.py scripts/build_full_audiobook.py tests/test_build_family_site.py tests/test_build_full_audiobook.py`,
`make methodology-compile`, `make methodology-check`, and `make build-family-site`
runs plus artifact checks in `build/family-site/index.html`,
`build/family-site/audiobook.html`, and
`build/family-site/audiobook/ElevenLabs_Onward_to_the_Unknown/full-audiobook.mp3`,
next step: run `/validate` before marking the story done.
20260411-2218 — action: refined page-to-page navigation cues from user
feedback, result: the standard left and right chapter pills now render visible
back and next arrows alongside the destination titles while keeping the home
button and clickable site title unchanged, evidence: fresh focused builder
test, lint, and rebuilt HTML inspection are the next verification step, next
step: rebuild the site and confirm the rendered labels read clearly on real
pages before `/validate`.
20260411-2236 — action: refined the landing-page hero title layout from user
feedback, result: the homepage hero now uses a dedicated `home-hero` override
 so the site title is no longer constrained by the shared `40rem` hero-heading
 width cap, evidence: fresh focused builder test, lint, and rebuilt landing
 HTML/CSS inspection are the next verification step, next step: confirm the
 title stays on one line on the built homepage before `/validate`.
20260411-2243 — action: refined the homepage jump-row affordances from user
feedback, result: the landing-page `Audiobook` button now renders with an
audio icon and the current book-section buttons render with a shared book icon,
using icon-capable nav-link markup that can accept a future podcast icon
without another structural rewrite, evidence: fresh focused builder test, lint,
and rebuilt landing HTML/CSS inspection are the next verification step, next
step: confirm the icons read clearly in the built homepage before `/validate`.
20260411-2307 — action: closed Story 011 after fresh validation, result:
confirmed the on-site audiobook surface, merged full-audiobook build, and
follow-up navigation refinements with fresh `make build-full-audiobook FORCE=1`,
`python -m pytest tests/`, `python -m ruff check modules/ tests/`,
`make methodology-compile`, `make methodology-check`, and
`make build-family-site` runs plus direct inspection of
`build/family-site/index.html`, `build/family-site/audiobook.html`,
`build/family-site/chapter-001.html`, `build/family-site/chapter-009.html`,
and the copied merged MP3 artifact, evidence: validation pass in this thread
and workflow gates now fully checked, next step: `/check-in-diff`.
20260411-2323 — action: fixed a narrow check-in risk during finish-and-push,
result: marked the generated merged `full-audiobook.mp3` as ignored git output
and clarified in the README/runbooks that `make build-full-audiobook` requires
`ffmpeg` and should be rerun locally before site build/deploy when full-book
audio needs to publish, evidence: `.gitignore`, `README.md`, `docs/RUNBOOK.md`,
and `docs/runbooks/elevenlabs-audiobook.md`, next step: `/check-in-diff`.
