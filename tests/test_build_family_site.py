from __future__ import annotations

from html import unescape
import json
from pathlib import Path

from modules.build_family_site import build_family_site


def test_build_family_site_emits_landing_pages_and_provenance(tmp_path):
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
        family_entry_ids=["chapter-009", "chapter-010"],
        site_title="Fixture Family Stories",
    )

    assert result.rendered_entry_ids == ("chapter-009", "chapter-010")
    assert (output_dir / "index.html").exists()
    assert (output_dir / "chapter-009.html").exists()
    assert (output_dir / "chapter-010.html").exists()
    assert (output_dir / "assets" / "family-site.css").exists()
    assert (output_dir / "images" / "family-portrait.svg").exists()
    assert (output_dir / "provenance" / "blocks.jsonl").exists()
    assert (output_dir / "provenance" / "entries" / "chapter-009.json").exists()
    assert (output_dir / "source-manifest.json").exists()

    landing_html = (output_dir / "index.html").read_text(encoding="utf-8")
    chapter_html = (output_dir / "chapter-009.html").read_text(encoding="utf-8")

    assert "Fixture Family Stories" in landing_html
    assert "Whole-page family story" in chapter_html
    assert "Alma Marie (L'Heureux) Alain" in unescape(landing_html)
    assert 'id="blk-chapter-009-0001"' in chapter_html
    assert "Source pages: 22, 23" in chapter_html
    assert "Entry provenance JSON" in chapter_html

    entry_rows = json.loads(
        (output_dir / "provenance" / "entries" / "chapter-009.json").read_text(encoding="utf-8")
    )
    assert entry_rows[0]["block_id"] == "blk-chapter-009-0001"


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
            family_entry_ids=["chapter-999"],
        )
    except SystemExit as exc:
        assert "chapter-999" in str(exc)
    else:
        raise AssertionError("Expected build_family_site to reject missing entry ids.")
