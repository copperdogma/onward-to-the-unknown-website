# Changelog

## [2026-04-18-01] - Settled combined audio distribution plan (Story 009)

### Added
- Added a dated combined audiobook-and-podcast distribution scout that keeps
  the website as the canonical listening home and records the strongest
  external listening lanes that still fit the family-first, no-fee
  constraints.
- Added Story 015 as the concrete follow-up for a self-hosted podcast RSS feed
  and optional app-link handoff without changing the audiobook recommendation.

### Changed
- Replaced the older podcast-only Story 009 shell with one combined
  audiobook-and-podcast distribution story and refreshed the generated story
  index and methodology graph to match.
- Updated the presentation decisions, infrastructure truth, and runbook so they
  now consistently recommend a self-hosted podcast RSS feed submitted to Apple
  Podcasts first and Spotify second if an external duplicate is added later.

## [2026-04-17-01] - Added AI source notes to listening pages

### Added
- Added explicit AI-generation notes to the audiobook and podcast hero areas,
  with direct links to ElevenLabs and NotebookLM so readers can tell how those
  companion recordings were made.

## [2026-04-16-01] - Shipped the first on-site podcast surface (Story 014)

### Added
- Added a repo-owned podcast manifest plus the current NotebookLM-derived MP3
  set for the whole-book episode and chapter/supplement companion episodes.
- Added a dedicated `podcast.html` listening page and page-level podcast
  panels wherever the manifest maps an episode to a surfaced book entry.

### Changed
- Split the public shell into `Home`, `The Book`, `Archive Sources`,
  `Audiobook`, and `Podcast`, with a shared icon-bearing menu and a new
  `Open the Book PDF` action on the book page hero.
- Simplified the source-library and supplement PDF actions so readers open the
  documents directly in the browser instead of choosing between open/download
  controls first.

### Fixed
- Fixed the earlier podcast-to-page mapping drift so the later chapter episodes
  attach to the intended rendered entries instead of unrelated front-matter
  pages.
- Fixed redundant navigation noise on the archive/book shell, including the
  removed archive hero home button and restored menu icons across the shared
  five-link header.

## [2026-04-12-04] - Settled the first audiobook distribution lane (Story 008)

### Added
- Added a dated audiobook-distribution scout that compares the current
  site-hosted MP3 flow against ElevenReader, Spotify direct upload, Voices by
  INaudio, and Audio Native using current primary sources.

### Changed
- Recorded the site-hosted audiobook surface as the current primary family
  listening lane in the presentation decisions, infrastructure truth, runbook,
  coverage matrix, and generated methodology views.

### Fixed
- Fixed planning-truth drift so the coverage matrix and generated methodology
  graph no longer describe the audiobook distribution lane as unresolved after
  Story 008's recommendation.

## [2026-04-12-03] - Prevented stale stylesheet deploys (Story 013)

### Changed
- Versioned the generated `family-site.css` link across the family-site pages
  so each deploy requests the current stylesheet content instead of relying on
  a long-lived bare asset URL.

### Fixed
- Fixed the live site rendering stale CSS after deploy, which had been pairing
  the newer homepage and audiobook HTML with older layout styles.

## [2026-04-12-02] - Published archive sources and elder-friendly audio polish (Story 013)

### Added
- Added a central `Archive Sources` page that publishes the current root-level
  family PDFs and scans with direct open and download actions, including the
  featured `Onward to the Unknown.pdf` when it is present locally.

### Changed
- Updated the homepage to surface the archive library more clearly and to use
  warmer family-facing copy for older relatives.
- Refined the audiobook and chapter pages so the page headers use book/audio
  icon cues in the reading area, track rows stay compact, and every audiobook
  file now shows its runtime.

### Fixed
- Fixed the Rolland Alain memoir page so its original-PDF buttons resolve to
  the same published public source copy shown in the central archive library.
- Fixed lingering public-facing meta/process wording on the archive and
  audiobook pages, including the removed jump buttons and internal merge notes.

## [2026-04-12-01] - Polished the shared cross-page shell (Story 012)

### Changed
- Tightened the shared family-site shell so the homepage and audiobook hero
  headings stay stable on wide layouts while still wrapping naturally on
  smaller screens.
- Rebalanced the landing jump-row icon treatment and reused the same icon
  language in the homepage section headers so companion-media entry points read
  more consistently.

### Fixed
- Fixed the audiobook hero action row so the page no longer renders the stray
  stretched home button that appeared after the shared home-link change.

## [2026-04-11-09] - Shipped the first on-site audiobook surface (Story 011)

### Added
- Added a repo-owned audiobook manifest, dedicated audiobook page, chapter and
  supplement listening panels, and a maintained merged full-audiobook build
  command for the current static family-site surface.

### Changed
- Updated the whole-book builder, tests, runbooks, coverage matrix, and story
  graph so on-site audiobook delivery is tracked as a real partial surface
  rather than a planned-only lane.
- Refined the shared site navigation with a home icon, clickable site title,
  directional back/next cues, and icon-bearing landing-page jump buttons to
  keep the companion-media entry points clearer for readers.

## [2026-04-11-08] - Kept supplement wrappers reader-facing

### Changed
- Removed the Rolland memoir wrapper's public process note plus the raw
  imported-HTML and original-PDF actions so the surfaced page stays focused on
  reading rather than repository/process detail.
- Updated the presentation, input-contract, infrastructure, runbook, and deploy
  skill docs so they match the new public supplement policy and the deploy
  boundary for local maintenance artifacts.

### Fixed
- Fixed repeated local whole-book rebuilds leaving stale supplement directories
  behind after the public supplement bundle/PDF paths were removed.
- Fixed the static deploy helper so `_internal/` maintenance artifacts are
  excluded when publishing the generated whole-book shell.
- Regenerated three stale audiobook script chapters so the checked-in corpus
  again matches the current deterministic renderer and `make test` returns to
  green.

## [2026-04-11-07] - Shipped the Rolland Alain memoir family-story supplement (Story 007)

### Added
- Added the first repo-owned family-story supplement registry and accepted
  memoir bundle under `input/doc-web-html/`.
- Added a bounded `run-scanned-supplement` workflow to
  `scripts/doc_web_import.py` plus regression coverage for the non-TOC scanned
  supplement path.

### Changed
- Extended the local family-site builder so a checked-in supplement bundle can
  surface as a first-class family story with a short provenance preamble,
  imported-HTML link, and original-PDF download.
- Updated the memoir note copy on both the surfaced web page and generated
  audiobook chapter so they now use the same explicit photocopy-found wording
  supplied during close-out.
- Updated the input contract, presentation decisions, `doc-web` import runbook,
  README, omission-audit surface, and coverage matrix so the memoir supplement
  is documented as maintained project truth.

### Fixed
- Fixed the builder's absorbed-entry provenance handling so merged reader-facing
  pages keep the underlying absorbed provenance rows instead of silently
  dropping them from internal inspection output.

## [2026-04-11-06] - Promoted mobile to a first-class UI validation surface

### Added
- Added a fresh 2026-04-11 WB1 UI-scout rerun that records desktop and mobile
  evidence as co-equal pass/fail surfaces.

### Changed
- Rewrote the WB1 walkthrough runbook, UI-scout template, and central docs so
  mobile validation is required proof rather than a spot-check.
- Recorded explicit desktop/mobile viewport defaults in `state.ui_scout` and
  refreshed the latest UI-scout report pointer accordingly.
- Corrected `spec:7` so it reflects the real thin runtime plus manual
  desktop/mobile proof surface instead of claiming there is no runtime yet to
  evaluate.

## [2026-04-11-05] - Fixed `doc-web` runtime resolution for worktrees

### Changed
- Updated `scripts/doc_web_import.py` so repo-relative runtime paths can fall
  back to the primary git checkout when a Codex worktree does not have its own
  sibling `doc-web` checkout or local-only input PDF.
- Documented the worktree fallback behavior in the README and maintained
  `doc-web` import runbook so the repo truth matches the actual command path.

### Fixed
- Fixed `python scripts/doc_web_import.py contract` failing from this worktree
  even though the maintained sibling `doc-web` checkout exists beside the
  primary project checkout.

## [2026-04-11-04] - Noted ElevenReader distribution lanes in Story 008

### Changed
- Updated Story 008 to record the user-provided ElevenReader publish menu as
  scout input, listing the built-in candidate lanes to validate with
  primary-source research.

## [2026-04-11-02] - Added new planning stories for memoir and media lanes

### Added
- Added Story 007 for processing the Rolland Alain memoir through `doc-web`
  and surfacing it as a normalized family-story page with a short provenance
  preamble.
- Added Story 008 and Story 009 for scouting family-first, no-charge audiobook
  and podcast distribution options that stay easy for older listeners to use.
- Added Story 010 as a low-priority experiment for possible NotebookLM video
  companions.

### Changed
- Expanded Story 002 so it explicitly covers one whole-book NotebookLM podcast
  plus one podcast per family story, rather than leaving the scope ambiguous.
- Regenerated the story index and methodology graph to include the new planning
  slices and updated story statuses.

## [2026-04-11-03] - Built and verified the audiobook script corpus (Story 003)

### Added
- Added the repo-owned `audiobook-script/` Markdown corpus, deterministic
  builder entrypoints, regression tests, and a maintained ElevenLabs handoff
  runbook.

### Changed
- Narrowed the documented audiobook boundary to the verified spoken surface so
  the canonical corpus stays source-faithful while omitting figures, captions,
  tables, and headings that only introduce omitted tables.
- Clarified in story and runbook docs that ElevenLabs upload and final audio
  generation are downstream manual work, not part of the repo-owned
  implementation slice.

### Fixed
- Fixed the story/runbook contract drift around `20-i-wish.md` so it remains a
  poem-only epilogue instead of implying that the visual appendix should be
  spoken.
- Fixed the manual preamble formatting so prose paragraphs are no longer
  hard-wrapped in a way that causes ElevenLabs to insert sentence-ending pauses
  during paste/upload.

## [2026-04-11-01] - Refined whole-book presentation and archive flow

### Changed
- Reworked the whole-book landing page into `Opening Pages`, `Family Stories`,
  and `Closing Archive` so the surfaced site follows the book's reading flow
  more closely.
- Tightened the local builder's page presentation with mixed-case labels,
  centered front-matter leaves, sticky genealogy headers, inline-capable
  illustration treatment, and more restrained image sizing with full-image
  links.
- Updated the presentation decisions doc so it matches the current surfaced
  behavior for absorbed title leaves, deferred empty pages, and split archive
  photo material.

### Fixed
- Fixed the `page-001`/`page-002` opening-material merge so repeated title
  leaves are absorbed honestly instead of only being hidden in the omission
  audit.
- Fixed `chapter-024` so the poem stands alone and trailing archive photos
  render as separate closing-archive pages without missing-image placeholder
  noise.
- Fixed several page-level readability issues across the whole-book shell,
  including centered ancestry closing rows, cleaned index leaves, and more
  readable figure placement on narrative pages.

## [2026-04-10-04] - Refined the whole-book landing surface (Story 006)

### Added
- Added a dedicated internal UI-scout lane with a whole-book walkthrough
  runbook, report history, and methodology freshness tracking for the current
  website surface.
- Added Story 006 and its passing WB1 rerun report for the landing-page and
  page-label refinement slice.

### Changed
- Reoriented triage and methodology guidance toward manual refinement of the
  real whole-book website before adding deeper deterministic tooling.
- Shortened landing-card summaries and switched page/image cards and navigation
  to reader-facing display labels when the raw manifest title is only a
  placeholder.

### Fixed
- Fixed the public shell so `Pages & Images` no longer exposes placeholder-like
  titles such as `Image 1` or `Page i` when the page already contains a better
  label.
- Fixed duplicate browser titles on cover-like pages whose display label
  matches the site title.

## [2026-04-10-03] - Expanded the local builder to the full book (Story 005)

### Added
- Added a checked-in omission-audit snapshot at `docs/omission-audit.json` and
  mixed fixture coverage for a standalone page, a non-family chapter, and a
  family chapter.

### Changed
- Expanded the local `build-family-site` path into a whole-book reading surface
  with grouped landing sections, manifest-order navigation, and updated
  methodology/runbook truth surfaces.
- Moved provenance and source-manifest artifacts behind internal maintenance
  paths so the public reading surface stays focused on the book itself.

### Fixed
- Fixed the builder's default source resolution so `make build-family-site`
  works against the committed `input/` bundle without hidden env setup.

## [2026-04-10-02] - Built the first local family-site slice (Story 004)

### Added
- Added a thin local family-site builder, fixture-backed tests, and repo build
  commands for rendering the first accessible family-story slice from the
  staged `input/` bundle.
- Added `docs/input-contract.md` and `docs/presentation-decisions.md` to record
  the real staged-bundle contract and the first site-presentation rules.
- Added follow-up Story 005 for whole-book accessibility coverage and omission
  accounting beyond the family slice.

### Changed
- Updated repo docs, methodology state, and the golden-build runbook to reflect
  the first real local render path.
- Clarified that any source material omitted from reshaped surfaces must be an
  intentional, documented deferral rather than accidental loss.

## [2026-04-10-01] - Established DreamHost and Cloudflare deploy path (Story 001)

### Added
- Added infrastructure truth tracking in `docs/infrastructure.md` for DreamHost
  shared hosting, Cloudflare DNS, and the verified SFTP deploy path.
- Added follow-up Story 004 for the first local accessible family-pages site
  slice.
- Added a thin DreamHost static deploy command and repo-local `/deploy` skill
  for uploading the staged export over SFTP.

### Changed
- Rescoped Story 001 to the completed hosting and DNS substrate slice.
- Updated repo guidance to reflect the active `input/` intake boundary and the
  confirmed deploy environment.
- Reopened Story 001 so the first real static upload and deploy skill live with
  the infrastructure slice rather than the later site-shaping story.

## 2026-04-09

- Bootstrapped the repository with imported project skills from `doc-web`,
  greenfield methodology docs, skill sync wiring, and an initial methodology
  graph/compiler surface.
- Added the first explicit `doc-web` integration seam: repo-owned upstream
  manifest, local run/import wrapper, bundle validator, import snapshot
  metadata, and fixture-backed tests.
- Checked in the first committed source-material bundle for Onward: the staged
  `doc-web` HTML export plus companion archive PDFs and images needed for local
  evaluation and future site reshaping.
