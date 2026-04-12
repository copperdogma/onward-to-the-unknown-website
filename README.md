# Onward to the Unknown Website

This repo is the home for the public-facing website built around *Onward to the
Unknown* and its surrounding family-archive materials.

The current intake boundary is the local `input/` folder, which is expected to
hold the staged website/source material and companion assets this repo turns
into a real published site. This repo owns the website-specific layer:

- ingest or consume the staged source snapshot from `input/`
- normalize it into a site-friendly content model
- connect book chapters to companion media and scans
- present the material as a durable, navigable family archive site

The first accepted `doc-web` HTML export, the first accepted memoir supplement
bundle, and a curated set of companion archive assets are now committed under
`input/`. Local runtime snapshots stay uncommitted.

The current checked-in supplement seam is:

- main bundle: `input/doc-web-html/story206-onward-proof-r10/`
- supplement registry: `input/doc-web-html/family-story-supplements.json`
- first accepted supplement bundle: `input/doc-web-html/rolland-alain-memoir-r01/`
- preserved memoir source PDF:
  `input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf`

## Bootstrap Surface

This repo is currently bootstrapped with the shared methodology package and a
working local whole-book reading surface for the staged bundle.

Useful commands:

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
make preview-family-site
make deploy-static
make doc-web-contract
```

Operational environment truth lives in `docs/infrastructure.md`.

## Current State

The methodology package is installed. The repo now has a thin local builder
that renders the full staged book into an accessible whole-book reading
surface, keeps family stories grouped as a recognizable run, and emits an
inspectable omission audit at `docs/omission-audit.json`. The broader site
runtime is still partial, but the working mode is now hands-on website
refinement rather than abstract model-building. The next substantive work
should:

1. manually refine navigation, copy, layout, and accessibility on the real
   whole-book shell
2. use UI scouting to find the highest-friction pages and follow-up fixes
3. add deterministic tooling or deeper structure only where it removes repeated
   grunt work or protects against regressions and content loss

Currently confirmed infrastructure:

- Hosting provider: DreamHost
- Hosting plan: `Shared Unlimited`
- Public DNS for `copper-dog.com` is currently delegated to Cloudflare
- Static deploy command: `python scripts/deploy_static_site.py` (or
  `make deploy-static`)
- Deploy helper dependency: `python -m pip install -r requirements-deploy.txt`
- Deploy behavior: manifest-backed SFTP sync that can remove stale previously
  deployed files; when the source is `build/family-site/`, `_internal/`
  maintenance artifacts are not published

Current local build surface:

- Input contract: `docs/input-contract.md`
- Omission audit snapshot: `docs/omission-audit.json`
- Audiobook asset manifest: `audiobook/manifest.json`
- ElevenLabs audiobook MP3 set: `audiobook/ElevenLabs_Onward_to_the_Unknown/`
- Full merged audiobook build: `python scripts/build_full_audiobook.py`
  (or `make build-full-audiobook`); requires `ffmpeg` on `PATH`
- Audiobook script corpus: `audiobook/script/`
- Presentation decisions: `docs/presentation-decisions.md`
- Local whole-book reading-surface build: `python scripts/build_family_site.py`
  (or `make build-family-site`)
- Whole-book audiobook page output: `build/family-site/audiobook.html`
  when `audiobook/manifest.json` is present
- Full merged audiobook output:
  `audiobook/ElevenLabs_Onward_to_the_Unknown/full-audiobook.mp3`
  as a local generated artifact (not tracked in git)
- Audiobook script build: `python scripts/build_audiobook_script.py`
  (or `make build-audiobook-script`)
- Default local output: `build/family-site/`
- UI scout lane: `docs/ui-scout.md` and `docs/ui-scout/`
- Manual walkthrough runbook:
  `docs/runbooks/whole-book-ui-manual-walkthrough.md`
- Audiobook handoff runbook:
  `docs/runbooks/elevenlabs-audiobook.md`

Current UI proof requires a fresh WB1 walkthrough on both desktop and mobile.
Mobile is no longer treated as a spot-check surface.

## `doc-web` Integration

This repo now carries an explicit local integration manifest at
`doc-web-runtime.json` plus an upstream import wrapper at
`scripts/doc_web_import.py`.

When repo-relative paths in `doc-web-runtime.json` are missing from a git
worktree checkout, the wrapper now falls back to the primary checkout before
failing. That keeps the maintained sibling-`doc-web` contract usable from
Codex worktrees without hard-coding machine-specific absolute paths.

The intended flow is:

```bash
# Inspect the sibling checkout's contract payload
make doc-web-contract

# Run the maintained Onward recipe from the sibling checkout
python scripts/doc_web_import.py run-onward --run-id onward-book-r1 --force

# Snapshot the accepted bundle into this repo's local import root
python scripts/doc_web_import.py import-run --run-id onward-book-r1

# Build a bounded non-TOC scanned supplement bundle
python scripts/doc_web_import.py run-scanned-supplement \
  --run-id rolland-alain-memoir-r01 \
  --input-pdf "input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf" \
  --bundle-title "Rolland Alain Memoir Family Story" \
  --force
```

Accepted bundle snapshots are stored under `.runtime/doc-web-imports/` and are
local-only by default. Each snapshot records the source run id, bundle summary,
and the `doc-web` contract fingerprint that produced it.

The first committed accepted bundles live at
`input/doc-web-html/story206-onward-proof-r10/` and
`input/doc-web-html/rolland-alain-memoir-r01/`.
