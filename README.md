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
make test
make lint
make build-family-site
make preview-family-site
make deploy-static
```

Operational environment truth lives in
[`docs/infrastructure.md`](/Users/cam/.codex/worktrees/4201/onward-to-the-unknown-website/docs/infrastructure.md).

## Current State

The methodology package is installed. The repo now has a first local
family-site builder that reshapes the staged export into a more accessible
family-story slice, but the broader site runtime is still partial. The next
substantive work should define:

1. the broader canonical content/data model for the website
2. how the non-family chapters and standalone page/image surfaces should be
   presented
3. chapter/media linkage beyond the first reading slice
4. whether the local family-site approach should become the foundation for the
   wider site shell

Currently confirmed infrastructure:

- Hosting provider: DreamHost
- Hosting plan: `Shared Unlimited`
- Public DNS for `copper-dog.com` is currently delegated to Cloudflare
- Static deploy command: `python scripts/deploy_static_site.py` (or
  `make deploy-static`)
- Deploy helper dependency: `python -m pip install -r requirements-deploy.txt`
- Deploy behavior: manifest-backed SFTP sync that can remove stale previously
  deployed files

Current local build surface:

- Input contract: [`docs/input-contract.md`](/Users/cam/.codex/worktrees/4201/onward-to-the-unknown-website/docs/input-contract.md)
- Presentation decisions: [`docs/presentation-decisions.md`](/Users/cam/.codex/worktrees/4201/onward-to-the-unknown-website/docs/presentation-decisions.md)
- Local family-site build: `python scripts/build_family_site.py` (or
  `make build-family-site`)
- Default local output: `build/family-site/`
