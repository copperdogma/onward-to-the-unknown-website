# Runbook

This repo is still in bootstrap mode, so the operative commands are currently
the methodology and skill-sync surfaces.

## Bootstrap Commands

```bash
python -m pip install -r requirements-deploy.txt
make skills-sync
make methodology-compile
make methodology-check
make deploy-static
```

## Current Truth

- the imported skill surface lives in `.agents/skills/`
- the staged source material is expected to live in the local `input/` folder
- infrastructure truth lives in `docs/infrastructure.md`
- there is no chosen long-term site runtime yet
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

When the first real import and render paths land, extend this runbook rather
than replacing the current honest static-upload path in the abstract.
