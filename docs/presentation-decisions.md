# Presentation Decisions

Recorded presentation choices for the local reading surface built in Stories
004 and 005.

## Baseline

- The raw staged export in `input/doc-web-html/story206-onward-proof-r10` is
  the fidelity baseline.
- The local builder should reshape presentation, not rewrite the underlying
  chapter content.

## Whole-Book Surface Boundary

The current reshaped local slice covers every surfaced main-book manifest entry,
grouped into three explicit sections, and may insert repo-owned family-story
supplements into the `Family Stories` run:

- Opening Pages
- Family Stories
- Closing Archive

## Decisions Locked For This Pass

- Most manifest entries stay reachable as their own reader-facing page, but
  duplicate title leaves may be absorbed into an adjacent surfaced page and
  content-empty placeholders may be intentionally deferred.
- Family stories stay grouped as a recognizable run inside the wider book
  surface.
- Repo-owned family-story supplements may appear in that same family-story run
  when they are backed by an accepted `doc_web_bundle`, a preserved source PDF,
  and a short provenance preamble.
- A dedicated `Archive Sources` page may publish preserved root-level `input/`
  PDFs and image scans with open/download actions, so source files stay
  reachable from one central reader-facing location instead of being hidden in
  maintainer-only metadata.
- When the actual `Onward to the Unknown.pdf` is available locally, the
  `Archive Sources` page may feature it first as the primary book download and
  group the remaining photocopied reunion/family-history documents under their
  own note-led section.
- Source order across the full manifest stays intact for previous/next entry
  navigation.
- The landing page uses explicit grouped sections rather than the raw mixed
  source index.
- Landing-card summaries should start with actual entry content instead of
  repeating the visible card title, and they should stay short enough for
  first-pass scanning on desktop and mobile.
- Opening-page and archive cards on the landing page may show a thumbnail when
  the surfaced entry already contains a primary image, so those sections read
  more like a browsable archive than a bare list.
- Reader-facing pages stay focused on the book itself rather than provenance or
  audit commentary.
- Public page and image labels may derive from visible in-page headings,
  captions, or other honest page cues when the raw manifest title is a
  placeholder, while internal provenance and omission-audit surfaces keep the
  source manifest title unchanged.
- Reader-facing entry titles should use normal mixed case in surfaced labels
  and page headings even when the source entry title is all caps.
- Genealogy tables should keep their column headers sticky while scrolling so
  readers can stay oriented inside the long family tables.
- Inline images should render at a readable working size instead of always
  filling the article width, and clicking them should open the full asset for
  closer inspection.
- OCR-heavy facsimile pages may get entry-specific presentation treatment when
  the default article layout distorts the source page too far, such as the
  ancestry chart and the farm award certificate pages.
- Distinct archival inserts such as the home made beer recipe may be styled as
  callouts when that improves scanability without obscuring the source text.
- When a single source entry mixes a standalone text piece with a trailing
  appendix of photos, the surfaced site may split that material into multiple
  reader-facing pages while keeping the original source blocks and provenance
  intact.
- Repeated opening-material leaves may be absorbed into the first surfaced page
  when they do not add distinct reader-facing content.
- Supplement title leaves may be absorbed into a single surfaced supplement
  page when the accepted supplement bundle still preserves that raw title page
  separately for inspection.
- Content-empty facsimile leaves may be intentionally deferred when they have
  no text, no image, and no table content to surface honestly.
- A supplement wrapper page should stay reader-facing: keep the contextual
  preamble and the main reading action, and only add original-PDF links when a
  dedicated archive-copy surface or explicitly relevant page-level attachment
  exists. Raw imported HTML and internal audit affordances should still stay
  off the public page.
- The homepage may promote the archive-source library as a separate panel and
  may feature a direct `Open Book PDF` action when `input/Onward to the Unknown.pdf`
  exists in the local intake. If that file is absent, the source-library panel
  should still appear without inventing a missing-file promise.
- When the repo owns reviewed audiobook MP3 files, the first listening surface
  should stay simple: add a dedicated audiobook page plus a page-level
  listening panel on matching chapters or supplements, using native browser
  audio controls and an explicit download link instead of a custom player.
- Shared hero headings on the homepage and audiobook page should stay on one
  line on wide desktop layouts when the available space honestly permits it,
  while smaller layouts may wrap naturally.
- Landing jump-row icons are secondary cues, not primary artwork: keep them
  small, inline with the label, and visually quieter than the button text.
- Provenance and omission-audit artifacts remain internal maintenance surfaces,
  with the checked-in snapshot living at `docs/omission-audit.json`.
- `docs/omission-audit.json` is the checked-in proof that every manifest entry
  is either rendered or intentionally deferred in a filtered build, and it may
  also list shipped supplement wrappers that sit beside the main manifest.
- Any source material omitted from a reshaped surface must be omitted
  intentionally and documented, not dropped accidentally during the rebuild.
- Accessibility is a first-order concern:
  - larger default body type
  - larger navigation targets
  - simpler page structure
  - desktop/mobile layouts that remain easy to operate for older readers

## Deliberately Deferred

- Rich front matter redesign beyond whole-entry reachability
- Rich standalone image-page redesign beyond whole-entry reachability
- Final full-book information-architecture polish
- Podcast, video, and richer companion-media embeds beyond the first on-site
  audiobook surface
- A generalized public supplement gallery beyond the current `Archive Sources`
  page plus the bounded memoir wrapper/source link
- Breaking family pages into smaller fragments
- Any claim that this is the final visual language for the entire site

## Rationale

The raw source export already preserves the content faithfully, but it mixes
front matter, chapter pages, and standalone image pages in a way that is harder
to browse for older readers. Story 004 intentionally started with the family
run; Story 005 expands that into a whole-book surface so the rest of the book
no longer disappears during reshaping. Story 007 adds the first bounded
supplement case: a memoir found as a photocopy inside the user's copy of the
book. Story 013 adds the first central archive-copy surface for the root-level
`input/` PDFs and scans, plus a direct memoir-source link that reuses that
central publication seam. The current surface still stays thin and
whole-entry-first so the project can learn from a real full-book render, one
real supplement wrapper, and one real source-library page before committing to
a heavier runtime or deeper editorial restructuring. The audit and provenance
proof surfaces still exist for maintainers, but they should not compete with
the reading experience on the public pages themselves.
