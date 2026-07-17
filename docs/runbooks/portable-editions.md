# Runbook: Portable EPUB and chaptered M4B

This release lane creates two generated, gitignored files from the same trusted
inputs as the website:

- `output/portable/onward-to-the-unknown.epub`
- `audiobook/generated/onward-to-the-unknown.m4b`

`portable/manifest.json` is the only manually maintained portable-publication
contract. The EPUB consumes the whole-book rendered-entry and supplement seams;
the M4B consumes the reviewed tracks and order in `audiobook/manifest.json`.

## Prerequisites

```bash
python -m pip install -r requirements-portable.txt
```

`ffmpeg`, `ffprobe`, Java, and the official EPUBCheck 5.3.0 jar must be
available. The default checked location is
`.runtime/epubcheck-5.3.0/epubcheck.jar`; `.runtime/` remains local-only.

## Build and validate

```bash
make build-portable-editions
make test-portable-editions
make validate-portable-editions
make build-family-site RELEASE=1
```

Use `FORCE=1` only when intentionally replacing generated EPUB or M4B files.
Release mode validates both before copying them into the static bundle at:

- `downloads/onward-to-the-unknown.epub`
- `audiobook/onward-to-the-unknown.m4b`

It also writes Apache MIME declarations for `application/epub+zip` and
`audio/mp4`, and fails if the homepage, book page, audiobook page, or
`reading-apps.html` does not link both files.

## Familiar-app inspection

Before release, import both files into Apple Books with **File → Import**.
Check the EPUB cover, contents, representative prose, a table, a photograph and
caption, and the final Rolland Alain memoir entry. Check that the M4B appears as
one audiobook, lists all 21 named chapters in order, and plays at the beginning
and after at least one later boundary. Also open the unpacked EPUB in an
independent renderer and check reflow at ordinary and narrow widths.

Keep the existing searchable PDF and individual MP3s available. The portable
files add convenient app choices; they do not replace the no-account website
reader and listener.

## Deploy and public proof

Deploy the exact release bundle:

```bash
python scripts/deploy_static_site.py --source build/family-site
```

Then run:

```bash
make validate-public-portable BASE_URL=https://onward.copper-dog.com/
```

The public validator requires HTTP 200, exact local byte lengths, the declared
MIME types, successful byte-range requests, and visible EPUB/M4B links on the
reading-app help page. Finish with desktop and 390px browser checks of the
homepage, `reading-apps.html`, `book.html`, and `audiobook.html`, including
horizontal overflow and console-error checks.

Current platform instructions are based on the official Apple Books import,
Amazon Send to Kindle, Kobo USB sideload, and Google Play Books upload help.
Recheck them if those services materially change their import flows.
