# Changelog

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
