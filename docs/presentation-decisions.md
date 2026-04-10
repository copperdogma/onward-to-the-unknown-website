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

- Book Chapters
- Family stories
- Pages & Images

## Decisions Locked For This Pass

- Every manifest entry stays reachable as a whole-entry page.
- Family stories stay grouped as a recognizable run inside the wider book
  surface.
- Source order across the full manifest stays intact for previous/next entry
  navigation.
- The landing page uses explicit grouped sections rather than the raw mixed
  source index.
- Reader-facing pages stay focused on the book itself rather than provenance or
  audit commentary.
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
