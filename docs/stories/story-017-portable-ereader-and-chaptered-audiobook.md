---
title: "Portable eReader and chaptered audiobook editions"
status: "Done"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "2. Connected Companion Media"
  - "3. Trustworthy Source Lineage"
  - "4. Reusable Content Model"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:2"
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "spec:7"
  - "C2"
  - "C4"
  - "C5"
  - "C6"
  - "C7"
adr_refs: []
depends_on:
  - "story-003-elevenlabs-full-audiobook"
  - "story-005-whole-book-accessible-reading-surface-and-omission-audit"
  - "story-011-first-on-site-audiobook-listening-surface"
category_refs:
  - "spec:2"
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "spec:7"
compromise_refs:
  - "C2"
  - "C4"
  - "C5"
  - "C6"
  - "C7"
input_coverage_refs:
  - "book-core-html"
  - "chapter-audio"
  - "full-book-audio"
  - "portable-ebook"
  - "chaptered-audiobook"
architecture_domains:
  - "content_model"
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "website, searchable PDF, individual MP3s, and optional merged MP3 without EPUB or chaptered audiobook downloads"
---

# Story 017 — Portable eReader and chaptered audiobook editions

**Priority**: High
**Status**: Done
**Decision Refs**: `docs/ideal.md`, `docs/spec.md`,
`docs/input-contract.md`, `docs/infrastructure.md`, `docs/RUNBOOK.md`,
`docs/runbooks/golden-build.md`, `docs/runbooks/elevenlabs-audiobook.md`,
`tests/fixtures/formats/_coverage-matrix.json`, Stories 003, 005, and 011,
the accepted `doc-web` bundle and omission audit, the Alain Lessard Story 005
handoff checklist, EPUB 3.3, EPUB Accessibility 1.1, EPUBCheck, and current
Apple, Amazon, Kobo, and Google import guidance; none found after search for a
repo-local portable-publication ADR
**Depends On**: Stories 003, 005, and 011

## Goal

Publish the trusted *Onward to the Unknown* family edition in two portable
formats that relatives can take into familiar reading and listening apps: a
reflowable, accessible EPUB 3 generated from the same complete, omission-
accounted reading model as the website, and one M4B generated directly from the
21 reviewed audiobook tracks with a named chapter for each track. Add warm,
large, plain-language direct download choices and short Apple Books, Kindle,
Kobo, Google Play Books, and audiobook-app instructions to the existing static
site without claiming that a browser can silently install files into another
app.

## Acceptance Criteria

- [x] A maintained deterministic command builds a DRM-free EPUB 3 from the
      accepted staged bundle and the same whole-book transformation path as the
      site, including the Rolland Alain memoir supplement, without hand-copied
      prose or dependence on already-rendered public page routes.
- [x] The EPUB contains a real cover, publication metadata, landmarks, table of
      contents, all 37 rendered main-book entries in reading order, the memoir
      supplement, every referenced meaningful figure/caption, responsive
      tables, a visible source/archive note, and all 520 visible semantic
      main-book source block ids exactly once; the two source figures that have
      no image asset remain intentionally absent rather than becoming empty
      placeholders.
- [x] EPUB content is reflowable and accessible: Canadian English language and
      title metadata, semantic headings, image alternative text, visible
      links, responsive images/tables, no website navigation/player chrome,
      scripting, or remote assets, and a packaged size below the current
      200 MB Send to Kindle ceiling.
- [x] The EPUB passes a repo-owned structural validator and the current
      official EPUBCheck release with zero errors; its contents, reflow,
      figures, captions, tables, links, and supplement are inspected in Apple
      Books and at least one independent renderer available in this pass.
- [x] A maintained deterministic command builds one `.m4b` directly from the
      21 reviewed MP3s in manifest order, inserts the manifest-configured
      pauses, performs one compatible AAC-LC encode, embeds a compact cover and
      title/album/author/narration metadata, and defines exactly 21 correctly
      named chapters.
- [x] M4B validation proves chapter numbering, names, order, boundaries,
      duration, codec, channel/sample profile, embedded cover, and metadata;
      representative beginning, middle, chapter-boundary, and ending samples
      decode successfully without changing the reviewed source MP3s.
- [x] The static release bundle publishes stable direct paths for the EPUB and
      M4B while retaining the searchable PDF, merged MP3 when built, and 21
      individual MP3s; release mode fails if a portable artifact is missing,
      empty, invalid, or not linked.
- [x] The family site adds a warm `Read or listen in another app` handoff with
      large literal EPUB, M4B, MP3, PDF, and help actions plus short Apple
      Books, Kindle/Send to Kindle, Kobo, Google Play Books, and generic
      audiobook-app steps. Direct downloads work without JavaScript, user-agent
      sniffing, brittle app deep links, account requirements, or a universal-
      install promise.
- [x] Focused fixtures cover EPUB package/source/image invariants, M4B chapter
      math and metadata, site copying/links, strict release failure, platform-
      help content, and ordinary no-JavaScript download links without copying
      the real media corpus into tests.
- [x] README, audiobook/runbook/infrastructure guidance, spec/state/coverage
      truth, and changelog describe the portable release and its public
      delivery honestly after fresh evidence exists.
- [x] Production serves the EPUB as `application/epub+zip` and the M4B as
      `audio/mp4` at stable paths with exact local byte lengths and working
      byte-range requests; live desktop and 390px mobile smoke checks cover the
      homepage, reading-app help, book, and audiobook handoff with no broken
      links, horizontal overflow, or browser-console errors.

## Out of Scope

- Publishing to Audible, Apple Books Store, Kindle Store, Kobo Store, Spotify,
  podcast directories, or any account-backed commercial catalog.
- DRM, purchases, account creation, or uploading files into a relative's
  third-party account on their behalf.
- MOBI/AZW3, fixed-layout EPUB, a bespoke reader app, synchronized read-along
  media overlays, or regenerating narration.
- Replacing the existing website reader, searchable source PDF, individual
  MP3s, merged MP3, or podcast surfaces.
- Claiming universal one-click installation where the platform requires a
  download, share sheet, upload, or USB sideload.

## Approach Evaluation

- **Simplification baseline**: The current baseline is zero `.epub`/`.m4b`
  files and zero portable-app links. One LLM call cannot create or prove ZIP/XML
  publication invariants, audio chapter boundaries, media profiles, or public
  byte delivery; deterministic code is the simpler baseline.
- **Candidate A — Pandoc plus the existing merged MP3**: quick scaffolding, but
  it would flatten/reconstruct the maintained reading model, risk source ids,
  figures, and tables, and add a second lossy encode from an already merged MP3.
- **Candidate B — repo-owned EPUB package plus manifest-driven M4B assembly**:
  consume the same rendered-entry model and supplement seam as the site, copy
  only referenced images, and build chapter timing directly from the 21 source
  tracks. Selected because it preserves lineage and makes validation explicit.
- **Candidate C — synchronized EPUB or W3C audiobook package**: expressive but
  poorly matched to familiar consumer-app imports and dependent on timing data
  the repo does not own.
- **AI-only**: Not appropriate for standards packaging, media conversion,
  chapter math, ZIP ordering, XML validation, or byte-level artifact checks.
- **Hybrid**: AI judgment can help review reader-facing language and rendered
  output, while deterministic builders and validators own release truth.
- **Pure code**: Correct for content transformation, image copying, metadata,
  chapter math, transcoding, static rendering, and validation.
- **Repo constraints / prior decisions**: `input/` remains the intake contract;
  binaries stay reproducible and ignored; `build/family-site/` remains the
  deploy source; source PDFs, reviewed MP3s, and accepted HTML stay unchanged.
- **Existing patterns to reuse**: `build_rendered_entries`, supplement
  insertion, `load_audiobook_catalog`, the audiobook manifest's pause and order,
  the direct-download site components, and the current SFTP deployment path.
- **Eval**: Small package/media/site fixtures establish the failing baseline;
  the full proof adds exact source coverage, official EPUBCheck, `ffprobe`
  assertions, representative media decodes, rendered app/browser inspection,
  and production MIME/length/range checks.

## Tasks

- [x] Add one tracked portable-edition manifest and focused failing fixtures
      for EPUB package/source/image rules, M4B chapter math/metadata, site
      copying/links, and release-mode failure.
- [x] Add focused `modules/` builders/validators plus thin `scripts/` commands
      for a complete EPUB 3 and manifest-driven chaptered M4B.
- [x] Extend the static site build with optional portable artifacts, strict
      release mode, stable MIME declarations, direct download/help surfaces,
      and PDF/MP3 fallbacks.
- [x] Build and inspect the real EPUB/M4B with official EPUBCheck, source/image
      audits, `ffprobe`, representative decodes, file-size/hash recording, and
      the available familiar/independent reader apps.
- [x] Update repo documentation and methodology truth after validation, not in
      advance of it.
- [x] If this story changes documented format coverage or graduation reality:
      update `tests/fixtures/formats/_coverage-matrix.json` and relevant
      methodology state honestly.
- [x] Check whether the chosen implementation makes any existing code, helper
      paths, or docs redundant; keep a single portable contract and remove
      repeated metadata/constants where practical.
- [x] Run required checks for touched scope:
  - [x] `make test`
  - [x] `make lint`
  - [x] focused portable build and validation commands
  - [x] full `make build-family-site RELEASE=1` plus artifact inspection
  - [x] `make methodology-compile`, `make methodology-check`, and
        `make skills-check`
- [x] Evals/goldens: no AI eval is expected; record deterministic fixture,
      standards, media, and renderer checks instead.
- [x] Search all docs and update any related to portable outputs, release
      validation, or deployment.
- [x] Run formal `/validate` across tracked and untracked changes, then fix any
      narrow current-story findings before release.
- [x] Deploy the exact validated `build/family-site/` bundle to the documented
      DreamHost path and prove the public EPUB/M4B MIME, bytes, links, and range
      behavior from `onward.copper-dog.com`.
- [x] Smoke the live homepage/help/book/audiobook flow at desktop and 390px
      mobile widths, then close via `/mark-story-done`; landing follows through
      `/check-in-diff`.
- [x] Verify Central Tenets:
  - [x] T0 — Traceability: EPUB entries/images and M4B chapters map to accepted
        manifests, source ids, and reviewed tracks.
  - [x] T1 — AI-First: AI is bounded to review judgment; deterministic tooling
        owns publication and media truth.
  - [x] T2 — Eval Before Build: the zero-artifact/link baseline and fixtures
        precede the implementation.
  - [x] T3 — Fidelity: all accepted reading blocks and reviewed audio order are
        preserved without editorial or narration changes.
  - [x] T4 — Modular: focused format modules consume existing contracts rather
        than fork the book or audio model.
  - [x] T5 — Inspect Artifacts: the EPUB is rendered/opened and the M4B is
        probed/decoded/listened to rather than trusted from exit codes alone.

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

- **Owning module / area**: New focused portable-publication and M4B modules
  own package/media generation and validation. Existing reading/audio contracts
  own order and lineage; the large site builder stays limited to copying,
  linking, and release-mode enforcement.
- **Methodology reality**: `spec:2`, `spec:4`, `spec:5`, `spec:6`, and `spec:7`
  all have partial substrate in the active bootstrap campaign. Coverage rows
  `book-core-html`, `chapter-audio`, and `full-book-audio` prove the inputs but
  do not yet record portable publication artifacts.
- **Substrate evidence**: the accepted manifest has 33 source entries; the
  current transformation produces 37 ordered main-book reading entries with
  520 visible semantic source block ids plus one 100-block Rolland memoir
  supplement; two empty source figures have no image asset and remain excluded.
  `audiobook/manifest.json` points to 21 present reviewed MP3 tracks in order
  with a four-second configured pause. `ffmpeg`, `ffprobe`, Java, lxml, and
  Pillow exist locally; the final EPUB passes the locally retained official
  EPUBCheck 5.3.0 jar with zero messages.
- **Data contracts / schemas**: Add one tracked portable manifest owning
  publication metadata, cover, generated/public paths, MIME types, size
  ceiling, codec profile, and expected entry/block/chapter counts. EPUB uses
  standard OCF/EPUB schemas; M4B chapter order stays derived from the existing
  audiobook manifest. No database or cross-repo schema changes.
- **File sizes**: `modules/build_family_site.py` is 4,977 lines and
  `tests/test_build_family_site.py` is 1,877 lines, so format logic and focused
  tests must remain outside them. `modules/build_full_audiobook.py` is 139
  lines and remains the merged-MP3 lane rather than becoming the M4B owner.
- **Decision context**: Reviewed the Ideal, spec, state, graph, coverage
  matrix, Stories 003/005/011/013/015/016, input/build/audio/deploy runbooks,
  and the Alain handoff. No ADR exists or is required because this adds
  deterministic outputs inside the existing static publishing boundary; a
  storefront, shared publication service, or new intake API would require one.

## Files to Modify

- `docs/stories/story-017-portable-ereader-and-chaptered-audiobook.md` — plan,
  evidence, and closure record (new)
- `portable/manifest.json` — sole portable publication/output contract (new)
- `modules/portable_editions.py`, `scripts/portable_editions.py` — EPUB build
  and validation (new)
- `modules/build_m4b.py`, `scripts/build_m4b.py` — chaptered audiobook build
  and validation (new)
- `modules/build_family_site.py` — thin portable copy/link/help/release seam
  (4,977 lines)
- `tests/test_portable_editions.py`, `tests/test_build_m4b.py` — focused small
  fixtures (new)
- `tests/test_build_family_site.py` — narrow integration assertions (1,877
  lines)
- `Makefile`, `.gitignore` — maintained commands and ignored binary outputs
- `README.md`, `audiobook/README.md`, `docs/RUNBOOK.md`,
  `docs/infrastructure.md`, `docs/spec.md`, `docs/methodology/state.yaml`,
  `tests/fixtures/formats/_coverage-matrix.json`, `AGENTS.md`, and
  `CHANGELOG.md` — durable truth after fresh proof

## Redundancy / Removal Targets

- Repeated EPUB/M4B filenames, MIME types, or publication metadata in builders,
  site rendering, and validation; `portable/manifest.json` is the sole manual
  contract.
- A second reading order or second audio chapter list; consume the maintained
  site transformation and audiobook manifest.
- User-agent-specific or pseudo-universal install links; keep ordinary direct
  downloads and clear platform guidance.
- Re-encoding the optional merged MP3; build M4B directly from reviewed tracks.

## Notes

This is a new Story 017 rather than reopening Story 003, 005, or 011 because
those stories closed on the reviewed MP3 corpus, complete web reading model,
and on-site player respectively. EPUB/M4B standards, third-party app handoff,
strict binary release validation, and public ranged delivery are a distinct
success surface. The user explicitly granted every human permission gate for
this execution on 2026-07-17.

## Plan

1. **Lock contracts and failing fixtures (S).** Add the portable manifest and
   small EPUB/audio/site fixtures. Done means tests express OCF ordering,
   metadata/navigation/spine, source/image coverage, chapter math/profile, and
   release-link failures while the baseline remains zero artifacts/links.
2. **Build the EPUB from the maintained reading model (L).** Reuse the exact
   entry grouping, absorption, split-page, supplement, and provenance seams;
   normalize XHTML, rewrite/copy referenced images, add cover/CSS/nav/package,
   and validate ZIP/XML/content graphs. Done means 38 content documents, all
   520 main ids once, prefixed supplement ids, local-only assets, and a
   sub-200 MB EPUB.
3. **Build the M4B directly from reviewed tracks (M).** Probe all 21 sources,
   derive chapter timing plus pauses, perform one AAC-LC encode, attach cover
   and metadata, and validate with `ffprobe`. Done means exactly 21 named,
   ordered chapters and representative decodes.
4. **Publish a literal, elder-friendly handoff (M).** Add one help page and
   large direct EPUB/M4B actions to existing book/audio/home surfaces while
   retaining PDF/MP3 options. Release mode and `.htaccess` fail closed on
   missing/invalid binaries or links; development builds remain usable before
   the generated binaries exist.
5. **Exercise real formats and renderers (L).** Build the full outputs, run the
   repo validators and official EPUBCheck, inspect the EPUB in Apple Books plus
   an independent renderer, probe/decode/listen to representative M4B samples,
   record sizes/hashes/tool versions, and inspect local desktop/mobile output.
6. **Align and validate the whole change (M).** Update durable docs/state/
   coverage only after proof, compile methodology, run all repo checks, audit
   tracked/untracked diffs, and require a formal `Close now` recommendation.
7. **Deploy and prove production (L).** Upload the exact strict bundle to the
   documented DreamHost path; verify public pages/links, MIME, exact bytes, and
   `206` ranges, then smoke desktop and 390px mobile UI and browser logs.
8. **Close and land (M).** Record production proof, check all tasks/criteria/
   tenets/gates, run `/mark-story-done`, commit intended files, sync safely,
   push `main`, and confirm the remote tip.

Impact/risk: malformed XHTML, duplicate ids, image-path rewriting, wide tables,
AAC compatibility, very large output transfer, and accidental growth in the
already-large site builder are the main risks. The user explicitly pre-
approved the build-story human gate and all later human permission gates, so
the written plan can proceed without another stop.

## Work Log

20260717-1607 — action: created Story 017 and completed build-story exploration
and planning under the user's explicit pre-approval; result: confirmed this is
a distinct portable-publication success surface and that the current repo has
enough substrate to build it without editorial changes; evidence: the accepted
bundle produces 37 ordered main reading entries with 520 visible source block
ids, the Rolland supplement contributes 100 blocks, the audiobook manifest has
21 present reviewed MP3s with a four-second pause, local `make test` passes all
47 tests, Ruff is clean, and no EPUB/M4B artifacts or portable links exist;
decision: use focused repo-owned EPUB/M4B modules, one portable manifest, the
existing reading/audio contracts, and a thin site integration rather than
Pandoc, the already-lossy merged MP3, synchronized media, or a second content
model; files at risk: the 4,977-line site builder, 1,877-line site test, ignored
binary outputs, and full static bundle; next step: mark the story In Progress,
add the contract and fixtures, and implement through the pre-approved plan.

20260717-1709 — action: implemented and exercised the portable-publication
contract, focused EPUB/M4B builders and validators, strict static-release seam,
literal help/download surfaces, deploy-process hardening, fixtures, and durable
operator/methodology guidance; result: the final local EPUB contains 38 content
documents, 42 referenced images, and all 520 main-book source ids in 105,785,550
bytes, while the M4B contains exactly 21 chapters and 3 streams over 10,745.765
seconds in 89,314,472 bytes; evidence: official EPUBCheck 5.3.0 reported zero
messages, repo validators passed, representative audio decoded at the start,
middle, chapter boundary, and ending, and strict site staging preserved exact
SHA-256 hashes `bf410a2e2426dc4bf7e2ff73a8c0c34415f9e9694b7160d980f369e7f2e361cb`
and `bcdf175637e9f2605e3d806c57f816bf2f15073d67a61efd59cabc5233bb69be`;
decision: keep generated binaries ignored and require release validation before
site copying; next step: complete formal validation, deploy the exact staged
bundle, and run public byte/UI checks.

20260717-1709 — action: inspected both real artifacts in familiar and
independent readers rather than relying on structural exit codes; result:
Apple Books imported the EPUB with all 38 TOC entries through the Rolland Alain
memoir on page 208, displayed the cover and representative illustration with
caption/alt text, and opened the memoir prose; Apple Books imported the M4B as
one audiobook, played and paused eight seconds successfully, and exposed all 21
ordered named tracks from `01. Preamble` through `21. I Wish`; evidence: the
independent EPUB renderer exposed a large-image pagination defect, the CSS was
corrected with a reader-resistant 420px image ceiling, and the final renderer
showed the Hereford photograph and caption on one page with no console errors;
decision: retain the focused EPUB CSS regression assertions because the reader
defect was invisible to EPUBCheck; next step: formal `/validate` and production
release.

20260717-1710 — action: ran formal `/validate` across every tracked and
untracked Story 017 file plus the final ignored artifacts and release bundle;
result: grade A, 98/100, recommendation `Proceed to release` with no
acceptance-blocking finding; evidence: completeness 20/20, correctness 20/20,
code quality 18/20, tests 20/20, and accessibility/resilience 20/20; `make
test` passed 55 tests, Ruff, methodology compile/check, skills check, focused
portable tests, official EPUB/M4B validation, four decode samples, exact staged
hash matching, `git diff --check`, and a 44-page/901-reference local crawl with
zero missing paths all passed; decision: the two-point quality deduction
reflects the necessarily large existing site-builder integration surface, not
a release blocker, because format logic remains in focused modules and the
site change is limited to copy/link/help enforcement; next step: deploy the
exact `build/family-site/` bundle and validate production.

20260717-1715 — action: deployed the exact strict `build/family-site/` bundle
to `/home/onward_user/onward.copper-dog.com` and exercised the production
release surface; result: SFTP completed with exit status 0, wrote the remote
manifest, and public validation passed for both artifacts and the help page;
evidence: the EPUB returned `application/epub+zip`, exactly 105,785,550 bytes,
and valid `206` range delivery; the M4B returned `audio/mp4`, exactly 89,314,472
bytes, and valid `206` range delivery; desktop `1280x900` and mobile `390x844`
checks covered `/`, `reading-apps.html`, `book.html`, and `audiobook.html`, all
four had viewport-equal scroll widths, the audiobook page exposed 21 players,
and browser logs were empty; decision: a Cloudflare 403 against Python's
default user agent warranted a narrow validator fix and regression test using
an explicit browser-compatible validator identity, after which the maintained
public command passed; next step: rerun the full post-deploy gate, mark Story
017 Done, and land the tracked change.

20260717-1716 — action: completed `/mark-story-done` after the production and
post-deploy gates; result: Story 017 is Done with every acceptance criterion,
implementation task, tenet, and workflow gate satisfied, and formal validation
recommendation `Close now` at grade A (98/100); evidence: 56 tests, Ruff,
methodology compile/check, skill sync check, official EPUBCheck, M4B validation,
strict release rebuild, public exact-byte/MIME/range validation, familiar-app
inspection, independent rendering, and desktop/mobile production smokes are
all green; decision: no follow-up story is required because remaining
storefront publication and DRM paths are explicitly out of scope, while the
existing PDF/MP3 fallbacks remain intact; next step: execute `/check-in-diff`,
push `main`, and confirm the remote tip.
