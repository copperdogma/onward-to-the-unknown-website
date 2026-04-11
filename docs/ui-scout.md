# UI Scout Runs

Internal product-truth scouting log for the website's own surfaced reading
experience.

This lane is intentionally separate from `docs/scout/`, which is reserved for
external-source research. Use this lane when the work is: "walk the current
website like a real reader, record what feels excellent, and record what still
blocks shipping."

Companion runbook: `docs/runbooks/whole-book-ui-manual-walkthrough.md`

Machine-readable freshness source: `docs/methodology/state.yaml` `ui_scout`

## Canonical Scenario Coverage

| Scenario | Goal | Last Checked | Notes |
|---|---|---|---|
| WB1 — Whole-Book Reading Surface | Build the accepted bundle through the current whole-book shell, then walk the key reading paths on desktop and mobile as co-equal required proof surfaces until the site feels honest, legible, and ready to ship for older family readers | 2026-04-11 | Initial runs found landing-page scan fatigue and generic page/image labels. The Story 006 rerun cleared those shell issues, and the 2026-04-11 rerun hardened the validation contract so mobile is no longer a spot-check. |

## Run Index

| Date | Scenario | Surface | Follow-Up | Status |
|---|---|---|---|---|
| [2026-04-10 local walkthrough](ui-scout/2026-04-10-whole-book-local.md) | `WB1` | `build/family-site/` | [006](stories/story-006-whole-book-landing-scannability-and-page-label-clarity.md) | Issues Found |
| [2026-04-10 Story 006 rerun](ui-scout/2026-04-10-whole-book-local-story-006-rerun.md) | `WB1` | `build/family-site/` | `/validate` on [006](stories/story-006-whole-book-landing-scannability-and-page-label-clarity.md) | Pass |
| [2026-04-11 mobile-first-class rerun](ui-scout/2026-04-11-whole-book-local-mobile-first-class.md) | `WB1` | `build/family-site/` | Validation-surface hardening | Pass |

## Operating Notes

- Keep this markdown lane and `state.ui_scout` in sync on every run so triage
  can see whether website product truth is stale.
- Keep this repo on one canonical scenario until repeated real use proves that
  a second scenario is needed. Do not invent taxonomy for its own sake.
- A `Pass` now requires explicit desktop and mobile evidence. Mobile is not a
  spot-check or tie-break surface.
- Older reports that still say `mobile spot-check` remain valid history, but
  they predate the stricter dual-surface proof contract.
- If a run finds a product defect, keep the failed report and link the focused
  follow-up story instead of rewriting history into a green-only log.
- This lane exists to prioritize manual website refinement on the real surfaced
  site, not to create a second external research system.
