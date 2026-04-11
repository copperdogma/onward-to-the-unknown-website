---
title: "Rolland Alain Memoir Family Story"
status: "Pending"
priority: "Medium"
ideal_refs:
  - "1. Canonical Book Experience"
  - "2. Connected Companion Media"
  - "3. Trustworthy Source Lineage"
  - "4. Reusable Content Model"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:1"
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "C1"
  - "C2"
  - "C3"
  - "C4"
  - "C5"
  - "C6"
adr_refs: []
depends_on:
  - "story-005"
  - "story-006"
category_refs:
  - "spec:1"
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:5"
  - "spec:6"
compromise_refs:
  - "C1"
  - "C2"
  - "C3"
  - "C4"
  - "C5"
  - "C6"
input_coverage_refs:
  - "book-core-html"
  - "scanned-supplements"
architecture_domains:
  - "upstream_integration"
  - "content_model"
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "manual family-archive PDF supplement found as a photocopy inside the user's bound copy"
---

# Story 007 — Rolland Alain Memoir Family Story

**Priority**: Medium
**Status**: Pending
**Decision Refs**: `docs/runbooks/doc-web-import.md`, `docs/input-contract.md`, `docs/presentation-decisions.md`, `docs/omission-audit.json`, `tests/fixtures/formats/_coverage-matrix.json`, none found after search for repo-local ADRs or supplement-intake runbooks
**Depends On**: Stories 005 and 006

## Goal

Process `input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf`
through the existing `doc-web` seam, normalize the resulting HTML so it reads
like the other family stories, and surface it on the website as `Rolland Alain
Memoir Family Story` with an honest short provenance note explaining that the
memoir was found as a photocopy inside the user's original book copy and may
have either missed the original publishing deadline or been distributed later
at the reunion.

## Acceptance Criteria

- [ ] The memoir PDF is run through `doc-web` and lands in a validated import
      shape the repo can consume without inventing a second one-off PDF path.
- [ ] The repo defines an honest placement and normalization rule for the
      memoir, including its displayed title, family-story placement, and source
      provenance without overclaiming how or when it joined the archive.
- [ ] The public site can surface the memoir through the family-story area with
      a very short preamble explaining that it was found as a photocopy in the
      user's copy of the book and may represent either a late-added or
      separately distributed reunion document.
- [ ] The original PDF remains inspectable as source material, and the import /
      omission / coverage truth is updated so this supplement is no longer an
      untracked sidecar file.

## Out of Scope

- Proving the exact historical reason the memoir was not part of the bound
  book.
  beyond what is needed to normalize the memoir into the current family-story
  format.
- A generalized supplement-gallery system for every future PDF in the family
  archive.

## Approach Evaluation

- **Simplification baseline**: A straight `doc-web` conversion plus a thin
  normalization pass may already be enough to make the memoir read like the
  other family stories, so measure that before inventing special-case PDF
  transformation logic.
- **AI-only**: Useful for rough OCR or summary drafting, but weak on provenance
  language and family-story placement unless a human verifies every claim.
- **Hybrid**: Strongest fit. Keep the original PDF, add a human-reviewed
  provenance note, and only use automation for extraction or presentation where
  it reduces tedious cleanup.
- **Pure code**: Adequate for normalization and site integration once `doc-web`
  provides HTML, but not sufficient alone if the preamble needs careful
  editorial framing.
- **Repo constraints / prior decisions**: The current input contract and local
  builder only cover the staged `doc-web` HTML bundle for the main book.
  Supplementary scans are acknowledged in the coverage matrix but still
  `planned`, and the existing public surface intentionally hides provenance
  commentary from reader pages.
- **Existing patterns to reuse**: Reuse the `doc-web` import runbook and
  validation seam, then extend the whole-book builder, omission-audit
  expectations, and family-story landing treatment from Stories 005 and 006
  instead of inventing a separate microsite for one memoir.
- **Eval**: Import one memoir bundle through `doc-web`, normalize it into the
  family-story shape, then inspect the surfaced page on desktop and mobile to
  confirm the story is easy to find, the short preamble is honest, and the
  source PDF remains reachable.

## Tasks

- [ ] Run the memoir PDF through `doc-web` and validate the resulting bundle or
      imported snapshot through the existing import seam.
- [ ] Inspect the generated HTML and decide the thinnest normalization needed
      to make it match the current family-story reading format.
- [ ] Define the canonical metadata for this supplement: displayed title,
      family-story placement, source note, and the exact short preamble
      language that preserves the provenance uncertainty.
- [ ] Extend the local site build so the memoir appears alongside the family
      stories as a readable HTML story with accessible open/read/download
      actions, while still linking the original PDF.
- [ ] Preserve the original PDF as an inspectable source attachment rather than
      replacing it with an untraceable rewrite.
- [ ] Add or extend tests and fixture coverage for supplement discovery and
      rendering behavior, including the `doc-web` import seam if needed.
- [ ] Update `tests/fixtures/formats/_coverage-matrix.json`,
      `docs/input-contract.md`, `docs/runbooks/doc-web-import.md`,
      `docs/presentation-decisions.md`, and `docs/omission-audit.json` if the
      supplement becomes a real shipped surface.
- [ ] Check whether the chosen implementation makes any ad hoc supplement notes
      or temporary side-loading paths redundant; remove them or create a
      concrete follow-up.
- [ ] Run required checks for touched scope:
  - [ ] `make test`
  - [ ] `make lint`
  - [ ] `make build-family-site`
  - [ ] Run the real `doc-web` import path or directly validate the imported
        bundle used for the memoir.
  - [ ] `make methodology-compile`
  - [ ] `make methodology-check`
  - [ ] Inspect the memoir surface manually on desktop and mobile widths.
- [ ] If the implementation adds a repeatable supplement review gate, update
      `docs/evals/registry.yaml`.
- [ ] Search docs and update any related to supplement intake and family-story
      placement.
- [ ] Verify project tenets:
  - [ ] Provenance remains visible and honest.
  - [ ] The new family-story surface is easy for older readers to discover and
        use.
  - [ ] The original source artifact remains inspectable.
  - [ ] No supplement file disappears into an undocumented side path.

## Workflow Gates

- [ ] Build complete: implementation finished, required checks run, and summary
      shared
- [ ] Validation complete or explicitly skipped by user
- [ ] Story marked done via `/mark-story-done`

## Blocker Summary

N/A

## Blocker Evidence

N/A

## Unblock Condition

N/A

## Architectural Fit

- **Owning module / area**: The local whole-book builder, supplement metadata
  rules, `doc-web` import seam, and family-story presentation docs.
- **Methodology reality**: `spec:1` through `spec:6` are all still `partial`
  on this line; the supplement exists in the repo as a raw PDF, but the
  site-facing intake rule for standalone family-archive PDFs still needs to be
  connected to the already-existing `doc-web` import seam.
- **Substrate evidence**: `docs/runbooks/doc-web-import.md` documents a
  maintained import seam, and `tests/test_doc_web_import.py` proves bundle
  validation/import behavior. The current builder still only consumes the
  accepted main-book bundle from `input/doc-web-html/story206-onward-proof-r10`
  as documented in `docs/input-contract.md`.
- **Data contracts / schemas**: This story likely needs a thin supplement
  metadata contract plus a documented rule for attaching a standalone imported
  `doc-web` memoir bundle to the surfaced family-story run.
- **File sizes**: `modules/build_family_site.py` (1853),
  `tests/test_build_family_site.py` (548),
  `tests/test_doc_web_import.py` (82),
  `docs/presentation-decisions.md` (96), `docs/input-contract.md` (104),
  `docs/runbooks/doc-web-import.md` (68),
  `tests/fixtures/formats/_coverage-matrix.json` (60),
  `docs/omission-audit.json` (830).
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/runbooks/doc-web-import.md`, `docs/input-contract.md`,
  `docs/presentation-decisions.md`, `docs/methodology/state.yaml`,
  `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`, and `docs/omission-audit.json`.
  No repo-local ADRs or supplement-specific runbooks exist yet.

## Files to Modify

- `modules/build_family_site.py` — add a thin surfaced path for a standalone
  imported memoir bundle inside the family-story area (1853 lines)
- `tests/test_build_family_site.py` — cover memoir discovery and rendering or
  linking behavior (548 lines)
- `tests/test_doc_web_import.py` — extend proof if the memoir intake shape
  needs a new validated import case (82 lines)
- `docs/presentation-decisions.md` — record how a non-book family-archive
  memoir appears beside the family stories after `doc-web` processing (96 lines)
- `docs/input-contract.md` — document any new supplement-intake rule or sidecar
  metadata contract for imported memoir bundles (104 lines)
- `docs/runbooks/doc-web-import.md` — document the memoir PDF -> `doc-web` ->
  imported bundle workflow if it becomes maintained truth (68 lines)
- `tests/fixtures/formats/_coverage-matrix.json` — graduate
  `scanned-supplements` honestly if the memoir becomes a real surface (60 lines)
- `docs/omission-audit.json` — keep supplement accounting truthful if the
  shipped surface changes (830 lines)

## Redundancy / Removal Targets

- Ad hoc personal notes about where the memoir came from if the surfaced site
  and repo docs already preserve that truth.
- One-off supplement links that bypass the family-story entry points.
- Untracked sidecar handling for standalone archive PDFs.
- A second non-`doc-web` PDF processing path just for this memoir.

## Notes

- This is a new story instead of a reopen of Story 005 because it introduces a
  distinct imported-archive seam outside the staged main-book `doc-web`
  manifest, plus a new provenance-sensitive family-story attachment pattern.
- The display title is now fixed by user decision as `Rolland Alain Memoir
  Family Story`; do not reuse the OCR-damaged filename as reader-facing copy.
- The expected implementation path is `PDF -> doc-web -> normalized HTML ->
  family-story surface`, not `PDF link only`.

## Plan

1. Run the memoir through `doc-web` and inspect the imported HTML.
2. Define the normalization rules, metadata, and short provenance preamble.
3. Add the memoir to the family-story surface without hiding the original PDF.
4. Update the import, omission, and coverage truth so the supplement is
   first-class rather than a sidecar.

## Work Log

20260411-1107 — action: created story from user request, result: preserved the
Rolland memoir as a distinct supplement-intake story with explicit provenance
uncertainty, evidence: `input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf`
and the current lack of supplement intake rules in `docs/input-contract.md`,
next step: inspect the PDF and choose the thinnest honest surfaced form.
20260411-1118 — action: incorporated user decisions, result: fixed the
display title and shifted the implementation path to `doc-web` processing plus
HTML normalization into the family-story format, evidence:
`docs/runbooks/doc-web-import.md`, `tests/test_doc_web_import.py`, and user
direction in this thread, next step: run the memoir through `doc-web` and
inspect the generated HTML.
