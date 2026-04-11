# Spec

This spec records the active constraints between the ideal and current repo
reality. Categories use stable `spec:N` ids so stories, decisions, and evals
can point at them without depending on heading wording.

## spec:1 Source Intake & Content Inventory

The repo needs a clear inventory of what comes from the staged `input/`
snapshot and what comes from separate family-archive sources.

### spec:1.1 Upstream Truth

The website should consume named, inspectable upstream inputs rather than a
bundle of undocumented local files.

### C1 Source content still arrives as a staged website snapshot plus hand-curated companion assets

- Ideal: ingest a stable structured canon directly from the upstream book and
  companion sources
- Constraint: start from the locally staged website/source files in `input/`
  for the book body and manually curated companion links/files for everything
  else
- Limitation: the source material is currently fragmented across separate tools
  and asset locations
- Limitation type: ecosystem
- Evolution signal: a repeatable import manifest exists for both book content
  and companion assets
- Residual form: keep a thin import manifest and delete ad hoc mapping notes

## spec:2 Canonical Content Model & Transformation

The repo should turn imported source material into canonical site data rather
than binding directly to the first presentation format it receives.

### spec:2.1 Canonical chapter records

Chapters, sections, people, places, audio links, and supplements should land in
structured artifacts that are reusable across pages and future tools.

### C2 Canonical site data still has to be derived from presentation-oriented HTML

- Ideal: the intake boundary delivers a stable structured export tailored for
  downstream site composition
- Constraint: derive the canonical site model from staged website files that
  were originally generated for browsing rather than downstream reuse
- Limitation: the existing upstream output is intentionally simple and does not
  yet expose all website-oriented structure
- Limitation type: ecosystem
- Evolution signal: the `input/` intake shape is documented by a durable
  structured export contract or this repo proves a better ingest seam
- Residual form: keep only a thin adapter layer

## spec:3 Information Architecture & Navigation

The site should make the book easy to traverse by chapter, topic, and companion
material without losing narrative continuity.

### spec:3.1 Reading flow and cross-links

Readers need stable chapter navigation, contextual next/previous flow, and
clear links out to companion materials. Subsection-oriented views are fine, but
they should not accidentally make parts of the book disappear; any deferred or
omitted source material needs to be intentional and documented.

### C3 Navigation and chapter-to-media links are still a handcrafted editorial surface

- Ideal: chapter relationships and companion links are assembled from canonical
  structured data with minimal manual glue
- Constraint: the first pass will likely require explicit per-chapter editorial
  mapping for some media surfaces
- Limitation: the companion material is not yet normalized into the same
  content model as the book
- Limitation type: human
- Evolution signal: chapter-level media metadata becomes complete and validated
- Residual form: keep only the editorial notes that reflect genuine curation

## spec:4 Companion Media & Archive Materials

The website should package scans, audio, and reunion extras as first-class
materials without obscuring what belongs to the core book.

### spec:4.1 Archive attachments and extra surfaces

Companion assets need honest labeling, provenance, and page-level or
chapter-level placement when appropriate.

### C4 Supplementary materials still need manual curation and packaging

- Ideal: companion assets arrive with canonical metadata and clear placement
- Constraint: curate scans, podcast links, and archive extras manually during
  the first import passes
- Limitation: those materials have not yet been gathered into a verified
  machine-readable inventory
- Limitation type: human
- Evolution signal: the source inventory is complete enough to generate the
  companion surfaces from structured records
- Residual form: keep curator notes, delete repetitive wiring

## spec:5 Site Experience & Presentation

This repo eventually needs a real website runtime and design system, but it
does not have one yet.

### spec:5.1 Frontend substrate

The chosen site stack should support a reading experience, archive browsing,
audio embeds, and later expansion without fighting the content model. It also
needs to support an interface that is highly usable on both desktop and mobile,
with room for large interactive targets and straightforward navigation for
older readers.

### C5 The website shell and design system do not exist yet

- Ideal: the canonical content model feeds a durable, expressive site shell
- Constraint: bootstrap planning and content-model work before committing to a
  frontend runtime
- Limitation: the project is brand new and the presentation substrate is still
  undecided
- Limitation type: execution
- Evolution signal: one chapter can be rendered end to end through a chosen
  site stack with honest content and media hooks
- Residual form: keep only the site shell that proves reusable

## spec:6 Provenance, Editorial Controls & Publishing

The repo should make imports, changes, and publication decisions inspectable.

### spec:6.1 Editorial and deployment honesty

Maintainers should be able to see what was imported, what was curated, and what
remains manual.

### C6 Publishing and editorial provenance are only partially defined

- Ideal: every published surface can be traced to a canonical source record and
  a repeatable build
- Constraint: begin with explicit manifests, repo docs, and generated planning
  artifacts before a full publishing pipeline exists
- Limitation: the project has not yet chosen its final deployment or content
  editing workflow
- Limitation type: execution
- Evolution signal: import records, content transforms, and deploy steps are
  encoded in the repo and re-runnable
- Residual form: keep lightweight manifests and release notes

## spec:7 Accessibility, Performance & Delivery

The final site should be readable, fast enough, and robust across devices and
connection quality.

### spec:7.1 Public-readiness quality floor

Accessibility, performance, and link integrity should be treated as product
requirements, not late polish. For this project, accessibility explicitly
includes large hit targets, strong legibility, and forgiving interactions for
an audience that will skew 80+ years old across desktop and mobile use.

### C7 Public-readiness quality still lacks measured proof on real content

- Ideal: accessibility, performance, and media integrity have repeatable checks,
  including verification that critical controls stay large, readable, and easy
  to operate across desktop and mobile
- Constraint: use the current whole-book shell as the first real quality-proof
  surface, then strengthen its checks instead of inventing fake completeness
- Limitation: the repo now has a thin runtime and UI-scout lane, but its
  desktop/mobile proof is still mostly manual and narrower than the final
  public-readiness bar
- Limitation type: execution
- Evolution signal: the first real rendered slice keeps gaining repeatable
  desktop/mobile quality checks without hiding the current manual proof
- Residual form: keep only the checks that protect the reading floor

## spec:8 AI Harnesses & Content Ops

AI should reduce repetitive cleanup and comparison work, but the outputs still
need inspectable records and human review where the archive demands it.

### spec:8.1 AI as bounded helper, not hidden source of truth

AI-driven transforms, comparisons, or summaries should emit artifacts that can
be reviewed and replaced.

### B1 AI-assisted content operations still need explicit eval and review surfaces

- Ideal: AI help is cheap, reliable, and transparent enough that heavy process
  scaffolding can disappear
- Constraint: keep eval notes, review rules, and explicit source-of-truth docs
  while the content import and site-shaping workflows are still being proven
- Limitation: current AI workflows still drift without durable context and
  inspection surfaces
- Limitation type: AI capability
- Evolution signal: repeated operations are stable enough to compress into
  simpler tooling and fewer manual review steps
- Residual form: keep only the high-value audit surfaces

## spec:9 Planning Infrastructure

The repo needs enough planning structure to survive long gaps and handoffs
without turning into process theater.

### spec:9.1 Methodology package

Ideal, spec, state, graph, stories, evals, and decisions should stay aligned.

### B2 Planning continuity still depends on explicit methodology artifacts

- Ideal: the project context would stay coherent without manual scaffolding
- Constraint: keep methodology state, compiled graph, checklist, and aligned
  runbooks while the repo is still forming
- Limitation: cross-session AI work still benefits from stable repo memory
- Limitation type: AI capability
- Evolution signal: the project settles into a smaller stable workflow that no
  longer needs the full package
- Residual form: keep only the pieces that still pay for themselves

### B3 Local intake is not yet a one-command contract

- Ideal: this repo can ingest the authoritative staged source snapshot through
  a small documented interface
- Constraint: define the `input/` intake seam before automating it
- Limitation: the current local intake relationship is known conceptually but
  not encoded as a maintained contract here
- Limitation type: ecosystem
- Evolution signal: import commands, formats, and validation live in this repo
- Residual form: keep a thin import command and its validation
