---
title: "Reunion book flyer and phone QR card"
status: "Done"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "2. Connected Companion Media"
  - "3. Trustworthy Source Lineage"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "spec:7"
  - "C4"
  - "C5"
  - "C6"
  - "C7"
adr_refs: []
depends_on:
  - "story-005-whole-book-accessible-reading-surface-and-omission-audit"
  - "story-011-first-on-site-audiobook-listening-surface"
  - "story-017-portable-ereader-and-chaptered-audiobook"
category_refs:
  - "spec:4"
  - "spec:5"
  - "spec:6"
  - "spec:7"
compromise_refs:
  - "C4"
  - "C5"
  - "C6"
  - "C7"
input_coverage_refs:
  - "book-core-html"
  - "full-book-audio"
  - "portable-ebook"
  - "chaptered-audiobook"
  - "reunion-outreach"
architecture_domains:
  - "site_experience"
  - "offline family outreach"
roadmap_tags:
  - "bootstrap-canon-and-shell"
  - "reunion-outreach"
legacy_system: "word-of-mouth sharing without a readable printed or phone-display handoff"
---

# Story 018 — Reunion book flyer and phone QR card

**Priority**: High
**Status**: Done
**Decision Refs**: `docs/ideal.md`, `docs/spec.md`,
`docs/infrastructure.md`, `docs/presentation-decisions.md`,
`portable/manifest.json`, `tests/fixtures/formats/_coverage-matrix.json`,
Stories 005, 011, and 017, and the complete reproduction handoff in Alain
Lessard Story 006; no repo-local print-design or QR ADR exists after search,
and none is needed for this bounded derivative
**Depends On**: Stories 005, 011, and 017

## Goal

Create a warm, highly legible US Letter reunion flyer that lets an older family
audience immediately recognize *Onward to the Unknown*, understand that the
L'Heureux family book is online free of charge, and reach the canonical family
site by either scanning a large QR code or typing a large hostname. Create a
matching phone-display card for sharing while walking around the reunion. Keep
both surfaces deterministic, source-backed, laser-printer friendly, and visibly
related to the Alain Lessard outreach package without copying that book's
content or palette.

## Acceptance Criteria

- [x] One maintained content/design contract generates a one-page portrait US
      Letter PDF at exactly 612 × 792 points, a 2550 × 3300 print-preview PNG,
      a 1080 × 1920 phone-display PNG, a reusable standalone QR PNG, and a JSON
      build report under `output/outreach/`; canonical source inputs remain
      unchanged.
- [x] The composition retains the Alain handoff's shared visual system: true
      white background, Vera typography, large title and hostname, equal-height
      cover/QR row, four-module QR quiet zone, restrained low-coverage accents,
      and a phone card dominated by the QR. Only Onward-specific content,
      cover, palette, and evidence are substituted.
- [x] The flyer uses the exact title `Onward to the Unknown`, the formal
      subtitle `A Genealogy and Biography of the L'Heureux Family`, the
      canonical destination `https://onward.copper-dog.com/`, a literal
      `onward.copper-dog.com` fallback, and plain-language read, search,
      download, and listen choices. It does not use the rejected phrase
      `No cost. No account needed.` or imply any account requirement.
- [x] The flyer includes the unmodified canonical 1987 cover from
      `input/doc-web-html/story206-onward-proof-r10/images/page-001-000.jpg`,
      verifies its dimensions and SHA-256 hash, preserves its aspect ratio,
      matches its printed height to the 4.1-inch QR, and records source and
      effective-resolution evidence.
- [x] The reader-facing family band is source-backed by the accepted book:
      Moïse and Sophie plus the 15 children named in the book index. Names are
      spelled exactly, remain at least 18 pt, and fit without clipping.
- [x] The design meets the older-reader floor: high contrast, no essential
      print text below 18 pt, hostname at least 23 pt, generous spacing, no
      dense paragraph, no reliance on color or icons for meaning, and a
      readable grayscale rendering.
- [x] The print and phone backgrounds are true white `#ffffff`. Onward's site
      palette supplies low-coverage brown accents—ink `#231c14`, muted
      `#675d52`, border `#d7c7b3`, deep accent `#6f2e1d`, and strong accent
      `#8a3e29`—only in type, thin rules, and small bullets. No large tinted or
      dark decorative field is introduced, and the preview remains at or below
      a measured 27 percent non-white ratio including the cover and QR.
- [x] PDF inspection proves exactly one letter-size page, selectable title,
      hostname, and action text, embedded Vera regular/bold fonts, one embedded
      cover image with expected pixel dimensions, and no clipping or unintended
      transparency/font fallback. Final PNG dimensions and RGB mode are exact.
- [x] The QR uses pure black modules on white, Q error correction, a fixed
      version and four-module quiet zone, preserves square integer modules in
      raster outputs, and independently decodes from the final preview, phone
      card, standalone asset, grayscale reduction, smaller flyer reductions,
      and low-brightness phone simulations to the exact canonical HTTPS URL.
- [x] Focused fixtures cover contract validation, URL/hostname consistency,
      required copy and names, cover path/dimensions/hash, output inventory,
      exact PDF/PNG geometry, font/text/image evidence, QR structure/decode,
      grayscale/toner constraints, and failure on missing or inconsistent
      inputs.
- [x] The canonical homepage is freshly verified over HTTPS before the final
      QR is frozen, and the live page still exposes the online book, searchable
      PDF/eBook choices, and complete audiobook choices. Any production proof
      is recorded separately from local artifact proof.
- [x] The tracked handoff records exact geometry, typography, copy, palette,
      tool/font versions and hashes, commands, output paths and hashes, visual
      judgment, and practical guidance: print at 100% on matte white paper,
      mount near eye level, avoid window glare, and keep a second copy or
      weather sleeve available.
- [x] Digital proof is not described as physical proof. Story closure remains
      blocked until the hash-bound final PDF is printed at 100% and accepted on
      the intended printer, with real-device scan behavior recorded or the user
      explicitly accepting equivalent real-world evidence.

## Out of Scope

- Redesigning the family website, changing the book or narration, repackaging
  PDF/EPUB/MP3/M4B outputs, or creating a URL shortener or tracking parameter.
- A full genealogy chart, reunion program, directory, contact details,
  donation request, advertising, or commercial promotion.
- Sending files to a print shop, purchasing materials, mounting the flyer, or
  claiming physical results that were not observed.

## Approach Evaluation

- **Simplification baseline**: A single image-generation call could produce a
  visual mockup but cannot guarantee exact page/pixel geometry, spelling,
  selectable PDF text, source-cover fidelity, a four-module quiet zone, or a
  decodable canonical URL. The starting repo has zero outreach contract,
  build target, focused test, or `output/outreach/` artifact.
- **Candidate A — HTML/CSS print page**: accessible text and familiar layout,
  but exact margins, font embedding, print output, and deterministic raster
  geometry depend on a pinned browser stack this repo does not otherwise need.
- **Candidate B — ReportLab vector masters plus Poppler raster derivatives**:
  exact canvas control, embedded/selectable text, vector QR, and one geometry
  model for letter and phone surfaces using dependencies already callable in
  this environment.
- **Candidate C — SVG master**: exact vector geometry, but requires a new
  PDF/raster renderer seam without a demonstrated quality advantage here.
- **Candidate D — Pillow-only raster composition**: deterministic but gives up
  selectable PDF text and vector print/QR quality.
- **AI-only**: Appropriate only for bounded hierarchy and wording review, not
  the final QR, dimensions, names, URL, or export truth.
- **Hybrid**: Deterministic source/content/geometry/QR validation plus visual
  judgment for warmth, balance, spacing, and final physical acceptance.
- **Pure code**: Appropriate for production and verification, with the risk
  that a mechanically valid layout still needs actual-size visual judgment.
- **Repo constraints / prior decisions**: Reader-facing language must remain
  warm and family-centered; `input/` remains the source contract; generated
  artifacts belong outside canonical inputs; the first-party homepage is the
  durable publication destination; and physical proof must stay distinct from
  digital simulation.
- **Existing patterns to reuse**: `portable/manifest.json` owns title,
  subtitle, homepage, and cover; `modules/build_family_site.py` owns the site
  palette and publication links; the source index owns family names; the Alain
  Story 006 handoff owns cross-book print/phone geometry and QR treatment.
- **Eval**: Focused contract/artifact fixtures establish the zero-artifact
  baseline, followed by PDF/PNG/QR inspection, grayscale/toner measurements,
  independent QR decoding, public route checks, and actual artifact viewing.

## Tasks

- [x] Add a tracked Onward outreach contract with all book-specific content,
      source cover evidence, site-derived palette, shared geometry tokens,
      minimum type/QR rules, and output paths.
- [x] Add focused failing fixtures for contract validation and the complete
      artifact proof surface before implementation.
- [x] Implement one focused ReportLab builder/validator and thin script entry
      point without adding flyer logic to the large family-site builder.
- [x] Add maintained Makefile targets for focused tests, build, validation, and
      the combined flyer workflow.
- [x] Generate the real PDF/PNGs/report, independently decode every final and
      stress QR, inspect PDF text/font/image properties, and visually inspect
      full-size color, grayscale, and phone outputs.
- [x] Freshly verify the canonical homepage and public read/searchable-PDF,
      EPUB, individual-MP3, and complete-M4B handoffs before recording the
      final destination.
- [x] Add a complete reproduction/design spec and hash-bound physical
      validation sheet, then update README, CHANGELOG, spec/state, and coverage
      truth only from fresh evidence.
- [x] If this story changes documented format coverage or graduation reality:
      update `tests/fixtures/formats/_coverage-matrix.json` and relevant
      methodology state honestly.
- [x] Check whether the implementation makes prototype artwork, duplicated
      content constants, or manual QR files redundant; remove them or record a
      concrete follow-up.
- [x] Run required checks for touched scope:
  - [x] Focused flyer tests, Python compilation, and Ruff.
  - [x] `make test` and `make lint`.
  - [x] `make build-family-site RELEASE=1` and inspect advertised local format
        choices without rebuilding or changing canonical portable/audio input.
  - [x] `make methodology-compile`, `make methodology-check`, and
        `make skills-check`.
- [x] Evals/goldens: no AI-model eval is expected; record deterministic and
      visual/physical evidence in the story instead.
- [x] Search all docs and update any related to outreach or generated/public
      artifacts.
- [x] Verify Central Tenets:
  - [x] T0 — Traceability: copy, names, cover, destination, and format claims
        trace to accepted repo contracts and source pages.
  - [x] T1 — AI-First: AI is bounded to design judgment; deterministic tooling
        owns exact QR/export truth.
  - [x] T2 — Eval Before Build: zero-artifact baseline and focused fixtures
        precede implementation.
  - [x] T3 — Fidelity: title, names, cover, and publication claims remain
        source-faithful with no invented genealogy.
  - [x] T4 — Modular: one outreach contract and focused module own the feature;
        the large site builder is not expanded.
  - [x] T5 — Inspect Artifacts: outputs are rendered, viewed, decoded, and
        hash-bound rather than trusted from command exits.

## Workflow Gates

- [x] Build complete: implementation finished, required checks run, and summary shared
- [x] Validation complete or explicitly skipped by user
- [x] Story marked done via `/mark-story-done`

## Closure Disposition

The deterministic package and digital/public verification are complete. After
the remaining printer and second-device gap was reported explicitly, the user
accepted the final digitally inspected package as sufficient for closure by
replying `Perfect.` and invoking `/finish-and-push` on 2026-07-19.

## Accepted Evidence Boundary

- Final PDF SHA-256:
  `51b34cc53ae47689217b928365468fc98215936292c99d953c5629fb5bac5d2e`.
- `outreach/reunion-flyer-physical-validation.md` still has all printer,
  3/6-foot, bright/shaded, second-camera, and phone-card cells marked Pending.
- This execution environment produced and inspected digital files but did not
  operate the user's intended printer or a second physical phone.
- User acceptance closes the story with those observations unreported; it does
  not convert digital simulation into physical proof.

## Optional Physical Follow-up

If the flyer is later printed, use the hash-matching sheet to record actual-size
legibility and exact-URL scans with the intended printer and available phones.
That would add useful real-world evidence but is not an unfinished requirement
after the user's explicit close-out acceptance.

## Architectural Fit

- **Owning module / area**: A new small outreach contract and focused
  renderer/validator own the derivative artifacts; the site builder remains a
  read-only source of publication truth and palette values.
- **Methodology reality**: `spec:4`, `spec:5`, `spec:6`, and `spec:7` have
  partial substrate in the active bootstrap campaign; `C4`–`C7` are in climb.
  Coverage rows `book-core-html`, `full-book-audio`, `portable-ebook`, and
  `chaptered-audiobook` prove the advertised source/publication surfaces, but
  no row currently records offline reunion outreach.
- **Substrate evidence**: `portable/manifest.json` supplies the formal title,
  subtitle, cover path, and homepage; the cover exists at 5096 × 6772 pixels
  with SHA-256 `53ed0e7fd6403d8c42800f46b7aac056d4cc9a49a8f32368ccdf4ac0735516a2`;
  `page-008.html` supplies the 15 child names; the live/publication substrate
  was closed by Story 017; ReportLab, Pillow, pypdf, Poppler, and macOS Vision
  are callable locally.
- **Data contracts / schemas**: Add one repo-owned JSON contract for reader
  copy, provenance, geometry, palette, and outputs. No source, publication,
  database, or cross-repo schema changes.
- **File sizes**: `modules/reunion_flyer.py` is 876 cohesive build/validation
  lines, the CLI is 35 lines, focused tests are 150 lines, and `Makefile` is 108
  lines. The 5,000+ line family-site builder remains deliberately unmodified;
  split contract/build/validation modules if this bounded workflow grows.
- **Decision context**: Reviewed the Ideal, spec/state/graph, coverage matrix,
  infrastructure and presentation docs, Stories 005/011/017, source manifest,
  portable contract, site palette, source index, and Alain Story 006 plus its
  complete design handoff. No ADR is required for a bounded deterministic
  derivative; a shared cross-book service or new publishing route would.

## Files to Modify

- `docs/stories/story-018-reunion-book-flyer-and-phone-qr.md` — plan, evidence,
  and handoff record (new)
- `outreach/reunion-flyer.json` — sole content/design/output contract (new)
- `outreach/reunion-flyer-design-spec.md` — exact reproduction handoff (new)
- `outreach/reunion-flyer-physical-validation.md` — hash-bound real-world proof
  sheet (new)
- `modules/reunion_flyer.py`, `scripts/reunion_flyer.py` — focused
  builder/validator and CLI (new)
- `scripts/decode_qr_vision.swift` — independent macOS Vision decode helper
  (new)
- `tests/test_reunion_flyer.py` — focused contract and artifact fixtures (new)
- `Makefile` — maintained build/test/validate targets
- `.gitignore`, `requirements-outreach.txt` — generated-output boundary and
  pinned Python dependencies
- `README.md`, `CHANGELOG.md`, `docs/spec.md`,
  `docs/methodology/state.yaml`, and
  `tests/fixtures/formats/_coverage-matrix.json` — durable truth after proof
- `docs/methodology/graph.json`, `docs/stories.md` — regenerated views

## Redundancy / Removal Targets

- Repeated title, URL, family names, palette, cover evidence, output paths, or
  QR parameters outside `outreach/reunion-flyer.json`.
- Prototype PDFs/PNGs or manually generated QR screenshots; final pixels must
  be builder-owned and reproducible.
- Any attempt to add outreach rendering to `modules/build_family_site.py`.

## Notes

This is a new Story 018 rather than reopening Story 017 because the portable
release closed standards packaging, app handoff, and public byte delivery.
Printed/phone outreach introduces exact page geometry, QR scanning, cover/toner
constraints, and physical acceptance as a distinct validation boundary. The
user explicitly requested creation and execution of this Onward counterpart on
2026-07-19, satisfying the implementation human gate once this detailed plan
is recorded.

## Final Production Record

- **Selected candidate**: Candidate B, deterministic ReportLab vector masters
  with Poppler raster derivatives, licensed bundled Vera fonts, a source-owned
  cover image, and independent QR decoding. It won because the real artifacts
  preserve exact letter/phone geometry, selectable PDF text, an undistorted
  4.1-inch QR, equal-height cover recognition, and a reproducible low-toner
  system without a browser or hand-edited image seam.
- **Final reader copy**: `A L'HEUREUX FAMILY BOOK`; two-line title `Onward to`
  / `the Unknown`; formal subtitle; `The family book is online — free for
  everyone`; camera instruction; literal `onward.copper-dog.com`; actions
  `Read the book online`, `Open the searchable PDF`, `Get eBook or audiobook`,
  and `Listen chapter by chapter`; source-index family-name band; phone summary
  `Read • Search • Download • Listen`.
- **Actual-size judgment**: Full 2550 × 3300 print, 1080 × 1920 phone, and 25%
  grayscale images were viewed in this pass. The two-line title is dominant
  without crowding, the complete cover and QR form a balanced equal-height row,
  the hostname/actions/names remain plainly legible, the phone QR dominates its
  useful area, and no clipping, overlap, broken glyph, unintended tint, or weak
  grayscale hierarchy was observed.
- **Geometry**: Letter 612 × 792 pt; cover x/y 36.5845/256 pt at 222.1411 ×
  295.2 pt; 21.49 pt gap; QR x/y 280.2155/256 pt at 295.2 pt; group width
  538.8311 pt. Phone 1080 × 1920 px with an 820 px QR at x/y 130/430. Exact
  typography and baselines are in `outreach/reunion-flyer-design-spec.md`.
- **QR/digital evidence**: version 4, Q correction, 33 data modules, four quiet
  modules, 41 total modules, and a 1640 px master at 40 px/module. OpenCV
  QRCodeDetector 4.10.0 independently decoded the preview, phone, master, 50%
  and 25% reductions, 25% grayscale, blurred/JPEG camera proxy, and 80%/65%
  phone-brightness images to `https://onward.copper-dog.com/`. macOS Core
  Image/Vision was attempted first but the sandbox could not allocate its
  pixel buffer; the validator preserves that error rather than masking it.
- **PDF/raster evidence**: one 612 × 792 pt page, 476 selectable characters,
  embedded/subset Bitstream Vera Sans regular/bold, exactly one embedded 5096 ×
  6772 source-cover image at 1651.7 ppi, no transparency resource, exact RGB
  preview/phone/master pixels, 26.2594% print non-white ratio, and 15.9292%
  phone non-white ratio.
- **Public evidence**: Fresh 2026-07-19 HTTP checks returned 200 for the HTTPS
  homepage, `book.html`, searchable source PDF, EPUB, `audiobook.html`, and M4B;
  the PDF/EPUB/M4B reported `application/pdf`, `application/epub+zip`, and
  `audio/mp4`. Fresh live HTML showed online reading, searchable PDF, EPUB,
  complete M4B, and 21 individual MP3 choices. The absent merged MP3 was not
  advertised on the flyer.
- **Manual/post-processing**: AI/human visual judgment selected the Onward
  line breaks, palette, family band, and truth-matched actions. There was no
  image retouching, crop, manual QR replacement, or post-build pixel edit;
  every reader-facing pixel is generator-owned.
- **Commands**: `make test-reunion-flyer`, `make build-reunion-flyer`,
  `make validate-reunion-flyer`, `make test`, `make lint`,
  `make build-family-site RELEASE=1`, `make methodology-compile`,
  `make methodology-check`, `make skills-check`, plus `pdfinfo`, `pdffonts`,
  `pdftotext`, JSON parsing, SHA-256 inventory, and `git diff --check`.
- **Final artifacts**:

  | Path | Bytes | SHA-256 |
  | --- | ---: | --- |
  | `output/outreach/onward-to-the-unknown-reunion-flyer-letter.pdf` | 10,143,568 | `51b34cc53ae47689217b928365468fc98215936292c99d953c5629fb5bac5d2e` |
  | `output/outreach/onward-to-the-unknown-reunion-flyer-letter-preview.png` | 2,720,885 | `bf60ddd36614c21936e1ffbbb70917852fade1dee9b8b6fc90fbbd7c4fc12c0a` |
  | `output/outreach/onward-to-the-unknown-phone-qr.png` | 93,799 | `ee2063a7a7d30db8f74f4d55dc61a0460141d19a013e14ca81abfa1cab779e0c` |
  | `output/outreach/onward-to-the-unknown-qr.png` | 12,638 | `adebc20ec10e2614a792d1b6dd95efc54ea613386b12bfb521d0490096ba1f0e` |
  | `output/outreach/reunion-flyer-build-report.json` | 3,184 | `92b680d75319228f13295608e2817ccd8ac3cb0a26707e47b8cd0d523c48e761` |

- **Physical evidence**: Unreported and explicitly accepted as a remaining
  evidence gap. No print or second-device result is inferred from digital
  simulation. The hash-bound optional matrix lives at
  `outreach/reunion-flyer-physical-validation.md`.

## Optional Physical Follow-up Plan

These steps are preserved for a future reunion setup, not as dangling Story 018
work after the user's explicit close-out acceptance.

1. **Confirm the final file.** Verify that the printed PDF has SHA-256
   `51b34cc53ae47689217b928365468fc98215936292c99d953c5629fb5bac5d2e`.
2. **Print at actual size.** Print on matte-white US Letter paper at
   100% / Actual Size with no Fit or Shrink setting.
3. **Check the flyer in the room.** Confirm comfortable reading at actual
   size and scan the exact URL at roughly 3 and 6 feet in bright and shaded
   conditions with two available phone cameras.
4. **Check the phone card.** Show the PNG full-screen without cropping and
   scan it from a second physical device at normal and high brightness.
5. **Record observations.** Enter any later real-world results in
   `outreach/reunion-flyer-physical-validation.md` without rewriting the
   original digital-validation record.

**Impact and risk**: The slice adds a deterministic derivative workflow but
does not change the website, source book, portable packages, narration, public
routes, or deployment. Principal risks are QR distortion, font fallback,
cover-driven toner load, overly long family-name rows, and accidental claims
of physical proof. Focused geometry/decode tests, full-resolution inspection,
and a hash-bound physical sheet contain those risks.

## Work Log

20260719-1146 — story creation and exploration: created Story 018 as a distinct
offline/phone outreach validation boundary, reviewed the Ideal, spec/state/
graph, coverage matrix, infrastructure, site palette, accepted title/subtitle/
homepage/cover contracts, source index names, Stories 005/011/017, repo-local
decisions, Alain Story 006, and its self-sufficient design specification;
verified the public-format and local rendering substrate exists, the canonical
cover is 5096 × 6772 RGB with SHA-256
`53ed0e7fd6403d8c42800f46b7aac056d4cc9a49a8f32368ccdf4ac0735516a2`,
and the required Python/Poppler/Vision tools are callable; found no print/QR ADR
or existing outreach implementation, so the story is honestly Pending and the
next step is methodology compilation followed by the recorded, user-approved
implementation plan.

20260719-1151 — eval baseline and implementation gate: freshly confirmed that
`output/outreach/` is absent and `make test-reunion-flyer` has no rule, so the
repo starts with zero maintained outreach outputs or validation surface; the
detailed five-step Plan above has no new dependency, schema, deployment, or
human-approval blocker, and the user's explicit instruction to make and execute
the Onward version authorizes implementation; promoted the fully detailed,
substrate-verified story from Pending to In Progress, next step is focused
contract/tests followed by the deterministic builder.

20260719-1201 — deterministic build and refinement: added the sole tracked
outreach contract, pinned requirements, focused ReportLab builder/validator and
CLI, Mac QR helper with recorded OpenCV fallback, focused tests, Makefile
targets, ignored generated-output boundary, and the full PDF/preview/phone/QR/
report artifact family; first independent decode exposed unavailable macOS
Vision/ANE and CPU pixel-buffer paths, so validation retained the failure and
used independent OpenCV rather than weakening the decode gate; full-resolution
color, phone, and grayscale inspection then prompted truth-matching action copy
(`searchable PDF`, `EPUB or M4B`, `chapter by chapter`) from the freshly fetched
public HTML, next step was rebuild and final verification.

20260719-1210 — final digital/public verification and methodology alignment:
rebuilt the final action-copy revision and passed all 8 focused tests; all nine
final/stress QR surfaces decoded to the exact canonical URL; PDF inspection
proved one letter page, selectable text, embedded Vera fonts, exact source
cover, and no transparency; print/phone non-white ratios were 0.262634 and
0.159292; live HTTPS HEAD/HTML checks proved the homepage, book, searchable
PDF, EPUB, audiobook page, complete M4B, and individual MP3 handoffs; added the
reproduction spec, physical-validation sheet, README/changelog/spec/state/
coverage updates, and the `reunion-outreach` trace found by `/align`; fresh full
verification passed `64` tests, Ruff, strict release site build, methodology
compile/check, skills-check, JSON parsing, PDF command-line inspection, and
`git diff --check`; implementation is complete, but status is Blocked pending
the hash-bound physical print and real-device acceptance required for closure.

20260719-1216 — reader-copy revision reopened: the user correctly identified
that `Download EPUB or M4B` asks an 80-year-old audience to understand format
extensions; current artifact text and exact-copy fixture confirm that baseline,
while the phone summary is already plain-language; resumed Story 018 from
Blocked to In Progress with explicit approval to substitute familiar eBook and
audiobook wording, rebuild all generated artifacts, refresh hashes, and return to
the unchanged physical-proof gate.

20260719-1225 — reader-copy revision verified: an initial `Download eBook or
audiobook` candidate exceeded the 250-point action column at the protected
18-point type size, so the final sole-contract wording is `Get eBook or
audiobook` at 217.28 points with no type reduction; rebuilt every generated
artifact, passed all 8 focused tests and the complete QR/PDF validator, and
visually inspected the full-resolution preview for fit, balance, contrast, and
clipping; the revised PDF has 476 selectable characters, a 26.2594% non-white
ratio, nine exact-URL QR decodes, and SHA-256
`51b34cc53ae47689217b928365468fc98215936292c99d953c5629fb5bac5d2e`;
refreshed the reproduction and physical-proof handoffs and returned Story 018
to Blocked because the real print and second-device checks remain pending.

20260719-1251 — `/mark-story-done` close-out: after being told that printing
and a second-phone check were the only remaining gate, the user replied
`Perfect.` and invoked `/finish-and-push`; recorded that as explicit acceptance
to close with the physical matrix unreported, not as a claim of physical proof;
fresh close-out validation rebuilt the identical hash-bound artifact family,
decoded all nine final/stress QR surfaces to the exact URL, passed all 64 Python
tests and Ruff, built the strict release site, passed methodology, skill, and
diff checks, and confirmed HTTP 200 plus expected content types for the live
homepage, book, source PDF, EPUB, audiobook page, and M4B; all tasks, acceptance
criteria, dependencies, tenets, documentation, and workflow gates are resolved,
no model eval or ADR update applies, Story 018 is Done, and the recommended next
step is `/check-in-diff`.
