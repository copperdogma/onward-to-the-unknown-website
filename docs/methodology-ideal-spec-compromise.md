# The Ideal-First Methodology

## TLDR

This repo starts from two authored north stars:

- the **Product Ideal** in `docs/ideal.md`
- the **Execution Ideal** in `docs/ideal.md`

`docs/spec.md` then records the active compromises between that ideal and the
current project reality. Mutable planning state lives in
`docs/methodology/state.yaml`, the machine-readable source inventory lives in
`tests/fixtures/formats/_coverage-matrix.json`, and
`docs/methodology/graph.json` compiles those surfaces into one inspectable view.

The goal is not to preserve process forever. The goal is to make every layer of
extra machinery easy to delete once the corresponding limitation stops being
real.

## What It Produces

1. **Ideal** — `docs/ideal.md`
2. **Spec** — `docs/spec.md`
3. **Structured Methodology State** — `docs/methodology/state.yaml`
4. **Coverage Matrix** — `tests/fixtures/formats/_coverage-matrix.json`
5. **Compiled Graph** — `docs/methodology/graph.json`
6. **Generated Views** — `docs/stories.md`
7. **Decision Records** — `docs/decisions/`
8. **Stories** — `docs/stories/`
9. **Evals** — `docs/evals/registry.yaml`

## Core Idea

The method is simple:

1. describe what the project should look like without current limitations
2. describe what reality forces us to do instead
3. keep that workaround explicitly tied to a named limitation
4. delete or shrink the workaround when the limitation changes

For this repo, common early examples include:

- importing from `doc-web` HTML because there is not yet a richer maintained
  upstream contract
- manually curating companion media because those materials are not yet in a
  canonical inventory
- carrying setup, story, and eval scaffolding because AI and human memory still
  drift across long-running archival work

## Product Constraints vs Execution Constraints

**Product constraints** affect what the site and content pipeline can do.

Examples here:

- the initial import seam is still HTML-centric
- companion media metadata is incomplete
- the frontend/runtime choice is not yet fixed

**Execution constraints** affect how the project has to be built right now.

Examples here:

- keeping an explicit methodology state and compiled graph
- keeping an eval registry even before the first runtime exists
- documenting the `doc-web` relationship instead of assuming it will stay in
  someone's head

## Phase Governance

Each compromise carries a phase in `docs/methodology/state.yaml`:

- `climb` — improve or establish the missing substrate
- `hold` — protect an honest working floor without adding sprawl
- `converge` — simplify or delete the workaround

This helps distinguish useful growth from premature complexity.

## Operating Rule

Planning starts from:

- `docs/methodology/state.yaml`
- `docs/methodology/graph.json`
- `tests/fixtures/formats/_coverage-matrix.json`

Implementation starts from the active story, but the story still needs the
relevant `spec:N` context.

## Why The Graph Exists

The compiled graph is a lightweight join surface. It keeps the authored canon,
mutable planning state, and source inventory aligned for AI and human readers.

If the graph, checklist, or eval surfaces stop paying for themselves, they
should be simplified. They are scaffolding, not a sacred ritual.

