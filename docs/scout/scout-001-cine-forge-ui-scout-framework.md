# Scout 001 — cine-forge-ui-scout-framework

**Source:** `/Users/cam/Documents/Projects/cine-forge`
**Scouted:** 2026-04-10
**Scope:** Port CineForge's dedicated internal UI-scout lane, freshness
tracking, and triage pressure into this repo, adapted to the whole-book reading
surface instead of CineForge's app-specific walkthroughs
**Previous:** None
**Status:** Done

## Findings

1. **A dedicated internal UI-scout lane is better than burying site walkthroughs in generic notes** — HIGH value
   What: CineForge keeps internal product-truth runs in `docs/ui-scout.md` and
   `docs/ui-scout/`, explicitly separate from external-source `docs/scout/`.
   Us: This repo had no dedicated lane for repeated website walkthroughs, so
   manual refinement pressure would have lived in ad hoc chat memory or generic
   scout notes.
   Recommendation: Adopt inline
   Transfusion:
   Exemplar: `/Users/cam/Documents/Projects/cine-forge/docs/ui-scout.md` and
   `/Users/cam/Documents/Projects/cine-forge/docs/ui-scout/_template.md`
   Invariant: Internal product-truth walkthrough history must live in a
   dedicated lane separate from external research
   Adaptation: Keep one scenario centered on this repo's whole-book reading
   surface instead of CineForge's full-pipeline app flow
   Proof target: This repo gains `docs/ui-scout.md`, `docs/ui-scout/`, and a
   single canonical scenario `WB1`

2. **Machine-readable UI freshness is what keeps manual refinement from disappearing** — HIGH value
   What: CineForge records `state.ui_scout` freshness so triage can see whether
   product truth is stale, never run, or awaiting recheck.
   Us: This repo had no machine-readable signal for website walkthrough
   freshness, so triage could ignore real site quality pressure.
   Recommendation: Adopt inline
   Transfusion:
   Exemplar: `/Users/cam/Documents/Projects/cine-forge/docs/methodology/state.yaml`
   `ui_scout`
   Invariant: UI scouting must be visible in canonical planning state, not only
   in markdown notes
   Adaptation: Use a minimal single-scenario `WB1` block and start it at
   `never` until the first site walkthrough is run
   Proof target: `docs/methodology/state.yaml` carries `ui_scout`, and triage
   can inspect it

3. **Triage should treat manual site refinement and stale UI truth as first-class work** — HIGH value
   What: CineForge teaches `/triage` to inspect UI-scout freshness before
   outranking real surfaced-product issues with unrelated abstraction work.
   Us: Local triage was over-biasing toward schema/tooling-first recommendations
   even after a real whole-book website surface existed.
   Recommendation: Adopt inline
   Transfusion:
   Exemplar: `/Users/cam/Documents/Projects/cine-forge/.agents/skills/triage/SKILL.md`
   and `/Users/cam/Documents/Projects/cine-forge/docs/runbooks/triage.md`
   Invariant: Stale or missing UI product truth must count as a real triage
   signal
   Adaptation: Point the hook at this repo's whole-book reading surface and
   manual ship-readiness work, not CineForge's app routes or scenario matrix
   Proof target: Local triage skill language now explicitly recognizes manual
   site refinement and `state.ui_scout`

4. **CineForge's exact walkthrough routes and app-specific taxonomy should not be copied literally** — MEDIUM value
   What: CineForge's runbook is built around its own product routes, fixture,
   and app workflow.
   Us: This repo is a book website with a different surfaced path and no need
   for CineForge's route-by-route app walkthrough.
   Recommendation: Skip
   Transfusion:
   Exemplar: `/Users/cam/Documents/Projects/cine-forge/docs/runbooks/full-pipeline-ui-manual-walkthrough.md`
   Invariant: Keep one canonical product-truth walkthrough
   Adaptation: Replace CineForge's app flow with a whole-book landing page plus
   representative reading-page walkthrough
   Proof target: This repo gains a website-specific manual walkthrough runbook,
   not a copied app checklist

## Approved

- [x] 1. Dedicated internal UI-scout lane — Approved inline by user request on
      2026-04-10
- [x] 2. Machine-readable UI-scout freshness — Approved inline by user request
      on 2026-04-10
- [x] 3. Triage hook for UI truth and manual refinement — Approved inline by
      user request on 2026-04-10

## Skipped / Rejected

- 4. CineForge's literal app-route walkthrough and taxonomy — rejected because
  the user asked to adapt the framework to this website, not cargo-cult
  CineForge's product-specific flow

## Verification

- `make methodology-compile`
- `make methodology-check`
- `./scripts/sync-agent-skills.sh`
- `./scripts/sync-agent-skills.sh --check`
- `make skills-check`
- `git diff --check`

## Evidence

- Source evidence reviewed:
  - `/Users/cam/Documents/Projects/cine-forge/docs/ui-scout.md`
  - `/Users/cam/Documents/Projects/cine-forge/docs/ui-scout/_template.md`
  - `/Users/cam/Documents/Projects/cine-forge/docs/scout/scout-020-storybook-ui-scouting-delta.md`
  - `/Users/cam/Documents/Projects/cine-forge/.agents/skills/triage/SKILL.md`
  - `/Users/cam/Documents/Projects/cine-forge/docs/runbooks/triage.md`
  - `/Users/cam/Documents/Projects/cine-forge/docs/runbooks/full-pipeline-ui-manual-walkthrough.md`
- Local changes landed in:
  - `.agents/skills/triage/SKILL.md`
  - `.agents/skills/triage-stories/SKILL.md`
  - `docs/methodology/state.yaml`
  - generated `docs/methodology/graph.json`
  - generated `docs/stories.md`
  - `docs/ui-scout.md`
  - `docs/ui-scout/_template.md`
  - `docs/runbooks/whole-book-ui-manual-walkthrough.md`
  - `docs/scout.md`
  - `README.md`
  - `docs/RUNBOOK.md`
