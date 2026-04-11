---
title: "Rolland Alain Memoir Family Story"
status: "Done"
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
**Status**: Done
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

- [x] The memoir PDF is run through `doc-web` and lands in a validated import
      shape the repo can consume without inventing a second one-off PDF path;
      if the default TOC-based lane is insufficient, the accepted path is a
      documented bounded non-TOC supplement lane that still emits the standard
      `doc_web_bundle` contract.
- [x] The accepted memoir bundle lives in a repo-owned intake location rather
      than only under `.runtime/doc-web-imports/`.
- [x] The repo defines an honest placement and normalization rule for the
      memoir, including its displayed title, family-story placement, and source
      provenance without overclaiming how or when it joined the archive, while
      intentionally handling title-page or unnumbered-page leftovers from the
      imported bundle.
- [x] The public site can surface the memoir through the family-story area with
      a very short preamble explaining that it was found as a photocopy in the
      user's copy of the book and may represent either a late-added or
      separately distributed reunion document.
- [x] The original PDF remains inspectable as source material, and the import /
      omission / coverage truth is updated so this supplement is no longer an
      untracked sidecar file.

## Out of Scope

- Proving the exact historical reason the memoir was not part of the bound
  book.
- A generalized supplement-gallery system for every future PDF in the family
  archive.
- Refreshing audiobook or podcast assets to include the memoir; record any
  impact honestly, but keep media regeneration as a follow-up unless the user
  explicitly widens the slice.

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

- [x] Run the memoir PDF through `doc-web`, capture the baseline failure or
      success honestly, and prove the thinnest maintained non-TOC bundle path
      that yields a valid import.
- [x] Accept the validated memoir bundle into a repo-owned intake location
      instead of leaving it only under `.runtime/doc-web-imports/`.
- [x] Inspect the generated HTML and decide the thinnest normalization needed
      to make it match the current family-story reading format.
- [x] Define the canonical metadata for this supplement: displayed title,
      family-story placement, source note, and the exact short preamble
      language that preserves the provenance uncertainty.
- [x] Decide how title-page and unnumbered-page leftovers from the imported
      memoir bundle should be handled so the surfaced reading flow feels like
      one intentional family story rather than a loose bundle index.
- [x] Extend the local site build so the memoir appears alongside the family
      stories as a readable HTML story with accessible open/read/download
      actions, while still linking the original PDF.
- [x] Preserve the original PDF as an inspectable source attachment rather than
      replacing it with an untraceable rewrite.
- [x] Add or extend tests and fixture coverage for supplement discovery and
      rendering behavior, including the `doc-web` import seam if needed.
- [x] Update `tests/fixtures/formats/_coverage-matrix.json`,
      `docs/input-contract.md`, `docs/runbooks/doc-web-import.md`,
      `docs/presentation-decisions.md`, and `docs/omission-audit.json` if the
      supplement becomes a real shipped surface.
- [x] Check whether the chosen implementation makes any ad hoc supplement notes
      or temporary side-loading paths redundant; remove them or create a
      concrete follow-up.
- [x] If the shipped memoir creates a known audiobook or podcast completeness
      gap, record that follow-up explicitly instead of silently widening this
      story.
- [x] Run required checks for touched scope:
  - [x] `make test`
  - [x] `make lint`
  - [x] `make build-family-site`
  - [x] Run the real `doc-web` import path or directly validate the imported
        bundle used for the memoir.
  - [x] `make methodology-compile`
  - [x] `make methodology-check`
  - [x] Inspect the memoir surface manually on desktop and mobile widths.
- [x] Decide whether the implementation adds a repeatable supplement review
      gate; no `docs/evals/registry.yaml` update was needed because validation
      remains covered by the touched-scope tests plus desktop/mobile manual
      proof.
- [x] Search docs and update any related to supplement intake and family-story
      placement.
- [x] Verify project tenets:
  - [x] Provenance remains visible and honest.
  - [x] The new family-story surface is easy for older readers to discover and
        use.
  - [x] The original source artifact remains inspectable.
  - [x] No supplement file disappears into an undocumented side path.

## Workflow Gates

- [x] Build complete: implementation finished, required checks run, and summary
      shared
- [x] Validation complete or explicitly skipped by user
- [x] Story marked done via `/mark-story-done`

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
  validation/import behavior. Fresh exploration on `2026-04-11` showed that
  `python scripts/doc_web_import.py run-onward --run-id rolland-memoir-story007-explore --input-pdf "input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf" --force`
  failed at `portionize_toc` because the memoir exposes no usable TOC, but the
  existing `doc-web` modules `portionize_headings_html_v1` and
  `build_chapter_html_v1` still produced a valid bundle from the same OCR
  artifacts, and
  `python scripts/doc_web_import.py import-bundle --bundle-path /Users/cam/Documents/Projects/doc-web/output/runs/rolland-memoir-story007-explore/output/html --snapshot-id rolland-memoir-story007-probe --force`
  imported that bundle successfully. The story is therefore buildable, but the
  honest maintained seam is a bounded non-TOC scanned supplement path rather
  than the default TOC-driven Onward recipe.
- **Data contracts / schemas**: This story likely needs a thin supplement
  metadata contract plus a documented rule for attaching a standalone imported
  `doc-web` memoir bundle to the surfaced family-story run. The current builder
  still only consumes the accepted main-book bundle from
  `input/doc-web-html/story206-onward-proof-r10` as documented in
  `docs/input-contract.md`, so the memoir also needs a repo-owned accepted
  bundle location under the intake contract.
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

- `scripts/doc_web_import.py` — add or document the bounded memoir/non-TOC
  supplement orchestration path that still lands in the standard import seam
- `modules/build_family_site.py` — add a thin surfaced path for a standalone
  imported memoir bundle inside the family-story area (1853 lines)
- `tests/test_build_family_site.py` — cover memoir discovery and rendering or
  linking behavior (548 lines)
- `tests/test_doc_web_import.py` — extend proof if the memoir intake shape
  needs a new validated import case (82 lines)
- `input/doc-web-html/<rolland-alain-memoir-bundle>/` — checked-in accepted
  memoir bundle snapshot derived from the validated `doc-web` output
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
- Fresh probe output currently yields one main chapter plus two stray page
  entries (`page-001` title page and `page-002` from an unnumbered page), so
  reader-facing normalization has to be intentional rather than assuming the
  imported bundle is already publication-shaped.
- Shipping the memoir now requires one more ElevenLabs generation/upload step
  to bring the produced audiobook audio corpus back into sync with the updated
  Markdown script set.

## Work Log

20260411-2034 — exploration: verified Ideal/spec alignment against `docs/ideal.md`, `docs/spec.md`, `docs/methodology/state.yaml`, `docs/methodology/graph.json`, `docs/input-contract.md`, `docs/presentation-decisions.md`, `docs/omission-audit.json`, dependency stories `story-005` / `story-006`, and `tests/fixtures/formats/_coverage-matrix.json` (`book-core-html`, `scanned-supplements`); no repo-local ADR applied. Traced code and risk surfaces through `scripts/doc_web_import.py`, `modules/build_family_site.py`, `tests/test_build_family_site.py`, and `tests/test_doc_web_import.py`. Fresh substrate evidence: `python scripts/doc_web_import.py run-onward --run-id rolland-memoir-story007-explore --input-pdf "input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf" --force` reached OCR/page extraction but failed at `portionize_toc` with `No TOC entries found; cannot build chapters.` Probe commands in the sibling `doc-web` checkout — `python -m modules.portionize.portionize_headings_html_v1.main ... --fallback-mode single-document` and `python -m modules.build.build_chapter_html_v1.main ... --book-title "Rolland Alain Memoir Family Story"` — produced `output/html/manifest.json` plus provenance sidecars, and `python scripts/doc_web_import.py import-bundle --bundle-path /Users/cam/Documents/Projects/doc-web/output/runs/rolland-memoir-story007-explore/output/html --snapshot-id rolland-memoir-story007-probe --force` imported that bundle successfully. Conclusion: the story is not blocked, but it needs a small coherent scope expansion for a maintained non-TOC scanned supplement lane, a repo-owned accepted memoir bundle under the intake contract, and explicit handling for stray page leftovers in the imported bundle. Likely files to change remain `scripts/doc_web_import.py`, `modules/build_family_site.py`, tests, and intake/presentation docs. Follow-up risk recorded: current audiobook output will not include the memoir unless a later story refreshes media coverage.

## Plan

- **Eval baseline**
  - Baseline failure: the default maintained Onward PDF recipe does not finish
    on this memoir because `portionize_toc` requires TOC-derived chapter
    boundaries the PDF does not expose.
  - Baseline success probe: existing `doc-web` non-TOC heading portionization
    plus `build_chapter_html_v1` do emit an importable `doc_web_bundle`; the
    current imported probe contains `3` entries with reading order
    `page-001 -> chapter-001 -> page-002`.
- **Implementation order**
  1. `S` Establish the accepted memoir intake artifact.
     Files: `scripts/doc_web_import.py`, `tests/test_doc_web_import.py`,
     `docs/runbooks/doc-web-import.md`, `docs/input-contract.md`,
     `input/doc-web-html/<rolland-alain-memoir-bundle>/`.
     Change: wrap or explicitly document the bounded non-TOC memoir path so the
     accepted output is reproducible from this repo, then check the validated
     memoir bundle into the repo-owned intake contract instead of relying on
     `.runtime/`.
     Impact/risk: import metadata expectations and path resolution could break;
     keep the standard bundle-contract validation as the gate.
     Done looks like: a checked-in memoir bundle exists under `input/`, and the
     runbook names the honest non-TOC workflow that produced it.
  2. `M` Add supplement metadata and builder composition.
     Files: `modules/build_family_site.py`, `tests/test_build_family_site.py`,
     plus a thin supplement metadata artifact under `input/` or another
     repo-owned content contract path chosen during implementation.
     Change: teach the family-site builder how to merge the memoir bundle into
     the family-story area without disturbing the main-book manifest flow.
     Impact/risk: the current builder is single-manifest and the omission audit
     assumes one source bundle, so supplement ordering and provenance linkage
     are the main regression surface.
     Done looks like: the memoir appears in the family-story surface with a
     deterministic placement and a stable source link.
  3. `S` Normalize reader-facing presentation.
     Files: `modules/build_family_site.py`, `docs/presentation-decisions.md`.
     Change: define the exact title, short provenance preamble, PDF attachment,
     and handling for probe leftovers (`page-001`, `page-002`) so readers land
     on one intentional memoir story instead of a raw bundle index.
     Impact/risk: over-explaining provenance or surfacing OCR leftovers would
     harm the reading experience for older readers.
     Done looks like: desktop/mobile manual inspection shows an easy-to-find
     memoir surface with honest framing and no confusing stray entries.
  4. `S` Update proof surfaces and truth accounting.
     Files: `tests/fixtures/formats/_coverage-matrix.json`,
     `docs/omission-audit.json`, `docs/presentation-decisions.md`,
     `docs/input-contract.md`, `docs/runbooks/doc-web-import.md`, and any
     generated methodology artifacts if status/coverage truth changes.
     Change: graduate `scanned-supplements` honestly if the memoir ships, keep
     omission accounting truthful, and document any deliberate non-goals.
     Impact/risk: truth surfaces can drift if the memoir is shipped without
     updating intake/coverage accounting in the same slice.
     Done looks like: docs, coverage, and omission surfaces all acknowledge the
     memoir as a first-class supplement rather than a sidecar.
- **Structural health notes**
  - Prefer a thin supplement metadata contract over hard-coding memoir-specific
    IDs in `modules/build_family_site.py`; the builder already carries enough
    book-specific branching.
  - Reuse the validated `doc_web_bundle` contract instead of inventing a second
    repo-local HTML schema.
  - The imported probe already proves the upstream OCR/build substrate exists,
    so implementation should stay inside this repo and avoid depending on
    unreviewed `doc-web` changes.
- **Human-approval blockers**
  - Small scope expansion already folded into the story: repo-owned accepted
    memoir bundle plus a bounded non-TOC supplement intake rule.
  - Recommended follow-up, not folded in: finish the extra ElevenLabs memoir
    chapter generation if you want the produced audio corpus to stay complete.

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
20260411-2112 — implementation: shipped the memoir supplement intake and family-story surface through `scripts/doc_web_import.py`, `modules/build_family_site.py`, tests, and intake/presentation docs; accepted the validated bundle under `input/doc-web-html/rolland-alain-memoir-r01/` and surfaced it at `rolland-alain-memoir-family-story.html` with the original PDF preserved. Verification in this pass: `python scripts/doc_web_import.py run-scanned-supplement --run-id rolland-alain-memoir-r01 --input-pdf "input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf" --bundle-title "Rolland Alain Memoir Family Story" --force`, `python scripts/doc_web_import.py import-bundle --bundle-path input/doc-web-html/rolland-alain-memoir-r01 --snapshot-id rolland-alain-memoir-r01 --force`, `python -m pytest tests/test_doc_web_import.py -q`, `make test`, `make lint`, `make build-family-site`, `make refresh-omission-audit`, `make methodology-compile`, and `make methodology-check`. Manual proof caught one upstream `doc-web` defect in the accepted memoir output: [input/doc-web-html/rolland-alain-memoir-r01/chapter-001.html](/Users/cam/.codex/worktrees/5ede/onward-to-the-unknown-website/input/doc-web-html/rolland-alain-memoir-r01/chapter-001.html) duplicated its opening block sequence. Rather than block Story 007 on upstream repair, I manually removed the bad first copy from the accepted bundle, rebuilt the site, reran `python -m pytest tests/test_build_family_site.py -q` and `make build-family-site`, then rechecked `http://127.0.0.1:4183/rolland-alain-memoir-family-story.html` and `http://127.0.0.1:4183/index.html` at `1200x872` and `390x844`. Final manual result: one memoir opening only, no horizontal overflow, memoir nav/actions remain usable, and the family-story landing card still appears after `chapter-023`. Follow-up left explicit: audiobook/podcast coverage is now incomplete until a later media-refresh story decides whether to add the memoir.
20260411-2134 — follow-through: extended the canonical audiobook Markdown corpus so the memoir now has a source-derived upload chapter at `audiobook/script/20-rolland-alain-memoir-family-story.md`, with `I Wish` shifted to `audiobook/script/21-i-wish.md` to preserve the memoir-before-epilogue listening order. Implementation touched `modules/build_audiobook_script.py`, `tests/test_audiobook_script.py`, and `docs/runbooks/elevenlabs-audiobook.md`, and the generated corpus was refreshed with `make build-audiobook-script FORCE=1`. Verification in this pass: `python -m pytest tests/test_audiobook_script.py -q` and `make lint`. Result: the Markdown script corpus is now complete for the memoir, but the produced ElevenLabs audio set will stay one chapter short until the new Markdown file is uploaded/generated.
20260411-2202 — validation repair: removed stale provenance rows `blk-chapter-001-0001` through `blk-chapter-001-0006` from the checked-in accepted bundle so `input/doc-web-html/rolland-alain-memoir-r01/` again satisfies the `doc_web_bundle` import contract after the earlier duplicate-opening cleanup. Fresh verification in this pass: reran `python scripts/doc_web_import.py run-scanned-supplement --run-id rolland-alain-memoir-r01 --input-pdf "input/Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf" --bundle-title "Rolland Alain Memoir Family Story" --force` against the current local sibling `doc-web` checkout, confirmed that local upstream rerun still reproduces the duplicated opening, then reran `python scripts/doc_web_import.py import-bundle --bundle-path input/doc-web-html/rolland-alain-memoir-r01 --snapshot-id rolland-alain-memoir-r01-repaired --force`, `make build-audiobook-script FORCE=1`, `make build-family-site`, `make refresh-omission-audit`, `make test`, `make lint`, `make methodology-compile`, and `make methodology-check`, followed by Playwright checks at `1200x872` and `390x844` on `index.html` and `rolland-alain-memoir-family-story.html`. Result: the accepted memoir bundle validates again, the public memoir page keeps one opening with working imported-HTML/PDF actions, omission/input truth is refreshed, and the story is now ready for close-out through `/mark-story-done`.
20260411-2209 — close-out: marked Story 007 done after fresh current-state evidence confirmed all acceptance criteria, tasks, tenet checks, and workflow gates. Close-out evidence in this pass: `python scripts/doc_web_import.py import-bundle --bundle-path input/doc-web-html/rolland-alain-memoir-r01 --snapshot-id rolland-alain-memoir-r01-repaired --force`, `make build-audiobook-script FORCE=1`, `make build-family-site`, `make refresh-omission-audit`, `python -m pytest tests/`, `python -m ruff check modules/ scripts/ tests/`, `make methodology-compile`, and `make methodology-check`, plus Playwright inspection of `index.html` and `rolland-alain-memoir-family-story.html` at `1200x872` and `390x844`. Result: story status, generated story index, and methodology graph can now move to `Done`. Next step: `/check-in-diff`.
20260411-2222 — memoir note copy: updated the Rolland memoir's surfaced note to the user-specified wording so the web page and audiobook script both state plainly that the memoir was not originally included in the book and was found as photocopied pages in one copy. Implementation touched `input/doc-web-html/family-story-supplements.json`, `modules/build_audiobook_script.py`, and touched-scope tests. Next step: rebuild the memoir outputs, rerun touched validation, and then resume `/check-in-diff`.
