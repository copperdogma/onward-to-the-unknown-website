# Runbook: Golden Build

This repo does not have a golden-build workflow yet because it does not have a
rendered site or import pipeline to benchmark.

That absence is intentional for the current bootstrap stage. Until the first
real import/render slice exists:

- treat `tests/fixtures/formats/_coverage-matrix.json` as the source inventory
  truth surface
- record any real measured checks in `docs/evals/registry.yaml`
- avoid claiming benchmark or golden coverage that the repo does not yet have

Once the first import and rendering path lands, replace this placeholder with:

- the golden corpus location
- the command(s) that regenerate or verify the slice
- the inspection points that define an acceptable result

