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
