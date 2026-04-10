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

`input/` is intentionally gitignored because the family/source material is
local working data rather than committed repo content.

## Bootstrap Surface

This repo is currently bootstrapped with the shared methodology package and an
initial planning surface for the site work.

Useful commands:

```bash
python -m pip install -r requirements-deploy.txt
make skills-sync
make methodology-compile
make methodology-check
make deploy-static
```

Operational environment truth lives in
[`docs/infrastructure.md`](/Users/cam/.codex/worktrees/4201/onward-to-the-unknown-website/docs/infrastructure.md).

## Current State

The methodology package is installed. The current deploy path can already ship
an existing static bundle to DreamHost shared hosting, but the long-term site
runtime has not been chosen yet. The next substantive work should define:

1. the intake contract for the staged source material in `input/`
2. the canonical content/data model for the website
3. the first end-to-end website slice for one chapter plus linked media
4. the first reshaped website slice beyond the raw staged export now being
   used for infrastructure proof

Currently confirmed infrastructure:

- Hosting provider: DreamHost
- Hosting plan: `Shared Unlimited`
- Public DNS for `copper-dog.com` is currently delegated to Cloudflare
- Static deploy command: `python scripts/deploy_static_site.py` (or
  `make deploy-static`)
- Deploy helper dependency: `python -m pip install -r requirements-deploy.txt`
- Deploy behavior: manifest-backed SFTP sync that can remove stale previously
  deployed files
