---
title: "Archive Source Library And Download Links"
status: "Done"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "2. Connected Companion Media"
  - "3. Trustworthy Source Lineage"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:1"
  - "spec:3"
  - "spec:4"
  - "spec:6"
  - "spec:7"
  - "C1"
  - "C3"
  - "C4"
  - "C6"
  - "C7"
adr_refs: []
depends_on:
  - "story-005"
  - "story-007"
category_refs:
  - "spec:1"
  - "spec:3"
  - "spec:4"
  - "spec:6"
  - "spec:7"
compromise_refs:
  - "C1"
  - "C3"
  - "C4"
  - "C6"
  - "C7"
input_coverage_refs:
  - "scanned-supplements"
architecture_domains:
  - "content_model"
  - "site_experience"
  - "upstream_integration"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "top-level `input/` PDFs and photocopied archive files currently exist only as repo-local source files, with the memoir PDF referenced internally but not exposed on the public site"
---

# Story 013 — Archive Source Library And Download Links

**Priority**: High
**Status**: Done
**Decision Refs**: `docs/input-contract.md`, `docs/presentation-decisions.md`, `docs/runbooks/golden-build.md`, `tests/fixtures/formats/_coverage-matrix.json`, `docs/omission-audit.json`, `docs/stories/story-007-rolland-alain-memoir-family-story.md`, none found after search for repo-local ADRs or a dedicated source-library runbook
**Depends On**: Stories 005 and 007

## Goal

Publish the root-level archive source files from `input/` as a reader-facing
site surface so family members can open or download the original photocopied
materials from one central location, while also wiring the memoir page to its
source PDF and making the main `Onward to the Unknown.pdf` the most prominent
source file whenever it is present in the local intake.

## Acceptance Criteria

- [ ] The built site emits a dedicated central source-library page that lists
      every supported root-level archive file currently present in `input/`
      without pulling in the `input/doc-web-html/` bundle or the page-image
      directory.
- [ ] The source-library page provides reader-facing open and download actions
      for each published source file, including the current archive PDFs plus
      `Jackfish-Lake-Fishing-Guide.jpg`.
- [ ] If `input/Onward to the Unknown.pdf` is present at build time, the site
      gives it the most prominent source-library placement and a direct
      homepage action; if the file is absent, the build remains successful and
      the site stays honest about the currently available source files.
- [ ] The Rolland Alain memoir page exposes a direct original-PDF action that
      resolves to the same published source-file copy shown on the central
      source-library page.
- [ ] The current input/build/documentation truth is updated so these archive
      source files are no longer an undocumented side path.

## Out of Scope

- OCRing the remaining archive PDFs into new reader-facing chapter or
  supplement pages.
- A generalized metadata CMS or editorial UI for every future archive asset.
- Reorganizing the `input/` contract beyond the thin documented rule for
  publishable root-level source files.
- Any claim that the local worktree currently contains `input/Onward to the
  Unknown.pdf`; this story should handle that path honestly, not invent it.

## Approach Evaluation

- **Simplification baseline**: The current builder already knows how to copy
  public audiobook assets and already carries memoir `source_pdf` metadata, so
  the thinnest honest move is deterministic file discovery plus a reader-facing
  page and links. No AI path is needed.
- **AI-only**: Not a fit. This is file publishing, navigation, and static-page
  wiring rather than an interpretation problem.
- **Hybrid**: Unnecessary unless later work wants AI-generated summaries for
  archive documents. This story should stay deterministic.
- **Pure code**: Strong fit. The work is small-surface static build plumbing
  plus shell updates.
- **Repo constraints / prior decisions**: `docs/presentation-decisions.md`
  explicitly deferred a generalized public supplement gallery; Story 007 also
  deferred public PDF links on the memoir wrapper until a dedicated archive
  surface existed. The current whole-book builder is the real site, so the new
  surface should extend that builder rather than inventing another runtime.
- **Existing patterns to reuse**: Reuse `copy_audiobook_public_assets()`, the
  supplement `source_pdf` metadata path, `render_action_row()`, `render_nav_link()`,
  the existing standalone `audiobook.html` output seam, and the current
  homepage panel pattern.
- **Eval**: Builder regression tests should prove the central source-library
  page, copied public files, memoir source link, and the presence/absence
  behavior for `input/Onward to the Unknown.pdf`. Fresh local site builds and
  rendered inspection should confirm the source-library page and homepage entry
  remain easy to use on desktop and mobile.

## Tasks

- [x] Define the thin publishable-source contract for this slice: which
      root-level `input/` file types count, which paths are intentionally
      excluded, and how the `Onward to the Unknown.pdf` path is prioritized
      when present.
- [x] Extend the local site build to discover the publishable source files,
      copy them into the public output, and expose a dedicated central
      source-library page with open/download actions.
- [x] Extend the homepage so the source-library page is easy to discover and
      the main book PDF gets a featured action when it exists locally.
- [x] Extend the memoir supplement wrapper so it exposes an original-PDF action
      that points at the published source-file copy instead of maintainer-only
      metadata.
- [x] Add or extend tests for source discovery, copied public files,
      source-library rendering, memoir download wiring, and the missing-book-PDF
      fallback.
- [x] Update `docs/input-contract.md`, `docs/presentation-decisions.md`,
      `tests/fixtures/formats/_coverage-matrix.json`, and
      `docs/omission-audit.json` because the shipped build truth now covers the
      public source-file surface.
- [x] Check whether the chosen implementation makes any old “no public PDF
      link yet” guidance or tests redundant; remove or update them in the same
      slice.
- [x] Run required checks for touched scope:
  - [x] Default Python checks: `make test`
  - [x] Default Python lint: `make lint`
  - [x] Fresh site build proof: `make build-family-site`
  - [x] Refresh generated methodology views: `make methodology-compile`
  - [x] Check methodology consistency: `make methodology-check`
  - [x] Manual desktop/mobile inspection of the homepage, source-library page,
        and memoir page
- [x] Evals/goldens did not change, so no `/improve-eval` or
      `docs/evals/registry.yaml` update was needed for this slice.
- [x] Search all docs and update any related to what we touched
- [x] Verify Central Tenets:
  - [x] T0 — Traceability: each published source link traces back to a concrete
        `input/` file path
  - [x] T1 — AI-First: no AI code is added where deterministic file plumbing is
        sufficient
  - [x] T2 — Eval Before Build: baseline absence of the source-library surface
        is recorded before implementation and replaced with passing regression
        proof
  - [x] T3 — Fidelity: published source files remain the original files, not
        transformed derivatives
  - [x] T4 — Modular: the new source-library seam stays a thin extension of the
        current builder instead of a second ad hoc site path
  - [x] T5 — Inspect Artifacts: rendered desktop/mobile pages and copied public
        files are inspected directly in this pass

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

- **Owning module / area**: `modules/build_family_site.py` should own source
  discovery, public asset copying, and the reader-facing source-library page;
  the contract and presentation truth should live in the existing input and
  presentation docs.
- **Methodology reality**: This sits in `spec:1`, `spec:3`, `spec:4`,
  `spec:6`, and `spec:7`, all still `partial` in
  `docs/methodology/state.yaml`; the relevant current coverage row is
  `scanned-supplements`, whose notes already say additional family-archive
  scans remain future work.
- **Substrate evidence**: `make build-family-site` on `2026-04-12` produced
  `build/family-site/index.html` and
  `build/family-site/rolland-alain-memoir-family-story.html`, but no
  `archive-sources.html`; fresh inspection of the built HTML confirmed that the
  homepage exposes no source-library link and the memoir page exposes no
  `Download Original PDF` or `Open Original PDF` action. The builder already
  copies public audiobook files through `copy_audiobook_public_assets()`,
  writes standalone pages like `audiobook.html`, and carries supplement
  `source_pdf` metadata via `load_family_story_supplements()` and
  `build_supplement_rendered_entry()`. `.gitignore` also reserves
  `input/Onward to the Unknown.pdf`, but that file is absent in this worktree
  as of `2026-04-12`.
- **Data contracts / schemas**: No repo-wide schema module is involved. The
  likely contract change is a documented builder rule for publishable root-level
  `input/` source files plus the existing supplement `source_pdf` link path
  resolving to a public copy when available.
- **File sizes**: `modules/build_family_site.py` (2882 lines),
  `tests/test_build_family_site.py` (1068),
  `docs/input-contract.md` (147),
  `docs/presentation-decisions.md` (121),
  `tests/fixtures/formats/_coverage-matrix.json` (60),
  `docs/omission-audit.json` (851),
  `docs/stories/story-007-rolland-alain-memoir-family-story.md` (387).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `docs/input-contract.md`, `docs/presentation-decisions.md`,
  `docs/runbooks/golden-build.md`, `docs/omission-audit.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, and Story 007. No repo-local
  ADRs exist beyond `docs/decisions/README.md`.

## Files to Modify

- `modules/build_family_site.py` — add root-level source discovery, public file
  copying, a source-library page, homepage/source actions, and memoir PDF link
  plumbing (2882 lines)
- `tests/test_build_family_site.py` — cover source-library rendering, copied
  files, memoir source link wiring, and missing-book-PDF behavior (1068 lines)
- `docs/input-contract.md` — document the thin contract for publishable
  root-level source files (147 lines)
- `docs/presentation-decisions.md` — record the public source-library and
  memoir-link presentation decision (121 lines)
- `tests/fixtures/formats/_coverage-matrix.json` — update coverage truth for
  archive-source publication progress if shipped behavior changes the recorded
  reality (60 lines)
- `docs/omission-audit.json` — refresh the checked-in audit snapshot if the
  public build now records source-library truth there (851 lines)

## Redundancy / Removal Targets

- The existing “defer raw imported HTML, original PDF links, and similar
  provenance/process affordances” note in `docs/presentation-decisions.md`
  should be narrowed so it no longer blocks a dedicated source-library surface.
- The current test assertions that the memoir page must not show
  `Download Original PDF` should be replaced with the new public-source truth.

## Notes

- This is a new story rather than a Story 007 reopen because the validation
  boundary is broader than the memoir wrapper. It now covers a central
  cross-site source-library page, homepage discoverability, published public
  file copies for multiple archive documents, and memoir-page attachment
  wiring.
- Small scope expansion folded in automatically: include
  `Jackfish-Lake-Fishing-Guide.jpg` on the same central page because the user
  explicitly requested it and it shares the identical publication seam.

## Plan

- Task 1 (`XS`): Add small source-library helpers in
  `modules/build_family_site.py` for root-level `input/` file discovery,
  ordering, and public-copy paths.
  Done looks like: the builder can enumerate top-level PDF/JPG source files,
  exclude `doc-web-html/` and page-image directories, and give
  `input/Onward to the Unknown.pdf` featured ordering when it exists.
- Task 2 (`S`): Extend the builder output with a dedicated
  `archive-sources.html` page plus copied public files under a stable asset
  directory, and render homepage source actions that point to that page and the
  book PDF when present.
  Impact / risk: touches the main site shell and homepage output; avoid
  spreading ad hoc string concatenation by following the existing audiobook page
  pattern.
  Done looks like: a central source page exists, every current root-level
  archive file is openable/downloadable from it, and the homepage links users
  there without adding provenance clutter to every reader page.
- Task 3 (`XS`): Wire the memoir supplement wrapper to the same published
  source-file record rather than leaving `source_pdf` as internal-only metadata.
  Impact / risk: supplement page copy and tests currently assume no public PDF
  action, so this needs coordinated template and assertion updates.
  Done looks like: the memoir page shows an original-PDF action and it resolves
  to the same public file surfaced on the source-library page.
- Task 4 (`S`): Update regression tests and repo truth docs, then rebuild and
  manually inspect the rendered result on desktop/mobile.
  Impact / risk: `modules/build_family_site.py` is already large, so keep new
  logic in focused helpers and avoid mixing source-library decisions into
  unrelated chapter rendering paths.
  Done looks like: focused tests pass, docs describe the current contract
  honestly, and a fresh build/manual inspection proves the homepage,
  source-library page, and memoir page behave as intended.
- Approval blockers: none for code changes. The only local-gap note is that the
  actual `input/Onward to the Unknown.pdf` file is absent in this worktree, so
  this pass should implement graceful support and prove it with tests/logic
  rather than claiming the file is currently shipped here.

## Work Log

20260412-1107 — exploration: verified Ideal/spec alignment against `docs/ideal.md`, `docs/spec.md`, `docs/methodology/state.yaml`, `docs/methodology/graph.json`, `docs/input-contract.md`, `docs/presentation-decisions.md`, `docs/runbooks/golden-build.md`, `docs/omission-audit.json`, `tests/fixtures/formats/_coverage-matrix.json`, and Story 007; no repo-local ADR applied. Traced the current site surface through `modules/build_family_site.py` and `tests/test_build_family_site.py`. Fresh baseline evidence: `make build-family-site` produced `build/family-site/index.html` and `build/family-site/rolland-alain-memoir-family-story.html`, but there was no `build/family-site/archive-sources.html`; direct HTML inspection also confirmed `Download Original PDF`, `Open Original PDF`, `Browse Source Library`, and `Open Book PDF` were absent from the homepage and memoir page. Substrate verified: the builder already copies public audiobook assets, emits standalone non-entry pages, and preserves supplement `source_pdf` metadata. Local gap verified: `.gitignore` reserves `input/Onward to the Unknown.pdf`, but the file is absent from this worktree today. Next step: implement the thin public source-library seam instead of reopening Story 007.
20260412-1110 — status: promoted the story from `Pending` to `In Progress` before implementation because the required substrate already exists in the current builder and the work is honestly buildable now. Next step: regenerate methodology views, then land the source-library, homepage, and memoir-link changes described in the plan.
20260412-1118 — implementation: extended `modules/build_family_site.py` with root-level source-file discovery for supported `input/` PDFs/image scans, public copying under `build/family-site/source-files/`, an `_internal/source-library.json` manifest, a dedicated `archive-sources.html` page, homepage `Archive Sources` entry points, and memoir wrapper actions that now open/download the preserved source PDF through the same public library seam. Updated regression coverage in `tests/test_build_family_site.py` for both the featured-book-PDF path and the missing-book-PDF fallback. Updated truth docs in `docs/input-contract.md`, `docs/presentation-decisions.md`, and `tests/fixtures/formats/_coverage-matrix.json` to reflect the new public source-library surface.
20260412-1124 — verification: reran `make test`, `make lint`, `make build-family-site`, `make refresh-omission-audit`, `make methodology-compile`, and `make methodology-check` sequentially after avoiding a shared-output race from an earlier parallel attempt. Fresh rendered inspection used Playwright on `http://localhost:4183/` at `1280x900` and `390x844`, with screenshots `story013-index-desktop.png`, `story013-sources-desktop.png`, `story013-memoir-desktop.png`, `story013-index-mobile.png`, `story013-sources-mobile.png`, and `story013-memoir-mobile-top.png` / `story013-memoir-mobile-actions.png`. Current real-worktree result: homepage now exposes the `Archive Sources` panel and link, `archive-sources.html` lists 6 published root-level source files with open/download actions, the memoir page exposes original-PDF buttons, and the homepage correctly omits `Open Book PDF` because `input/Onward to the Unknown.pdf` is still absent locally. Next step: run `/validate`, then close via `/mark-story-done` if the user accepts the slice.
20260412-1141 — refinement: copied the locally available `Onward to the Unknown.pdf` into this worktree's ignored `input/` path so the current build can feature the actual book, then refined `archive-sources.html` to show the same book icon treatment as the homepage, separate the featured book from the remaining photocopied documents, add the user-provided photocopy note, and replace generic archive blurbs with document-specific one-sentence summaries derived from fresh PDF text extraction / OCR review. Fresh proof in this pass: `python -m pytest tests/test_build_family_site.py -q`, `python -m ruff check modules/build_family_site.py tests/test_build_family_site.py`, and `make build-family-site` all passed, and the rebuilt `build/family-site/archive-sources.html` now contains the featured book actions plus the note-led photocopy section.
20260412-1157 — homepage refinement: upgraded the landing-page hero in `modules/build_family_site.py` with a short archive-intro block and surface stats, then wrapped the `Archive Sources` and `Audiobook` overview panels in a shared responsive feature grid so they sit side by side on desktop and stack again on mobile. Regression proof for this pass: `python -m pytest tests/test_build_family_site.py -q`, `python -m ruff check modules/build_family_site.py tests/test_build_family_site.py`, and `make build-family-site` all passed. Fresh visual inspection used temporary local Playwright screenshots at desktop and mobile widths, confirming the two overview panels share a row at desktop width and collapse cleanly on mobile while the richer hero remains readable.
20260412-1208 — tone correction: replaced the homepage hero copy with warmer family-facing language, renamed the summary panel to reader-friendly wording, and removed the lingering site/process meta-language from the homepage text and screen-reader label. Updated `AGENTS.md` and `docs/ideal.md` to make the audience and tone explicit: the site is primarily for elderly relatives and published copy should stay warm, inviting, and free of implementation or process language. Fresh proof in this pass: `python -m pytest tests/test_build_family_site.py -q`, `python -m ruff check modules/build_family_site.py tests/test_build_family_site.py`, `make build-family-site`, `make methodology-compile`, and `make methodology-check`.
20260412-1227 — validation follow-through: replaced the remaining public-facing `Back to Reading Surface` label with `Back to Home`, refreshed `docs/omission-audit.json` so the checked-in snapshot matches the current local source-library state with the featured book PDF present, and updated `docs/input-contract.md` to explain that the featured book depends on a repo-local ignored input file. Fresh proof in this pass: `make refresh-omission-audit`, `make test`, `make lint`, `make methodology-compile`, and `make methodology-check` all passed, and fresh Playwright checks confirmed `index.html`, `archive-sources.html`, and `rolland-alain-memoir-family-story.html` remain readable at both `1280x900` and `390x844`.
20260412-1316 — completion: confirmed Story 013 is implementation-complete and closed it via `/mark-story-done`. Fresh close-out proof in this pass: `python -m pytest tests/`, `python -m ruff check modules/ tests/`, `make test`, `make lint`, `make build-family-site`, `make methodology-compile`, and `make methodology-check` all passed; direct artifact inspection also reconfirmed the published source-library page, memoir original-PDF actions, full audiobook asset, and per-track runtime labels in the rebuilt output. Next step: `/check-in-diff`.
20260412-1443 — post-deploy fix: diagnosed the live-site styling regression as a stale cached `assets/family-site.css` response while the HTML had already updated, then versioned the generated stylesheet URL in `modules/build_family_site.py` so rebuilt pages request the current CSS content after deploy. Fresh proof in this pass: `python -m pytest tests/test_build_family_site.py -q`, `python -m ruff check modules/build_family_site.py tests/test_build_family_site.py`, and `make build-family-site` all passed; public verification also confirmed the live homepage now links `assets/family-site.css?v=c9476588610a` and Cloudflare served the updated stylesheet on cache miss.
