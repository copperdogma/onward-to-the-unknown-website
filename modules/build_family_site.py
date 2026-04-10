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

DEFAULT_FAMILY_ENTRY_IDS = [f"chapter-{number:03d}" for number in range(9, 24)]
DEFAULT_OUTPUT_DIR = Path("build/family-site")
DEFAULT_SITE_TITLE = "Onward Family Stories"
SOURCE_ENV_KEYS = ("ONWARD_INPUT_SOURCE_DIR", "DREAMHOST_DEPLOY_SOURCE_DIR")
ARTICLE_PATTERN = re.compile(r"<article>(.*)</article>", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")

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
      --max-width: 72rem;
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

    .eyebrow,
    .meta-kicker {
      font-family: var(--ui-font);
      font-size: 0.85rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent-strong);
    }

    .hero,
    .panel,
    .story-card,
    .article-card,
    .provenance-card {
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
      font-size: clamp(2.2rem, 4vw, 3.6rem);
      margin: 0.35rem 0 0.9rem;
    }

    .lede {
      font-size: 1.12rem;
      max-width: 48rem;
      color: var(--ink);
      margin: 0 0 1rem;
    }

    .hero-note {
      margin: 0;
      font-size: 0.98rem;
      color: var(--muted);
      max-width: 48rem;
    }

    .decision-list,
    .provenance-list,
    .meta-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    .decision-list li,
    .provenance-list li,
    .meta-list li {
      padding: 0.55rem 0;
      border-top: 1px solid rgba(111, 46, 29, 0.12);
    }

    .decision-list li:first-child,
    .provenance-list li:first-child,
    .meta-list li:first-child {
      border-top: none;
      padding-top: 0;
    }

    .story-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
      gap: 1rem;
      margin: 1.5rem 0;
    }

    .story-card {
      display: block;
      text-decoration: none;
      padding: 1.15rem;
      min-height: 16rem;
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
      font-size: 1.4rem;
      margin: 0.35rem 0 0.75rem;
    }

    .story-card p {
      margin: 0.7rem 0 0;
      color: var(--ink);
    }

    .story-meta {
      font-family: var(--ui-font);
      font-size: 0.95rem;
      color: var(--muted);
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
      flex: 1 1 12rem;
      border: 1px solid var(--border);
      background: var(--paper-strong);
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

    .page-layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(18rem, 22rem);
      gap: 1rem;
      align-items: start;
    }

    .article-card,
    .provenance-card {
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

    .article-card .page-meta {
      font-family: var(--ui-font);
      font-size: 0.97rem;
      color: var(--muted);
      margin-bottom: 1rem;
    }

    .provenance-card h2 {
      margin: 0.2rem 0 1rem;
      font-size: 1.2rem;
      font-family: var(--ui-font);
    }

    .provenance-card p {
      margin: 0 0 1rem;
      color: var(--muted);
    }

    .link-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      margin-top: 1rem;
    }

    .inline-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 2.8rem;
      padding: 0.7rem 0.95rem;
      border-radius: 0.85rem;
      border: 1px solid rgba(111, 46, 29, 0.16);
      background: rgba(255, 255, 255, 0.72);
      text-decoration: none;
      font-family: var(--ui-font);
      font-size: 0.98rem;
    }

    .site-footer {
      margin-top: 2rem;
      color: var(--muted);
      font-size: 0.98rem;
    }

    @media (max-width: 54rem) {
      html { font-size: 106.25%; }

      .site-shell {
        width: min(var(--max-width), calc(100% - 1rem));
      }

      .page-layout {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 38rem) {
      html { font-size: 100%; }

      .hero,
      .article-card,
      .provenance-card,
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
    article_html: str
    summary_text: str
    block_counts: dict[str, int]
    provenance_path: str


@dataclass(frozen=True)
class BuildResult:
    source_dir: Path
    output_dir: Path
    rendered_entry_ids: tuple[str, ...]


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


def plain_text_excerpt(article_html: str, limit: int = 220) -> str:
    text = unescape(TAG_PATTERN.sub(" ", article_html))
    text = WHITESPACE_PATTERN.sub(" ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


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


def build_block_counts(provenance_rows: list[dict]) -> dict[str, int]:
    counts = Counter(row["block_kind"] for row in provenance_rows)
    return dict(sorted(counts.items()))


def build_rendered_entries(
    source_dir: Path,
    entries: list[BundleEntry],
    provenance_rows: dict[str, list[dict]],
) -> list[RenderedEntry]:
    rendered: list[RenderedEntry] = []
    for entry in entries:
        document_text = (source_dir / entry.path).read_text(encoding="utf-8")
        article_html = extract_article_html(document_text, source_dir / entry.path)
        rendered.append(
            RenderedEntry(
                entry=entry,
                article_html=article_html,
                summary_text=plain_text_excerpt(article_html),
                block_counts=build_block_counts(provenance_rows.get(entry.entry_id, [])),
                provenance_path=f"provenance/entries/{entry.entry_id}.json",
            )
        )
    return rendered


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


def render_index_page(
    site_title: str,
    manifest: dict,
    rendered_entries: list[RenderedEntry],
) -> str:
    cards: list[str] = []
    for rendered in rendered_entries:
        entry = rendered.entry
        cards.append(
            dedent(
                f"""\
                <a class="story-card" href="{escape(entry.path)}">
                  <div class="eyebrow">Family story</div>
                  <h2 class="story-title">{escape(entry.title)}</h2>
                  <div class="story-meta">
                    {escape(format_range("Printed pages", entry.printed_page_start, entry.printed_page_end))}
                  </div>
                  <p>{escape(rendered.summary_text)}</p>
                  <p class="story-meta">{escape(format_list("Source pages", entry.source_pages))}</p>
                </a>
                """
            ).strip()
        )

    decisions = "\n".join(
        [
            "<li>Each selected family story stays a whole page in this first pass.</li>",
            "<li>The landing page covers the family-story run only, not the front matter or raw image-page sequence.</li>",
            "<li>Every page exposes source-page and provenance cues instead of hiding the bundle lineage.</li>",
            "<li>Navigation and control sizing are tuned for older readers on both desktop and mobile.</li>",
        ]
    )

    body = dedent(
        f"""\
        <main class="site-shell">
          <header class="site-header">
            <div>
              <div class="eyebrow">First local family-site slice</div>
              <strong>{escape(site_title)}</strong>
            </div>
            <div class="meta-kicker">Source run {escape(manifest["run_id"])}</div>
          </header>
          <section class="hero">
            <div class="eyebrow">Archive-first reading surface</div>
            <h1>Family stories, preserved as whole pages.</h1>
            <p class="lede">
              This local slice reshapes the staged export into a more readable family-story run
              without fragmenting the source pages. It starts with the individual family stories
              and leaves the rest of the raw export intact for later stories.
            </p>
            <p class="hero-note">
              Built from <code>manifest.json</code>, chapter HTML, copied images, and raw provenance
              records from the local input bundle. Use this slice to evaluate presentation decisions
              before expanding the rest of the book.
            </p>
          </section>

          <section class="panel" style="padding: 1.3rem; margin-bottom: 1.5rem;">
            <div class="eyebrow">First presentation decisions</div>
            <ul class="decision-list">
              {decisions}
            </ul>
          </section>

          <section class="story-grid">
            {' '.join(cards)}
          </section>

          <footer class="site-footer">
            <p>
              Inspectable source artifacts:
              <a href="source-manifest.json">bundle manifest</a> and
              <a href="provenance/blocks.jsonl">raw provenance JSONL</a>.
            </p>
          </footer>
        </main>
        """
    )
    return render_layout(title=f"{site_title} — Family stories", body_html=body)


def render_block_counts(block_counts: dict[str, int]) -> str:
    if not block_counts:
        return "<li>No per-block provenance rows were found for this entry.</li>"
    items = [
        f"<li>{escape(kind.replace('_', ' ').title())}: {count}</li>"
        for kind, count in block_counts.items()
    ]
    return "".join(items)


def render_nav_link(label: str, href: str | None, *, primary: bool = False) -> str:
    if href is None:
        return f'<span class="nav-placeholder">{escape(label)}</span>'
    class_name = "nav-button primary" if primary else "nav-button secondary"
    return f'<a class="{class_name}" href="{escape(href)}">{escape(label)}</a>'


def render_entry_page(
    site_title: str,
    manifest: dict,
    rendered_entries: list[RenderedEntry],
    index: int,
) -> str:
    rendered = rendered_entries[index]
    entry = rendered.entry
    previous_entry = rendered_entries[index - 1].entry if index > 0 else None
    next_entry = rendered_entries[index + 1].entry if index + 1 < len(rendered_entries) else None

    body = dedent(
        f"""\
        <main class="site-shell">
          <header class="site-header">
            <div>
              <div class="eyebrow">Whole-page family story</div>
              <strong>{escape(site_title)}</strong>
            </div>
            <div class="meta-kicker">{escape(format_range("Printed pages", entry.printed_page_start, entry.printed_page_end))}</div>
          </header>

          <nav class="page-nav" aria-label="Family story navigation">
            {render_nav_link(f"Previous: {previous_entry.title}" if previous_entry else "No previous family story", previous_entry.path if previous_entry else None)}
            {render_nav_link("Back to family landing", "index.html", primary=True)}
            {render_nav_link(f"Next: {next_entry.title}" if next_entry else "No next family story", next_entry.path if next_entry else None)}
          </nav>

          <section class="page-layout">
            <article class="article-card">
              <div class="page-meta">
                {escape(format_list("Source pages", entry.source_pages))}
              </div>
              {rendered.article_html}
            </article>

            <aside class="provenance-card">
              <div class="eyebrow">Where this page came from</div>
              <h2>Visible provenance</h2>
              <p>
                This page keeps the source block ids from the staged export and links back to the
                raw provenance records for inspection.
              </p>
              <ul class="meta-list">
                <li>{escape(format_list("Source pages", entry.source_pages))}</li>
                <li>{escape(format_range("Printed pages", entry.printed_page_start, entry.printed_page_end))}</li>
                <li>Provenance rows: {sum(rendered.block_counts.values())}</li>
              </ul>
              <h2>Block types</h2>
              <ul class="provenance-list">
                {render_block_counts(rendered.block_counts)}
              </ul>
              <div class="link-row">
                <a class="inline-link" href="{escape(rendered.provenance_path)}">Entry provenance JSON</a>
                <a class="inline-link" href="provenance/blocks.jsonl">Raw provenance JSONL</a>
                <a class="inline-link" href="source-manifest.json">Bundle manifest</a>
              </div>
            </aside>
          </section>

          <footer class="site-footer">
            <p>
              Built from source run <strong>{escape(manifest["run_id"])}</strong> and preserved as a whole page
              for this first family-site slice.
            </p>
          </footer>
        </main>
        """
    )
    return render_layout(title=f"{entry.title} — {site_title}", body_html=body)


def build_family_site(
    source_dir: Path,
    output_dir: Path,
    *,
    family_entry_ids: list[str] | None = None,
    site_title: str = DEFAULT_SITE_TITLE,
) -> BuildResult:
    manifest = load_manifest(source_dir)
    all_entries = [bundle_entry_from_manifest(row) for row in manifest.get("entries", [])]
    entries_by_id = {entry.entry_id: entry for entry in all_entries}
    selected_ids = family_entry_ids or list(DEFAULT_FAMILY_ENTRY_IDS)

    selected_entries: list[BundleEntry] = []
    for entry_id in selected_ids:
        entry = entries_by_id.get(entry_id)
        if entry is None:
            raise SystemExit(f"Manifest does not contain requested entry id: {entry_id}")
        if entry.kind != "chapter":
            raise SystemExit(f"Requested family entry is not a chapter: {entry_id}")
        selected_entries.append(entry)

    ensure_clean_output_dir(output_dir)
    write_text(output_dir / "assets" / "family-site.css", SITE_STYLESHEET + "\n")
    write_text(output_dir / "source-manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    images_source = source_dir / "images"
    if images_source.exists():
        shutil.copytree(images_source, output_dir / "images", dirs_exist_ok=True)

    provenance_source = source_dir / "provenance" / "blocks.jsonl"
    if provenance_source.exists():
        write_text(output_dir / "provenance" / "blocks.jsonl", provenance_source.read_text(encoding="utf-8"))

    provenance_rows = load_provenance_rows(source_dir)
    rendered_entries = build_rendered_entries(source_dir, selected_entries, provenance_rows)

    for rendered in rendered_entries:
        entry_rows = provenance_rows.get(rendered.entry.entry_id, [])
        write_text(
            output_dir / rendered.provenance_path,
            json.dumps(entry_rows, indent=2, sort_keys=True) + "\n",
        )
        write_text(
            output_dir / rendered.entry.path,
            render_entry_page(site_title=site_title, manifest=manifest, rendered_entries=rendered_entries, index=rendered_entries.index(rendered)),
        )

    write_text(output_dir / "index.html", render_index_page(site_title=site_title, manifest=manifest, rendered_entries=rendered_entries))

    return BuildResult(
        source_dir=source_dir,
        output_dir=output_dir,
        rendered_entry_ids=tuple(rendered.entry.entry_id for rendered in rendered_entries),
    )


def cli_main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Build the first local accessible family-site slice from the staged input bundle."
    )
    parser.add_argument("--source", help="Path to the staged input bundle directory containing manifest.json.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for the generated local family-site slice.",
    )
    parser.add_argument(
        "--entry-id",
        action="append",
        dest="entry_ids",
        help="Optional manifest chapter entry id to include. Repeat to override the default family sequence.",
    )
    parser.add_argument(
        "--site-title",
        default=DEFAULT_SITE_TITLE,
        help="Display title for the generated family-site slice.",
    )
    args = parser.parse_args(argv)

    source_dir = resolve_source_dir(args.source)
    output_dir = Path(args.output).expanduser().resolve()
    result = build_family_site(
        source_dir=source_dir,
        output_dir=output_dir,
        family_entry_ids=args.entry_ids,
        site_title=args.site_title,
    )
    print(f"Built family-site slice from {result.source_dir} into {result.output_dir}")
    print("Rendered entries: " + ", ".join(result.rendered_entry_ids))
    return 0
