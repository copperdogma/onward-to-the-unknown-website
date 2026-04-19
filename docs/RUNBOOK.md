# Runbook

This repo is still in bootstrap mode, so the operative commands are currently
the methodology and skill-sync surfaces.

## Bootstrap Commands

```bash
python -m pip install -r requirements-deploy.txt
make skills-sync
make methodology-compile
make methodology-check
make test
make lint
make build-family-site
make build-audiobook-script
make build-full-audiobook
make refresh-omission-audit
make deploy-static
make doc-web-contract
```

## Current Truth

- the imported skill surface lives in `.agents/skills/`
- the staged source material is expected to live in the local `input/` folder
- infrastructure truth lives in `docs/infrastructure.md`
- the first local site runtime exists as a thin whole-book static builder in
  `scripts/build_family_site.py`
- the current input-bundle contract is documented in `docs/input-contract.md`
- the current whole-book omission-audit snapshot lives at
  `docs/omission-audit.json`
- the current audiobook asset manifest lives at `audiobook/manifest.json`
- the current podcast asset manifest lives at `podcast/manifest.json`
- the active presentation choices are documented in
  `docs/presentation-decisions.md`
- UI product-truth scouting now lives in `docs/ui-scout.md` and
  `docs/ui-scout/`
- there is still no fully generalized long-term site runtime yet
- the first committed accepted source bundle lives under
  `input/doc-web-html/story206-onward-proof-r10/`
- the current deploy command is `python scripts/deploy_static_site.py` (or
  `make deploy-static`), which uploads an existing static bundle to the
  DreamHost shared-hosting site path over SFTP using the local gitignored
  `.env`
- the deploy helper currently depends on `pexpect`, installed via
  `python -m pip install -r requirements-deploy.txt`
- the deploy helper maintains a remote `.deploy-manifest.json` so repeat
  deploys can remove files that were deleted locally
- when the deploy source is `build/family-site/`, `_internal/` stays a local
  maintenance surface and is excluded from the published payload

Current default deploy payload: the staged `doc-web` export bundle at
`input/doc-web-html/story206-onward-proof-r10` via
`DREAMHOST_DEPLOY_SOURCE_DIR` in the local `.env`.

The current operating mode is manual refinement of the whole-book website until
it is ready to ship. Add deterministic tooling only where it removes repeated
grunt work or protects the reading surface from regressions.

## Local Whole-Book Slice

Build the current local whole-book reading surface:

```bash
make build-family-site
```

Override the bundle path if needed:

```bash
make build-family-site SOURCE=/absolute/path/to/bundle
```

Preview the generated output locally:

```bash
make preview-family-site
```

That serves `build/family-site/` on `http://127.0.0.1:4173` by default.

Refresh the checked-in omission-audit snapshot from the current accepted
bundle:

```bash
make refresh-omission-audit
```

Validation commands for the current local builder:

```bash
make test
make lint
make methodology-compile
make methodology-check
```

## Audiobook Script Corpus

Build the source-derived audiobook chapters from the staged bundle:

```bash
make build-audiobook-script
```

Regenerate those source-derived chapters only when you intentionally want to
refresh them from the HTML source:

```bash
make build-audiobook-script FORCE=1
```

The manual preamble lives at `audiobook/script/01-preamble.md` and is not
touched by the generator. See `docs/runbooks/elevenlabs-audiobook.md` for the
source-fidelity review and ElevenLabs handoff flow.

## Full Audiobook Build

Build the merged full-audiobook MP3 from the ordered manifest track set:

```bash
make build-full-audiobook
```

This command requires `ffmpeg` on `PATH`.

By default this writes to the manifest-declared path:

```text
audiobook/ElevenLabs_Onward_to_the_Unknown/full-audiobook.mp3
```

Treat that file as a local generated artifact rather than tracked repo source.
Rebuild it before `make build-family-site` or deploy prep whenever you want the
full-book play/download controls included in the published site bundle.

Pass `FORCE=1` if you intentionally want to rebuild and replace the current
merged file:

```bash
make build-full-audiobook FORCE=1
```

## On-Site Audiobook Surface

The whole-book site build now reads `audiobook/manifest.json` when it exists.
That manifest points at the reviewed MP3 files under
`audiobook/ElevenLabs_Onward_to_the_Unknown/` and lets the builder:

- copy the referenced MP3 files into `build/family-site/audiobook/`
- emit `build/family-site/audiobook.html`
- expose the merged full-audiobook file for direct play and download when it
  exists
- add a page-level listening panel to matching chapters or supplements

To refresh that surface locally:

```bash
make build-family-site
```

For a quick manual inspection after the build, check:

- `build/family-site/index.html`
- `build/family-site/audiobook.html`
- `build/family-site/podcast.html`
- a representative chapter page such as `build/family-site/chapter-009.html`
- the memoir supplement page when present:
  `build/family-site/rolland-alain-memoir-family-story.html`

For the current family-facing launch plan, treat this site-hosted surface as
the canonical audiobook lane. The expected reader path is simple browser play
or direct MP3 download with no app or account requirement. External platforms
such as Spotify, ElevenReader, or Voices by INaudio are optional follow-up
lanes, not prerequisites for shipping the current audiobook surface.

## On-Site Podcast Surface

The whole-book site build now also reads `podcast/manifest.json` when it
exists. That manifest points at the reviewed MP3 files under `podcast/` and
lets the builder:

- copy the referenced MP3 files into `build/family-site/podcast/`
- emit `build/family-site/podcast.html`
- expose the full-book episode for direct browser play and download when it
  exists
- add a page-level podcast panel to matching chapters

To refresh that surface locally:

```bash
make build-family-site
```

For a quick manual inspection after the build, check:

- `build/family-site/index.html`
- `build/family-site/podcast.html`
- a matching chapter page such as `build/family-site/chapter-002.html`

For the current family-facing launch plan, treat this site-hosted surface as
the canonical podcast lane. The expected reader path is simple browser play or
direct MP3 download with no app or account requirement. External podcast feeds
or directory listings remain optional follow-up lanes, not prerequisites for
shipping the current podcast surface.

## External Audio Distribution Guidance

Scout 003 keeps the website as the canonical home for both audio surfaces and
recommends this external order only if a duplicate lane is later added:

1. emit one public podcast RSS feed from the repo-owned site
2. submit that feed to Apple Podcasts
3. claim that same feed on Spotify
4. treat Pocket Casts, Overcast, and YouTube Music as optional follow-on
   conveniences for listeners who already use those apps

No public podcast RSS feed exists in repo output yet. If that feed is built
later, prefer keeping it on `onward.copper-dog.com` beside the current MP3
assets rather than moving the project to a paid podcast host.

Dedicated audiobook-platform duplication is still optional later work. Under
the current no-charge family constraint, the direct website flow and any future
podcast-feed duplicate remain better first fits than audiobook storefronts or
retail networks.

## UI Scout Lane

Use the dedicated internal UI-scout lane when walking the current website like
a real reader:

- index and freshness: `docs/ui-scout.md`
- dated reports: `docs/ui-scout/`
- walkthrough instructions:
  `docs/runbooks/whole-book-ui-manual-walkthrough.md`

This lane is for manual website refinement on the real whole-book shell, not
for external research.

A current-pass UI proof now requires both desktop and mobile evidence through
that lane. Mobile is not a spot-check.

## `doc-web` Commands

```bash
make doc-web-contract
python scripts/doc_web_import.py run-onward --run-id onward-book-r1 --force
python scripts/doc_web_import.py import-run --run-id onward-book-r1
```

See `docs/runbooks/doc-web-import.md` for the maintained upstream/import flow.

Keep extending this runbook from the real local builder, deploy, and import
paths rather than replacing them in the abstract.
