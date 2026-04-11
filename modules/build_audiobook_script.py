from __future__ import annotations

import re
from dataclasses import dataclass
from html import unescape
from pathlib import Path

from modules.build_family_site import (
    article_blocks,
    bundle_entry_from_manifest,
    extract_article_html,
    load_manifest,
    resolve_source_dir,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("audiobook/script")
BLOCK_TAG_PATTERN = re.compile(r"^<([a-z0-9]+)\b", re.IGNORECASE)
TAG_PATTERN = re.compile(r"<[^>]+>")
LINEBREAK_TAG_PATTERN = re.compile(r"<br\s*/?>", re.IGNORECASE)
EMPHASIS_TAG_PATTERN = re.compile(r"</?(?:em|i)\b[^>]*>", re.IGNORECASE)
STRONG_TAG_PATTERN = re.compile(r"</?(?:strong|b)\b[^>]*>", re.IGNORECASE)
WHITESPACE_PATTERN = re.compile(r"[^\S\n]+")


@dataclass(frozen=True)
class ScriptChapterSpec:
    filename: str
    title: str
    source_entry_id: str | None
    mode: str
    source_dir: Path | None = None
    inline_note: str | None = None


@dataclass(frozen=True)
class ScriptBuildResult:
    source_dir: Path
    output_dir: Path
    written_files: tuple[str, ...]


SCRIPT_CHAPTER_SPECS = (
    ScriptChapterSpec("01-preamble.md", "Preamble", None, "manual"),
    ScriptChapterSpec(
        "02-the-first-lheureuxs-in-canada.md",
        "The First L'Heureux's in Canada",
        "chapter-002",
        "full",
    ),
    ScriptChapterSpec("03-moise-and-sophie.md", "Moïse and Sophie", "chapter-005", "full"),
    ScriptChapterSpec("04-memories.md", "Memories", "chapter-007", "full"),
    ScriptChapterSpec(
        "05-alma-marie-lheureux-alain.md",
        "Alma Marie (L'Heureux) Alain",
        "chapter-009",
        "before_first_table",
    ),
    ScriptChapterSpec("06-arthur-lheureux.md", "Arthur L'Heureux", "chapter-010", "before_first_table"),
    ScriptChapterSpec("07-leonidas-lheureux.md", "Leonidas L'Heureux", "chapter-011", "before_first_table"),
    ScriptChapterSpec(
        "08-josephine-lheureux-alain.md",
        "Josephine (L'Heureux) Alain",
        "chapter-012",
        "before_first_table",
    ),
    ScriptChapterSpec("09-paul-lheureux.md", "Paul L'Heureux", "chapter-013", "before_first_table"),
    ScriptChapterSpec("10-george-lheureux.md", "George L'Heureux", "chapter-014", "before_first_table"),
    ScriptChapterSpec(
        "11-joe-joseph-lheureux.md",
        "Joe (Joseph) L'Heureux",
        "chapter-015",
        "before_first_table",
    ),
    ScriptChapterSpec(
        "12-mathilda-lheureux-devlin.md",
        "Mathilda (L'Heureux) Devlin",
        "chapter-016",
        "before_first_table",
    ),
    ScriptChapterSpec(
        "13-marie-louise-lheureux-laclare.md",
        "Marie-Louise (L'Heureux) LaClare",
        "chapter-017",
        "before_first_table",
    ),
    ScriptChapterSpec(
        "14-roseanna-lheureux-landreville.md",
        "Roseanna (L'Heureux) Landreville",
        "chapter-018",
        "before_first_table",
    ),
    ScriptChapterSpec(
        "15-antoinette-lheureux-richard.md",
        "Antoinette (L'Heureux) Richard",
        "chapter-019",
        "before_first_table",
    ),
    ScriptChapterSpec(
        "16-emilie-lheureux-nolin.md",
        "Emilie (L'Heureux) Nolin",
        "chapter-020",
        "before_first_table",
    ),
    ScriptChapterSpec("17-wilfrid-lheureux.md", "Wilfrid L'Heureux", "chapter-021", "before_first_table"),
    ScriptChapterSpec("18-pierre-lheureux.md", "Pierre L'Heureux", "chapter-022", "before_first_table"),
    ScriptChapterSpec("19-antoine-lheureux.md", "Antoine L'Heureux", "chapter-023", "before_first_table"),
    ScriptChapterSpec(
        "20-rolland-alain-memoir-family-story.md",
        "Rolland Alain Memoir Family Story",
        "chapter-001",
        "full",
        Path("input/doc-web-html/rolland-alain-memoir-r01"),
        "Note that this was not a story originally included in the Onward to the Unknown book. It was found in one copy of the book as a set of photocopied pages.",
    ),
    ScriptChapterSpec("21-i-wish.md", "I Wish", "chapter-024", "before_first_figure"),
)


def managed_chapter_specs() -> tuple[ScriptChapterSpec, ...]:
    return tuple(spec for spec in SCRIPT_CHAPTER_SPECS if spec.source_entry_id is not None)


def expected_filenames() -> tuple[str, ...]:
    return tuple(spec.filename for spec in SCRIPT_CHAPTER_SPECS)


def load_entries_by_id(source_dir: Path) -> dict[str, object]:
    manifest = load_manifest(source_dir)
    entries = [bundle_entry_from_manifest(row) for row in manifest.get("entries", [])]
    return {entry.entry_id: entry for entry in entries}


def script_source_dir(spec: ScriptChapterSpec, default_source_dir: Path) -> Path:
    if spec.source_dir is None:
        return default_source_dir
    source_dir = spec.source_dir
    if not source_dir.is_absolute():
        source_dir = (REPO_ROOT / source_dir).resolve()
    return source_dir


def block_tag(block_html: str) -> str | None:
    match = BLOCK_TAG_PATTERN.match(block_html.lstrip())
    if not match:
        return None
    return match.group(1).lower()


def inner_html(block_html: str) -> str:
    stripped = block_html.strip()
    opening_end = stripped.find(">")
    closing_start = stripped.rfind("</")
    if opening_end == -1 or closing_start == -1 or closing_start <= opening_end:
        return stripped
    return stripped[opening_end + 1 : closing_start]


def normalize_markdown_text(text: str) -> str:
    normalized_lines: list[str] = []
    for line in text.splitlines():
        collapsed = WHITESPACE_PATTERN.sub(" ", line).strip()
        collapsed = re.sub(r"\s+([,.;:!?])", r"\1", collapsed)
        normalized_lines.append(collapsed)
    normalized_lines = [line for line in normalized_lines if line]
    return "\n".join(normalized_lines)


def markdown_inline(fragment_html: str) -> str:
    text = LINEBREAK_TAG_PATTERN.sub("\n", fragment_html)
    text = STRONG_TAG_PATTERN.sub("**", text)
    text = EMPHASIS_TAG_PATTERN.sub("*", text)
    text = TAG_PATTERN.sub("", text)
    return normalize_markdown_text(unescape(text))


def markdown_from_block(block_html: str) -> str | None:
    tag = block_tag(block_html)
    if tag is None:
        return None

    content = markdown_inline(inner_html(block_html))
    if not content:
        return None

    if tag == "h1":
        return f"# {content}"
    if tag == "h2":
        return f"## {content}"
    if tag == "h3":
        return f"### {content}"
    if tag == "p":
        return content
    if tag == "li":
        return f"- {content}"
    return None


def select_script_blocks(spec: ScriptChapterSpec, article_html: str) -> list[str]:
    blocks = article_blocks(article_html)
    selected: list[str] = []
    for index, block_html in enumerate(blocks):
        tag = block_tag(block_html)
        next_tag = block_tag(blocks[index + 1]) if index + 1 < len(blocks) else None

        if spec.mode == "before_first_figure" and tag in {"figure", "table"}:
            break
        if spec.mode == "before_first_table":
            if tag == "table":
                break
            if tag in {"h1", "h2", "h3"} and next_tag == "table":
                break
        if tag in {"figure", "table"}:
            continue
        selected.append(block_html)
    return selected


def render_source_markdown(spec: ScriptChapterSpec, source_dir: Path, entries_by_id: dict[str, object]) -> str:
    if spec.source_entry_id is None:
        raise ValueError(f"{spec.filename} is manual and cannot be rendered from source HTML.")

    entry = entries_by_id.get(spec.source_entry_id)
    if entry is None:
        raise SystemExit(f"Source bundle is missing the expected entry: {spec.source_entry_id}")

    source_path = source_dir / entry.path
    article_html = extract_article_html(source_path.read_text(encoding="utf-8"), source_path)
    markdown_blocks = [
        markdown
        for block_html in select_script_blocks(spec, article_html)
        if (markdown := markdown_from_block(block_html))
    ]
    if not markdown_blocks:
        raise SystemExit(f"No Markdown content was produced for {spec.source_entry_id} from {source_path}")
    if markdown_blocks[0].startswith("# "):
        markdown_blocks[0] = f"# {spec.title}"
    else:
        for index, block in enumerate(markdown_blocks):
            if not block.startswith("# "):
                continue
            markdown_blocks[index] = "## " + block[2:]
            break
        markdown_blocks.insert(0, f"# {spec.title}")
    if spec.inline_note:
        insertion_index = 2 if len(markdown_blocks) > 1 else len(markdown_blocks)
        markdown_blocks.insert(insertion_index, f"> {spec.inline_note}")
    return "\n\n".join(markdown_blocks).rstrip() + "\n"


def build_audiobook_script(
    source_dir: str | Path | None = None,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    *,
    force: bool = False,
) -> ScriptBuildResult:
    resolved_source_dir = resolve_source_dir(source_dir)
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    entries_cache: dict[Path, dict[str, object]] = {}

    written_files: list[str] = []
    for spec in managed_chapter_specs():
        target_path = target_dir / spec.filename
        if target_path.exists() and not force:
            raise SystemExit(
                f"Refusing to overwrite existing audiobook script file without --force: {target_path}"
            )
        spec_source_dir = script_source_dir(spec, resolved_source_dir)
        entries_by_id = entries_cache.setdefault(spec_source_dir, load_entries_by_id(spec_source_dir))
        target_path.write_text(
            render_source_markdown(spec, spec_source_dir, entries_by_id),
            encoding="utf-8",
        )
        written_files.append(spec.filename)

    return ScriptBuildResult(
        source_dir=resolved_source_dir,
        output_dir=target_dir,
        written_files=tuple(written_files),
    )


def cli_main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Generate source-derived audiobook Markdown chapters from the staged "
            "input bundle without touching the manual preamble."
        )
    )
    parser.add_argument("--source", help="Path to the staged input bundle directory containing manifest.json.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Directory to receive generated Markdown chapters (default: {DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated chapter files. Use with care after manual cleanup.",
    )
    args = parser.parse_args(argv)

    result = build_audiobook_script(args.source, args.output, force=args.force)
    print(
        f"Wrote {len(result.written_files)} source-derived audiobook chapters to "
        f"{result.output_dir} from {result.source_dir}."
    )
    return 0
