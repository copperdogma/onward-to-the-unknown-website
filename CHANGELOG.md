# Changelog

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
