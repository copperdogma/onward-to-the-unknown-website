# Reunion Flyer Design and Reproduction Specification

This is the portable design handoff for Story 018. It records how to reproduce
the *Onward to the Unknown* reunion flyer and phone QR card, and which values
belong to the shared Alain/Onward outreach system versus this book alone.

## Deliverables

| Surface | Final format | Exact size | Purpose |
| --- | --- | --- | --- |
| Print master | PDF | 612 × 792 points; one US Letter page | Print at 100% / Actual Size |
| Print preview | RGB PNG | 2550 × 3300 pixels | Exact 300 ppi rendering of the PDF |
| Phone card | RGB PNG | 1080 × 1920 pixels | Full-screen sharing from a phone |
| QR master | RGB PNG | 1640 × 1640 pixels | Reusable integer-module QR asset |
| Build report | JSON | N/A | Contract, tool, font, QR, geometry, size, and hash evidence |

Generated deliverables live under `output/outreach/`. Temporary phone-vector
and stress-test files live under `tmp/pdfs/outreach/` and are not reader-facing
or tracked.

## Approved Toolchain

- Python and ReportLab 4.4.10 for the deterministic vector PDF masters and QR
  encoding.
- ReportLab-bundled Bitstream Vera Sans regular and bold TrueType fonts. The
  renderer resolves the fonts and license relative to the installed package;
  the PDF embeds subsets of both fonts.
- Poppler `pdftocairo` 25.04.0 for the 300 ppi print preview and exact-size
  72 ppi phone PNG.
- Pillow 10.4.0 for the pure black-and-white standalone QR, image inspection,
  grayscale, reductions, blur/JPEG, and phone-brightness stress variants.
- pypdf 4.3.1 for PDF page, text, font, image, and transparency inspection.
- macOS Core Image/Vision is attempted first as an independent QR decoder. In
  the current sandbox it cannot create the required pixel buffer, so the
  validator records that error and uses OpenCV `QRCodeDetector` 4.10.0. OpenCV
  is independent of ReportLab's encoder and decoded the full final matrix.

Install the Python requirements with:

```bash
python -m pip install -r requirements-outreach.txt
```

Poppler and Swift/macOS frameworks remain system dependencies. The OpenCV
fallback is required when the macOS decoder is unavailable.

## Canonical Contract and Source Map

`outreach/reunion-flyer.json` is the only maintained content/design contract.
It owns reader copy, title wrapping, canonical URL, display hostname, actions,
family-name rows, cover provenance, palette, typography floors, QR parameters,
surface geometry, toner ceilings, and output paths.

| Contract content | Repo authority |
| --- | --- |
| Title, subtitle, homepage, cover path | `portable/manifest.json` |
| Canonical cover pixels | `input/doc-web-html/story206-onward-proof-r10/images/page-001-000.jpg` |
| Moïse, Sophie, and fifteen child names | accepted `page-001.html` and `page-008.html` |
| Website palette | `modules/build_family_site.py` site stylesheet |
| Read, searchable PDF, EPUB/M4B, and chapter-listening claims | live homepage, book page, and audiobook page verified 2026-07-19 |

The builder rejects a changed cover hash/dimensions, a display hostname that
does not match the encoded HTTPS URL, missing actions/name rows, essential type
below its floor, a non-white page, altered QR geometry, an incomplete output
inventory, or the prohibited phrase `No cost. No account needed.` in reader
copy.

## Shared Visual System

Keep these invariants when reproducing the Alain/Onward pair:

- one portrait US Letter page and one 1080 × 1920 phone card;
- true white page and QR quiet zone;
- Vera Sans regular/bold, large centered hierarchy, and no essential print
  text below 18 pt;
- a 4.1-inch printed QR with Q correction and four quiet modules;
- cover and QR at exactly the same 4.1-inch height, centered as one row;
- a dominant 820-pixel phone QR without the cover or family-name band;
- low-coverage type/rules/bullets only; no tinted or dark decorative panels;
- ordinary literal hostname fallback and no QR-only access;
- deterministic vector masters, Poppler derivatives, source/hash checks,
  independent QR decoding, grayscale/toner review, and separate physical proof.

## Final Print Geometry

PDF coordinates are points from the bottom-left of the 612 × 792 page.

| Component | Final geometry or baseline | Style |
| --- | --- | --- |
| Safe margin | 36 pt | No essential content outside |
| Top rules | x 36–576; y 766 and 760 | 2.4 pt accent; 1.2 pt secondary accent |
| Eyebrow | centered; baseline 742 | Vera Bold 15 pt |
| Title line 1 | `Onward to`; baseline 696 | Vera Bold 42 pt |
| Title line 2 | `the Unknown`; baseline 649 | Vera Bold 42 pt |
| Subtitle | centered; baseline 617 | Vera 17 pt |
| Free headline | centered; baseline 590 | Vera Bold 21 pt |
| Camera instruction | centered; baseline 565 | Vera 18 pt |
| Cover | x 36.5845; y 256; 222.1411 × 295.2 pt | Full source image, native aspect ratio |
| QR | x 280.2155; y 256; 295.2 pt square | 4.1 inches; Q correction |
| Display hostname | centered; baseline 226 | Vera Bold 23 pt |
| Action columns | x 49 and 313; baselines 188 and 160 | Vera 18 pt; small accent bullet |
| Family heading | centered; baseline 128 | Vera Bold 13 pt; nonessential label |
| Family-name rows | centered; baselines 98, 71, and 44 | Vera 18 pt |
| Bottom rules | y 27 and 21 | Light line and short accent rule |

The cover/QR gap is 21.49 points. The combined row is 538.8311 points wide,
leaving it inside the 540-point safe area. The two-line title is the approved
content adaptation from the Alain one-line template; no type or QR floor was
reduced.

### Cover Artwork

- Source: `input/doc-web-html/story206-onward-proof-r10/images/page-001-000.jpg`
- Source dimensions: 5096 × 6772 RGB pixels
- Source SHA-256:
  `53ed0e7fd6403d8c42800f46b7aac056d4cc9a49a8f32368ccdf4ac0735516a2`
- Printed geometry: 222.1411 × 295.2 points, or about 3.085 × 4.1 inches
- Effective embedded resolution: 1651.7 ppi in both directions
- Treatment: complete source image, no crop, stretch, retouch, transparency,
  tint, shadow, caption, or frame
- Scope: letter flyer only; the phone card remains cover-free so its QR stays
  dominant

The PDF validator requires exactly one 5096 × 6772 embedded raster image and
the original source hash/dimensions.

## Final Phone Geometry

Coordinates are pixels from the bottom-left of a 1080 × 1920 vector page that
Poppler renders at 72 ppi.

| Component | Final geometry or baseline | Style |
| --- | --- | --- |
| Safe margin | 72 px | No essential content outside |
| Top rules | y 1845 and 1827 | 8 px accent; 4 px secondary accent |
| Eyebrow | centered; baseline 1755 | Vera Bold 38 px |
| Title lines | baselines 1655 and 1555 | Vera Bold 84 px |
| Subtitle | centered; baseline 1470 | Vera 34 px |
| Free headline | two centered lines; baselines 1410 and 1355 | Vera Bold 43 px |
| Camera instruction | centered; baseline 1295 | Vera 32 px |
| QR | x 130; y 430; 820 px square | Exactly 20 px per total module |
| Hostname | centered; baseline 335 | Vera Bold 52 px |
| Availability | centered; baseline 255 | Vera Bold 29 px |
| Bottom rules | y 132 and 112 | Light line and short accent rule |

## Onward Color System

The background is always true paper white. The website's pale gradient and
paper-panel colors are deliberately omitted from the printable surfaces.

| Role | Hex | Use |
| --- | --- | --- |
| Paper | `#ffffff` | Entire background and QR quiet zone |
| Ink | `#231c14` | Main explanatory/action text |
| Muted | `#675d52` | Small nonessential family label |
| Light rule | `#d7c7b3` | Thin bottom separator |
| Deep/accent | `#6f2e1d` | Title, hostname, names, primary rules |
| Strong/secondary accent | `#8a3e29` | Free headline, bullets, secondary rules |
| QR | `#000000` | QR modules only |

The final print preview measures 26.2594% non-white pixels, including the dark
cover and QR, below the 27% ceiling. The phone card measures 15.9292%, below
its 20% ceiling. Grayscale inspection retains every hierarchy and action.

## QR Specification

- Encoded value: `https://onward.copper-dog.com/`
- Error correction: Q
- QR version: 4
- Data matrix: 33 × 33 modules
- Quiet zone: 4 modules on every edge
- Total matrix: 41 × 41 modules
- Print size: 295.2 points / 4.1 inches
- Phone size: 820 pixels / 20 pixels per total module
- Standalone master: 1640 pixels / 40 pixels per total module
- Colors: pure black on pure white; no logo, rounding, texture, tint, or
  transparency

The final preview, phone image, standalone QR, 50% and 25% flyer reductions,
25% grayscale reduction, blurred/JPEG camera proxy, and phone images at 80%
and 65% brightness all independently decode to the exact HTTPS URL.

## Commands and Practical Handoff

```bash
make test-reunion-flyer
make build-reunion-flyer
make validate-reunion-flyer
make reunion-flyer
```

Additional inspection:

```bash
pdfinfo output/outreach/onward-to-the-unknown-reunion-flyer-letter.pdf
pdffonts output/outreach/onward-to-the-unknown-reunion-flyer-letter.pdf
pdftotext output/outreach/onward-to-the-unknown-reunion-flyer-letter.pdf -
shasum -a 256 output/outreach/*
```

Print the PDF at 100% / Actual Size on matte white letter paper. Mount it near
eye level, avoid window glare, and keep a spare copy or weather sleeve. Put the
phone PNG in Photos/Favorites and show it full screen; do not crop it.

## Final Artifact Evidence

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `onward-to-the-unknown-reunion-flyer-letter.pdf` | 10,143,568 | `51b34cc53ae47689217b928365468fc98215936292c99d953c5629fb5bac5d2e` |
| `onward-to-the-unknown-reunion-flyer-letter-preview.png` | 2,720,885 | `bf60ddd36614c21936e1ffbbb70917852fade1dee9b8b6fc90fbbd7c4fc12c0a` |
| `onward-to-the-unknown-phone-qr.png` | 93,799 | `ee2063a7a7d30db8f74f4d55dc61a0460141d19a013e14ca81abfa1cab779e0c` |
| `onward-to-the-unknown-qr.png` | 12,638 | `adebc20ec10e2614a792d1b6dd95efc54ea613386b12bfb521d0490096ba1f0e` |
| `reunion-flyer-build-report.json` | 3,184 | `92b680d75319228f13295608e2817ccd8ac3cb0a26707e47b8cd0d523c48e761` |

Fresh digital proof on 2026-07-19 established one exact letter page, 476
selectable text characters, embedded Vera regular/bold, one exact source cover,
no transparency resource, exact RGB PNG sizes, pure integer-module QR master,
toner ceilings, nine independent QR decodes, and full-resolution color/phone/
grayscale visual inspection without clipping, overlap, weak contrast, or broken
glyphs.

Fresh public checks returned HTTP 200 for the homepage, book, searchable PDF,
EPUB, audiobook page, and M4B with expected PDF/EPUB/audio MIME types. The live
HTML visibly offers the book, searchable PDF, EPUB, complete M4B, and 21
individual MP3 tracks. A merged full-audiobook MP3 is not advertised as ready,
so the flyer truthfully says `Listen chapter by chapter` and uses the familiar
reader-facing description `Get eBook or audiobook` instead.

Physical proof is not inferred from these checks. Use
`outreach/reunion-flyer-physical-validation.md` against the final PDF hash
before closing Story 018.
