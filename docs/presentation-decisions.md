# Presentation Decisions

Recorded presentation choices for the local reading surface built in Stories
004 and 005.

## Baseline

- The raw staged export in `input/doc-web-html/story206-onward-proof-r10` is
  the fidelity baseline.
- The local builder should reshape presentation, not rewrite the underlying
  chapter content.

## Whole-Book Surface Boundary

The current reshaped local slice covers every manifest entry, grouped into
three explicit sections:

- Opening Pages
- Family Stories
- Closing Archive

## Decisions Locked For This Pass

- Most manifest entries stay reachable as their own reader-facing page, but
  duplicate title leaves may be absorbed into an adjacent surfaced page and
  content-empty placeholders may be intentionally deferred.
- Family stories stay grouped as a recognizable run inside the wider book
  surface.
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
- Content-empty facsimile leaves may be intentionally deferred when they have
  no text, no image, and no table content to surface honestly.
- Provenance and omission-audit artifacts remain internal maintenance surfaces,
  with the checked-in snapshot living at `docs/omission-audit.json`.
- `docs/omission-audit.json` is the checked-in proof that every manifest entry
  is either rendered or intentionally deferred in a filtered build.
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
- Audio, podcasts, and companion-media embeds
- Breaking family pages into smaller fragments
- Any claim that this is the final visual language for the entire site

## Rationale

The raw source export already preserves the content faithfully, but it mixes
front matter, chapter pages, and standalone image pages in a way that is harder
to browse for older readers. Story 004 intentionally started with the family
run; Story 005 expands that into a whole-book surface so the rest of the book
no longer disappears during reshaping. The current surface still stays thin and
whole-entry-first so the project can learn from a real full-book render before
committing to a heavier runtime or deeper editorial restructuring. The audit
and provenance proof surfaces still exist for maintainers, but they should not
compete with the reading experience on the public pages themselves.
