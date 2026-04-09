# Eval Registry System

Central tracking for eval metrics, verified attempts, and quality-floor signals.

Baseline eval-surface setup belongs to `/setup-methodology`.

- Use `/improve-eval` to iterate on existing evals.
- Use this README plus the attempt template when a new eval must be scaffolded.

## Structure

```text
docs/evals/
├── registry.yaml
├── attempt-template.md
├── attempts/
└── README.md
```

## What Should Eventually Be Measured Here

Likely early eval families for this repo:

- import fidelity from `doc-web` into the canonical site model
- chapter/media linkage integrity
- link rot or missing-asset checks
- accessibility checks on real rendered pages
- performance checks on the first real site slice

## Registry Protocol

Update `docs/evals/registry.yaml` whenever an eval is run or materially
re-verified.

Every new eval entry should carry explicit lineage:

- `story_refs`
- `category_refs`
- `compromise_refs`
- `spec_refs` when the direct spec linkage matters

The goal is to answer "why does this eval exist?" without scraping prose notes.

## Staleness

A score is stale if the relevant content model, render path, benchmark assets,
or scoring surface changed materially after the recorded baseline.

When in doubt, re-measure.

## Improvement Attempts

For non-trivial or ambiguous retries:

1. copy `docs/evals/attempt-template.md`
2. create `docs/evals/attempts/{NNN}-{eval-id}-{short-title}.md`
3. summarize the prior attempts first
4. record the before/after state and retry conditions

## Principle

Do not create fake eval completeness for surfaces that do not exist yet. Be
honest about what can be measured today.

