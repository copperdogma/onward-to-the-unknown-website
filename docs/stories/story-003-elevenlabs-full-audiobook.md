---
title: "ElevenLabs Full Audiobook"
status: "Done"
priority: "High"
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
  - "spec:6"
  - "spec:8"
  - "C1"
  - "C2"
  - "C3"
  - "C4"
  - "C6"
  - "B1"
adr_refs: []
depends_on:
  - "story-005"
category_refs:
  - "spec:1"
  - "spec:2"
  - "spec:3"
  - "spec:4"
  - "spec:6"
  - "spec:8"
compromise_refs:
  - "C1"
  - "C2"
  - "C3"
  - "C4"
  - "C6"
  - "B1"
input_coverage_refs:
  - "book-core-html"
  - "chapter-audio"
  - "full-book-audio"
architecture_domains:
  - "content_model"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "ElevenLabs audiobook workflow over staged bundle text plus repo-owned audiobook script files"
---

# Story 003 — ElevenLabs Full Audiobook

**Priority**: High
**Status**: Done
**Decision Refs**: `docs/input-contract.md`, `docs/runbooks/golden-build.md`, `tests/fixtures/formats/_coverage-matrix.json`, `input/doc-web-html/story206-onward-proof-r10/manifest.json`, `input/doc-web-html/story206-onward-proof-r10/provenance/blocks.jsonl`, `modules/build_family_site.py`, representative source pages and chapters inspected on 2026-04-11, none found after search for repo-local ADRs or audiobook runbooks
**Depends On**: Story 005 for the verified whole-book intake surface and omission-audit baseline

## Goal

Prepare the full *Onward to the Unknown* audiobook script corpus in a
repeatable way, with a repo-owned `audiobook-script/` folder containing one
narration-ready Markdown file per spoken chapter, a deterministic HTML-to-
Markdown path for source-derived chapters, an explicit include/exclude policy
for source material, and an inspectable handoff to the user's manual
ElevenLabs workflow.

## Acceptance Criteria

- [x] A repo-owned `audiobook-script/` directory exists at the repo root and
      contains one ordered `.md` file per spoken audiobook chapter.
- [x] The audiobook chapter map is explicit and stable, with each family story
      from `chapter-009` through `chapter-023` represented as exactly one
      audiobook chapter.
- [x] The spoken script corpus intentionally excludes genealogy tables and
      other print-first table surfaces, with the exclusions recorded in repo
      docs instead of handled ad hoc during generation.
- [x] A short preamble explains what the book is, why it was created, and what
      the listener will hear, without forcing title pages, index pages, or
      reunion minutes to be read verbatim.
- [x] A repeatable validation surface checks the committed
      `audiobook-script/` corpus for the expected chapter filenames and basic
      exclusion rules so the script set does not silently drift.
- [x] A maintained runbook explains how the finished Markdown corpus should be
      used in the user's manual ElevenLabs workflow, including pronunciation
      notes, cleanup expectations, and where later audio-output metadata should
      be recorded if it becomes repo truth.

## Out of Scope

- Reading genealogy tables, printed indexes, or other table-shaped reference
  matter aloud.
- Forcing every photo caption, illustration page, certificate, or blank image
  placeholder into the audiobook just because it exists in the print source.
- Building the public player UI beyond the metadata needed for later site
  integration.
- Running the user's ElevenLabs account, handling credentials, uploading the
  scripts, or creating the final audio files in this implementation pass.
- Heavy historical rewriting, fact correction, or stylistic modernization of
  the source narrative.
- Studio mastering or post-production beyond an honest first full pass.

## Approach Evaluation

- **Ideal alignment**: Strong. This story directly serves the Ideal's connected
  companion-media goal while keeping source lineage explicit. It does not move
  away from the archive-first model because the spoken script remains anchored
  to the staged bundle and documented editorial cuts.
- **Simplification baseline**: A single representative family chapter plus the
  preamble may already be enough to validate pronunciation, pacing, and voice
  fit in the user's later manual ElevenLabs pass. The repo-owned slice should
  stop at a trustworthy script corpus and handoff.
- **AI-only**: Weak fit. ElevenLabs can synthesize the voice, but it should not
  decide chapter boundaries, source exclusions, or what counts as spoken canon.
- **Hybrid**: Strongest fit. Use repo-documented editorial rules and stable
  script files, then use ElevenLabs only for the narration step.
- **Pure code**: Strong for extraction, cleanup, and file packaging, but not
  sufficient for the actual voice generation.
- **Repo constraints / prior decisions**: The repo has a verified staged bundle
  with manifest order and block-level provenance, but no audiobook-script
  directory, no audiobook runbook, and no prior decision about which print
  surfaces deserve spoken treatment.
- **Existing patterns to reuse**: Story 005 and the input contract already
  prove that the staged bundle is the active source of truth; the provenance
  JSONL exposes `block_kind` values that make table exclusions inspectable
  instead of guesswork.
- **Eval**: Keep repo validation focused on deterministic regeneration and
  source-fidelity checks. Any voice-fit or pronunciation pilot happens later in
  the user's manual ElevenLabs workflow.

## Editorial Decisions

- Create a short repo-authored preamble chapter instead of reading raw front
  matter verbatim.
  Reason: the title pages, grant acknowledgement, index, and reunion minutes
  contain useful context but poor listening flow. A short spoken introduction
  can explain the book's origin and structure more clearly.
- Use the staged bundle at `input/doc-web-html/story206-onward-proof-r10` as
  the authoritative source for this pass.
  Reason: the manifest order, chapter HTML, and block-level provenance already
  exist and were freshly verified. Waiting for a richer export would only delay
  a now-buildable workflow.
- Keep each family story from `chapter-009` through `chapter-023` as exactly
  one audiobook chapter.
  Reason: this matches the source book's clearest story units and follows the
  user's explicit requirement.
- Number audiobook files by listening order, not by source entry id, and use
  ASCII filenames like `01-preamble.md`.
  Reason: ElevenLabs upload order should be obvious without needing to know the
  source bundle's mixed page/chapter numbering.
- Use Markdown as the maintained script format instead of plain text.
  Reason: Markdown preserves simple chapter structure and emphasis cues while
  remaining easy for ElevenLabs to parse and for the repo to review.
- Exclude all HTML tables from the spoken script, not only the obvious
  genealogy tables.
  Reason: the user explicitly does not want genealogy tables spoken, and the
  other table surfaces in this bundle, such as indexes, veterans rosters, and
  plaque tables, are also print-first material that sounds unnatural aloud.
- Exclude standalone page entries as audiobook chapters.
  Reason: the `page-*` entries are title matter, acknowledgements, index
  matter, blank image placeholders, or other print scaffolding. Their useful
  context belongs in the preamble, not as separate spoken tracks.
- Exclude `chapter-001` as a spoken chapter.
  Reason: it is entirely an ancestral lineage table and would violate the
  no-genealogy-table rule.
- Exclude `chapter-003` and `chapter-004` as standalone spoken chapters.
  Reason: the farm-award certificate and reunion meeting minutes are relevant
  context, but they work better as compressed preamble material than as full
  narrated chapters.
- Exclude `chapter-006` and `chapter-008` as standalone spoken chapters.
  Reason: `chapter-006` is effectively a photo plate with captions and
  `chapter-008` is a veterans table. Both are valuable archive surfaces for the
  site, but weak audiobook material.
- Keep the committed source-derived corpus source-faithful within the spoken
  audiobook boundary: omit figures, image captions, HTML tables, and headings
  that only introduce omitted tables.
  Reason: the user explicitly asked for a safer, deterministic path that does
  not lose content in manual copying, and the verification pass showed that the
  reliable spoken boundary is narrower than "all non-table text" while still
  keeping the retained wording source-faithful.
- Keep `chapter-024` as chapter `20`, but limit it to the poem and attribution,
  stopping before the visual appendix that follows.
  Reason: the poem works as a clean closing epilogue, while the following
  plaque-style material is visual archive content rather than natural audiobook
  narration.
- Keep signatures, dates, and letter framing only when they materially define
  the voice of a piece.
  Reason: a section like `MEMORIES` reads naturally as a signed reminiscence,
  while visual-only captions should not interrupt the flow unless intentionally
  promoted.
- Treat pronunciation and pacing checks as downstream manual ElevenLabs work,
  not as a blocking repo-owned task in this story.
  Reason: the repo deliverable is the verified Markdown corpus plus handoff; the
  user is intentionally handling generation manually.

## Planned Audiobook Chapters

- `01-preamble.md` — new short introduction grounded in `page-006`,
  `page-007`, `page-009`, and `chapter-004`
- `02-the-first-lheureuxs-in-canada.md` — source `chapter-002`
- `03-moise-and-sophie.md` — source `chapter-005`
- `04-memories.md` — source `chapter-007`
- `05-alma-marie-lheureux-alain.md` — source `chapter-009`
- `06-arthur-lheureux.md` — source `chapter-010`
- `07-leonidas-lheureux.md` — source `chapter-011`
- `08-josephine-lheureux-alain.md` — source `chapter-012`
- `09-paul-lheureux.md` — source `chapter-013`
- `10-george-lheureux.md` — source `chapter-014`
- `11-joe-joseph-lheureux.md` — source `chapter-015`
- `12-mathilda-lheureux-devlin.md` — source `chapter-016`
- `13-marie-louise-lheureux-laclare.md` — source `chapter-017`
- `14-roseanna-lheureux-landreville.md` — source `chapter-018`
- `15-antoinette-lheureux-richard.md` — source `chapter-019`
- `16-emilie-lheureux-nolin.md` — source `chapter-020`
- `17-wilfrid-lheureux.md` — source `chapter-021`
- `18-pierre-lheureux.md` — source `chapter-022`
- `19-antoine-lheureux.md` — source `chapter-023`
- `20-i-wish.md` — poem-only epilogue from source `chapter-024`

## Excluded Source Material

- `page-001` through `page-009` as standalone audiobook tracks
- `chapter-001`
- `chapter-003`
- `chapter-004`
- `chapter-006`
- `chapter-008`
- figures, image captions, and visual appendix material in included chapters
- every HTML table in included chapters, including descendant charts and
  tabular memorial lists
- headings that only introduce omitted tables

## Tasks

- [x] Create the repo-root `audiobook-script/` folder and add the 20 ordered
      `.md` chapter files defined in this story.
- [x] Write `01-preamble.md` as a short original introduction that explains
      where the book came from, what kind of material it contains, and what the
      listener will and will not hear in the audiobook.
- [x] Extract narration-ready text from the included source chapters by using
      the staged HTML bundle's article content while removing navigation chrome,
      figures, captions, tables, blank visual placeholders, and other
      non-spoken scaffolding.
- [x] Keep every family story from `chapter-009` through `chapter-023` as one
      audiobook file while stopping before descendant/genealogy tables and
      omitting headings that only introduce those omitted tables.
- [x] Build `20-i-wish.md` from `chapter-024` as a poem-only epilogue that
      stops before the post-poem visual appendix.
- [x] Keep the committed source-derived corpus faithful to source wording and
      casing within the spoken boundary, limiting deterministic transformation
      to HTML-to-Markdown conversion plus omission of figures, captions,
      tables, and headings that only introduce omitted tables.
- [x] Add a narrow automated validation surface for the committed
      `audiobook-script/` corpus, covering expected filenames, basic structure,
      and the absence of raw HTML table or navigation chrome in representative
      files.
- [x] Document that the actual ElevenLabs generation step is manual and
      credentialed outside the repo, keeping secrets out of repo artifacts and
      making the human step explicit.
- [x] Record any recurring proper names that need pronunciation help in the
      manual ElevenLabs handoff notes.
- [x] Document the user's manual ElevenLabs handoff flow, including which
      script files are source-derived versus manually authored, what cleanup is
      still expected after deterministic conversion, and where later audio
      metadata should be recorded if it becomes repo truth.
- [x] Remove or avoid temporary copied full-book exports outside the
      `audiobook-script/` contract if the stable chapter files are sufficient.
- [x] Run required checks for touched scope:
  - [x] `make methodology-compile`
  - [x] `make methodology-check`
  - [x] Manually review the preamble and a sample of family-story scripts
        against source HTML during the fidelity pass.
- [x] Search docs and update any truth surfaces changed by the chosen
      audiobook-script and ElevenLabs workflow.
- [x] Verify project tenets:
  - [x] Spoken chapters remain tied to inspectable source entries.
  - [x] Exclusions are explicit and reproducible rather than improvised.
  - [x] AI reduces narration labor without becoming a hidden source of truth.
  - [x] The workflow can be resumed after a long gap from repo artifacts alone.

## Downstream Manual Follow-Up

- The user may run a small ElevenLabs pilot before any full batch to confirm
  pronunciation, pacing, and voice fit.
- If audiobook assets later become repo truth, update
  `tests/fixtures/formats/_coverage-matrix.json` and related docs accordingly.
- If a manual pilot establishes a meaningful maintained quality gate, record it
  in `docs/evals/registry.yaml`.
- If agent tooling changes in a later follow-up, run `make skills-check`.

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

- **Owning module / area**: Audiobook script preparation, chapter mapping,
  pronunciation notes, and future audiobook asset inventory.
- **Methodology reality**: `spec:1`, `spec:2`, `spec:3`, `spec:4`, `spec:6`,
  and `spec:8` are all currently `partial`; `C1`, `C2`, `C3`, `C4`, and `C6`
  remain in `climb`, while `B1` remains in `hold`.
- **Substrate evidence**: The verified bundle at
  `input/doc-web-html/story206-onward-proof-r10` contains `24` chapter entries,
  `9` page entries, a stable `manifest.json`, and `525` provenance rows. The
  family stories form a continuous run from `chapter-009` through
  `chapter-023`, and `provenance/blocks.jsonl` marks table blocks explicitly,
  which makes descendant-table suppression inspectable.
- **Data contracts / schemas**: This story relies on manifest ordering plus
  provenance block kinds instead of inventing a second hidden source-selection
  layer. The chapter list and filename contract in this story are the current
  operational truth for audiobook-script preparation.
- **Status rationale**: `Done` is honest because the reopened ElevenLabs paste
  bug was narrowed to the manual preamble, fixed in the committed script set,
  and covered by a regression test plus runbook guidance. Any further
  narration-shaping changes remain downstream editorial follow-up rather than a
  repo-owned workflow gap.
- **Decision context**: Reviewed `docs/ideal.md`, `docs/spec.md`,
  `docs/input-contract.md`, `docs/runbooks/golden-build.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`,
  `tests/fixtures/formats/_coverage-matrix.json`,
  `input/doc-web-html/story206-onward-proof-r10/manifest.json`,
  `input/doc-web-html/story206-onward-proof-r10/provenance/blocks.jsonl`, and
  representative `page-*` and `chapter-*` source files. No repo-local ADRs or
  audiobook-specific runbooks exist yet.

## Files to Modify

- `docs/stories/story-003-elevenlabs-full-audiobook.md` — capture the explicit
  audiobook chapter map and editorial rules
- `modules/build_audiobook_script.py` — deterministically convert source
  chapter HTML into reviewable Markdown while stopping at the documented
  listening boundaries
- `scripts/build_audiobook_script.py` — expose the converter as a maintained
  repo command
- `Makefile` — add the audiobook-script build target and `FORCE=1`
  regeneration surface
- `audiobook-script/*.md` — one narration-ready Markdown file per audiobook
  chapter, using the ordered filename contract defined above
- `tests/test_audiobook_script.py` — validate the committed script corpus shape
  and key exclusion invariants
- `docs/runbooks/elevenlabs-audiobook.md` — future repeatable workflow notes
  for voice settings, pronunciation, upload steps, and asset recording
- `docs/RUNBOOK.md` — add the maintained audiobook-script and generation
  workflow surface if this becomes a stable repo path
- `README.md` — mention the audiobook-script artifact surface once it exists
- `tests/fixtures/formats/_coverage-matrix.json` — update audio surface truth
  once audiobook outputs are real
- `docs/evals/registry.yaml` — record any pilot quality gate that becomes part
  of the maintained workflow

## Redundancy / Removal Targets

- Temporary copied full-book exports that drift from the maintained
  `audiobook-script/` files
- Ad hoc chapter naming that is not tied to the ordered audiobook filename
  contract
- One-off include/exclude notes outside the story or future audiobook runbook
- Manual table-suppression decisions that are not anchored to source structure

## Notes

- Expanding the existing audiobook story is the honest move. This remains the
  same subsystem, the same success surface, and the same validation boundary as
  the earlier draft; the missing piece was concrete editorial scope, not a new
  story line.
- The preamble should state plainly that the print book is a mix of narrative
  family history and reference material, and that the audiobook focuses on the
  narrative reading experience rather than speaking every printed list.
- Any future expansion of the spoken boundary, such as promoting a specific
  caption or certificate line into canon, should be handled as an explicit
  story/doc change rather than improvised inside the generator.

## Plan

### Eval-First Gate

- **Success eval**: keep `tests/test_audiobook_script.py` as the committed
  validation surface and add a smoke regeneration path via
  `make build-audiobook-script AUDIOBOOK_SCRIPT_OUTPUT=build/audiobook-script-check`
  so the deterministic converter can be proven separately from the manually
  reviewed canonical corpus.
- **Baseline before implementation**:
  - `audiobook-script/` did not exist, so the committed script baseline was
    `0 / 20` files.
  - There was no repo command for source-derived audiobook chapters.
  - There was no maintained runbook for the user's manual ElevenLabs handoff.
- **Chosen approach**:
  - Hybrid thin helper. The user explicitly redirected the story away from
    manual re-copying of family stories and asked for deterministic HTML-to-
    Markdown conversion first, table stripping second, then source-fidelity
    verification on the committed chapter files.
  - Reuse `modules/build_family_site.py` article extraction helpers rather than
    inventing a second parser stack.
  - Keep `01-preamble.md` manual and source-grounded while treating the
    remaining chapters as source-derived files that can be regenerated on
    purpose and then re-reviewed.
- **Rejected path**:
  - Manual first-pass transcription of family chapters. It creates too much
    risk of silent omission or paraphrase drift compared with deterministic
    conversion from the staged HTML bundle.

### Scope Delta Folded In

- Add a narrow committed test surface for the audiobook-script corpus. This
  makes the chapter set inspectable and repeatable after the deterministic
  conversion and fidelity pass.
- Document the manual ElevenLabs boundary explicitly. The repo does not store
  credentials and this story leaves upload and generation to the user.
- Add a thin maintained generator command because the user explicitly preferred
  deterministic source conversion over manual copying.

### Implementation Order

1. **Add the deterministic source-derived builder** (`S`)
   - Files: `modules/build_audiobook_script.py`,
     `scripts/build_audiobook_script.py`, `Makefile`
   - Reuse the staged-bundle article extraction helpers, keep the preamble
     manual, and preserve source wording only within the documented audiobook
     boundary for the source-derived chapters.
   - Done looks like: `make build-audiobook-script` can materialize the
     source-derived chapter set into any target directory without touching the
     preamble.

2. **Commit the reviewed canonical Markdown corpus** (`M`)
   - Files: `audiobook-script/*.md`
   - Keep `01-preamble.md` repo-authored and source-grounded.
   - Commit the generated chapter set in listening order and keep the
     source-derived files faithful to source wording and ordering instead of
     normalizing OCR/spelling in the canonical corpus.
   - Done looks like: the repo has the full ordered chapter corpus ready for
     the user's manual upload flow.

3. **Add a repeatable artifact validation surface** (`S`)
   - Files: `tests/test_audiobook_script.py`
   - Assert exact filenames, reader-facing Markdown structure, and key
     exclusion invariants such as no raw HTML, preserved source-only spellings,
     and omitted table content.
   - Done looks like: `make test` can catch obvious drift in the committed
     corpus.

4. **Document the maintained workflow and manual handoff** (`S`)
   - Files: `docs/runbooks/elevenlabs-audiobook.md`, `docs/RUNBOOK.md`,
     `README.md`
   - Record the generator command, the source-fidelity boundary, the filename
     ordering contract, the pronunciation note surface, and the fact that the
     actual ElevenLabs generation step is intentionally manual and outside repo
     credentials.
   - Done looks like: a future session can rebuild, review, and hand off the
     script corpus without relying on memory.

### Impact And Risk Notes

- `tests/fixtures/formats/_coverage-matrix.json` is **not** expected to move in
  the script-authoring phase alone. Update it only if actual audiobook outputs
  become repo truth in the same pass.
- The main blast radius is editorial fidelity, not runtime behavior. The risk
  is accidental omission or over-cleaning of source text, which is why the
  story should prefer explicit source comparison and narrow content tests over
  extra infrastructure.
- Existing reusable helpers are in `modules/build_family_site.py`, especially
  `load_manifest`, `bundle_entry_from_manifest`, `extract_article_html`,
  `article_blocks`, and the table detection patterns.
- No schema migration or frontend runtime change is expected in this slice.

## Work Log

20260410-1243 — action: created initial story draft, result: captured the
ElevenLabs audiobook line as a separate workflow, evidence: coverage rows and
repo planning surfaces, next step: inspect the staged source bundle and make
the editorial boundary explicit.

20260411-0952 — action: expanded the story with a verified source-backed
chapter plan, result: recorded the audiobook-script folder contract, the 20
spoken chapter files, and explicit include/exclude decisions, evidence:
`manifest.json`, `provenance/blocks.jsonl`, `page-*` front matter, and
representative `chapter-*` HTML reads, next step: build the chapter text files
and document the manual ElevenLabs handoff.

20260411-1056 — action: completed `/build-story` exploration, result: verified
that Story 005's staged-bundle substrate and `modules/build_family_site.py`
already provide enough manifest/article/table parsing support for a first-pass
Markdown corpus without adding a second heavy parser; folded in a narrow test
surface and explicit ElevenLabs-auth documentation as small scope expansions,
evidence: `docs/ideal.md`, `docs/spec.md`, `docs/methodology/state.yaml`,
`docs/methodology/graph.json`, `docs/stories/story-005-whole-book-accessible-reading-surface-and-omission-audit.md`,
`tests/fixtures/formats/_coverage-matrix.json`, `docs/decisions/README.md`,
`modules/build_family_site.py`, `tests/test_build_family_site.py`, baseline
check showing `audiobook-script/` currently has `0` Markdown files, parser
probe showing `chapter-009.html` and `chapter-024.html` expose clean prose
before their first tables, and env check showing no current `ELEVEN*`
credentials in shell, next step: get human approval on the direct-authoring
plus validation-plan before implementation.

20260411-1109 — action: implementation start and scope refinement, result:
user approved implementation but redirected the repo slice away from agent-run
ElevenLabs generation toward deterministic HTML-to-Markdown conversion for the
source-derived chapters, followed by manual cleanup and a manual user handoff
for ElevenLabs, evidence: current thread instruction, next step: promote the
story status in generated surfaces and build the deterministic script path plus
the committed Markdown corpus.

20260411-1148 — action: implemented the deterministic audiobook-script slice,
result: added `modules/build_audiobook_script.py`,
`scripts/build_audiobook_script.py`, and `make build-audiobook-script`; built
the `20`-file `audiobook-script/` corpus with a manual `01-preamble.md`,
source-derived chapters that skip figures and tables, and a light cleanup pass
for obvious OCR defects; added `tests/test_audiobook_script.py`; documented the
manual handoff in `docs/runbooks/elevenlabs-audiobook.md`, `docs/RUNBOOK.md`,
and `README.md`, evidence: committed chapter filenames in
`audiobook-script/`, source spot-checks against `page-006.html`,
`page-007.html`, `page-009.html`, `chapter-004.html`, `chapter-009.html`, and
`chapter-024.html`, plus fresh command runs for `make build-audiobook-script
AUDIOBOOK_SCRIPT_OUTPUT=build/audiobook-script-check`, `make test`,
`make lint`, `make methodology-compile`, and `make methodology-check`, next
step: leave the story `In Progress` for `/validate` and any user-requested
editorial tweaks before `/mark-story-done`.

20260411-1238 — action: ran a source-fidelity verification pass with parallel
subagent review plus local block-level comparison, result: found and fixed
text drift caused by title normalization and manual OCR/spelling cleanup;
reconfirmed the narrower audiobook boundary that omits figures, captions,
tables, headings that only introduce omitted tables, and the post-poem visual
appendix in `chapter-024`, evidence: subagent findings across chapters `02`
through `20`, local source-to-script diff against `chapter-002.html`,
`chapter-005.html`, `chapter-007.html`, `chapter-009.html` through
`chapter-024.html`, generator updates in `modules/build_audiobook_script.py`,
and refreshed regression checks in `tests/test_audiobook_script.py`, next
step: realign story docs to the verified boundary and close the repo-owned
script-corpus slice.

20260411-1248 — action: rescoped and closed the repo-owned story slice, result:
the story contract, runbook, and close-out gates now match the verified spoken
boundary; manual ElevenLabs upload, pilot listening, and final audio-file
creation are explicitly downstream user-run follow-up, evidence: edits in
`docs/stories/story-003-elevenlabs-full-audiobook.md` and
`docs/runbooks/elevenlabs-audiobook.md`, fresh command runs for `python -m
pytest tests/`, `python -m ruff check modules/ tests/`, `make
build-audiobook-script AUDIOBOOK_SCRIPT_OUTPUT=build/audiobook-script-closeout
FORCE=1`, `make methodology-compile`, and `make methodology-check`, next step:
`/check-in-diff`.

20260411-1328 — action: reopened the story after a real ElevenLabs paste test,
result: identified that the manual preamble still used artificial column-style
hard wrapping even though the source-derived prose chapters were already
single-line paragraphs; flattened the preamble prose, added a regression test,
and updated the runbook to forbid hard-wrapped upload text, evidence:
`audiobook-script/01-preamble.md`, `tests/test_audiobook_script.py`, and
`docs/runbooks/elevenlabs-audiobook.md`, next step: rerun validation and have
the user verify the updated upload behavior.

20260411-1345 — action: revalidated and reclosed the story after the ElevenLabs
upload-format fix, result: Story 003 is back to `Done` with the preamble now
using single-line prose paragraphs and the reopened formatting bug captured in
tests and runbook guidance, evidence: `audiobook-script/01-preamble.md`,
`tests/test_audiobook_script.py`, `docs/runbooks/elevenlabs-audiobook.md`,
fresh command runs for `make build-audiobook-script
AUDIOBOOK_SCRIPT_OUTPUT=build/audiobook-script-check FORCE=1`, `python -m
pytest tests/`, `python -m ruff check modules/ tests/`, `make
methodology-compile`, and `make methodology-check`, next step:
`/check-in-diff`.
