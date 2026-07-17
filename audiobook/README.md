The audiobook was created via ElevenLabs. The project is here: https://elevenlabs.io/app/audiobooks/AARuHDjv0GPkmtXddblf?chapterId=U8diN6iheSAEUQaBZl8d&menu=chapters
# Onward audiobook assets

`manifest.json` owns the reviewed 21-track narration order and pause settings.
The checked-in MP3 tracks remain the source recordings; generated merged or
chaptered editions are reproducible release artifacts and stay out of git.

Build and validate the chaptered Apple Books-compatible audiobook with:

```bash
make build-m4b
make validate-portable-editions
```

The M4B is written to `audiobook/generated/onward-to-the-unknown.m4b`. It uses
one AAC-LC encode from the reviewed MP3 tracks, embeds the book cover and
publication metadata, and exposes the exact 21 manifest titles as chapters.
Use `FORCE=1` only when intentionally replacing an existing generated file.

The older merged MP3 remains optional and is built separately with
`make build-full-audiobook`. The website keeps all 21 individual MP3 tracks as
the no-extra-app fallback.

See `docs/runbooks/portable-editions.md` for the full release and smoke-check
sequence.
