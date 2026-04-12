from __future__ import annotations

from html import unescape
import json
from pathlib import Path

from modules.build_family_site import (
    BundleEntry,
    absorbed_output_paths,
    build_family_site,
    build_summary_text,
    derive_display_title,
    enhance_article_html,
    expand_entry_fragments,
    merge_absorbed_article_html,
)


def write_fixture_audiobook_manifest(
    tmp_path: Path,
    *,
    tracks: list[dict[str, object]],
    full_audiobook: dict[str, object] | None = None,
    title: str = "Fixture Audiobook",
) -> Path:
    audiobook_root = tmp_path / "audiobook-fixture"
    for track in tracks:
        audio_relative_path = Path(str(track["audio_path"]))
        script_relative_path = Path(str(track["script_path"]))
        audio_path = audiobook_root / audio_relative_path
        script_path = audiobook_root / script_relative_path
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.parent.mkdir(parents=True, exist_ok=True)
        audio_path.write_bytes(b"ID3 fixture mp3")
        script_path.write_text(f"# {track['title']}\n", encoding="utf-8")

    if full_audiobook:
        full_audio_path = audiobook_root / Path(str(full_audiobook["audio_path"]))
        full_audio_path.parent.mkdir(parents=True, exist_ok=True)
        full_audio_path.write_bytes(b"ID3 fixture full audiobook")

    manifest_path = audiobook_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "onward_audiobook_manifest_v1",
                "title": title,
                "full_audiobook": full_audiobook,
                "tracks": tracks,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest_path


def test_build_family_site_emits_reader_facing_pages_and_internal_audit(tmp_path):
    fixture_dir = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "family_site_minimal"
        / "input"
        / "story206-onward-proof-r10"
    )
    output_dir = tmp_path / "family-site"

    result = build_family_site(
        source_dir=fixture_dir,
        output_dir=output_dir,
        site_title="Fixture Reading Surface",
        audiobook_manifest_path=None,
    )

    assert result.rendered_entry_ids == ("page-001", "chapter-001", "chapter-009")
    assert (output_dir / "index.html").exists()
    assert (output_dir / "page-001.html").exists()
    assert (output_dir / "chapter-001.html").exists()
    assert (output_dir / "chapter-009.html").exists()
    assert (output_dir / "assets" / "family-site.css").exists()
    assert (output_dir / "images" / "family-portrait.svg").exists()
    assert (output_dir / "_internal" / "provenance" / "blocks.jsonl").exists()
    assert (output_dir / "_internal" / "provenance" / "entries" / "page-001.json").exists()
    assert (output_dir / "_internal" / "provenance" / "entries" / "chapter-001.json").exists()
    assert (output_dir / "_internal" / "provenance" / "entries" / "chapter-009.json").exists()
    assert result.omission_audit_path.exists()
    assert (output_dir / "_internal" / "source-manifest.json").exists()

    landing_html = (output_dir / "index.html").read_text(encoding="utf-8")
    page_html = (output_dir / "page-001.html").read_text(encoding="utf-8")
    chapter_one_html = (output_dir / "chapter-001.html").read_text(encoding="utf-8")
    chapter_html = (output_dir / "chapter-009.html").read_text(encoding="utf-8")
    stylesheet = (output_dir / "assets" / "family-site.css").read_text(encoding="utf-8")
    omission_audit = json.loads(result.omission_audit_path.read_text(encoding="utf-8"))

    assert "Fixture Reading Surface" in landing_html
    assert '<section class="hero home-hero">' in landing_html
    assert "Opening Pages" in landing_html
    assert "Family Stories" in landing_html
    assert "Closing Archive" not in unescape(landing_html)
    assert landing_html.count('class="nav-button-icon"') == 2
    assert 'href="#opening-pages"><span class="nav-button-content"><span class="nav-button-icon">' in landing_html
    assert 'href="#family-stories"><span class="nav-button-content"><span class="nav-button-icon">' in landing_html
    assert "Alma Marie (L'Heureux) Alain" in unescape(landing_html)
    assert "The Ancestral Lineage of Moïse and Sophie" in unescape(landing_html)
    assert "Onward to the Unknown" in unescape(landing_html)
    assert "Image 1" not in landing_html
    assert "ONWARD TO THE UNKNOWN 1887 - 1987" not in unescape(landing_html)
    assert 'class="story-card-media"' in landing_html
    assert 'src="images/family-portrait.svg"' in landing_html
    assert "<title>Onward to the Unknown — Fixture Reading Surface</title>" in page_html
    assert "<h1 id=\"blk-page-001-0001\">Onward to the Unknown</h1>" in page_html
    assert 'id="blk-chapter-009-0001"' in chapter_html
    assert 'id="blk-page-001-0001"' in page_html
    assert 'aria-label="Home"' in page_html
    assert 'aria-label="Home"' in chapter_one_html
    assert 'aria-label="Home"' in chapter_html
    assert 'class="site-title site-title-link" href="index.html"' in page_html
    assert 'class="site-title site-title-link" href="index.html"' in chapter_html
    assert 'href="page-001.html">← Onward to the Unknown</a>' in chapter_one_html
    assert 'href="chapter-009.html"' in chapter_one_html
    assert "Alma Marie (L'Heureux) Alain →" in unescape(chapter_one_html)
    assert "Image 1" not in chapter_one_html
    assert "Visible provenance" not in chapter_html
    assert "Omission audit" not in chapter_html
    assert "Whole-book access, with no silent losses." not in landing_html
    assert "source-manifest" not in landing_html
    assert "table.genealogy-table thead th" in stylesheet
    assert "position: sticky;" in stylesheet
    assert ".recipe-callout" in stylesheet
    assert ".home-hero h1" in stylesheet
    assert "max-width: none;" in stylesheet
    assert ".nav-button-icon" in stylesheet
    assert ".nav-button-content" in stylesheet

    entry_rows = json.loads(
        (output_dir / "_internal" / "provenance" / "entries" / "chapter-009.json").read_text(encoding="utf-8")
    )
    assert entry_rows[0]["block_id"] == "blk-chapter-009-0001"
    assert omission_audit["manifest_entry_count"] == 3
    assert omission_audit["status_counts"] == {"rendered": 3}
    assert omission_audit["entries"][0]["entry_id"] == "page-001"
    assert omission_audit["entries"][1]["group_id"] == "opening-pages"
    assert omission_audit["entries"][2]["group_id"] == "family-stories"


def test_build_family_site_rejects_missing_requested_entry(tmp_path):
    fixture_dir = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "family_site_minimal"
        / "input"
        / "story206-onward-proof-r10"
    )

    try:
        build_family_site(
            source_dir=fixture_dir,
            output_dir=tmp_path / "family-site",
            entry_ids=["chapter-999"],
            audiobook_manifest_path=None,
        )
    except SystemExit as exc:
        assert "chapter-999" in str(exc)
    else:
        raise AssertionError("Expected build_family_site to reject missing entry ids.")


def test_build_family_site_audits_filtered_subset(tmp_path):
    fixture_dir = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "family_site_minimal"
        / "input"
        / "story206-onward-proof-r10"
    )
    output_dir = tmp_path / "family-site"

    result = build_family_site(
        source_dir=fixture_dir,
        output_dir=output_dir,
        entry_ids=["chapter-009"],
        site_title="Fixture Reading Surface",
        audiobook_manifest_path=None,
    )

    assert result.rendered_entry_ids == ("chapter-009",)
    omission_audit = json.loads(result.omission_audit_path.read_text(encoding="utf-8"))

    assert omission_audit["status_counts"] == {
        "intentionally_deferred": 2,
        "rendered": 1,
    }
    deferred_rows = [row for row in omission_audit["entries"] if row["status"] == "intentionally_deferred"]
    assert len(deferred_rows) == 2
    assert deferred_rows[0]["surface"] == "audit-only"


def test_derive_display_title_prefers_reader_facing_page_heading():
    entry = BundleEntry(
        entry_id="page-001",
        kind="page",
        title="Image 1",
        path="page-001.html",
        order=1,
        prev_entry_id=None,
        next_entry_id="chapter-001",
        source_pages=(1,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )

    assert (
        derive_display_title(entry, "<h1>ONWARD<br/>TO THE UNKNOWN</h1><p>1887 - 1987</p>")
        == "Onward to the Unknown"
    )


def test_derive_display_title_falls_back_for_empty_placeholder_image_page():
    entry = BundleEntry(
        entry_id="page-003",
        kind="page",
        title="Image 3",
        path="page-003.html",
        order=3,
        prev_entry_id="chapter-002",
        next_entry_id="chapter-003",
        source_pages=(3,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )

    assert derive_display_title(entry, "") == "Illustration page 3"


def test_derive_display_title_normalizes_all_caps_chapter_title():
    entry = BundleEntry(
        entry_id="chapter-010",
        kind="chapter",
        title="ARTHUR L'HEUREUX",
        path="chapter-010.html",
        order=10,
        prev_entry_id="chapter-009",
        next_entry_id="chapter-011",
        source_pages=(28,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )

    assert derive_display_title(entry, "<h1>ARTHUR L'HEUREUX</h1>") == "Arthur L'Heureux"


def test_build_summary_text_strips_repeated_title_prefix_before_excerpting():
    article_html = "<h1>ONWARD TO THE UNKNOWN</h1><p>1887 - 1987</p><p>Family history begins here.</p>"

    assert build_summary_text(article_html, "Onward to the Unknown", limit=48) == (
        "1887 - 1987 Family history begins here."
    )


def test_build_family_site_avoids_duplicate_browser_title_for_cover_page(tmp_path):
    fixture_dir = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "family_site_minimal"
        / "input"
        / "story206-onward-proof-r10"
    )
    output_dir = tmp_path / "family-site"

    build_family_site(source_dir=fixture_dir, output_dir=output_dir, audiobook_manifest_path=None)

    page_html = (output_dir / "page-001.html").read_text(encoding="utf-8")
    assert "<title>Onward to the Unknown</title>" in page_html


def test_build_family_site_surfaces_audiobook_page_and_entry_panel(tmp_path):
    fixture_dir = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "family_site_minimal"
        / "input"
        / "story206-onward-proof-r10"
    )
    output_dir = tmp_path / "family-site"
    audiobook_manifest_path = write_fixture_audiobook_manifest(
        tmp_path,
        tracks=[
            {
                "track_number": 1,
                "title": "Preamble",
                "audio_path": "tracks/01-preamble.mp3",
                "script_path": "script/01-preamble.md",
                "notes": "Opening orientation for the audiobook.",
            },
            {
                "track_number": 5,
                "title": "Alma Marie (L'Heureux) Alain",
                "audio_path": "tracks/05-alma-marie.mp3",
                "script_path": "script/05-alma-marie-lheureux-alain.md",
                "target_entry_id": "chapter-009",
            },
        ],
        full_audiobook={
            "title": "Full Audiobook",
            "audio_path": "tracks/full-audiobook.mp3",
            "silence_between_tracks_seconds": 4,
            "notes": "Merged fixture audiobook.",
        },
    )

    build_family_site(
        source_dir=fixture_dir,
        output_dir=output_dir,
        site_title="Fixture Reading Surface",
        audiobook_manifest_path=audiobook_manifest_path,
    )

    landing_html = (output_dir / "index.html").read_text(encoding="utf-8")
    audiobook_html = (output_dir / "audiobook.html").read_text(encoding="utf-8")
    chapter_html = (output_dir / "chapter-009.html").read_text(encoding="utf-8")

    assert (output_dir / "audiobook.html").exists()
    assert (output_dir / "audiobook" / "tracks" / "01-preamble.mp3").exists()
    assert (output_dir / "audiobook" / "tracks" / "05-alma-marie.mp3").exists()
    assert (output_dir / "audiobook" / "tracks" / "full-audiobook.mp3").exists()
    assert (output_dir / "_internal" / "audiobook" / "manifest.json").exists()
    assert "Fixture Audiobook" in landing_html
    assert "Open Audiobook Player" in landing_html
    assert "Play Full Audiobook" in landing_html
    assert "Download Full Audiobook" in landing_html
    assert landing_html.count('class="nav-button-icon"') == 3
    assert 'href="#audiobook"><span class="nav-button-content"><span class="nav-button-icon">' in landing_html
    assert 'aria-label="Home"' in audiobook_html
    assert 'class="site-title site-title-link" href="index.html"' in audiobook_html
    assert 'id="full-audiobook"' in audiobook_html
    assert "Merged fixture audiobook." in audiobook_html
    assert 'src="audiobook/tracks/full-audiobook.mp3"' in audiobook_html
    assert "Listen to this section" in chapter_html
    assert 'src="audiobook/tracks/05-alma-marie.mp3"' in chapter_html
    assert "Open Full Audiobook" in chapter_html
    assert "Opening orientation for the audiobook." in audiobook_html
    assert "Track 05" in audiobook_html
    assert 'href="chapter-009.html"' in audiobook_html


def test_merge_absorbed_article_html_skips_duplicate_cover_blocks():
    primary_html = """
    <h1 id="blk-page-001-0001">ONWARD TO THE UNKNOWN</h1>
    <p id="blk-page-001-0002">1887 - 1987</p>
    <p id="blk-page-001-0003">Moïse and Sophie L'Heureux</p>
    """
    absorbed_entry = BundleEntry(
        entry_id="page-002",
        kind="page",
        title="Page i",
        path="page-002.html",
        order=2,
        prev_entry_id="page-001",
        next_entry_id="chapter-001",
        source_pages=(2,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )
    absorbed_html = """
    <h1 id="blk-page-002-0001">ONWARD TO THE UNKNOWN</h1>
    <p id="blk-page-002-0002">1887 - 1987</p>
    <p id="blk-page-002-0003">Moise and Sophie L'Heureux</p>
    """

    merged = merge_absorbed_article_html(primary_html, [(absorbed_entry, absorbed_html)])

    assert "merged-entry-ids: page-002" in merged
    assert merged.count("ONWARD TO THE UNKNOWN") == 1
    assert merged.count("1887 - 1987") == 1


def test_absorbed_output_paths_merges_page_002_into_page_001_when_both_selected():
    page_001 = BundleEntry(
        entry_id="page-001",
        kind="page",
        title="Image 1",
        path="page-001.html",
        order=1,
        prev_entry_id=None,
        next_entry_id="chapter-001",
        source_pages=(1,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )
    page_002 = BundleEntry(
        entry_id="page-002",
        kind="page",
        title="Page i",
        path="page-002.html",
        order=3,
        prev_entry_id="chapter-001",
        next_entry_id="chapter-002",
        source_pages=(2,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )

    assert absorbed_output_paths([page_001, page_002]) == {"page-002": "page-001.html"}


def test_build_family_site_absorbs_page_002_content_into_page_001(tmp_path):
    source_dir = tmp_path / "input" / "story206-onward-proof-r10"
    source_dir.mkdir(parents=True)
    output_dir = tmp_path / "build" / "family-site"

    manifest = {
        "run_id": "fixture-run",
        "document_id": "fixture-doc",
        "title": "Onward to the Unknown",
        "entries": [
            {
                "entry_id": "page-001",
                "kind": "page",
                "title": "Image 1",
                "path": "page-001.html",
                "order": 1,
                "prev_entry_id": None,
                "next_entry_id": "page-002",
                "source_pages": [1],
            },
            {
                "entry_id": "page-002",
                "kind": "page",
                "title": "Page i",
                "path": "page-002.html",
                "order": 2,
                "prev_entry_id": "page-001",
                "next_entry_id": None,
                "source_pages": [2],
            },
        ],
    }
    (source_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (source_dir / "page-001.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-page-001-0001">ONWARD TO THE UNKNOWN</h1>
        <p id="blk-page-001-0002">1887 - 1987</p>
        </article></body></html>""",
        encoding="utf-8",
    )
    (source_dir / "page-002.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-page-002-0001">ONWARD TO THE UNKNOWN</h1>
        <p id="blk-page-002-0002">1887 - 1987</p>
        <p id="blk-page-002-0003">Presented by the L'Heureux family.</p>
        </article></body></html>""",
        encoding="utf-8",
    )

    result = build_family_site(source_dir=source_dir, output_dir=output_dir, audiobook_manifest_path=None)

    assert result.rendered_entry_ids == ("page-001",)
    assert not (output_dir / "page-002.html").exists()

    page_html = (output_dir / "page-001.html").read_text(encoding="utf-8")
    omission_audit = json.loads(result.omission_audit_path.read_text(encoding="utf-8"))

    assert "Presented by the L'Heureux family." in page_html
    assert "merged-entry-ids: page-002" in page_html
    page_002_audit_row = next(row for row in omission_audit["entries"] if row["entry_id"] == "page-002")
    assert page_002_audit_row["status"] == "rendered"
    assert page_002_audit_row["surface"] == "merged-entry-page"
    assert page_002_audit_row["output_path"] == "page-001.html"


def test_build_family_site_keeps_absorbed_page_provenance_rows(tmp_path):
    source_dir = tmp_path / "input" / "story206-onward-proof-r10"
    provenance_dir = source_dir / "provenance"
    source_dir.mkdir(parents=True)
    provenance_dir.mkdir(parents=True)
    output_dir = tmp_path / "build" / "family-site"

    manifest = {
        "run_id": "fixture-run",
        "document_id": "fixture-doc",
        "title": "Onward to the Unknown",
        "entries": [
            {
                "entry_id": "page-001",
                "kind": "page",
                "title": "Image 1",
                "path": "page-001.html",
                "order": 1,
                "prev_entry_id": None,
                "next_entry_id": "page-002",
                "source_pages": [1],
            },
            {
                "entry_id": "page-002",
                "kind": "page",
                "title": "Page i",
                "path": "page-002.html",
                "order": 2,
                "prev_entry_id": "page-001",
                "next_entry_id": None,
                "source_pages": [2],
            },
        ],
    }
    (source_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (source_dir / "page-001.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-page-001-0001">ONWARD TO THE UNKNOWN</h1>
        <p id="blk-page-001-0002">1887 - 1987</p>
        </article></body></html>""",
        encoding="utf-8",
    )
    (source_dir / "page-002.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-page-002-0001">ONWARD TO THE UNKNOWN</h1>
        <p id="blk-page-002-0002">Presented by the L'Heureux family.</p>
        </article></body></html>""",
        encoding="utf-8",
    )
    (provenance_dir / "blocks.jsonl").write_text(
        "\n".join(
            json.dumps(row)
            for row in [
                {
                    "entry_id": "page-001",
                    "block_id": "blk-page-001-0001",
                    "block_kind": "heading",
                    "source_element_ids": ["src-1"],
                },
                {
                    "entry_id": "page-001",
                    "block_id": "blk-page-001-0002",
                    "block_kind": "paragraph",
                    "source_element_ids": ["src-2"],
                },
                {
                    "entry_id": "page-002",
                    "block_id": "blk-page-002-0001",
                    "block_kind": "heading",
                    "source_element_ids": ["src-3"],
                },
                {
                    "entry_id": "page-002",
                    "block_id": "blk-page-002-0002",
                    "block_kind": "paragraph",
                    "source_element_ids": ["src-4"],
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    build_family_site(source_dir=source_dir, output_dir=output_dir, audiobook_manifest_path=None)

    provenance_rows = json.loads(
        (output_dir / "_internal" / "provenance" / "entries" / "page-001.json").read_text(encoding="utf-8")
    )
    assert [row["block_id"] for row in provenance_rows] == [
        "blk-page-001-0001",
        "blk-page-001-0002",
        "blk-page-002-0002",
    ]


def test_build_family_site_surfaces_family_story_supplement(tmp_path):
    input_root = tmp_path / "input"
    doc_web_root = input_root / "doc-web-html"
    source_dir = doc_web_root / "story206-onward-proof-r10"
    supplement_bundle_dir = doc_web_root / "rolland-alain-memoir-r01"
    output_dir = tmp_path / "build" / "family-site"
    source_pdf = input_root / "Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf"

    source_dir.mkdir(parents=True)
    (source_dir / "provenance").mkdir(parents=True)
    supplement_bundle_dir.mkdir(parents=True)
    (supplement_bundle_dir / "provenance").mkdir(parents=True)
    source_pdf.write_text("fixture memoir pdf", encoding="utf-8")

    main_manifest = {
        "run_id": "fixture-run",
        "document_id": "onward-to-the-unknown",
        "title": "Onward to the Unknown",
        "entries": [
            {
                "entry_id": "page-001",
                "kind": "page",
                "title": "Image 1",
                "path": "page-001.html",
                "order": 1,
                "prev_entry_id": None,
                "next_entry_id": "chapter-009",
                "source_pages": [1],
            },
            {
                "entry_id": "chapter-009",
                "kind": "chapter",
                "title": "ALMA MARIE (L'HEUREUX) ALAIN",
                "path": "chapter-009.html",
                "order": 2,
                "prev_entry_id": "page-001",
                "next_entry_id": "chapter-024",
                "source_pages": [9],
                "printed_pages": [9],
                "printed_page_start": 9,
                "printed_page_end": 9,
            },
            {
                "entry_id": "chapter-024",
                "kind": "chapter",
                "title": "ARCHIVE PHOTOS",
                "path": "chapter-024.html",
                "order": 3,
                "prev_entry_id": "chapter-009",
                "next_entry_id": None,
                "source_pages": [24],
                "printed_pages": [24],
                "printed_page_start": 24,
                "printed_page_end": 24,
            },
        ],
    }
    (source_dir / "manifest.json").write_text(json.dumps(main_manifest), encoding="utf-8")
    (source_dir / "page-001.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-page-001-0001">Onward to the Unknown</h1>
        </article></body></html>""",
        encoding="utf-8",
    )
    (source_dir / "chapter-009.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-chapter-009-0001">ALMA MARIE (L'HEUREUX) ALAIN</h1>
        <p id="blk-chapter-009-0002">Family story text.</p>
        </article></body></html>""",
        encoding="utf-8",
    )
    (source_dir / "chapter-024.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-chapter-024-0001">ARCHIVE PHOTOS</h1>
        <p id="blk-chapter-024-0002">Closing archive text.</p>
        </article></body></html>""",
        encoding="utf-8",
    )
    (source_dir / "provenance" / "blocks.jsonl").write_text(
        "\n".join(
            json.dumps(row)
            for row in [
                {
                    "entry_id": "page-001",
                    "block_id": "blk-page-001-0001",
                    "block_kind": "heading",
                    "source_element_ids": ["main-1"],
                },
                {
                    "entry_id": "chapter-009",
                    "block_id": "blk-chapter-009-0001",
                    "block_kind": "heading",
                    "source_element_ids": ["main-2"],
                },
                {
                    "entry_id": "chapter-009",
                    "block_id": "blk-chapter-009-0002",
                    "block_kind": "paragraph",
                    "source_element_ids": ["main-3"],
                },
                {
                    "entry_id": "chapter-024",
                    "block_id": "blk-chapter-024-0001",
                    "block_kind": "heading",
                    "source_element_ids": ["main-4"],
                },
                {
                    "entry_id": "chapter-024",
                    "block_id": "blk-chapter-024-0002",
                    "block_kind": "paragraph",
                    "source_element_ids": ["main-5"],
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    supplement_manifest = {
        "run_id": "memoir-run",
        "document_id": "rolland-alain-memoir-family-story",
        "title": "Rolland Alain Memoir Family Story",
        "index_path": "index.html",
        "provenance_path": "provenance/blocks.jsonl",
        "entries": [
            {
                "entry_id": "page-001",
                "kind": "page",
                "title": "Image 1",
                "path": "page-001.html",
                "order": 1,
                "prev_entry_id": None,
                "next_entry_id": "chapter-001",
                "source_pages": [1],
            },
            {
                "entry_id": "chapter-001",
                "kind": "chapter",
                "title": "Memoires of Rolland Alain from birth 1913 to 71st year 1985",
                "path": "chapter-001.html",
                "order": 2,
                "prev_entry_id": "page-001",
                "next_entry_id": "page-002",
                "source_pages": [2, 3],
                "printed_pages": [1, 2],
                "printed_page_start": 1,
                "printed_page_end": 2,
            },
            {
                "entry_id": "page-002",
                "kind": "page",
                "title": "Image 11",
                "path": "page-002.html",
                "order": 3,
                "prev_entry_id": "chapter-001",
                "next_entry_id": None,
                "source_pages": [11],
            },
        ],
        "reading_order": ["page-001", "chapter-001", "page-002"],
        "source_artifact": "05_extract_page_numbers_html_v1/pages_html_with_page_numbers.jsonl",
    }
    (supplement_bundle_dir / "manifest.json").write_text(json.dumps(supplement_manifest), encoding="utf-8")
    (supplement_bundle_dir / "index.html").write_text("<html><body>bundle index</body></html>", encoding="utf-8")
    (supplement_bundle_dir / "page-001.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-page-001-0001">Memoires</h1>
        <p id="blk-page-001-0002">de Rolland Alain</p>
        </article></body></html>""",
        encoding="utf-8",
    )
    (supplement_bundle_dir / "chapter-001.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <h1 id="blk-chapter-001-0001">Memoires of Rolland Alain from birth 1913 to 71st year 1985</h1>
        <p id="blk-chapter-001-0002">Primary memoir text.</p>
        </article></body></html>""",
        encoding="utf-8",
    )
    (supplement_bundle_dir / "page-002.html").write_text(
        """<!DOCTYPE html><html><body><article>
        <p id="blk-page-002-0001">A missing middle leaf continues here.</p>
        </article></body></html>""",
        encoding="utf-8",
    )
    (supplement_bundle_dir / "provenance" / "blocks.jsonl").write_text(
        "\n".join(
            json.dumps(row)
            for row in [
                {
                    "entry_id": "chapter-001",
                    "block_id": "blk-chapter-001-0001",
                    "block_kind": "heading",
                    "source_element_ids": ["memoir-1"],
                },
                {
                    "entry_id": "chapter-001",
                    "block_id": "blk-chapter-001-0002",
                    "block_kind": "paragraph",
                    "source_element_ids": ["memoir-2"],
                },
                {
                    "entry_id": "page-002",
                    "block_id": "blk-page-002-0001",
                    "block_kind": "paragraph",
                    "source_element_ids": ["memoir-3"],
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (doc_web_root / "family-story-supplements.json").write_text(
        json.dumps(
            {
                "schema_version": "onward_family_story_supplement_registry_v1",
                "supplements": [
                    {
                        "supplement_id": "rolland-alain-memoir",
                        "title": "Rolland Alain Memoir Family Story",
                        "output_path": "rolland-alain-memoir-family-story.html",
                        "bundle_dir": "rolland-alain-memoir-r01",
                        "source_pdf": "../Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf",
                        "group_id": "family-stories",
                        "insert_after_entry_id": "chapter-009",
                        "entry_ids": ["chapter-001", "page-002"],
                        "absorbed_entry_ids": ["page-001"],
                        "preamble": "Note that this was not a story originally included in the Onward to the Unknown book. It was found in one copy of the book as a set of photocopied pages.",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    stale_public_dir = output_dir / "supplements" / "rolland-alain-memoir"
    stale_public_dir.mkdir(parents=True)
    (stale_public_dir / "stale.txt").write_text("stale", encoding="utf-8")

    result = build_family_site(source_dir=source_dir, output_dir=output_dir, audiobook_manifest_path=None)

    assert result.rendered_entry_ids == (
        "page-001",
        "chapter-009",
        "supplement-rolland-alain-memoir",
        "chapter-024",
    )
    landing_html = (output_dir / "index.html").read_text(encoding="utf-8")
    supplement_html = (output_dir / "rolland-alain-memoir-family-story.html").read_text(encoding="utf-8")
    omission_audit = json.loads(result.omission_audit_path.read_text(encoding="utf-8"))
    supplement_provenance = json.loads(
        (output_dir / "_internal" / "provenance" / "entries" / "supplement-rolland-alain-memoir.json").read_text(
            encoding="utf-8"
        )
    )
    supplement_metadata = json.loads(
        (output_dir / "_internal" / "supplements" / "rolland-alain-memoir" / "metadata.json").read_text(
            encoding="utf-8"
        )
    )

    assert "Rolland Alain Memoir Family Story" in landing_html
    assert 'href="rolland-alain-memoir-family-story.html"' in landing_html
    assert "Note that this was not a story originally included in the Onward to the Unknown book." in supplement_html
    assert "Processed through the repo's bounded non-TOC scanned supplement lane." not in supplement_html
    assert "Open Imported HTML" not in supplement_html
    assert "Download Original PDF" not in supplement_html
    assert "A missing middle leaf continues here." in supplement_html
    assert "<h2" in supplement_html
    assert "supplement-source-title" in supplement_html
    assert "de Rolland Alain" not in supplement_html
    assert not (output_dir / "supplements" / "rolland-alain-memoir").exists()
    assert not (output_dir / "supplements" / "rolland-alain-memoir" / "bundle").exists()
    assert not (output_dir / "supplements" / "rolland-alain-memoir" / "source.pdf").exists()
    assert not (output_dir / "supplements" / "rolland-alain-memoir" / "assets").exists()
    assert supplement_metadata["source_bundle_dir"].endswith("rolland-alain-memoir-r01")
    assert "public_bundle_index" not in supplement_metadata
    assert "public_source_pdf" not in supplement_metadata
    assert omission_audit["supplement_count"] == 1
    assert omission_audit["supplements"][0]["supplement_id"] == "rolland-alain-memoir"
    assert omission_audit["supplements"][0]["absorbed_entry_ids"] == ["page-001"]
    assert [row["block_id"] for row in supplement_provenance] == [
        "blk-chapter-001-0001",
        "blk-chapter-001-0002",
        "blk-page-002-0001",
    ]


def test_enhance_article_html_marks_genealogy_tables_and_rewrites_all_caps_heading():
    entry = BundleEntry(
        entry_id="chapter-010",
        kind="chapter",
        title="ARTHUR L'HEUREUX",
        path="chapter-010.html",
        order=10,
        prev_entry_id="chapter-009",
        next_entry_id="chapter-011",
        source_pages=(28,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )
    article_html = """
    <h1 id="blk-chapter-010-0001">ARTHUR L'HEUREUX</h1>
    <table id="blk-chapter-010-0028"><thead><tr>
    <th>NAME</th><th>BORN</th><th>MARRIED</th><th>SPOUSE</th><th>BOY</th><th>GIRL</th><th>DIED</th>
    </tr></thead><tbody><tr><td>Arthur</td><td>1885</td><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>
    """

    enhanced = enhance_article_html(entry, article_html, "Arthur L'Heureux")

    assert '<h1 id="blk-chapter-010-0001">Arthur L&#x27;Heureux</h1>' in enhanced
    assert 'class="genealogy-table"' in enhanced


def test_enhance_article_html_marks_ancestry_table_for_chapter_001():
    entry = BundleEntry(
        entry_id="chapter-001",
        kind="chapter",
        title="The Ancestral Lineage of Moïse and Sophie",
        path="chapter-001.html",
        order=2,
        prev_entry_id="page-001",
        next_entry_id="page-002",
        source_pages=(10,),
        printed_pages=(1,),
        printed_page_start=1,
        printed_page_end=1,
    )
    article_html = """
    <h1 id="blk-chapter-001-0001">The Ancestral Lineage of Moïse and Sophie</h1>
    <table id="blk-chapter-001-0003"><tbody><tr><td>RENE</td><td></td></tr></tbody></table>
    """

    enhanced = enhance_article_html(entry, article_html, "The Ancestral Lineage of Moïse and Sophie")

    assert 'class="ancestry-table"' in enhanced


def test_enhance_article_html_repairs_ancestry_table_final_rows():
    entry = BundleEntry(
        entry_id="chapter-001",
        kind="chapter",
        title="The Ancestral Lineage of Moïse and Sophie",
        path="chapter-001.html",
        order=2,
        prev_entry_id="page-001",
        next_entry_id="page-002",
        source_pages=(10,),
        printed_pages=(1,),
        printed_page_start=1,
        printed_page_end=1,
    )
    article_html = """
    <table id="blk-chapter-001-0003"><tbody>
    <tr><td>PIERRE L'HEUREUX &amp; MARIE TREPANIER</td><td>GEORGE PICHET &amp; SOPHIE CAUCHON</td></tr>
    <tr><td>\\</td><td>/</td></tr>
    <tr><td>MOÏSE L'HEUREUX &amp; SOPHIE PICHETTE</td></tr>
    <tr><td>m. January 17, 1882</td></tr>
    <tr><td>Chateau-Richer, Québec</td></tr>
    </tbody></table>
    """

    enhanced = enhance_article_html(entry, article_html, "The Ancestral Lineage of Moïse and Sophie")

    assert 'class="ancestry-final-row ancestry-connector-row"' in enhanced
    assert "<td colspan=\"2\">MOÏSE L'HEUREUX &amp; SOPHIE PICHETTE</td>" in enhanced


def test_enhance_article_html_rewrites_all_caps_page_heading():
    entry = BundleEntry(
        entry_id="page-009",
        kind="page",
        title="INTRODUCTION AND DEDICATION",
        path="page-009.html",
        order=9,
        prev_entry_id="page-008",
        next_entry_id="chapter-006",
        source_pages=(9,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )
    article_html = '<h1 id="blk-page-009-0001">INTRODUCTION AND DEDICATION</h1><p>Intro text.</p>'

    enhanced = enhance_article_html(entry, article_html, "Introduction and Dedication")

    assert '<h1 id="blk-page-009-0001">Introduction and Dedication</h1>' in enhanced


def test_enhance_article_html_wraps_figure_images_with_links_and_drops_missing_artifacts():
    entry = BundleEntry(
        entry_id="chapter-003",
        kind="chapter",
        title="Farm Heritage Award",
        path="chapter-003.html",
        order=6,
        prev_entry_id="page-003",
        next_entry_id="page-004",
        source_pages=(12,),
        printed_pages=(3,),
        printed_page_start=3,
        printed_page_end=3,
    )
    article_html = """
    <figure id="blk-chapter-003-0008"><img alt="Official Seal" data-crop-filename="page-012-001.jpg" src="images/page-012-001.jpg"/></figure>
    <figure id="blk-chapter-003-0011"><img alt="Signature of Ed Tchorzewski"/></figure>
    """

    enhanced = enhance_article_html(entry, article_html, "Farm Heritage Award")

    assert 'class="figure-emblem"' in enhanced
    assert 'href="images/page-012-001.jpg"' in enhanced
    assert 'target="_blank"' in enhanced
    assert "Signature of Ed Tchorzewski" not in enhanced


def test_enhance_article_html_wraps_chapter_005_recipe_block():
    entry = BundleEntry(
        entry_id="chapter-005",
        kind="chapter",
        title="Moïse and Sophie",
        path="chapter-005.html",
        order=5,
        prev_entry_id="page-005",
        next_entry_id="page-006",
        source_pages=(14,),
        printed_pages=(),
        printed_page_start=None,
        printed_page_end=None,
    )
    article_html = """
    <p id="blk-chapter-005-0031">It would be an injustice not to provide the reader with Moise and Sophie's famous home made beer recipe.</p>
    <h3 id="blk-chapter-005-0032"><em>FOR 10 GALLONS</em></h3>
    <p id="blk-chapter-005-0033"><em>10 pounds of barley</em></p>
    <p id="blk-chapter-005-0034"><strong><em>METHOD</em></strong></p>
    <p id="blk-chapter-005-0035"><em>Roast barley.</em></p>
    <p id="blk-chapter-005-0036"><strong><em>THE YEAST</em></strong></p>
    <p id="blk-chapter-005-0037"><em>1 yeast cake</em></p>
    <p id="blk-chapter-005-0038"><em>When the water in the barrel is lukewarm.</em></p>
    """

    enhanced = enhance_article_html(entry, article_html, "Moïse and Sophie")

    assert '<section class="recipe-callout">' in enhanced
    assert 'blk-chapter-005-0032' in enhanced


def test_expand_entry_fragments_splits_chapter_024_into_poem_and_photo_pages():
    entry = BundleEntry(
        entry_id="chapter-024",
        kind="chapter",
        title="I WISH",
        path="chapter-024.html",
        order=33,
        prev_entry_id="chapter-023",
        next_entry_id=None,
        source_pages=(120, 121, 122),
        printed_pages=(111, 112, 113),
        printed_page_start=111,
        printed_page_end=113,
    )
    article_html = """
    <h1 id="blk-chapter-024-0001"><strong><em>I WISH</em></strong></h1>
    <p id="blk-chapter-024-0002"><em>I wish that every child could know</em></p>
    <figure id="blk-chapter-024-0009"><img alt="Family gathering" data-crop-filename="page-121-000.jpg" src="images/page-121-000.jpg"/></figure>
    <figure id="blk-chapter-024-0010"><img alt="Ranch horse" data-crop-filename="page-121-001.jpg" src="images/page-121-001.jpg"/></figure>
    <figure id="blk-chapter-024-0011"><img alt="Reunion" data-crop-filename="page-122-000.jpg" src="images/page-122-000.jpg"/></figure>
    <figure id="blk-chapter-024-0012"><img alt="Woman seated"/></figure>
    """

    fragments = expand_entry_fragments(entry, article_html, source_entry_ids=(entry.entry_id,))

    assert [fragment.entry.entry_id for fragment in fragments] == [
        "chapter-024",
        "page-photo-121",
        "page-photo-122",
    ]
    assert fragments[0].block_ids == ("blk-chapter-024-0001", "blk-chapter-024-0002")
    assert fragments[1].block_ids == ("blk-chapter-024-0009", "blk-chapter-024-0010")
    assert fragments[2].block_ids == ("blk-chapter-024-0011", "blk-chapter-024-0012")
    assert fragments[1].entry.title == "Family Gathering and Ranch Stallion"
    assert fragments[2].entry.printed_pages == (113,)
