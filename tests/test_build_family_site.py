from __future__ import annotations

from html import unescape
import json
from pathlib import Path

from modules.build_family_site import build_family_site


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
    omission_audit = json.loads(result.omission_audit_path.read_text(encoding="utf-8"))

    assert "Fixture Reading Surface" in landing_html
    assert "Book Chapters" in landing_html
    assert "Family stories" in landing_html
    assert "Pages & Images" in unescape(landing_html)
    assert "Alma Marie (L'Heureux) Alain" in unescape(landing_html)
    assert "The Ancestral Lineage of Moïse and Sophie" in unescape(landing_html)
    assert "Image 1" in landing_html
    assert 'id="blk-chapter-009-0001"' in chapter_html
    assert 'id="blk-page-001-0001"' in page_html
    assert "Contents" in page_html
    assert "Contents" in chapter_one_html
    assert "Contents" in chapter_html
    assert "Visible provenance" not in chapter_html
    assert "Omission audit" not in chapter_html
    assert "Whole-book access, with no silent losses." not in landing_html
    assert "source-manifest" not in landing_html

    entry_rows = json.loads(
        (output_dir / "_internal" / "provenance" / "entries" / "chapter-009.json").read_text(encoding="utf-8")
    )
    assert entry_rows[0]["block_id"] == "blk-chapter-009-0001"
    assert omission_audit["manifest_entry_count"] == 3
    assert omission_audit["status_counts"] == {"rendered": 3}
    assert omission_audit["entries"][0]["entry_id"] == "page-001"
    assert omission_audit["entries"][1]["group_id"] == "book-chapters"
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
