from __future__ import annotations

from pathlib import Path

from modules.build_audiobook_script import (
    expected_filenames,
    load_entries_by_id,
    managed_chapter_specs,
    render_source_markdown,
)
from modules.build_family_site import resolve_source_dir


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "audiobook-script"
RAW_HTML_MARKERS = ("<table", "<article", "<nav", "<figure", "<img")


def read_script(name: str) -> str:
    return (SCRIPT_DIR / name).read_text(encoding="utf-8")


def test_audiobook_script_contains_expected_markdown_files_in_order():
    assert SCRIPT_DIR.exists()

    actual_files = sorted(path.name for path in SCRIPT_DIR.glob("*.md"))

    assert actual_files == list(expected_filenames())


def test_audiobook_script_files_are_reader_facing_markdown_not_raw_html():
    for filename in expected_filenames():
        text = read_script(filename)

        assert text.startswith("# ")
        for marker in RAW_HTML_MARKERS:
            assert marker not in text


def test_preamble_explains_the_listening_boundary():
    text = read_script("01-preamble.md")
    normalized = text.replace("\n", " ")

    assert "Centennial Reunion" in text
    assert "Genealogy tables" in text
    assert "narrative chapters" in normalized


def test_family_story_sample_stops_before_genealogy_tables():
    text = read_script("05-alma-marie-lheureux-alain.md")

    assert "While Alma was still a young girl" in text
    assert "Henry and Alma Alain on their 50th wedding anniversary in 1957." not in text
    assert "\n# Alma L'Heureux Alain" not in text
    assert "TOTAL DESCENDANTS" not in text


def test_epilogue_stops_before_visual_appendix_material():
    text = read_script("20-i-wish.md")

    assert "I wish that every child could know" in text
    assert "Author Unknown" in text
    assert "L'HEUREUX VETERANS" not in text
    assert "MOISE & SOPHIE L'HEUREUX" not in text
    assert "THE FIRST POST OFFICE IN THIS AREA" not in text
    assert "THIS HISTORICAL SITE IS DEDICATED TO THE DESCENDANTS" not in text
    assert "CANADA POSTES" not in text


def test_source_derived_scripts_match_the_current_deterministic_renderer():
    source_dir = resolve_source_dir(None)
    entries_by_id = load_entries_by_id(source_dir)

    for spec in managed_chapter_specs():
        assert read_script(spec.filename) == render_source_markdown(spec, source_dir, entries_by_id)
