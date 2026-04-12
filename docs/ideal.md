# The Ideal

## Product Ideal

The website is the durable digital edition of *Onward to the Unknown* for the
family and anyone invited into the archive, with mostly elderly relatives as
the primary audience. Reading the book should feel frictionless: a person can
move chapter by chapter, jump by topic or person, follow links to companion
audio and scans, and trust that every piece of content belongs where it
appears.

The site should make the full book materially accessible on the web. If any
source material is deferred, hidden from a given surface, or omitted from an
early slice, that needs to be an intentional and inspectable choice rather than
an accidental loss during reshaping.

The site should treat the book as the center of a living archive rather than a
single isolated artifact. Chapters, recordings, scans, reunion ephemera, and
future annotations should all connect cleanly without making the site feel like
a cluttered grab bag.

The reading and browsing experience should be especially accommodating for
older family members. Core actions need large hit targets, legible controls,
clear page structure, and interaction patterns that remain easy to use on both
desktop and mobile devices.

The tone should be warm, welcoming, and family-centered. Reader-facing copy
should never drift into meta-language about the site, build process, intake
process, workflow, or implementation; it should speak directly about the book,
the people, the stories, the photographs, and the family documents.

## Execution Ideal

Bootstrapping or updating the site should feel boring in the best sense. The
canonical book content and companion materials should be ingested once,
normalized into a reusable content model, and then published into whatever site
experience the project chooses next. AI should help where it eliminates
drudgery or ambiguity, not create a pile of opaque one-off transformations.

The project should be easy to resume after long gaps. The active constraints,
source inventory, and next steps should be inspectable from repo artifacts
instead of relying on memory.

## Vision-Level Preferences

- **Archive-First.** The site should feel like a careful family archive, not a
  generic marketing site or disposable microsite.
- **Warm and Inviting.** The language and presentation should help older
  relatives feel welcomed into familiar family history rather than confronted
  with technical or institutional wording.
- **Structure Before Chrome.** Prefer a clean canonical content model over
  presentation-only fixes that trap the project inside one rendering path.
- **Provenance Is Visible.** Users and maintainers should be able to tell where
  a page, link, recording, or scan came from.
- **One Canon, Many Experiences.** The same core content should be able to feed
  chapter pages, indexes, audio companions, and future derivatives.
- **Gentle Expansion.** The initial site can be small, but the architecture
  should not make later additions painful.

## Requirements

1. **Canonical Book Experience** — Publish the book as a readable, stable, and
   navigable web experience with chapter-level entry points.
2. **Connected Companion Media** — Link audiobook, chapter podcasts, full-book
   audio, scans, and future extras where they clarify or deepen the material.
3. **Trustworthy Source Lineage** — Keep the relationship between upstream
   sources, imported content, and published pages inspectable.
4. **Reusable Content Model** — Normalize imported material into data and
   content structures that can outlive the first frontend implementation.
5. **Accessible Family Archive** — Reading, listening, and browsing should be
   legible, forgiving, and usable across devices, with large hit targets and
   clear controls that work well for older readers on desktop and mobile.
6. **Low-Friction Maintenance** — Updating the site with revised content or new
   archive assets should not require heroic manual cleanup.
