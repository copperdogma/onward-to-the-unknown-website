from __future__ import annotations

import json
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest
from lxml import etree
from PIL import Image

from modules.portable_editions import (
    EpubDocument,
    PortableArtifact,
    PortableCatalog,
    PortableEditionError,
    Publication,
    build_epub_package,
    copy_portable_artifacts,
    _request,
    validate_epub,
)


def test_public_request_uses_browser_compatible_user_agent() -> None:
    with patch("modules.portable_editions.urllib.request.urlopen") as urlopen:
        _request("https://example.test/file.epub", headers={"Range": "bytes=0-31"})

    request = urlopen.call_args.args[0]
    assert request.get_header("User-agent").startswith("Mozilla/5.0")
    assert request.get_header("Range") == "bytes=0-31"


def fixture_catalog(root: Path, cover: Path) -> PortableCatalog:
    publication = Publication(
        identifier="urn:uuid:26c825db-e424-47aa-82f0-559d0f899c84",
        title="Fixture Family Book",
        subtitle="A fixture subtitle",
        language="en-CA",
        author="Fixture Family",
        publisher="Fixture Family",
        original_publication_year="1987",
        modified="2026-07-17T20:00:00Z",
        description="Fixture description.",
        source_url="https://example.test/",
        cover_source_path=cover,
        cover_output_path=root / "generated-cover.jpg",
    )
    return PortableCatalog(
        manifest_path=root / "manifest.json",
        publication=publication,
        epub=PortableArtifact(
            output_path=root / "fixture.epub",
            public_path="downloads/fixture.epub",
            media_type="application/epub+zip",
            settings={"maximum_bytes": 2_000_000},
        ),
        m4b=PortableArtifact(
            output_path=root / "fixture.m4b",
            public_path="audiobook/fixture.m4b",
            media_type="audio/mp4",
            settings={},
        ),
    )


def write_cover(path: Path) -> None:
    Image.new("RGB", (400, 600), "#38584f").save(path, "JPEG")


def test_epub_package_preserves_source_ids_images_links_and_ocf_order(tmp_path: Path) -> None:
    cover = tmp_path / "cover-source.jpg"
    figure = tmp_path / "figure.jpg"
    write_cover(cover)
    Image.new("RGB", (120, 80), "#b8a67c").save(figure, "JPEG")
    catalog = fixture_catalog(tmp_path, cover)
    catalog.manifest_path.write_text("{}\n", encoding="utf-8")
    documents = [
        EpubDocument(
            slug="first-story",
            title="First Story",
            part_id="opening-pages",
            page_path="first.html",
            content_html=(
                '<p id="blk-first">A <a href="second.html">story</a>.</p>'
                '<figure><img src="images/figure.jpg" alt="Fixture family"/>'
                "<figcaption>A caption.</figcaption></figure>"
            ),
            image_sources={"images/figure.jpg": figure},
        ),
        EpubDocument(
            slug="companion-note",
            title="Companion Note",
            part_id="companions",
            page_path="second.html",
            content_html='<p id="blk-first">A companion with a source-local id.</p>',
            image_sources={},
            is_main_book=False,
        ),
    ]

    output = build_epub_package(catalog, documents, expected_main_source_ids=["blk-first"])
    validation = validate_epub(
        output,
        expected_document_count=2,
        expected_main_source_ids=["blk-first"],
        maximum_bytes=2_000_000,
    )

    assert validation.ok, validation.errors
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist()[0] == "mimetype"
        assert archive.getinfo("mimetype").compress_type == zipfile.ZIP_STORED
        first = archive.read("EPUB/text/001-first-story.xhtml").decode()
        companion = archive.read("EPUB/text/002-companion-note.xhtml").decode()
        package = archive.read("EPUB/package.opf").decode()
        stylesheet = archive.read("EPUB/styles/book.css").decode()
    assert 'id="blk-first"' in first
    assert '<body epub:type="bodymatter" aria-labelledby="publication-heading">' in first
    assert '<section aria-labelledby="publication-heading">' not in first
    assert 'href="002-companion-note.xhtml"' in first
    assert 'id="companion-note-blk-first"' in companion
    assert "Fixture family" in first
    assert "max-height: 420px !important" in stylesheet
    assert "object-fit: contain" in stylesheet
    assert "margin: 1.5em" in stylesheet
    assert "margin: 5%" not in stylesheet
    assert "body > h1 { break-before: page; }" in stylesheet
    assert ".supplement-intro { display: inline-block; max-width: 90vw; width: 34em; }" in stylesheet
    assert ".supplement-body { display: contents; }" in stylesheet
    assert "About this digital family edition" in first
    assert "A fixture subtitle" in package
    assert "<dc:source>https://example.test/</dc:source>" in package


def test_epub_does_not_repeat_matching_source_heading(tmp_path: Path) -> None:
    cover = tmp_path / "cover.jpg"
    write_cover(cover)
    catalog = fixture_catalog(tmp_path, cover)
    catalog.manifest_path.write_text("{}\n", encoding="utf-8")
    document = EpubDocument(
        slug="first-story",
        title="First Story",
        part_id="opening-pages",
        page_path="first.html",
        content_html='<h1 id="story-heading">First Story</h1><p id="blk-first">A story.</p>',
        image_sources={},
    )

    output = build_epub_package(catalog, [document], expected_main_source_ids=["blk-first"])

    with zipfile.ZipFile(output) as archive:
        xhtml = archive.read("EPUB/text/001-first-story.xhtml")
    root = etree.fromstring(xhtml)
    headings = root.xpath("//*[local-name()='h1']")
    assert ["".join(heading.itertext()) for heading in headings] == ["First Story"]
    assert b'aria-label="First Story"' in xhtml


def test_epub_builder_rejects_image_without_alt_text(tmp_path: Path) -> None:
    cover = tmp_path / "cover.jpg"
    figure = tmp_path / "figure.jpg"
    write_cover(cover)
    Image.new("RGB", (40, 40), "blue").save(figure, "JPEG")
    catalog = fixture_catalog(tmp_path, cover)
    catalog.manifest_path.write_text("{}\n", encoding="utf-8")
    document = EpubDocument(
        slug="story",
        title="Story",
        part_id="opening-pages",
        page_path="story.html",
        content_html='<p id="blk-one">Text</p><img src="figure.jpg"/>',
        image_sources={"figure.jpg": figure},
    )

    with pytest.raises(PortableEditionError, match="alternative text"):
        build_epub_package(catalog, [document], expected_main_source_ids=["blk-one"])


def test_copy_portable_artifacts_uses_declared_paths_and_release_requires_both(
    tmp_path: Path,
) -> None:
    cover = tmp_path / "cover.jpg"
    write_cover(cover)
    catalog = fixture_catalog(tmp_path, cover)
    catalog.manifest_path.write_text(json.dumps({"schema_version": "fixture"}), encoding="utf-8")
    catalog.epub.output_path.write_bytes(b"fixture epub")

    with pytest.raises(PortableEditionError, match="missing required artifacts"):
        copy_portable_artifacts(catalog, tmp_path / "missing-site", require_all=True)

    catalog.m4b.output_path.write_bytes(b"fixture m4b")
    count, size = copy_portable_artifacts(catalog, tmp_path / "site", require_all=True)

    assert count == 2
    assert size == len(b"fixture epub") + len(b"fixture m4b")
    assert (tmp_path / "site" / catalog.epub.public_path).read_bytes() == b"fixture epub"
    assert (tmp_path / "site" / catalog.m4b.public_path).read_bytes() == b"fixture m4b"
    assert (tmp_path / "site" / "_internal" / "portable" / "manifest.json").is_file()
