"""Build, inspect, and publish the portable EPUB/M4B edition contract."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
import zipfile
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from html import escape
from pathlib import Path, PurePosixPath
from typing import Iterable
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree as StdET

from lxml import etree, html
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_PATH = ROOT / "portable" / "manifest.json"
XHTML_NS = "http://www.w3.org/1999/xhtml"
EPUB_NS = "http://www.idpf.org/2007/ops"
BLOCK_ID_RE = re.compile(r'\bid="([^"]+)"')
PART_TITLES = {
    "opening-pages": "Opening Pages",
    "family-stories": "Family Stories",
    "closing-archive": "Closing Archive",
    "companions": "Companion Documents",
}


class PortableEditionError(ValueError):
    """Raised when a portable-edition contract or artifact is invalid."""


@dataclass(frozen=True)
class Publication:
    identifier: str
    title: str
    subtitle: str
    language: str
    author: str
    publisher: str
    original_publication_year: str
    modified: str
    description: str
    source_url: str
    cover_source_path: Path
    cover_output_path: Path


@dataclass(frozen=True)
class PortableArtifact:
    output_path: Path
    public_path: str
    media_type: str
    settings: dict[str, object]

    @property
    def is_available(self) -> bool:
        return self.output_path.is_file() and self.output_path.stat().st_size > 0


@dataclass(frozen=True)
class PortableCatalog:
    manifest_path: Path
    publication: Publication
    epub: PortableArtifact
    m4b: PortableArtifact

    @property
    def is_available(self) -> bool:
        return self.epub.is_available and self.m4b.is_available


@dataclass(frozen=True)
class EpubDocument:
    slug: str
    title: str
    part_id: str
    content_html: str
    image_sources: dict[str, Path]
    page_path: str
    is_main_book: bool = True


@dataclass
class EpubValidation:
    errors: list[str]
    notes: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


@dataclass
class PublicValidation:
    errors: list[str]
    notes: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def _required_string(payload: dict[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PortableEditionError(f"Portable manifest `{key}` must be a non-empty string.")
    return value.strip()


def _repo_path(value: object, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise PortableEditionError(f"Portable manifest `{label}` must be a relative path.")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise PortableEditionError(f"Portable manifest `{label}` must stay within the repo: {value}")
    return ROOT.joinpath(*path.parts)


def _public_path(value: object, label: str, suffix: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PortableEditionError(f"Portable manifest `{label}` must be a public path.")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not str(path).endswith(suffix):
        raise PortableEditionError(
            f"Portable manifest `{label}` is unsafe or has the wrong suffix: {value}"
        )
    try:
        str(path).encode("ascii")
    except UnicodeEncodeError as exc:
        raise PortableEditionError(
            f"Portable manifest `{label}` must be ASCII-safe: {value}"
        ) from exc
    return str(path)


def load_portable_catalog(path: str | Path = DEFAULT_MANIFEST_PATH) -> PortableCatalog:
    manifest_path = Path(path).expanduser().resolve()
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PortableEditionError(f"Cannot read portable manifest {manifest_path}: {exc}") from exc
    if payload.get("schema_version") != "onward_portable_editions_v1":
        raise PortableEditionError("Portable manifest has an unsupported schema version.")
    publication_payload = payload.get("publication")
    epub_payload = payload.get("epub")
    m4b_payload = payload.get("m4b")
    if not all(isinstance(item, dict) for item in (publication_payload, epub_payload, m4b_payload)):
        raise PortableEditionError("Portable manifest requires publication, epub, and m4b objects.")
    publication = Publication(
        identifier=_required_string(publication_payload, "identifier"),
        title=_required_string(publication_payload, "title"),
        subtitle=_required_string(publication_payload, "subtitle"),
        language=_required_string(publication_payload, "language"),
        author=_required_string(publication_payload, "author"),
        publisher=_required_string(publication_payload, "publisher"),
        original_publication_year=_required_string(publication_payload, "original_publication_year"),
        modified=_required_string(publication_payload, "modified"),
        description=_required_string(publication_payload, "description"),
        source_url=_required_string(publication_payload, "source_url"),
        cover_source_path=_repo_path(publication_payload.get("cover_source_path"), "cover_source_path"),
        cover_output_path=_repo_path(publication_payload.get("cover_output_path"), "cover_output_path"),
    )
    epub = PortableArtifact(
        output_path=_repo_path(epub_payload.get("output_path"), "epub.output_path"),
        public_path=_public_path(epub_payload.get("public_path"), "epub.public_path", ".epub"),
        media_type=_required_string(epub_payload, "media_type"),
        settings={
            key: value
            for key, value in epub_payload.items()
            if key not in {"output_path", "public_path", "media_type"}
        },
    )
    m4b = PortableArtifact(
        output_path=_repo_path(m4b_payload.get("output_path"), "m4b.output_path"),
        public_path=_public_path(m4b_payload.get("public_path"), "m4b.public_path", ".m4b"),
        media_type=_required_string(m4b_payload, "media_type"),
        settings={
            key: value
            for key, value in m4b_payload.items()
            if key not in {"output_path", "public_path", "media_type"}
        },
    )
    if epub.media_type != "application/epub+zip" or m4b.media_type != "audio/mp4":
        raise PortableEditionError("Portable manifest MIME types must be application/epub+zip and audio/mp4.")
    return PortableCatalog(manifest_path, publication, epub, m4b)


def ensure_portable_cover(publication: Publication, *, force: bool = False) -> Path:
    source = publication.cover_source_path
    output = publication.cover_output_path
    if not source.is_file():
        raise PortableEditionError(f"Portable-edition cover source is missing: {source}")
    if output.is_file() and not force and output.stat().st_mtime >= source.stat().st_mtime:
        return output
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((1600, 2000), Image.Resampling.LANCZOS)
        image.save(output, "JPEG", quality=84, optimize=True, progressive=False)
    return output


def canonical_epub_documents(source_dir: Path | None = None) -> tuple[list[EpubDocument], list[str]]:
    """Derive the EPUB from the same entries and supplement seams as the site."""
    from modules.build_family_site import (
        DEFAULT_SOURCE_DIR,
        absorbed_entries_by_target,
        absorbed_output_paths,
        build_rendered_entries,
        build_supplement_rendered_entry,
        bundle_entry_from_manifest,
        discover_published_source_assets,
        load_family_story_supplements,
        load_manifest,
        load_provenance_rows,
    )

    source_dir = source_dir or DEFAULT_SOURCE_DIR
    manifest = load_manifest(source_dir)
    entries = [bundle_entry_from_manifest(row) for row in manifest.get("entries", [])]
    absorbed = absorbed_output_paths(entries)
    rendered = build_rendered_entries(
        source_dir,
        entries,
        provenance_rows_by_entry_id=load_provenance_rows(source_dir),
        absorbed_entry_ids=set(absorbed),
        absorbed_entries_by_target_id=absorbed_entries_by_target(entries),
    )
    documents: list[EpubDocument] = []
    main_source_ids: list[str] = []
    for item in rendered:
        image_sources: dict[str, Path] = {}
        wrapper = html.fragment_fromstring(item.article_html, create_parent="div")
        for image in wrapper.xpath(".//img[@src]"):
            src = str(image.get("src") or "")
            if not src.startswith("images/"):
                raise PortableEditionError(
                    f"Unsupported main-book EPUB image path in {item.display_title}: {src}"
                )
            image_sources[src] = source_dir / src
        documents.append(
            EpubDocument(
                slug=item.entry.entry_id,
                title=item.display_title,
                part_id=item.group.id,
                content_html=item.article_html,
                image_sources=image_sources,
                page_path=item.entry.path,
                is_main_book=True,
            )
        )
        main_source_ids.extend(BLOCK_ID_RE.findall(item.article_html))

    supplements = load_family_story_supplements(source_dir)
    source_assets = discover_published_source_assets(source_dir, supplements)
    assets_by_path = {asset.source_path.resolve(): asset for asset in source_assets}
    with tempfile.TemporaryDirectory(prefix="onward-epub-supplement-") as tmp:
        output_dir = Path(tmp)
        for supplement in supplements:
            item, _audit = build_supplement_rendered_entry(
                supplement,
                output_dir=output_dir,
                internal_dir=output_dir / "_internal",
                published_source_assets_by_path=assets_by_path,
            )
            wrapper = html.fragment_fromstring(item.article_html, create_parent="div")
            images = wrapper.xpath(".//img[@src]")
            if images:
                raise PortableEditionError(
                    f"Supplement EPUB image handling is not configured for {item.display_title}."
                )
            documents.append(
                EpubDocument(
                    slug=item.entry.entry_id,
                    title=item.display_title,
                    part_id="companions",
                    content_html=item.article_html,
                    image_sources={},
                    page_path=item.entry.path,
                    is_main_book=False,
                )
            )
    return documents, main_source_ids


def _slug_filename(path: Path) -> str:
    digest = sha256(str(path.resolve()).encode("utf-8")).hexdigest()[:10]
    safe_name = re.sub(r"[^a-zA-Z0-9._-]+", "-", path.name)
    return f"{digest}-{safe_name}"


def _xhtmlize(element: etree._Element) -> None:
    if isinstance(element.tag, str) and not element.tag.startswith("{"):
        element.tag = f"{{{XHTML_NS}}}{element.tag.lower()}"
    for attribute in list(element.attrib):
        if attribute.startswith("data-") or attribute in {"loading", "decoding"}:
            del element.attrib[attribute]
    for child in element:
        _xhtmlize(child)


def _remove_element(element: etree._Element) -> None:
    parent = element.getparent()
    if parent is not None:
        parent.remove(element)


def _prepare_document(
    document: EpubDocument,
    image_names: dict[Path, str],
    page_links: dict[str, str],
    *,
    language: str,
    source_note_html: str = "",
) -> tuple[bytes, set[Path]]:
    wrapper = html.fragment_fromstring(document.content_html, create_parent="div")
    for element in wrapper.xpath(
        ".//*[contains(concat(' ', normalize-space(@class), ' '), ' article-heading-icon ') "
        "or contains(concat(' ', normalize-space(@class), ' '), ' supplement-actions ')]"
    ):
        _remove_element(element)
    if not document.is_main_book:
        id_prefix = f"{document.slug}-"
        for element in wrapper.xpath(".//*[@id]"):
            element.set("id", f"{id_prefix}{str(element.get('id') or '')}")
        for anchor in wrapper.xpath(".//a[starts-with(@href, '#')]"):
            anchor.set("href", f"#{id_prefix}{str(anchor.get('href'))[1:]}")
    used_images: set[Path] = set()
    for image in wrapper.xpath(".//img[@src]"):
        original = str(image.get("src") or "")
        source = document.image_sources.get(original)
        if source is None or not source.is_file():
            raise PortableEditionError(
                f"EPUB image cannot be resolved for {document.title}: {original}"
            )
        resolved = source.resolve()
        used_images.add(resolved)
        image.set("src", f"../images/{image_names[resolved]}")
        if not str(image.get("alt") or "").strip():
            raise PortableEditionError(
                f"EPUB image is missing alternative text in {document.title}: {original}"
            )
    for anchor in wrapper.xpath(".//a[@href]"):
        href = str(anchor.get("href") or "")
        parsed = urlsplit(href)
        if parsed.scheme or href.startswith(("#", "//")):
            continue
        target = page_links.get(parsed.path)
        if target:
            rewritten = PurePosixPath(target).name
            if parsed.fragment:
                rewritten += f"#{parsed.fragment}"
            anchor.set("href", rewritten)
        elif parsed.path in document.image_sources:
            anchor.drop_tag()
        elif parsed.path:
            anchor.drop_tag()
    first_heading = wrapper.xpath(".//*[self::h1 or self::h2][1]")
    source_heading = (
        re.sub(r"\s+", " ", first_heading[0].text_content()).strip().casefold()
        if first_heading
        else ""
    )
    document_heading = re.sub(r"\s+", " ", document.title).strip().casefold()
    include_publication_heading = source_heading != document_heading
    _xhtmlize(wrapper)
    body_children = b"".join(
        etree.tostring(child, encoding="utf-8", method="xml") for child in wrapper
    )
    title = escape(document.title)
    body_accessibility = (
        'aria-labelledby="publication-heading"'
        if include_publication_heading
        else f'aria-label="{title}"'
    )
    publication_heading = (
        f'<h1 id="publication-heading">{title}</h1>'
        if include_publication_heading
        else ""
    )
    content = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f'<html xmlns="{XHTML_NS}" xmlns:epub="{EPUB_NS}" lang="{escape(language)}" '
        f'xml:lang="{escape(language)}">\n'
        f'<head><title>{title}</title><link rel="stylesheet" type="text/css" '
        f'href="../styles/book.css"/></head>\n'
        f'<body epub:type="bodymatter" {body_accessibility}>'
        f"{publication_heading}{source_note_html}"
    ).encode("utf-8") + body_children + b"</body></html>\n"
    return content, used_images


def _media_type(path: Path) -> str:
    media_type = mimetypes.guess_type(path.name)[0]
    if media_type == "image/jpg":
        return "image/jpeg"
    if media_type not in {"image/jpeg", "image/png", "image/gif", "image/svg+xml", "image/webp"}:
        raise PortableEditionError(f"Unsupported EPUB image type: {path}")
    return media_type


def _zip_info(name: str, *, stored: bool = False) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    return info


def hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def build_epub_package(
    catalog: PortableCatalog,
    documents: Iterable[EpubDocument],
    *,
    expected_main_source_ids: Iterable[str],
    output: str | Path | None = None,
    force: bool = False,
) -> Path:
    docs = list(documents)
    if not docs:
        raise PortableEditionError("Cannot build an EPUB without documents.")
    output_path = Path(output).expanduser().resolve() if output else catalog.epub.output_path
    if output_path.exists() and not force:
        raise PortableEditionError(
            f"Refusing to overwrite existing EPUB without --force: {output_path}"
        )
    cover = ensure_portable_cover(catalog.publication, force=force)
    image_paths = {source.resolve() for doc in docs for source in doc.image_sources.values()}
    image_paths.add(cover.resolve())
    image_names = {path: _slug_filename(path) for path in sorted(image_paths)}
    image_names[cover.resolve()] = "cover.jpg"
    page_links = {
        document.page_path: f"text/{index:03d}-{document.slug}.xhtml"
        for index, document in enumerate(docs, start=1)
    }

    prepared: list[tuple[EpubDocument, str, bytes]] = []
    used_images: set[Path] = {cover.resolve()}
    for index, document in enumerate(docs, start=1):
        filename = f"text/{index:03d}-{document.slug}.xhtml"
        source_note_html = ""
        if index == 1:
            source_note_html = (
                '<aside class="source-note"><h2>About this digital family edition</h2>'
                '<p>This reading copy follows the 1987 <em>Onward to the Unknown</em> '
                'family book and includes the Rolland Alain memoir found inside one copy. '
                f'<a href="{escape(catalog.publication.source_url)}">The family website</a> '
                'keeps the searchable book PDF and source documents beside it.</p></aside>'
            )
        xhtml, document_images = _prepare_document(
            document,
            image_names,
            page_links,
            language=catalog.publication.language,
            source_note_html=source_note_html,
        )
        prepared.append((document, filename, xhtml))
        used_images.update(document_images)
    unused_images = image_paths - used_images
    if unused_images:
        raise PortableEditionError(
            "EPUB image inventory contains unused files: "
            + ", ".join(str(path) for path in sorted(unused_images))
        )

    publication = catalog.publication
    cover_xhtml = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="{XHTML_NS}" xmlns:epub="{EPUB_NS}" lang="{escape(publication.language)}" xml:lang="{escape(publication.language)}">
<head><title>Cover</title><link rel="stylesheet" type="text/css" href="styles/book.css"/></head>
<body epub:type="cover"><section class="cover"><img src="images/cover.jpg" alt="Cover of {escape(publication.title)}"/></section></body>
</html>
'''.encode()
    nav_rows: list[str] = []
    current_part: str | None = None
    for document, filename, _content in prepared:
        if document.part_id != current_part:
            if current_part is not None:
                nav_rows.append("</ol></li>")
            current_part = document.part_id
            nav_rows.append(
                f'<li><span>{escape(PART_TITLES.get(current_part, current_part.title()))}</span><ol>'
            )
        nav_rows.append(f'<li><a href="{filename}">{escape(document.title)}</a></li>')
    if current_part is not None:
        nav_rows.append("</ol></li>")
    nav_xhtml = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="{XHTML_NS}" xmlns:epub="{EPUB_NS}" lang="{escape(publication.language)}" xml:lang="{escape(publication.language)}">
<head><title>Contents</title><link rel="stylesheet" type="text/css" href="styles/book.css"/></head>
<body><nav epub:type="toc" id="toc" aria-labelledby="toc-heading"><h1 id="toc-heading">Contents</h1><ol>{''.join(nav_rows)}</ol></nav>
<nav epub:type="landmarks" hidden="hidden"><ol><li><a epub:type="cover" href="cover.xhtml">Cover</a></li><li><a epub:type="bodymatter" href="{prepared[0][1]}">Begin reading</a></li></ol></nav></body>
</html>
'''.encode()
    css = b'''body { color: #20211f; font-family: Georgia, serif; line-height: 1.55; margin: 1.5em; }
h1, h2, h3, h4 { color: #263c39; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.2; }
body > h1 { break-before: page; } body img { display: block; height: auto; margin: 1em auto; max-height: 420px !important; max-width: 100%; object-fit: contain; }
figure { break-inside: avoid; margin: 1em 0; } figcaption { font-size: .9em; font-style: italic; text-align: center; }
.table-scroll { max-width: 100%; overflow-x: auto; } table { border-collapse: collapse; display: table; font-size: .82em; max-width: 100%; width: 100%; }
th, td { border: 1px solid #8c8f89; padding: .25em; text-align: left; vertical-align: top; overflow-wrap: anywhere; }
.cover { margin: 0; padding: 0; text-align: center; } .cover img { max-height: 95vh !important; }
a { color: #184f72; text-decoration: underline; } nav ol { padding-left: 1.3em; } nav li { margin: .35em 0; }
.source-note, .supplement-intro { border: 1px solid #aab7b0; box-sizing: border-box; margin: 1em 0 2em; padding: .7em 1em; }
.supplement-intro { display: inline-block; max-width: 90vw; width: 34em; } .supplement-body { display: contents; }
.source-note h2 { font-size: 1.1em; margin-top: 0; }
'''
    image_items = []
    for index, source in enumerate(sorted(used_images), start=1):
        properties = ' properties="cover-image"' if source == cover.resolve() else ""
        image_items.append(
            f'<item id="image-{index}" href="images/{escape(image_names[source])}" '
            f'media-type="{_media_type(source)}"{properties}/>'
        )
    doc_items = [
        f'<item id="doc-{index}" href="{filename}" media-type="application/xhtml+xml"/>'
        for index, (_doc, filename, _content) in enumerate(prepared, start=1)
    ]
    spine_items = [f'<itemref idref="doc-{index}"/>' for index in range(1, len(prepared) + 1)]
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="{escape(publication.language)}" prefix="schema: http://schema.org/">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">
<dc:identifier id="pub-id">{escape(publication.identifier)}</dc:identifier>
<dc:title id="title">{escape(publication.title)}</dc:title><meta refines="#title" property="title-type">main</meta>
<dc:title id="subtitle">{escape(publication.subtitle)}</dc:title><meta refines="#subtitle" property="title-type">subtitle</meta>
<dc:creator>{escape(publication.author)}</dc:creator><dc:language>{escape(publication.language)}</dc:language>
<dc:publisher>{escape(publication.publisher)}</dc:publisher><dc:date>{escape(publication.original_publication_year)}</dc:date>
<dc:description>{escape(publication.description)}</dc:description><dc:source>{escape(publication.source_url)}</dc:source>
<dc:rights>Family archive edition; shared for family reading.</dc:rights>
<meta property="dcterms:modified">{escape(publication.modified)}</meta><meta property="schema:accessMode">textual</meta>
<meta property="schema:accessMode">visual</meta><meta property="schema:accessModeSufficient">textual,visual</meta>
<meta property="schema:accessibilityFeature">alternativeText</meta><meta property="schema:accessibilityFeature">structuralNavigation</meta>
<meta property="schema:accessibilityFeature">tableOfContents</meta><meta property="schema:accessibilityHazard">none</meta>
</metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/><item id="css" href="styles/book.css" media-type="text/css"/>
{''.join(doc_items)}{''.join(image_items)}</manifest><spine><itemref idref="cover" linear="no"/>{''.join(spine_items)}</spine>
</package>
'''.encode()
    container = b'''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>
'''

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w") as archive:
        archive.writestr(_zip_info("mimetype", stored=True), b"application/epub+zip")
        archive.writestr(_zip_info("META-INF/container.xml"), container)
        archive.writestr(_zip_info("EPUB/package.opf"), opf)
        archive.writestr(_zip_info("EPUB/nav.xhtml"), nav_xhtml)
        archive.writestr(_zip_info("EPUB/cover.xhtml"), cover_xhtml)
        archive.writestr(_zip_info("EPUB/styles/book.css"), css)
        for _document, filename, content in prepared:
            archive.writestr(_zip_info(f"EPUB/{filename}"), content)
        for source in sorted(used_images):
            archive.writestr(
                _zip_info(f"EPUB/images/{image_names[source]}"), source.read_bytes()
            )
    validation = validate_epub(
        output_path,
        expected_document_count=len(prepared),
        expected_main_source_ids=list(expected_main_source_ids),
        maximum_bytes=int(catalog.epub.settings.get("maximum_bytes") or 0),
    )
    if not validation.ok:
        output_path.unlink(missing_ok=True)
        raise PortableEditionError(
            "Built EPUB failed validation:\n"
            + "\n".join(f"- {error}" for error in validation.errors)
        )
    return output_path


def _xml(data: bytes, label: str, validation: EpubValidation) -> StdET.Element | None:
    try:
        return StdET.fromstring(data)
    except StdET.ParseError as exc:
        validation.errors.append(f"Invalid XML in {label}: {exc}")
        return None


def validate_epub(
    path: str | Path,
    *,
    expected_document_count: int | None = None,
    expected_main_source_ids: Iterable[str] | None = None,
    maximum_bytes: int | None = None,
) -> EpubValidation:
    epub = Path(path)
    validation = EpubValidation([], [])
    validation.require(epub.is_file(), f"EPUB is missing: {epub}")
    if not epub.is_file():
        return validation
    if maximum_bytes:
        validation.require(
            epub.stat().st_size < maximum_bytes,
            f"EPUB is {epub.stat().st_size} bytes, exceeding {maximum_bytes}.",
        )
    try:
        with zipfile.ZipFile(epub) as archive:
            names = archive.namelist()
            validation.require(bool(names) and names[0] == "mimetype", "EPUB mimetype must be first.")
            if names:
                validation.require(
                    archive.getinfo(names[0]).compress_type == zipfile.ZIP_STORED,
                    "EPUB mimetype must be uncompressed.",
                )
            required = {
                "mimetype",
                "META-INF/container.xml",
                "EPUB/package.opf",
                "EPUB/nav.xhtml",
                "EPUB/cover.xhtml",
            }
            validation.require(
                required.issubset(names),
                f"EPUB is missing required files: {sorted(required - set(names))}",
            )
            validation.require(
                archive.read("mimetype") == b"application/epub+zip",
                "EPUB mimetype content is wrong.",
            )
            xml_names = [name for name in names if name.endswith((".xml", ".opf", ".xhtml"))]
            roots = {name: _xml(archive.read(name), name, validation) for name in xml_names}
            opf = roots.get("EPUB/package.opf")
            if opf is not None:
                ns = {"opf": "http://www.idpf.org/2007/opf"}
                manifest_items = opf.findall(".//opf:manifest/opf:item", ns)
                hrefs = {str(item.get("href")) for item in manifest_items}
                for href in hrefs:
                    validation.require(
                        f"EPUB/{href}" in names, f"EPUB manifest target is missing: {href}"
                    )
                spine_refs = [
                    str(item.get("idref"))
                    for item in opf.findall(".//opf:spine/opf:itemref", ns)
                ]
                item_ids = {str(item.get("id")) for item in manifest_items}
                validation.require(
                    all(ref in item_ids for ref in spine_refs),
                    "EPUB spine references a missing manifest item.",
                )
                if expected_document_count is not None:
                    content_count = sum(
                        1
                        for item in manifest_items
                        if str(item.get("id", "")).startswith("doc-")
                    )
                    validation.require(
                        content_count == expected_document_count,
                        f"EPUB has {content_count} content documents, expected {expected_document_count}.",
                    )
            all_ids: list[str] = []
            image_refs: list[tuple[str, str]] = []
            script_count = 0
            anchors_without_href = 0
            for name, root in roots.items():
                if not name.endswith(".xhtml") or root is None:
                    continue
                all_ids.extend(value for element in root.iter() if (value := element.get("id")))
                for element in root.iter():
                    if element.tag.endswith("img"):
                        reference = str(element.get("src") or "")
                        image_refs.append((name, reference))
                        validation.require(
                            bool(str(element.get("alt") or "").strip()),
                            f"EPUB image has empty alternative text in {name}: {reference}",
                        )
                    if element.tag.endswith("script"):
                        script_count += 1
                    if element.tag.endswith("a") and not element.get("href"):
                        anchors_without_href += 1
            expected_ids = list(expected_main_source_ids or [])
            if expected_ids:
                actual = Counter(value for value in all_ids if value.startswith("blk-"))
                expected = Counter(expected_ids)
                validation.require(
                    actual == expected,
                    "EPUB source-block coverage differs: "
                    f"missing={list((expected - actual).elements())[:5]}, "
                    f"extra={list((actual - expected).elements())[:5]}",
                )
            for source_name, reference in image_refs:
                normalized = posixpath.normpath(
                    str(PurePosixPath(source_name).parent.joinpath(reference))
                )
                validation.require(
                    normalized in names,
                    f"EPUB image reference is missing from {source_name}: {reference}",
                )
                validation.require(
                    not reference.startswith(("http://", "https://", "//")),
                    f"EPUB image must be local: {reference}",
                )
            validation.require(script_count == 0, "EPUB content must not contain scripts.")
            validation.require(
                anchors_without_href == 0,
                f"EPUB contains {anchors_without_href} anchor elements without href.",
            )
            validation.notes.append(
                f"EPUB contains {len(names)} files, {len(image_refs)} image references, "
                f"{len(expected_ids)} main source ids, and {epub.stat().st_size} bytes."
            )
    except (OSError, zipfile.BadZipFile, KeyError) as exc:
        validation.errors.append(f"Cannot inspect EPUB {epub}: {exc}")
    return validation


def run_epubcheck(
    path: str | Path,
    *,
    epubcheck_bin: str | None = None,
    epubcheck_jar: str | Path | None = None,
) -> tuple[bool, str]:
    configured_jar = epubcheck_jar or os.environ.get("EPUBCHECK_JAR")
    jar = Path(configured_jar).expanduser().resolve() if configured_jar else None
    if jar:
        if not jar.is_file():
            return False, f"EPUBCheck jar does not exist: {jar}"
        command = ["java", "-jar", str(jar), str(Path(path))]
    else:
        executable = epubcheck_bin or shutil.which("epubcheck")
        if not executable:
            return False, (
                "EPUBCheck is not installed; set EPUBCHECK_JAR or install the "
                "official epubcheck executable."
            )
        command = [executable, str(Path(path))]
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode == 0, completed.stdout


def copy_portable_artifacts(
    catalog: PortableCatalog,
    output_dir: Path,
    *,
    require_all: bool = False,
) -> tuple[int, int]:
    copied_count = copied_bytes = 0
    missing = [
        artifact.output_path
        for artifact in (catalog.epub, catalog.m4b)
        if not artifact.is_available
    ]
    if require_all and missing:
        raise PortableEditionError(
            "Portable release is missing required artifacts: "
            + ", ".join(str(path) for path in missing)
        )
    for artifact in (catalog.epub, catalog.m4b):
        if not artifact.is_available:
            continue
        destination = output_dir / artifact.public_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(artifact.output_path, destination)
        if destination.stat().st_size != artifact.output_path.stat().st_size or hash_file(
            destination
        ) != hash_file(artifact.output_path):
            raise PortableEditionError(f"Copied portable artifact differs: {destination}")
        copied_count += 1
        copied_bytes += artifact.output_path.stat().st_size
    internal = output_dir / "_internal" / "portable"
    internal.mkdir(parents=True, exist_ok=True)
    shutil.copy2(catalog.manifest_path, internal / "manifest.json")
    return copied_count, copied_bytes


def build_canonical_epub(
    manifest_path: str | Path = DEFAULT_MANIFEST_PATH,
    *,
    output: str | Path | None = None,
    force: bool = False,
) -> Path:
    catalog = load_portable_catalog(manifest_path)
    documents, source_ids = canonical_epub_documents()
    expected_main = int(catalog.epub.settings.get("expected_main_document_count") or 0)
    expected_companions = int(catalog.epub.settings.get("expected_companion_count") or 0)
    expected_blocks = int(catalog.epub.settings.get("expected_main_source_block_count") or 0)
    main_count = sum(document.is_main_book for document in documents)
    companion_count = len(documents) - main_count
    actual = (main_count, companion_count, len(source_ids))
    expected = (expected_main, expected_companions, expected_blocks)
    if actual != expected:
        raise PortableEditionError(
            "Canonical EPUB source inventory differs from the portable manifest: "
            f"documents={main_count}/{expected_main}, companions={companion_count}/"
            f"{expected_companions}, source_blocks={len(source_ids)}/{expected_blocks}"
        )
    return build_epub_package(
        catalog,
        documents,
        expected_main_source_ids=source_ids,
        output=output,
        force=force,
    )


def _request(url: str, *, method: str = "GET", headers: dict[str, str] | None = None):
    request_headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; OnwardPortableValidator/1.0; "
            "+https://onward.copper-dog.com/)"
        ),
        "Accept": "*/*",
    }
    request_headers.update(headers or {})
    request = urllib.request.Request(url, method=method, headers=request_headers)
    return urllib.request.urlopen(request, timeout=60)


def validate_public_portable(
    catalog: PortableCatalog,
    *,
    base_url: str,
) -> PublicValidation:
    validation = PublicValidation([], [])
    for artifact in (catalog.epub, catalog.m4b):
        if not artifact.is_available:
            validation.errors.append(f"Local portable artifact is missing: {artifact.output_path}")
            continue
        url = urljoin(base_url.rstrip("/") + "/", artifact.public_path)
        try:
            with _request(url, method="HEAD") as response:
                content_type = response.headers.get_content_type()
                length = int(response.headers.get("Content-Length") or 0)
                if response.status != 200:
                    validation.errors.append(f"{url} returned HTTP {response.status} for HEAD.")
                if content_type != artifact.media_type:
                    validation.errors.append(
                        f"{url} returned {content_type!r}, expected {artifact.media_type!r}."
                    )
                if length != artifact.output_path.stat().st_size:
                    validation.errors.append(
                        f"{url} returned {length} bytes, expected {artifact.output_path.stat().st_size}."
                    )
            with _request(url, headers={"Range": "bytes=0-31"}) as response:
                payload = response.read()
                content_range = response.headers.get("Content-Range", "")
                if response.status != 206 or len(payload) != 32:
                    validation.errors.append(
                        f"{url} range request returned HTTP {response.status} and {len(payload)} bytes."
                    )
                if not content_range.startswith("bytes 0-31/"):
                    validation.errors.append(f"{url} has invalid Content-Range: {content_range!r}.")
            validation.notes.append(
                f"{url}: {artifact.media_type}, {artifact.output_path.stat().st_size} bytes, range OK"
            )
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, ValueError) as exc:
            validation.errors.append(f"Cannot validate {url}: {exc}")
    help_url = urljoin(base_url.rstrip("/") + "/", "reading-apps.html")
    try:
        with _request(help_url) as response:
            body = response.read().decode("utf-8")
        for artifact in (catalog.epub, catalog.m4b):
            if artifact.public_path not in body:
                validation.errors.append(
                    f"Production reading-app help does not link {artifact.public_path}."
                )
        validation.notes.append(f"{help_url}: portable links present")
    except (OSError, urllib.error.URLError, urllib.error.HTTPError, UnicodeDecodeError) as exc:
        validation.errors.append(f"Cannot validate {help_url}: {exc}")
    return validation


def cli_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build-epub")
    build_parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST_PATH))
    build_parser.add_argument("--output")
    build_parser.add_argument("--force", action="store_true")
    validate_parser = subparsers.add_parser("validate-epub")
    validate_parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST_PATH))
    validate_parser.add_argument("--epubcheck", action="store_true")
    validate_parser.add_argument("--epubcheck-jar")
    public_parser = subparsers.add_parser("validate-public")
    public_parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST_PATH))
    public_parser.add_argument("--base-url", default="https://onward.copper-dog.com/")
    args = parser.parse_args(argv)
    try:
        catalog = load_portable_catalog(args.manifest)
        if args.command == "build-epub":
            output = build_canonical_epub(args.manifest, output=args.output, force=args.force)
            print(f"Built EPUB: {output}")
            print(f"Size: {output.stat().st_size} bytes")
            return 0
        if args.command == "validate-public":
            public = validate_public_portable(catalog, base_url=args.base_url)
            for note in public.notes:
                print(note)
            if public.errors:
                print("FAILED public portable validation")
                for error in public.errors:
                    print(f"- {error}")
                return 1
            print("PASS: public portable artifacts are exact and range-readable")
            return 0
        documents, source_ids = canonical_epub_documents()
        validation = validate_epub(
            catalog.epub.output_path,
            expected_document_count=len(documents),
            expected_main_source_ids=source_ids,
            maximum_bytes=int(catalog.epub.settings.get("maximum_bytes") or 0),
        )
        for note in validation.notes:
            print(note)
        if validation.errors:
            print("FAILED EPUB validation")
            for error in validation.errors:
                print(f"- {error}")
            return 1
        if args.epubcheck:
            ok, output = run_epubcheck(
                catalog.epub.output_path, epubcheck_jar=args.epubcheck_jar
            )
            print(output.rstrip())
            if not ok:
                return 1
        print("PASS: EPUB validation is clean")
        return 0
    except PortableEditionError as exc:
        print(f"FAILED: {exc}")
        return 1
