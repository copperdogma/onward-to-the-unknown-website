# AGENTS.md — Onward to the Unknown Website

Read this file at the start of every session.

> **Mission:** Turn *Onward to the Unknown* and its companion family-archive
> materials into a trustworthy, navigable website. The current intake boundary
> is the local `input/` folder, which holds the staged website/source material
> this repo needs to consume; this repo owns that intake contract, site
> structure, presentation, linked media surfaces, and publication workflow.
>
> **The Ideal (`docs/ideal.md`) is the primary decision filter.**
> Every compromise in `docs/spec.md` should point back to a named limitation and
> an honest evolution path.

## Ideal-First Methodology

**Graph + state structure:** `docs/ideal.md` captures the product and execution
ideal. `docs/spec.md` records active constraints against that ideal.
`docs/methodology/state.yaml` owns the mutable planning state,
`tests/fixtures/formats/_coverage-matrix.json` owns the machine-readable source
inventory, and `docs/methodology/graph.json` compiles those surfaces into a
single inspectable planning artifact. `docs/stories.md` is generated from that
graph.

**Operating rule:** planning starts from `docs/methodology/state.yaml`,
`docs/methodology/graph.json`, and
`tests/fixtures/formats/_coverage-matrix.json`. Implementation starts from the
active story, but you still need the relevant spec and state context first.

**Canonical bootstrap / refresh surface:** `/setup-methodology`

## Working Rules

- Treat `input/` as the current source contract unless the user explicitly
  redirects the project. If `doc-web` remains part of the historical source
  lineage, preserve that provenance, but do not assume a live repo-to-repo
  integration exists.
- Structure before presentation. Prefer canonical data/content artifacts that
  can feed multiple site views over one-off HTML fixes.
- Provenance matters. Links to audio, scans, and companion materials should be
  inspectable and traceable to their source record.
- Do not invent runtime commands or framework conventions that do not exist in
  this repo yet.
- No implicit commits or pushes.
- Fresh verification required. Do not claim a content transform, import seam,
  or site behavior is working unless it was checked in this pass.

## Skills

Canonical location: `.agents/skills/`

- Use `/setup-methodology` to install or refresh the methodology package
- Use `/triage` to choose the next highest-leverage slice
- Use `/align` after meaningful changes to sweep for methodology drift
- Run `scripts/sync-agent-skills.sh` after changing project skills

## Core Docs

- `docs/ideal.md` — product and execution ideals
- `docs/spec.md` — active project constraints with stable `spec:N` ids
- `docs/infrastructure.md` — hosting, DNS, and deployment truth surface
- `docs/input-contract.md` — current staged-bundle intake contract
- `docs/omission-audit.json` — current manifest-entry coverage accounting snapshot
- `docs/presentation-decisions.md` — first recorded site-presentation choices
- `docs/methodology/state.yaml` — mutable planning state
- `docs/methodology/graph.json` — compiled methodology view
- `docs/setup-checklist.md` — working setup checklist
- `docs/evals/README.md` — eval registry protocol
- `docs/evals/registry.yaml` — eval source of truth
- `docs/runbooks/setup-methodology.md` — setup/refresh runbook
- `docs/runbooks/doc-web-import.md` — local `doc-web` run/import contract for this repo
- `docs/runbooks/golden-build.md` — honest statement of current golden/build proof surface
- `docs/scout.md` — scout expedition index
- `docs/stories.md` — generated story index
- `docs/stories/` — story files
- `docs/decisions/` — decision records
- `CHANGELOG.md` — repo change log
- `doc-web-runtime.json` — local upstream manifest for the sibling `doc-web` checkout

## Current Repo Reality

This repo now has a verified DreamHost/Cloudflare deploy path and a thin local
whole-book reading-surface builder with omission accounting, but it still does
not have a fully generalized frontend stack or final site shell. Treat any
broader runtime surface as genuinely missing, not implied.
