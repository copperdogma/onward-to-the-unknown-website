# Runbook: ElevenLabs Audiobook Script Handoff

This repo prepares the Markdown script corpus for the *Onward to the Unknown*
audiobook. The actual ElevenLabs upload and generation step is manual and
user-run.

## Current Script Surface

- Canonical script directory: `audiobook-script/`
- Manual chapter:
  - `01-preamble.md`
- Source-derived chapters:
  - `02-the-first-lheureuxs-in-canada.md` through `20-i-wish.md`

The source-derived chapters are produced from the staged bundle in
`input/doc-web-html/story206-onward-proof-r10/` by deterministic HTML-to-
Markdown conversion inside the repo's documented audiobook boundary. The
committed source-derived corpus preserves source wording for retained spoken
text while omitting navigation chrome, figures, image captions, HTML tables,
and headings that only introduce omitted tables. `20-i-wish.md` intentionally
stops after the poem and attribution, before the visual appendix that follows
in `chapter-024`.

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

1. Review the Markdown files in `audiobook-script/`.
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

Use the reviewed Markdown files in `audiobook-script/` as the upload-ready
chapter set. The intended listening order is the filename order.

Before or during upload, note any recurring pronunciation choices for names
such as:

- `Moïse`
- `Sophie`
- `L'Heureux`
- `Pichette`
- `LaClare`

If audiobook assets later become repo truth, record:

- the chosen voice/model/settings
- any pronunciation dictionary decisions worth preserving
- where the audio files or URLs live

At that point, update the related truth surfaces, including
`tests/fixtures/formats/_coverage-matrix.json`, if the audio has become a real
published companion surface rather than a local-only experiment.
