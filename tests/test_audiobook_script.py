from __future__ import annotations

from pathlib import Path

from modules.build_audiobook_script import (
    expected_filenames,
    load_entries_by_id,
    managed_chapter_specs,
    render_source_markdown,
    script_source_dir,
)
from modules.build_family_site import resolve_source_dir


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "audiobook/script"
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


def test_preamble_prose_is_not_hard_wrapped_for_tts_upload():
    paragraphs = [
        block.splitlines()
        for block in read_script("01-preamble.md").strip().split("\n\n")
        if block and not block.startswith("# ")
    ]

    assert paragraphs
    assert all(len(lines) == 1 for lines in paragraphs)


def test_family_story_sample_stops_before_genealogy_tables():
    text = read_script("05-alma-marie-lheureux-alain.md")

    assert "While Alma was still a young girl" in text
    assert "Henry and Alma Alain on their 50th wedding anniversary in 1957." not in text
    assert "\n# Alma L'Heureux Alain" not in text
    assert "TOTAL DESCENDANTS" not in text


def test_memoir_script_uses_reader_facing_title_and_omits_title_page():
    text = read_script("20-rolland-alain-memoir-family-story.md")

    assert text.startswith("# Rolland Alain Memoir Family Story")
    assert (
        "\n\nMarch 7th 1985\n\n> Note that this was not a story originally included in the Onward to the Unknown book. "
        "It was found in one copy of the book as a set of photocopied pages.\n\n"
        "## Memoires of Rolland Alain from birth 1913 to 71st year 1985\n\n"
    ) in text
    assert "Two of my best friends were Jean-Paul Schiller and Alfred Duvall and they were at our place a lot" in text
    assert "Memoires de Rolland Alain" not in text


def test_epilogue_stops_before_visual_appendix_material():
    text = read_script("21-i-wish.md")

    assert "I wish that every child could know" in text
    assert "Author Unknown" in text
    assert "L'HEUREUX VETERANS" not in text
    assert "MOISE & SOPHIE L'HEUREUX" not in text
    assert "THE FIRST POST OFFICE IN THIS AREA" not in text
    assert "THIS HISTORICAL SITE IS DEDICATED TO THE DESCENDANTS" not in text
    assert "CANADA POSTES" not in text


def test_source_derived_scripts_match_the_current_deterministic_renderer():
    source_dir = resolve_source_dir(None)

    for spec in managed_chapter_specs():
        spec_source_dir = script_source_dir(spec, source_dir)
        entries_by_id = load_entries_by_id(spec_source_dir)
        assert read_script(spec.filename) == render_source_markdown(spec, spec_source_dir, entries_by_id)
