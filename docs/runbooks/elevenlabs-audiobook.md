# Runbook: ElevenLabs Audiobook Script And Asset Handoff

This repo prepares the Markdown script corpus for the *Onward to the Unknown*
audiobook. The actual ElevenLabs upload and generation step is manual and
user-run.

## Current Script Surface

- Canonical script directory: `audiobook/script/`
- Manual chapter:
  - `01-preamble.md`
- Source-derived chapters:
  - `02-the-first-lheureuxs-in-canada.md` through `21-i-wish.md`

The source-derived chapters are produced from the staged main bundle in
`input/doc-web-html/story206-onward-proof-r10/` plus the accepted memoir
supplement bundle in `input/doc-web-html/rolland-alain-memoir-r01/` by
deterministic HTML-to-Markdown conversion inside the repo's documented
audiobook boundary. The committed source-derived corpus preserves source
wording for retained spoken text while omitting navigation chrome, figures,
image captions, HTML tables, and headings that only introduce omitted tables.
`20-rolland-alain-memoir-family-story.md` is the memoir supplement chapter, and
`21-i-wish.md` intentionally stops after the poem and attribution, before the
visual appendix that follows in `chapter-024`.

## Current Asset Surface

- Canonical audiobook manifest: `audiobook/manifest.json`
- Current MP3 directory: `audiobook/ElevenLabs_Onward_to_the_Unknown/`
- Current track count in repo truth: `21`
- Current merged full-audiobook output path:
  `audiobook/ElevenLabs_Onward_to_the_Unknown/full-audiobook.mp3`
  as a local generated artifact
- Current site build entry point: `build/family-site/audiobook.html` after
  `make build-family-site`

## Build The Merged Full Audiobook

```bash
make build-full-audiobook
```

This requires `ffmpeg` on `PATH`.

This reads `audiobook/manifest.json`, concatenates the ordered chapter track
set, and inserts the manifest-configured silence gap between tracks.

The merged `full-audiobook.mp3` is intentionally treated as generated local
output, not tracked repo source. Rebuild it before a local site build or deploy
prep when you want the published bundle to include the full-book audio file.

If you intentionally want to rebuild and overwrite the merged file:

```bash
make build-full-audiobook FORCE=1
```

## Build The Source-Derived Chapters

```bash
make build-audiobook-script
```

By default this refuses to overwrite existing generated chapter files.

If you intentionally want to regenerate the source-derived chapter files from
the staged bundle after changing the converter:

```bash
make build-audiobook-script FORCE=1
```

This command does **not** touch `01-preamble.md`.
It does overwrite the other chapter files, so treat a forced regeneration as a
fresh source-derived pass that still needs a fidelity review before replacing
the canonical reviewed corpus.

## Fidelity Review

After deterministic generation:

1. Review the Markdown files in `audiobook/script/`.
2. Verify that the source-derived chapters still preserve source wording inside
   the intended spoken boundary.
3. Keep the listening boundary intact:
   - do not reintroduce genealogy tables
   - do not reintroduce figure captions, visual appendix text, or headings that
     only exist to introduce omitted tables
   - keep prose paragraphs as single lines in Markdown; do not hard-wrap manual
     copy to a fixed column width because ElevenLabs treats those line breaks as
     pauses
   - do not silently normalize wording, casing, or punctuation in the canonical
     committed corpus
   - treat any narration-specific cleanup as a downstream working copy, not as
     a replacement for the source-faithful Markdown set

## Manual ElevenLabs Handoff

This repo does not store ElevenLabs credentials and does not automate upload.

Use the reviewed Markdown files in `audiobook/script/` as the upload-ready
chapter set. The intended listening order is the filename order.

Before or during upload, note any recurring pronunciation choices for names
such as:

- `Moïse`
- `Sophie`
- `L'Heureux`
- `Pichette`
- `LaClare`

The audio files are now repo truth under
`audiobook/ElevenLabs_Onward_to_the_Unknown/`, and the site build reads
`audiobook/manifest.json` to publish the current on-site listening surface.

Still record when known:

- the chosen voice/model/settings
- any pronunciation dictionary decisions worth preserving
- any external URLs or distribution lanes if the audiobook is later published
  off-site
