from __future__ import annotations

import json
import os
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from html import escape, unescape
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = REPO_ROOT / "input" / "doc-web-html" / "story206-onward-proof-r10"
DEFAULT_FAMILY_ENTRY_IDS = frozenset(f"chapter-{number:03d}" for number in range(9, 24))
DEFAULT_OUTPUT_DIR = Path("build/family-site")
DEFAULT_SITE_TITLE = "Onward to the Unknown"
SOURCE_ENV_KEYS = ("ONWARD_INPUT_SOURCE_DIR", "DREAMHOST_DEPLOY_SOURCE_DIR")
ARTICLE_PATTERN = re.compile(r"<article>(.*?)</article>", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
H1_PATTERN = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
H2_PATTERN = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.IGNORECASE | re.DOTALL)
FIGCAPTION_PATTERN = re.compile(r"<figcaption\b[^>]*>(.*?)</figcaption>", re.IGNORECASE | re.DOTALL)
PARAGRAPH_PATTERN = re.compile(r"<p\b[^>]*>(.*?)</p>", re.IGNORECASE | re.DOTALL)
IMG_ALT_PATTERN = re.compile(r"<img\b[^>]*\balt=(?:\"([^\"]+)\"|'([^']+)')", re.IGNORECASE)
PLACEHOLDER_PAGE_TITLE_PATTERN = re.compile(r"^(?:Image \d+|Page [ivxlcdm]+)$", re.IGNORECASE)
LANDING_CARD_SUMMARY_LIMIT = 140
SHORT_LABEL_MAX_LENGTH = 88
TITLE_CASE_SMALL_WORDS = frozenset(
    {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to"}
)

SITE_STYLESHEET = dedent(
    """
    :root {
      --bg: #f4ecdf;
      --paper: rgba(255, 251, 245, 0.94);
      --paper-strong: #fffdf9;
      --ink: #231c14;
      --muted: #675d52;
      --border: #d7c7b3;
      --accent: #6f2e1d;
      --accent-strong: #8a3e29;
      --accent-soft: #efe1d1;
      --shadow: 0 18px 45px rgba(71, 48, 26, 0.09);
      --body-font: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
      --ui-font: "Avenir Next", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
      --max-width: 74rem;
      --hit-target: 3.5rem;
    }

    * { box-sizing: border-box; }

    html {
      font-size: 112.5%;
      scroll-behavior: smooth;
      background: linear-gradient(180deg, #f8f2e8 0%, #efe3d3 100%);
    }

    body {
      margin: 0;
      color: var(--ink);
      font-family: var(--body-font);
      line-height: 1.85;
      background:
        radial-gradient(circle at top left, rgba(255, 255, 255, 0.45), transparent 38%),
        linear-gradient(180deg, #f8f2e8 0%, #efe3d3 100%);
    }

    a {
      color: inherit;
      text-underline-offset: 0.18em;
    }

    img {
      max-width: 100%;
      height: auto;
      display: block;
    }

    code {
      font-family: "SFMono-Regular", "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 0.92em;
    }

    .site-shell {
      width: min(var(--max-width), calc(100% - 1.5rem));
      margin: 0 auto;
      padding: 1rem 0 3rem;
    }

    .site-header {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
    }

    .site-title,
    .section-title {
      font-family: var(--ui-font);
      line-height: 1.12;
      letter-spacing: -0.02em;
    }

    .site-title {
      font-size: clamp(2rem, 4vw, 3.2rem);
      margin: 0;
    }

    .section-title {
      font-size: clamp(1.4rem, 3vw, 1.9rem);
      margin: 0;
    }

    .hero,
    .panel,
    .story-card,
    .article-card {
      background: var(--paper);
      border: 1px solid var(--border);
      border-radius: 1.15rem;
      box-shadow: var(--shadow);
    }

    .hero {
      padding: 1.6rem;
      margin-bottom: 1.5rem;
    }

    .hero h1,
    .story-title,
    .article-card h1,
    .article-card h2,
    .article-card h3 {
      font-family: var(--ui-font);
      line-height: 1.18;
      letter-spacing: -0.02em;
    }

    .hero h1 {
      font-size: clamp(2.6rem, 5vw, 4.2rem);
      margin: 0;
      max-width: 40rem;
    }

    .jump-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
    }

    .jump-row {
      margin-top: 1.25rem;
    }

    .section-panel {
      padding: 1.3rem;
      margin-bottom: 1.5rem;
    }

    .section-header {
      margin-bottom: 1rem;
    }

    .story-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
      gap: 1rem;
      margin: 0;
    }

    .story-card {
      display: block;
      text-decoration: none;
      padding: 1.15rem;
      min-height: 15rem;
      transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
    }

    .story-card:hover,
    .story-card:focus-visible {
      transform: translateY(-2px);
      box-shadow: 0 22px 48px rgba(71, 48, 26, 0.14);
      border-color: rgba(111, 46, 29, 0.38);
      outline: none;
    }

    .story-card .story-title {
      font-size: 1.35rem;
      margin: 0.35rem 0 0.75rem;
    }

    .story-card p {
      margin: 0.7rem 0 0;
      color: var(--ink);
    }

    .page-nav {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-bottom: 1.1rem;
    }

    .nav-button,
    .nav-placeholder {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: var(--hit-target);
      padding: 0.85rem 1rem;
      border-radius: 999px;
      font-family: var(--ui-font);
      font-size: 1rem;
      line-height: 1.2;
      text-decoration: none;
      border: 1px solid var(--border);
      background: var(--paper-strong);
    }

    .nav-button,
    .nav-placeholder {
      flex: 1 1 12rem;
    }

    .nav-button.primary {
      background: var(--accent);
      color: #fff8f0;
      border-color: transparent;
    }

    .nav-button.secondary {
      background: rgba(255, 255, 255, 0.72);
    }

    .nav-placeholder {
      color: var(--muted);
      background: rgba(255, 255, 255, 0.4);
    }

    .article-card {
      padding: 1.4rem;
    }

    .article-card {
      overflow: hidden;
    }

    .article-card h1 {
      font-size: clamp(2.1rem, 4vw, 3.2rem);
      margin: 0 0 1rem;
    }

    .article-card h2 {
      font-size: clamp(1.45rem, 3vw, 2rem);
      margin: 1.6rem 0 0.8rem;
    }

    .article-card h3 {
      font-size: 1.25rem;
      margin: 1.4rem 0 0.7rem;
    }

    .article-card p {
      margin: 0 0 1rem;
    }

    .article-card figure {
      margin: 1.5rem 0;
      padding: 0.9rem;
      border-radius: 0.85rem;
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(246, 237, 225, 0.92));
      border: 1px solid rgba(111, 46, 29, 0.14);
    }

    .article-card figcaption {
      margin-top: 0.7rem;
      font-family: var(--ui-font);
      font-size: 0.95rem;
      color: var(--muted);
    }

    .article-card table {
      width: 100%;
      border-collapse: collapse;
      display: block;
      overflow-x: auto;
      margin: 1.4rem 0;
      font-size: 1rem;
      background: rgba(255, 255, 255, 0.55);
      border-radius: 0.7rem;
    }

    .article-card th,
    .article-card td {
      border: 1px solid rgba(111, 46, 29, 0.14);
      padding: 0.8rem 0.9rem;
      text-align: left;
      vertical-align: top;
    }

    .article-card th {
      background: rgba(111, 46, 29, 0.08);
      font-family: var(--ui-font);
    }

    .article-card tr:nth-child(even) td {
      background: rgba(255, 255, 255, 0.35);
    }

    @media (max-width: 54rem) {
      html { font-size: 106.25%; }

      .site-shell {
        width: min(var(--max-width), calc(100% - 1rem));
      }
    }

    @media (max-width: 38rem) {
      html { font-size: 100%; }

      .hero,
      .section-panel,
      .article-card,
      .story-card {
        padding: 1rem;
      }

      .nav-button,
      .nav-placeholder {
        flex-basis: 100%;
      }
    }
    """
).strip()


@dataclass(frozen=True)
class EntryGroup:
    id: str
    label: str
    rendered_rationale: str


ENTRY_GROUPS = (
    EntryGroup(
        id="book-chapters",
        label="Book Chapters",
        rendered_rationale="Rendered as a whole-book chapter page in the accessible local reading surface.",
    ),
    EntryGroup(
        id="family-stories",
        label="Family stories",
        rendered_rationale="Rendered as a whole-page family story inside the whole-book local reading surface.",
    ),
    EntryGroup(
        id="pages-and-images",
        label="Pages & Images",
        rendered_rationale="Rendered as a standalone page/image entry with light reshaping so the source page remains reachable.",
    ),
)
ENTRY_GROUPS_BY_ID = {group.id: group for group in ENTRY_GROUPS}


@dataclass(frozen=True)
class BundleEntry:
    entry_id: str
    kind: str
    title: str
    path: str
    order: int
    prev_entry_id: str | None
    next_entry_id: str | None
    source_pages: tuple[int, ...]
    printed_pages: tuple[int, ...]
    printed_page_start: int | None
    printed_page_end: int | None


@dataclass(frozen=True)
class RenderedEntry:
    entry: BundleEntry
    group: EntryGroup
    article_html: str
    display_title: str
    summary_text: str


@dataclass(frozen=True)
class AuditRow:
    entry: BundleEntry
    group: EntryGroup
    status: str
    surface: str
    output_path: str | None
    rationale: str


@dataclass(frozen=True)
class BuildResult:
    source_dir: Path
    output_dir: Path
    rendered_entry_ids: tuple[str, ...]
    omission_audit_path: Path


def bundle_entry_from_manifest(row: dict) -> BundleEntry:
    return BundleEntry(
        entry_id=row["entry_id"],
        kind=row["kind"],
        title=row["title"],
        path=row["path"],
        order=row["order"],
        prev_entry_id=row.get("prev_entry_id"),
        next_entry_id=row.get("next_entry_id"),
        source_pages=tuple(row.get("source_pages", [])),
        printed_pages=tuple(row.get("printed_pages", [])),
        printed_page_start=row.get("printed_page_start"),
        printed_page_end=row.get("printed_page_end"),
    )


def resolve_source_dir(source: str | Path | None = None) -> Path:
    candidates: list[Path] = []
    if source:
        candidates.append(Path(source))
    for key in SOURCE_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            candidates.append(Path(value))
    candidates.append(DEFAULT_SOURCE_DIR)

    for candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if (resolved / "manifest.json").exists():
            return resolved

    searched = [str(path) for path in candidates] or ["<none>"]
    raise SystemExit(
        "Could not locate the input bundle. Looked for a directory containing "
        f"`manifest.json` in: {', '.join(searched)}"
    )


def load_manifest(source_dir: Path) -> dict:
    manifest_path = source_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest.json in source bundle: {source_dir}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def extract_article_html(document_text: str, source_path: Path) -> str:
    match = ARTICLE_PATTERN.search(document_text)
    if not match:
        raise SystemExit(f"Could not find <article>...</article> in {source_path}")
    return match.group(1).strip()


def plain_text_from_html(html_fragment: str) -> str:
    text = unescape(TAG_PATTERN.sub(" ", html_fragment))
    return WHITESPACE_PATTERN.sub(" ", text).strip()


def excerpt_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def plain_text_excerpt(article_html: str, limit: int = LANDING_CARD_SUMMARY_LIMIT) -> str:
    return excerpt_text(plain_text_from_html(article_html), limit)


def first_fragment_text(pattern: re.Pattern[str], article_html: str) -> str | None:
    match = pattern.search(article_html)
    if not match:
        return None
    text = plain_text_from_html(match.group(1))
    return text or None


def first_image_alt(article_html: str) -> str | None:
    match = IMG_ALT_PATTERN.search(article_html)
    if not match:
        return None
    text = unescape(match.group(1) or match.group(2) or "")
    text = WHITESPACE_PATTERN.sub(" ", text).strip()
    return text or None


def short_paragraph_label(article_html: str, max_length: int = SHORT_LABEL_MAX_LENGTH) -> str | None:
    for match in PARAGRAPH_PATTERN.finditer(article_html):
        text = plain_text_from_html(match.group(1))
        if text and len(text) <= max_length:
            return text
    return None


def is_mostly_uppercase(text: str) -> bool:
    letters = [character for character in text if character.isalpha()]
    if len(letters) < 4:
        return False
    uppercase = sum(1 for character in letters if character.isupper())
    return uppercase / len(letters) >= 0.8


def soften_display_title(text: str) -> str:
    normalized = WHITESPACE_PATTERN.sub(" ", text).strip()
    if not normalized or not is_mostly_uppercase(normalized):
        return normalized

    words = normalized.lower().split()
    softened: list[str] = []
    for index, word in enumerate(words):
        if 0 < index < len(words) - 1 and word in TITLE_CASE_SMALL_WORDS:
            softened.append(word)
            continue
        softened.append(word.title())
    return " ".join(softened)


def derive_display_title(entry: BundleEntry, article_html: str) -> str:
    if entry.kind != "page" or not PLACEHOLDER_PAGE_TITLE_PATTERN.fullmatch(entry.title.strip()):
        return entry.title

    candidates = (
        first_fragment_text(H1_PATTERN, article_html),
        first_fragment_text(H2_PATTERN, article_html),
        first_fragment_text(FIGCAPTION_PATTERN, article_html),
        short_paragraph_label(article_html),
        first_image_alt(article_html),
    )
    for candidate in candidates:
        if candidate:
            return soften_display_title(candidate)

    if entry.title.lower().startswith("image "):
        source_page = entry.source_pages[0] if entry.source_pages else None
        if source_page is not None:
            return f"Illustration page {source_page}"
        return "Illustration page"
    return entry.title


def build_summary_text(article_html: str, display_title: str, limit: int = LANDING_CARD_SUMMARY_LIMIT) -> str:
    text = plain_text_from_html(article_html)
    title_prefix = WHITESPACE_PATTERN.sub(" ", display_title).strip()
    if title_prefix and text.casefold().startswith(title_prefix.casefold()):
        text = text[len(title_prefix) :].lstrip(" :;,.!-")
    if not text:
        return ""
    return excerpt_text(text, limit)


def load_provenance_rows(source_dir: Path) -> dict[str, list[dict]]:
    provenance_path = source_dir / "provenance" / "blocks.jsonl"
    if not provenance_path.exists():
        return {}

    rows_by_entry: dict[str, list[dict]] = defaultdict(list)
    for raw_line in provenance_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        row = json.loads(raw_line)
        rows_by_entry[row["entry_id"]].append(row)
    return rows_by_entry


def format_range(label: str, start: int | None, end: int | None) -> str:
    if start is None:
        return f"{label}: not recorded"
    if end is None or end == start:
        return f"{label}: {start}"
    return f"{label}: {start}-{end}"


def format_list(label: str, values: tuple[int, ...]) -> str:
    if not values:
        return f"{label}: none recorded"
    return f"{label}: {', '.join(str(value) for value in values)}"


def group_for_entry(entry: BundleEntry) -> EntryGroup:
    if entry.kind == "page":
        return ENTRY_GROUPS_BY_ID["pages-and-images"]
    if entry.entry_id in DEFAULT_FAMILY_ENTRY_IDS:
        return ENTRY_GROUPS_BY_ID["family-stories"]
    return ENTRY_GROUPS_BY_ID["book-chapters"]


def select_entries(all_entries: list[BundleEntry], entry_ids: list[str] | None) -> list[BundleEntry]:
    if not entry_ids:
        return list(all_entries)

    entries_by_id = {entry.entry_id: entry for entry in all_entries}
    missing = [entry_id for entry_id in entry_ids if entry_id not in entries_by_id]
    if missing:
        raise SystemExit(
            "Manifest does not contain requested entry id(s): " + ", ".join(sorted(missing))
        )

    requested_ids = set(entry_ids)
    return [entry for entry in all_entries if entry.entry_id in requested_ids]


def build_rendered_entries(
    source_dir: Path,
    entries: list[BundleEntry],
) -> list[RenderedEntry]:
    rendered: list[RenderedEntry] = []
    for entry in entries:
        document_text = (source_dir / entry.path).read_text(encoding="utf-8")
        article_html = extract_article_html(document_text, source_dir / entry.path)
        display_title = derive_display_title(entry, article_html)
        rendered.append(
            RenderedEntry(
                entry=entry,
                group=group_for_entry(entry),
                article_html=article_html,
                display_title=display_title,
                summary_text=build_summary_text(article_html, display_title),
            )
        )
    return rendered


def build_omission_audit(
    all_entries: list[BundleEntry],
    selected_entries: list[BundleEntry],
) -> list[AuditRow]:
    selected_ids = {entry.entry_id for entry in selected_entries}
    audit_rows: list[AuditRow] = []
    for entry in all_entries:
        group = group_for_entry(entry)
        if entry.entry_id in selected_ids:
            audit_rows.append(
                AuditRow(
                    entry=entry,
                    group=group,
                    status="rendered",
                    surface="whole-entry-page",
                    output_path=entry.path,
                    rationale=group.rendered_rationale,
                )
            )
            continue

        audit_rows.append(
            AuditRow(
                entry=entry,
                group=group,
                status="intentionally_deferred",
                surface="audit-only",
                output_path=None,
                rationale="Excluded from this filtered build invocation because `--entry-id` requested a smaller subset.",
            )
        )
    return audit_rows


def ensure_clean_output_dir(output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_layout(title: str, body_html: str) -> str:
    return dedent(
        f"""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{escape(title)}</title>
        <link rel="stylesheet" href="assets/family-site.css">
        </head>
        <body>
        {body_html}
        </body>
        </html>
        """
    )


def render_entry_card(rendered: RenderedEntry) -> str:
    entry = rendered.entry
    summary_html = f"\n  <p>{escape(rendered.summary_text)}</p>" if rendered.summary_text else ""
    return dedent(
        f"""\
        <a class="story-card" href="{escape(entry.path)}">
          <h3 class="story-title">{escape(rendered.display_title)}</h3>{summary_html}
        </a>
        """
    ).strip()


def render_index_section(group: EntryGroup, rendered_entries: list[RenderedEntry]) -> str:
    if not rendered_entries:
        return ""

    cards = "\n".join(render_entry_card(rendered) for rendered in rendered_entries)
    return dedent(
        f"""\
        <section class="panel section-panel" id="{escape(group.id)}">
          <div class="section-header">
            <h2 class="section-title">{escape(group.label)}</h2>
          </div>
          <div class="story-grid">
            {cards}
          </div>
        </section>
        """
    )


def render_index_page(
    site_title: str,
    manifest: dict,
    rendered_entries: list[RenderedEntry],
) -> str:
    sections = {
        group.id: [rendered for rendered in rendered_entries if rendered.group.id == group.id]
        for group in ENTRY_GROUPS
    }
    section_links = " ".join(
        render_nav_link(group.label, f"#{group.id}")
        for group in ENTRY_GROUPS
        if sections[group.id]
    )
    section_html = "\n".join(
        render_index_section(group, sections[group.id])
        for group in ENTRY_GROUPS
        if sections[group.id]
    )

    body = dedent(
        f"""\
        <main class="site-shell">
          <section class="hero">
            <h1>{escape(manifest["title"])}</h1>
            <div class="jump-row">{section_links}</div>
          </section>

          {section_html}
        </main>
        """
    )
    return render_layout(title=site_title, body_html=body)


def render_nav_link(label: str, href: str | None, *, primary: bool = False) -> str:
    if href is None:
        return f'<span class="nav-placeholder">{escape(label)}</span>'
    class_name = "nav-button primary" if primary else "nav-button secondary"
    return f'<a class="{class_name}" href="{escape(href)}">{escape(label)}</a>'


def render_entry_page(
    site_title: str,
    rendered_entries: list[RenderedEntry],
    index: int,
) -> str:
    rendered = rendered_entries[index]
    previous_rendered = rendered_entries[index - 1] if index > 0 else None
    next_rendered = rendered_entries[index + 1] if index + 1 < len(rendered_entries) else None

    body = dedent(
        f"""\
        <main class="site-shell">
          <header class="site-header">
            <div class="site-title">{escape(site_title)}</div>
          </header>

          <nav class="page-nav" aria-label="Book entry navigation">
            {render_nav_link(previous_rendered.display_title if previous_rendered else "Previous", previous_rendered.entry.path if previous_rendered else None)}
            {render_nav_link("Contents", "index.html", primary=True)}
            {render_nav_link(next_rendered.display_title if next_rendered else "Next", next_rendered.entry.path if next_rendered else None)}
          </nav>

          <article class="article-card">
            {rendered.article_html}
          </article>
        </main>
        """
    )
    page_title = site_title
    if rendered.display_title != site_title:
        page_title = f"{rendered.display_title} — {site_title}"
    return render_layout(title=page_title, body_html=body)


def serialize_omission_audit(
    manifest: dict,
    site_title: str,
    audit_rows: list[AuditRow],
) -> str:
    status_counts = Counter(row.status for row in audit_rows)
    group_rows = []
    for group in ENTRY_GROUPS:
        group_entries = [row for row in audit_rows if row.group.id == group.id]
        if not group_entries:
            continue
        group_rows.append(
            {
                "group_id": group.id,
                "group_label": group.label,
                "entry_count": len(group_entries),
                "rendered_count": sum(1 for row in group_entries if row.status == "rendered"),
            }
        )

    payload = {
        "schema_version": "onward_omission_audit_v1",
        "run_id": manifest.get("run_id"),
        "document_id": manifest.get("document_id"),
        "title": manifest.get("title"),
        "site_title": site_title,
        "manifest_entry_count": len(audit_rows),
        "status_counts": dict(sorted(status_counts.items())),
        "groups": group_rows,
        "entries": [
            {
                "entry_id": row.entry.entry_id,
                "kind": row.entry.kind,
                "title": row.entry.title,
                "group_id": row.group.id,
                "group_label": row.group.label,
                "status": row.status,
                "surface": row.surface,
                "output_path": row.output_path,
                "rationale": row.rationale,
                "source_pages": list(row.entry.source_pages),
                "printed_pages": list(row.entry.printed_pages),
                "printed_page_start": row.entry.printed_page_start,
                "printed_page_end": row.entry.printed_page_end,
            }
            for row in audit_rows
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def build_family_site(
    source_dir: Path,
    output_dir: Path,
    *,
    entry_ids: list[str] | None = None,
    site_title: str = DEFAULT_SITE_TITLE,
) -> BuildResult:
    manifest = load_manifest(source_dir)
    all_entries = [bundle_entry_from_manifest(row) for row in manifest.get("entries", [])]
    selected_entries = select_entries(all_entries, entry_ids)

    ensure_clean_output_dir(output_dir)
    write_text(output_dir / "assets" / "family-site.css", SITE_STYLESHEET + "\n")
    internal_dir = output_dir / "_internal"
    write_text(internal_dir / "source-manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    images_source = source_dir / "images"
    if images_source.exists():
        shutil.copytree(images_source, output_dir / "images", dirs_exist_ok=True)

    provenance_source = source_dir / "provenance" / "blocks.jsonl"
    if provenance_source.exists():
        write_text(internal_dir / "provenance" / "blocks.jsonl", provenance_source.read_text(encoding="utf-8"))

    provenance_rows = load_provenance_rows(source_dir)
    rendered_entries = build_rendered_entries(source_dir, selected_entries)
    audit_rows = build_omission_audit(all_entries, selected_entries)
    omission_audit_path = internal_dir / "omission-audit.json"

    write_text(omission_audit_path, serialize_omission_audit(manifest, site_title, audit_rows))

    for rendered in rendered_entries:
        entry_rows = provenance_rows.get(rendered.entry.entry_id, [])
        write_text(
            internal_dir / "provenance" / "entries" / f"{rendered.entry.entry_id}.json",
            json.dumps(entry_rows, indent=2, sort_keys=True) + "\n",
        )

    for index, rendered in enumerate(rendered_entries):
        write_text(
            output_dir / rendered.entry.path,
            render_entry_page(
                site_title=site_title,
                rendered_entries=rendered_entries,
                index=index,
            ),
        )

    write_text(
        output_dir / "index.html",
        render_index_page(
            site_title=site_title,
            manifest=manifest,
            rendered_entries=rendered_entries,
        ),
    )

    return BuildResult(
        source_dir=source_dir,
        output_dir=output_dir,
        rendered_entry_ids=tuple(rendered.entry.entry_id for rendered in rendered_entries),
        omission_audit_path=omission_audit_path,
    )


def cli_main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Build the local accessible whole-book reading surface from the staged input bundle."
    )
    parser.add_argument("--source", help="Path to the staged input bundle directory containing manifest.json.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for the generated local whole-book reading surface.",
    )
    parser.add_argument(
        "--entry-id",
        action="append",
        dest="entry_ids",
        help="Optional manifest entry id to include. Repeat to build a smaller subset while still auditing every manifest entry.",
    )
    parser.add_argument(
        "--site-title",
        default=DEFAULT_SITE_TITLE,
        help="Display title for the generated reading surface.",
    )
    args = parser.parse_args(argv)

    source_dir = resolve_source_dir(args.source)
    output_dir = Path(args.output).expanduser().resolve()
    result = build_family_site(
        source_dir=source_dir,
        output_dir=output_dir,
        entry_ids=args.entry_ids,
        site_title=args.site_title,
    )
    print(f"Built reading surface from {result.source_dir} into {result.output_dir}")
    print(f"Omission audit: {result.omission_audit_path}")
    print("Rendered entries: " + ", ".join(result.rendered_entry_ids))
    return 0
