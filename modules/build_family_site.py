from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from html import escape, unescape
from pathlib import Path
from textwrap import dedent
from urllib.parse import quote, urlsplit
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = REPO_ROOT / "input" / "doc-web-html" / "story206-onward-proof-r10"
SUPPLEMENT_REGISTRY_PATH = REPO_ROOT / "input" / "doc-web-html" / "family-story-supplements.json"
DEFAULT_FAMILY_ENTRY_IDS = frozenset(f"chapter-{number:03d}" for number in range(9, 24))
DEFAULT_OUTPUT_DIR = Path("build/family-site")
DEFAULT_SITE_TITLE = "Onward to the Unknown"
DEFAULT_BOOK_PAGE_PATH = "book.html"
DEFAULT_AUDIOBOOK_MANIFEST_PATH = REPO_ROOT / "audiobook" / "manifest.json"
DEFAULT_AUDIOBOOK_PAGE_PATH = "audiobook.html"
DEFAULT_PODCAST_MANIFEST_PATH = REPO_ROOT / "podcast" / "manifest.json"
DEFAULT_PODCAST_PAGE_PATH = "podcast.html"
DEFAULT_PODCAST_FEED_PATH = "podcast/feed.xml"
DEFAULT_SOURCE_LIBRARY_PAGE_PATH = "archive-sources.html"
AUDIOBOOK_PUBLIC_ROOT = "audiobook"
PODCAST_PUBLIC_ROOT = "podcast"
SOURCE_LIBRARY_PUBLIC_ROOT = "source-files"
SOURCE_ENV_KEYS = ("ONWARD_INPUT_SOURCE_DIR", "DREAMHOST_DEPLOY_SOURCE_DIR")
FFPROBE_BIN = shutil.which("ffprobe")
ARTICLE_PATTERN = re.compile(r"<article>(.*?)</article>", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
H1_PATTERN = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
H2_PATTERN = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.IGNORECASE | re.DOTALL)
FIGCAPTION_PATTERN = re.compile(r"<figcaption\b[^>]*>(.*?)</figcaption>", re.IGNORECASE | re.DOTALL)
PARAGRAPH_PATTERN = re.compile(r"<p\b[^>]*>(.*?)</p>", re.IGNORECASE | re.DOTALL)
TABLE_PATTERN = re.compile(r"<table\b[^>]*>.*?</table>", re.IGNORECASE | re.DOTALL)
PRIMARY_HEADING_PATTERN = re.compile(r"(<h1\b[^>]*>)(.*?)(</h1>)", re.IGNORECASE | re.DOTALL)
IMG_TAG_PATTERN = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
IMG_ALT_PATTERN = re.compile(r"<img\b[^>]*\balt=(?:\"([^\"]+)\"|'([^']+)')", re.IGNORECASE)
FIGURE_PATTERN = re.compile(r"<figure\b[^>]*>.*?</figure>", re.IGNORECASE | re.DOTALL)
FIGCAPTION_BLOCK_PATTERN = re.compile(r"<figcaption\b[^>]*>.*?</figcaption>", re.IGNORECASE | re.DOTALL)
ARTICLE_BLOCK_PATTERN = re.compile(
    r"<(?:h1|h2|h3|p|figure|table)\b[^>]*>.*?</(?:h1|h2|h3|p|figure|table)>",
    re.IGNORECASE | re.DOTALL,
)
PLACEHOLDER_PAGE_TITLE_PATTERN = re.compile(r"^(?:Image \d+|Page [ivxlcdm]+)$", re.IGNORECASE)
ROMAN_NUMERAL_PATTERN = re.compile(r"^[ivxlcdm]+$", re.IGNORECASE)
RECIPE_BLOCK_PATTERN = re.compile(
    r'(<p id="blk-chapter-005-0031">.*?</p>\s*<h3 id="blk-chapter-005-0032".*?<p id="blk-chapter-005-0038">.*?</p>)',
    re.DOTALL,
)
CROP_FILENAME_PATTERN = re.compile(r"page-(\d+)-\d+\.[A-Za-z0-9]+", re.IGNORECASE)
ID_ATTR_PATTERN = re.compile(r'\bid=(?:"([^"]*)"|\'([^\']*)\')', re.IGNORECASE)
URL_ATTR_PATTERN = re.compile(
    r'(?P<attr>\b(?:src|href))=(?:"(?P<double>[^"]*)"|\'(?P<single>[^\']*)\')',
    re.IGNORECASE,
)
LANDING_CARD_SUMMARY_LIMIT = 140
SHORT_LABEL_MAX_LENGTH = 88
TITLE_CASE_SMALL_WORDS = frozenset(
    {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to"}
)
PUBLISHABLE_SOURCE_SUFFIX_LABELS = {
    ".pdf": "PDF document",
    ".jpg": "Image scan",
    ".jpeg": "Image scan",
    ".png": "Image scan",
}
FEATURED_BOOK_SOURCE_FILENAME = "Onward to the Unknown.pdf"
PHOTOCOPY_SECTION_NOTE = (
    "These documents were found as photocopies inside one copy of Onward to the Unknown "
    "and relate to the reunion or the family history in some way."
)
SPECIAL_SOURCE_TITLE_OVERRIDES = {
    FEATURED_BOOK_SOURCE_FILENAME: "Onward to the Unknown",
    "Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf": "Rolland Alain Memoir Family Story",
}
SPECIAL_SOURCE_SUMMARY_OVERRIDES = {
    FEATURED_BOOK_SOURCE_FILENAME: (
        "A complete scanned PDF of Onward to the Unknown, the reunion history book that anchors the website."
    ),
    "Dictionnaire généalogique des familles du Québec 1983.pdf": (
        "A Quebec genealogical dictionary used as a reference for French-Canadian family lines."
    ),
    "Founding of Doremey SK.pdf": (
        "A scanned newspaper article in which an early resident recounts the founding of the village of Doremy, Saskatchewan."
    ),
    "L'HEUREUX FAMILY DIRECTORY June, 1987.pdf": (
        "A June 1987 contact directory listing L'Heureux family households and addresses."
    ),
    "LE GRAND ARRANGEMENT DES ACADIENS AU QUÉBEC NOTES DE PETITE-HISTOIRE GÉNÉALOGIES FRANCE • ACADIE • QUÉBEC de 1625 à 1925.pdf": (
        "A genealogical and local-history volume tracing Acadian families in France, Acadia, and Quebec from 1625 to 1925."
    ),
    "Memoires of Rolland Alaln fron blrth 1913 to 71st year 1985.pdf": (
        "Rolland Alain's 1985 memoir recounting his life from his 1913 birth through age 71."
    ),
    "Jackfish-Lake-Fishing-Guide.jpg": (
        "A hand-drawn map-style fishing guide to Jackfish Lake showing camps, landmarks, and points of interest."
    ),
}
GENEALOGY_TABLE_HEADERS = ("NAME", "BORN", "MARRIED", "SPOUSE", "BOY", "GIRL", "DIED")
FIGURE_EMBLEM_KEYWORDS = frozenset({"logo", "seal"})
FIGURE_SIGNATURE_KEYWORDS = frozenset({"signature"})
FIGURE_ILLUSTRATION_KEYWORDS = frozenset({"illustration", "line drawing"})
CHAPTER_024_PHOTO_TITLES = {
    121: "Family Gathering and Ranch Stallion",
    122: "1939 Reunion and Family Portraits",
    123: "Sophie L'Heureux's Funeral and Church Move",
    124: "Joe L'Heureux and the Hereford Bull",
    125: "Covered Wagon Illustration",
    126: "L'Heureux Veterans Plaques",
    127: "Monument and Post Office Plaque",
}
MERGED_ENTRY_TARGETS = {
    "page-002": "page-001",
}
HOME_ICON_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M3.75 10.5 12 3.75l8.25 6.75v9a.75.75 0 0 1-.75.75H14.25V15a.75.75 0 0 0-.75-.75h-3A.75.75 0 0 0 9.75 15v5.25H4.5a.75.75 0 0 1-.75-.75v-9Z" fill="currentColor"/>'
    "</svg>"
)
BOOK_ICON_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M6.75 4.5A2.25 2.25 0 0 0 4.5 6.75v10.5a2.25 2.25 0 0 0 2.25 2.25h10.5a.75.75 0 0 0 .75-.75V6.75A2.25 2.25 0 0 0 15.75 4.5H6.75Zm0 1.5h9a.75.75 0 0 1 .75.75v9.818a2.24 2.24 0 0 0-.75-.123h-9A.75.75 0 0 1 6 15.75v-9A.75.75 0 0 1 6.75 6Zm0 11.95h9c.26 0 .515.043.75.123v.177h-9.75a.75.75 0 1 1 0-1.5Z" fill="currentColor"/>'
    "</svg>"
)
AUDIOBOOK_ICON_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M12 4.5a6.75 6.75 0 0 0-6.75 6.75v4.5a2.25 2.25 0 0 0 2.25 2.25h.75a.75.75 0 0 0 .75-.75v-4.5a.75.75 0 0 0-.75-.75H6.75v-.75a5.25 5.25 0 1 1 10.5 0V12h-1.5a.75.75 0 0 0-.75.75v4.5a.75.75 0 0 0 .75.75h.75A2.25 2.25 0 0 0 18.75 15.75v-4.5A6.75 6.75 0 0 0 12 4.5Z" fill="currentColor"/>'
    '<path d="M9.75 18.75a.75.75 0 0 0 0 1.5h4.5a.75.75 0 0 0 0-1.5h-4.5Z" fill="currentColor"/>'
    "</svg>"
)
PODCAST_ICON_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M12 3.75a4.5 4.5 0 0 0-4.5 4.5v3.75a4.5 4.5 0 1 0 9 0V8.25a4.5 4.5 0 0 0-4.5-4.5Zm0 1.5A3 3 0 0 1 15 8.25v3.75a3 3 0 1 1-6 0V8.25a3 3 0 0 1 3-3Z" fill="currentColor"/>'
    '<path d="M5.25 11.25a.75.75 0 0 0-1.5 0 8.25 8.25 0 0 0 7.5 8.213V21a.75.75 0 0 0 1.5 0v-1.537a8.25 8.25 0 0 0 7.5-8.213.75.75 0 0 0-1.5 0 6.75 6.75 0 1 1-13.5 0Z" fill="currentColor"/>'
    "</svg>"
)
ARCHIVE_ICON_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M4.5 6.75A2.25 2.25 0 0 1 6.75 4.5h10.5a2.25 2.25 0 0 1 2.25 2.25v1.5H4.5v-1.5Zm0 3h15v7.5a2.25 2.25 0 0 1-2.25 2.25H6.75A2.25 2.25 0 0 1 4.5 17.25v-7.5Zm4.5 2.25a.75.75 0 0 0 0 1.5h6a.75.75 0 0 0 0-1.5H9Z" fill="currentColor"/>'
    "</svg>"
)
DOWNLOAD_ICON_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M12.75 4.5a.75.75 0 0 0-1.5 0v8.19L8.78 10.22a.75.75 0 1 0-1.06 1.06l3.75 3.75a.75.75 0 0 0 1.06 0l3.75-3.75a.75.75 0 1 0-1.06-1.06l-2.47 2.47V4.5Z" fill="currentColor"/>'
    '<path d="M5.25 15.75a.75.75 0 0 0-.75.75v1.5A2.25 2.25 0 0 0 6.75 20.25h10.5A2.25 2.25 0 0 0 19.5 18v-1.5a.75.75 0 0 0-1.5 0V18a.75.75 0 0 1-.75.75H6.75A.75.75 0 0 1 6 18v-1.5a.75.75 0 0 0-.75-.75Z" fill="currentColor"/>'
    "</svg>"
)
ATOM_XML_NAMESPACE = "http://www.w3.org/2005/Atom"
CONTENT_XML_NAMESPACE = "http://purl.org/rss/1.0/modules/content/"
ITUNES_XML_NAMESPACE = "http://www.itunes.com/dtds/podcast-1.0.dtd"
ASCII_PUBLIC_PATH_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
PODCAST_SHOW_COVER_MIN_PIXELS = 1400
PODCAST_SHOW_COVER_MAX_PIXELS = 3000
JPEG_SOF_MARKERS = frozenset({0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF})
AI_ICON_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M12 3.75a.75.75 0 0 1 .731.582l.555 2.426a2.25 2.25 0 0 0 1.706 1.706l2.426.555a.75.75 0 0 1 0 1.462l-2.426.555a2.25 2.25 0 0 0-1.706 1.706l-.555 2.426a.75.75 0 0 1-1.462 0l-.555-2.426a2.25 2.25 0 0 0-1.706-1.706l-2.426-.555a.75.75 0 0 1 0-1.462l2.426-.555a2.25 2.25 0 0 0 1.706-1.706l.555-2.426A.75.75 0 0 1 12 3.75Z" fill="currentColor"/>'
    '<path d="M18.75 14.25a.75.75 0 0 1 .718.533l.26.868a1.5 1.5 0 0 0 .997.997l.868.26a.75.75 0 0 1 0 1.436l-.868.26a1.5 1.5 0 0 0-.997.997l-.26.868a.75.75 0 0 1-1.436 0l-.26-.868a1.5 1.5 0 0 0-.997-.997l-.868-.26a.75.75 0 0 1 0-1.436l.868-.26a1.5 1.5 0 0 0 .997-.997l.26-.868a.75.75 0 0 1 .718-.533Z" fill="currentColor"/>'
    '<circle cx="6" cy="18" r="1.125" fill="currentColor"/>'
    "</svg>"
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

    .site-title-link {
      text-decoration: none;
    }

    .site-title-link:hover,
    .site-title-link:focus-visible {
      text-decoration: underline;
    }

    .site-menu {
      display: flex;
      flex-wrap: wrap;
      gap: 0.55rem;
      justify-content: flex-end;
      align-items: center;
    }

    .site-menu-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 2.4rem;
      padding: 0.5rem 0.9rem;
      border-radius: 999px;
      font-family: var(--ui-font);
      font-size: 0.94rem;
      line-height: 1.2;
      text-decoration: none;
      color: var(--ink);
      border: 1px solid rgba(111, 46, 29, 0.14);
      background: rgba(255, 255, 255, 0.68);
    }

    .site-menu-link-content {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
    }

    .site-menu-link-icon {
      width: 1.1rem;
      height: 1.1rem;
      flex: 0 0 auto;
      color: currentColor;
    }

    .site-menu-link:hover,
    .site-menu-link:focus-visible {
      border-color: rgba(111, 46, 29, 0.3);
      background: rgba(255, 255, 255, 0.84);
      outline: none;
    }

    .site-menu-link.is-current {
      color: #fff8f0;
      border-color: transparent;
      background: var(--accent);
    }

    .section-title {
      font-size: clamp(1.4rem, 3vw, 1.9rem);
      margin: 0;
    }

    .section-title-row {
      display: inline-flex;
      align-items: center;
      gap: 0.55rem;
      min-width: 0;
    }

    .section-title-icon {
      width: 2.8rem;
      height: 2.8rem;
      flex: 0 0 auto;
      color: var(--accent-strong);
      opacity: 0.88;
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

    .home-hero h1 {
      font-size: clamp(2.8rem, 4.8vw, 4.2rem);
      max-width: 13ch;
    }

    .home-hero {
      position: relative;
      overflow: hidden;
      background:
        radial-gradient(circle at top right, rgba(193, 131, 76, 0.16), transparent 26%),
        radial-gradient(circle at left 18%, rgba(111, 46, 29, 0.08), transparent 32%),
        linear-gradient(180deg, rgba(255, 251, 245, 0.98), rgba(247, 239, 229, 0.98));
    }

    .home-hero-grid {
      display: grid;
      gap: 1.25rem;
      align-items: end;
    }

    .home-hero-copy {
      min-width: 0;
    }

    .home-hero-copy .audio-kicker,
    .home-hero-aside .audio-kicker {
      margin-bottom: 0.7rem;
    }

    .home-hero-summary {
      max-width: 38rem;
      margin: 1rem 0 0;
      font-size: clamp(1.08rem, 2vw, 1.28rem);
      color: var(--ink);
    }

    .home-hero-aside {
      padding: 1rem 1.05rem;
      border-radius: 1rem;
      border: 1px solid rgba(111, 46, 29, 0.16);
      background:
        radial-gradient(circle at top right, rgba(255, 255, 255, 0.42), transparent 34%),
        linear-gradient(180deg, rgba(252, 246, 239, 0.98), rgba(243, 231, 214, 0.92));
    }

    .home-hero-stat-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0.7rem;
      margin-top: 0.2rem;
    }

    .home-hero-stat {
      padding: 0.75rem 0.8rem;
      border-radius: 0.9rem;
      background: rgba(255, 255, 255, 0.68);
      border: 1px solid rgba(111, 46, 29, 0.12);
    }

    .home-hero-stat-value {
      display: block;
      font-family: var(--ui-font);
      font-size: 1.45rem;
      font-weight: 700;
      line-height: 1;
      color: var(--accent);
    }

    .home-hero-stat-label {
      display: block;
      margin-top: 0.35rem;
      font-family: var(--ui-font);
      font-size: 0.88rem;
      line-height: 1.35;
      color: var(--muted);
    }

    .home-hero-note {
      margin: 0.9rem 0 0;
      font-size: 0.98rem;
      color: var(--muted);
    }

    .home-feature-grid {
      display: grid;
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .home-feature-grid > .section-panel {
      margin-bottom: 0;
    }

    .home-feature-grid > :only-child {
      grid-column: 1 / -1;
    }

    .audio-hero h1 {
      font-size: clamp(2.3rem, 4.1vw, 3.7rem);
      max-width: none;
    }

    .section-panel {
      padding: 1.3rem;
      margin-bottom: 1.5rem;
    }

    .section-header {
      margin-bottom: 1rem;
    }

    .audio-kicker {
      margin: 0 0 0.45rem;
      font-family: var(--ui-font);
      font-size: 0.88rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent-strong);
    }

    .kicker-row {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      min-width: 0;
    }

    .kicker-icon {
      width: 1.1rem;
      height: 1.1rem;
      flex: 0 0 auto;
      color: var(--accent-strong);
      opacity: 0.88;
    }

    .audio-summary,
    .audio-note,
    .audio-runtime {
      max-width: 48rem;
      margin: 0 0 1rem;
    }

    .audio-note {
      color: var(--muted);
      font-size: 0.96rem;
    }

    .audio-attribution {
      display: inline-flex;
      align-items: flex-start;
      gap: 0.55rem;
      max-width: 42rem;
    }

    .audio-attribution-icon {
      width: 1rem;
      height: 1rem;
      flex: 0 0 auto;
      margin-top: 0.18rem;
      color: var(--accent-strong);
      opacity: 0.9;
    }

    .audio-attribution a {
      color: var(--accent);
      font-family: var(--ui-font);
      font-weight: 600;
    }

    .audio-runtime {
      margin: 0.3rem 0 0;
      font-family: var(--ui-font);
      font-size: 0.92rem;
      color: var(--muted);
    }

    .audio-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 1rem;
    }

    .audio-actions .nav-button,
    .audio-actions .nav-placeholder {
      flex: 1 1 12rem;
    }

    .audio-player {
      width: 100%;
      margin-top: 0.55rem;
    }

    .entry-audio-panel,
    .audio-track-card,
    .source-card {
      padding: 1.3rem;
      margin-bottom: 1.2rem;
    }

    .entry-audio-grid {
      display: grid;
      gap: 0.8rem;
      margin-bottom: 1.1rem;
    }

    .entry-audio-grid.has-single {
      max-width: 34rem;
    }

    .entry-audio-panel {
      padding: 0;
      margin-bottom: 0;
      overflow: hidden;
    }

    .entry-audio-summary {
      cursor: pointer;
      padding: 0.95rem 1rem;
      list-style-position: inside;
    }

    .entry-audio-summary-copy {
      display: grid;
      gap: 0.16rem;
      min-width: 0;
    }

    .entry-audio-summary-label {
      font-family: var(--ui-font);
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent-strong);
    }

    .entry-audio-summary-title {
      font-family: var(--ui-font);
      font-size: 1.02rem;
      line-height: 1.25;
      color: var(--ink);
    }

    .entry-audio-summary-meta {
      font-size: 0.92rem;
      color: var(--muted);
    }

    .entry-audio-panel[open] .entry-audio-summary {
      border-bottom: 1px solid rgba(111, 46, 29, 0.12);
      background: rgba(255, 255, 255, 0.45);
    }

    .entry-audio-panel-body {
      padding: 0.95rem 1rem 1rem;
    }

    .audio-hero,
    .audio-feature-card,
    .audio-section,
    .audiobook-overview,
    .source-hero,
    .source-overview,
    .source-section {
      margin-bottom: 1.5rem;
    }

    .audiobook-overview,
    .source-overview {
      display: flex;
      flex-direction: column;
      height: 100%;
    }

    .audiobook-overview .audio-summary,
    .source-overview .audio-summary {
      max-width: none;
    }

    .audiobook-overview .audio-actions,
    .source-overview .audio-actions {
      margin-top: auto;
      padding-top: 1rem;
    }

    .audio-track-grid,
    .source-library-grid {
      display: grid;
      gap: 1rem;
    }

    .audio-track-card {
      margin-bottom: 0;
      padding: 0.9rem 1rem;
      display: grid;
      gap: 0.75rem;
      align-items: center;
    }

    .audio-track-copy {
      min-width: 0;
    }

    .audio-track-copy .audio-kicker {
      margin-bottom: 0.25rem;
      font-size: 0.82rem;
    }

    .audio-track-copy .section-title {
      font-size: clamp(1.18rem, 2.1vw, 1.45rem);
      margin: 0;
    }

    .audio-track-copy .audio-runtime {
      margin-top: 0.3rem;
      margin-bottom: 0;
    }

    .audio-track-copy .audio-note {
      margin: 0.35rem 0 0;
      font-size: 0.92rem;
    }

    .audio-track-card .audio-player {
      margin-top: 0;
      min-width: 0;
    }

    .audio-track-card .audio-actions {
      gap: 0.45rem;
      margin-top: 0;
    }

    .audio-track-card .nav-button,
    .audio-track-card .nav-placeholder {
      flex: 0 0 auto;
      min-height: 2.5rem;
      padding: 0.55rem 0.85rem;
      font-size: 0.92rem;
    }

    .audio-track-card .nav-button-content {
      gap: 0.35rem;
    }

    .audio-track-card .nav-button-icon {
      width: 1rem;
      height: 1rem;
    }

    .source-card.featured {
      border-color: rgba(111, 46, 29, 0.26);
      background:
        radial-gradient(circle at top right, rgba(255, 255, 255, 0.42), transparent 32%),
        linear-gradient(180deg, rgba(252, 246, 239, 0.98), rgba(243, 231, 214, 0.92));
    }

    .source-meta {
      margin: 0.35rem 0 0;
      font-family: var(--ui-font);
      font-size: 0.96rem;
      color: var(--muted);
      overflow-wrap: anywhere;
    }

    .source-meta code {
      font-size: 0.9em;
    }

    .source-hero .source-page-title {
      font-size: clamp(2rem, 4vw, 3rem);
      margin: 0 0 0.85rem;
    }

    .source-section-note {
      max-width: 48rem;
      margin: 0 0 1rem;
      color: var(--muted);
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

    .story-card.has-thumbnail {
      padding: 0.9rem;
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

    .story-card.has-thumbnail .story-title {
      margin-top: 0;
    }

    .story-card p {
      margin: 0.7rem 0 0;
      color: var(--ink);
      overflow-wrap: anywhere;
    }

    .story-card-media {
      margin: 0 0 0.9rem;
      aspect-ratio: 5 / 4;
      overflow: hidden;
      border-radius: 0.9rem;
      border: 1px solid rgba(111, 46, 29, 0.14);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(246, 237, 225, 0.92));
    }

    .story-card-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
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

    .nav-button-content {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.55rem;
      min-width: 0;
    }

    .nav-button-icon {
      width: 1.1rem;
      height: 1.1rem;
      flex: 0 0 auto;
    }

    .nav-button-label {
      min-width: 0;
    }

    .nav-placeholder {
      color: var(--muted);
      background: rgba(255, 255, 255, 0.4);
    }

    .home-button {
      flex: 0 0 auto;
      width: var(--hit-target);
      padding: 0;
    }

    .home-button svg {
      width: 1.35rem;
      height: 1.35rem;
    }

    .article-card {
      padding: 1.4rem;
    }

    .article-card::after {
      content: "";
      display: block;
      clear: both;
    }

    .article-card h1 {
      font-size: clamp(2.1rem, 4vw, 3.2rem);
      margin: 0 0 1rem;
    }

    .article-heading-row {
      display: inline-flex;
      align-items: flex-start;
      gap: 0.65rem;
      min-width: 0;
    }

    .article-heading-icon {
      width: 1.8rem;
      height: 1.8rem;
      flex: 0 0 auto;
      color: var(--accent-strong);
      opacity: 0.88;
      transform: translateY(0.14em);
    }

    .article-heading-text {
      min-width: 0;
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
      width: min(100%, 46rem);
      margin: 1.5rem 0;
      padding: 0.9rem;
      border-radius: 0.85rem;
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(246, 237, 225, 0.92));
      border: 1px solid rgba(111, 46, 29, 0.14);
      display: grid;
      gap: 0.85rem;
      justify-items: center;
      margin-inline: auto;
    }

    .article-card figure.figure-gallery {
      width: min(100%, 58rem);
    }

    .article-card figure.figure-emblem {
      width: min(100%, 16rem);
      padding: 0.7rem;
    }

    .article-card figure.figure-signature {
      width: min(100%, 24rem);
      padding: 0.7rem;
    }

    .article-card figure.figure-illustration {
      width: min(100%, 34rem);
    }

    .article-card .figure-image-link {
      display: block;
      width: fit-content;
      max-width: 100%;
      color: inherit;
    }

    .article-card .figure-image-link img {
      max-width: 100%;
      width: auto;
      max-height: 34rem;
      margin: 0 auto;
      border-radius: 0.6rem;
      box-shadow: 0 12px 28px rgba(71, 48, 26, 0.1);
    }

    .article-card figure.figure-emblem .figure-image-link img {
      max-height: 13rem;
    }

    .article-card figure.figure-signature .figure-image-link img {
      max-height: 7rem;
      box-shadow: none;
    }

    .article-card .figure-image-grid {
      width: 100%;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
      gap: 0.75rem;
      align-items: start;
    }

    .article-card .figure-image-grid .figure-image-link {
      width: 100%;
    }

    .article-card .figure-image-grid .figure-image-link img {
      width: 100%;
      height: 18rem;
      object-fit: cover;
    }

    .article-card .figure-missing {
      width: 100%;
      padding: 1rem;
      border-radius: 0.7rem;
      border: 1px dashed rgba(111, 46, 29, 0.28);
      background: rgba(255, 255, 255, 0.72);
      font-family: var(--ui-font);
      font-size: 0.92rem;
      color: var(--muted);
      text-align: center;
    }

    .article-card .figure-orphaned-caption {
      margin: 0.25rem auto 1rem;
      max-width: 28rem;
      font-family: var(--ui-font);
      font-size: 0.95rem;
      color: var(--muted);
      text-align: center;
    }

    .article-card figcaption {
      width: 100%;
      margin-top: 0;
      font-family: var(--ui-font);
      font-size: 0.95rem;
      color: var(--muted);
    }

    .article-card figcaption > :last-child {
      margin-bottom: 0;
    }

    .article-card.entry-chapter-001 h1,
    .article-card.entry-chapter-001 h2,
    .article-card.entry-chapter-003 h1,
    .article-card.entry-chapter-003 p {
      text-align: center;
    }

    .article-card.entry-chapter-024 h1 {
      text-align: center;
    }

    .article-card.entry-chapter-024 p {
      max-width: 28rem;
      margin-left: auto;
      margin-right: auto;
      text-align: left;
    }

    .article-card.entry-page-004,
    .article-card.entry-page-006,
    .article-card.entry-page-008 {
      text-align: center;
    }

    .article-card.entry-page-004 p,
    .article-card.entry-page-006 p {
      max-width: 34rem;
      margin-left: auto;
      margin-right: auto;
    }

    .article-card.entry-page-008 .clean-index-list {
      list-style: none;
      padding: 0;
      margin: 1.4rem auto;
      max-width: 36rem;
      display: grid;
      gap: 0.55rem;
    }

    .article-card.entry-page-008 .clean-index-list li {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 0.85rem;
      align-items: baseline;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid rgba(111, 46, 29, 0.12);
      text-align: left;
      font-family: var(--ui-font);
    }

    .article-card.entry-page-008 table.summary-index-table {
      width: min(100%, 44rem);
      margin-left: auto;
      margin-right: auto;
      display: table;
      overflow: visible;
      table-layout: fixed;
    }

    .article-card.entry-page-008 table.summary-index-table td,
    .article-card.entry-page-008 table.summary-index-table th {
      text-align: left;
    }

    @media (min-width: 62rem) {
      .article-card figure.figure-inline {
        float: right;
        width: min(42%, 24rem);
        margin: 0.35rem 0 1.25rem 1.25rem;
      }
    }

    .article-card.entry-chapter-001 table.ancestry-table {
      width: min(100%, 48rem);
      margin: 1.4rem auto 0;
      display: table;
      overflow: visible;
      background: transparent;
      border-radius: 0;
    }

    .article-card.entry-chapter-001 tr:nth-child(even) td {
      background: transparent;
    }

    .article-card.entry-chapter-001 td,
    .article-card.entry-chapter-001 th {
      border: none;
      padding: 0.28rem 0.7rem;
      text-align: center;
      vertical-align: bottom;
    }

    .article-card.entry-chapter-001 tr.ancestry-final-row td {
      text-align: center;
    }

    .article-card.entry-chapter-003 p {
      max-width: 40rem;
      margin-left: auto;
      margin-right: auto;
    }

    .article-card.entry-chapter-003 figure.figure-emblem,
    .article-card.entry-chapter-003 figure.figure-signature {
      background: transparent;
      border-color: rgba(111, 46, 29, 0.08);
      box-shadow: none;
    }

    .article-card .appendix-note {
      font-family: var(--ui-font);
      font-size: 0.98rem;
      line-height: 1.55;
      color: var(--muted);
    }

    .article-card .supplement-intro {
      margin-bottom: 1.8rem;
      padding: 1.15rem 1.2rem;
      border-radius: 1rem;
      border: 1px solid rgba(111, 46, 29, 0.16);
      background:
        radial-gradient(circle at top right, rgba(255, 255, 255, 0.42), transparent 30%),
        linear-gradient(180deg, rgba(252, 246, 239, 0.98), rgba(243, 231, 214, 0.92));
    }

    .article-card .supplement-kicker {
      font-family: var(--ui-font);
      color: var(--muted);
    }

    .article-card .supplement-kicker {
      margin-bottom: 0.45rem;
      font-size: 0.92rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .article-card .supplement-preamble {
      max-width: 40rem;
      font-size: 1.02rem;
    }

    .article-card .supplement-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin: 1.1rem 0 0.6rem;
    }

    .article-card .supplement-source-title {
      margin-top: 0;
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

    .article-card table.genealogy-table {
      display: table;
      overflow: visible;
      table-layout: fixed;
    }

    .article-card table.genealogy-table th,
    .article-card table.genealogy-table td {
      overflow-wrap: anywhere;
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

    .article-card table.genealogy-table thead th {
      position: sticky;
      top: 0;
      z-index: 2;
      background: rgba(255, 251, 245, 0.97);
      box-shadow: inset 0 -1px 0 rgba(111, 46, 29, 0.18);
    }

    .article-card table.genealogy-table tr.genealogy-subgroup-heading th {
      position: static;
      background: rgba(111, 46, 29, 0.12);
    }

    .article-card tr:nth-child(even) td {
      background: rgba(255, 255, 255, 0.35);
    }

    .recipe-callout {
      margin: 2rem 0;
      padding: 1.3rem 1.4rem;
      border-radius: 1rem;
      border: 1px solid rgba(111, 46, 29, 0.18);
      border-left: 0.4rem solid var(--accent);
      background:
        radial-gradient(circle at top right, rgba(255, 255, 255, 0.44), transparent 30%),
        linear-gradient(180deg, rgba(253, 246, 236, 0.98), rgba(244, 228, 203, 0.92));
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
    }

    .recipe-callout > p:first-child {
      font-family: var(--ui-font);
      font-size: 1rem;
      line-height: 1.55;
      color: var(--muted);
    }

    .recipe-callout h3,
    .recipe-callout p strong {
      color: var(--ink);
    }

    .recipe-callout h3 {
      font-size: clamp(1.3rem, 2.8vw, 1.8rem);
      margin-top: 1rem;
      margin-bottom: 0.8rem;
    }

    .recipe-callout p:last-child {
      margin-bottom: 0;
    }

    @media (max-width: 54rem) {
      html { font-size: 106.25%; }

      .site-shell {
        width: min(var(--max-width), calc(100% - 1rem));
      }

      .site-header {
        align-items: flex-start;
      }

      .site-menu {
        justify-content: flex-start;
      }

      .article-card table.genealogy-table th,
      .article-card table.genealogy-table td {
        padding: 0.65rem 0.55rem;
        font-size: 0.92rem;
      }

      .article-card figure {
        width: min(100%, 40rem);
      }

      .article-card .figure-image-link img {
        max-height: 24rem;
      }

      .article-card figure.figure-signature {
        width: min(100%, 20rem);
      }
    }

    @media (min-width: 56rem) {
      .home-hero-grid {
        grid-template-columns: minmax(0, 1.55fr) minmax(18rem, 0.95fr);
      }

      .home-feature-grid {
        grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
      }

      .audio-track-grid {
        grid-template-columns: 1fr;
      }

      .audio-track-card {
        grid-template-columns: minmax(0, 1.5fr) minmax(18rem, 1.1fr) auto;
      }

      .entry-audio-grid.has-multiple {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .audio-hero h1 {
        white-space: nowrap;
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

      .site-menu-link {
        flex: 1 1 9rem;
      }

      .article-card figure,
      .article-card figure.figure-gallery,
      .article-card figure.figure-illustration {
        width: 100%;
      }

      .article-card .figure-image-grid {
        grid-template-columns: 1fr;
      }

      .article-card .figure-image-grid .figure-image-link img {
        height: auto;
        max-height: 20rem;
      }
    }
    """
).strip()
SITE_STYLESHEET_HREF = (
    f"assets/family-site.css?v={hashlib.sha256((SITE_STYLESHEET + chr(10)).encode('utf-8')).hexdigest()[:12]}"
)


@dataclass(frozen=True)
class EntryGroup:
    id: str
    label: str
    rendered_rationale: str


ENTRY_GROUPS = (
    EntryGroup(
        id="opening-pages",
        label="Opening Pages",
        rendered_rationale="Rendered as part of the opening material and early context in the local reading surface.",
    ),
    EntryGroup(
        id="family-stories",
        label="Family Stories",
        rendered_rationale="Rendered as a whole-page family story inside the local reading surface.",
    ),
    EntryGroup(
        id="closing-archive",
        label="Closing Archive",
        rendered_rationale="Rendered as part of the closing material or archive appendix in the local reading surface.",
    ),
)
ENTRY_GROUPS_BY_ID = {group.id: group for group in ENTRY_GROUPS}
SECTION_ICON_SVG_BY_ID = {
    "opening-pages": BOOK_ICON_SVG,
    "family-stories": BOOK_ICON_SVG,
    "closing-archive": BOOK_ICON_SVG,
}


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
    thumbnail_src: str | None
    thumbnail_alt: str | None
    source_entry_ids: tuple[str, ...]
    block_ids: tuple[str, ...]
    provenance_rows: tuple[dict[str, object], ...]


@dataclass(frozen=True)
class EntryFragment:
    entry: BundleEntry
    raw_article_html: str
    source_entry_ids: tuple[str, ...]
    block_ids: tuple[str, ...]


@dataclass(frozen=True)
class FamilyStorySupplement:
    supplement_id: str
    title: str
    output_path: str
    bundle_dir: Path
    source_pdf: Path
    group: EntryGroup
    insert_after_entry_id: str | None
    source_entry_ids: tuple[str, ...]
    absorbed_entry_ids: tuple[str, ...]
    preamble: str


@dataclass(frozen=True)
class SupplementAuditRow:
    supplement_id: str
    title: str
    group: EntryGroup
    status: str
    output_path: str
    bundle_root: str
    source_pdf_path: str
    source_entry_ids: tuple[str, ...]
    absorbed_entry_ids: tuple[str, ...]
    rationale: str


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


@dataclass(frozen=True)
class PublishedSourceAsset:
    source_path: Path
    relative_input_path: str
    public_output_path: str
    title: str
    filename: str
    kind_label: str
    summary_text: str
    size_bytes: int
    featured: bool


@dataclass(frozen=True)
class AudiobookTrack:
    track_number: int
    title: str
    audio_source_path: Path
    audio_output_path: str
    script_source_path: Path
    script_manifest_path: str
    target_entry_id: str | None
    notes: str | None
    duration_seconds: float | None


@dataclass(frozen=True)
class FullAudiobookAsset:
    title: str
    audio_source_path: Path
    audio_output_path: str
    silence_between_tracks_seconds: float
    notes: str | None
    is_available: bool
    duration_seconds: float | None


@dataclass(frozen=True)
class AudiobookCatalog:
    title: str
    manifest_path: Path
    tracks: tuple[AudiobookTrack, ...]
    full_audiobook: FullAudiobookAsset | None


@dataclass(frozen=True)
class PodcastCategory:
    name: str
    subcategory: str | None


@dataclass(frozen=True)
class PodcastFeedMetadata:
    description: str
    subtitle: str | None
    site_url: str
    page_path: str
    feed_path: str
    categories: tuple[PodcastCategory, ...]
    public_contact_email: str
    author_name: str
    owner_name: str
    language: str
    artwork_source_path: Path
    artwork_manifest_path: str
    artwork_output_path: str
    apple_podcasts_url: str | None
    spotify_url: str | None


@dataclass(frozen=True)
class PodcastEpisode:
    episode_number: int
    title: str
    audio_source_path: Path
    audio_output_path: str
    source_path: Path
    source_manifest_path: str
    target_entry_id: str | None
    notes: str | None
    summary: str
    published_at: date
    duration_seconds: float | None


@dataclass(frozen=True)
class FullBookPodcastEpisode:
    title: str
    audio_source_path: Path
    audio_output_path: str
    source_path: Path
    source_manifest_path: str
    notes: str | None
    summary: str
    published_at: date
    duration_seconds: float | None


@dataclass(frozen=True)
class PodcastCatalog:
    title: str
    manifest_path: Path
    prompt_source_path: Path
    prompt_manifest_path: str
    feed: PodcastFeedMetadata
    episodes: tuple[PodcastEpisode, ...]
    full_book_episode: FullBookPodcastEpisode | None


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


def parse_non_empty_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"Podcast manifest `{field_name}` must be a non-empty string.")
    return value.strip()


def parse_optional_string(value: object, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise SystemExit(f"Podcast manifest `{field_name}` must be a string when present.")
    normalized = value.strip()
    return normalized or None


def parse_iso_date(value: object, field_name: str) -> date:
    normalized = parse_non_empty_string(value, field_name)
    try:
        return date.fromisoformat(normalized)
    except ValueError as exc:
        raise SystemExit(f"Podcast manifest `{field_name}` must use YYYY-MM-DD.") from exc


def validate_absolute_url(value: object, field_name: str) -> str:
    normalized = parse_non_empty_string(value, field_name)
    parsed = urlsplit(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SystemExit(f"Podcast manifest `{field_name}` must be an absolute http(s) URL.")
    return normalized.rstrip("/")


def normalize_public_path(value: object, field_name: str) -> str:
    normalized = parse_non_empty_string(value, field_name).lstrip("/")
    parsed = urlsplit(normalized)
    if parsed.scheme or parsed.netloc:
        raise SystemExit(f"Podcast manifest `{field_name}` must be a site-relative output path.")
    return normalized


def validate_ascii_public_path(
    value: object,
    field_name: str,
    *,
    required_prefix: str | None = None,
) -> str:
    normalized = normalize_public_path(value, field_name)
    segments = normalized.split("/")
    if any(not ASCII_PUBLIC_PATH_SEGMENT_PATTERN.fullmatch(segment) for segment in segments):
        raise SystemExit(
            f"Podcast manifest `{field_name}` must use stable ASCII-only path segments "
            "with letters, numbers, dots, underscores, or hyphens."
        )
    if required_prefix and not (
        normalized == required_prefix or normalized.startswith(f"{required_prefix}/")
    ):
        raise SystemExit(f"Podcast manifest `{field_name}` must stay within `{required_prefix}/`.")
    return normalized


def parse_podcast_categories(value: object) -> tuple[PodcastCategory, ...]:
    if not isinstance(value, list) or not value:
        raise SystemExit("Podcast manifest `categories` must be a non-empty array.")

    categories: list[PodcastCategory] = []
    for index, item in enumerate(value):
        if isinstance(item, str):
            name = parse_non_empty_string(item, f"categories[{index}]")
            subcategory = None
        elif isinstance(item, dict):
            name = parse_non_empty_string(item.get("name"), f"categories[{index}].name")
            subcategory = parse_optional_string(
                item.get("subcategory"),
                f"categories[{index}].subcategory",
            )
        else:
            raise SystemExit(
                f"Podcast manifest `categories[{index}]` must be a string or object."
            )
        categories.append(PodcastCategory(name=name, subcategory=subcategory))

    return tuple(categories)


def probe_png_dimensions(image_path: Path) -> tuple[int, int] | None:
    try:
        with image_path.open("rb") as handle:
            header = handle.read(24)
    except OSError:
        return None
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def probe_jpeg_dimensions(image_path: Path) -> tuple[int, int] | None:
    try:
        with image_path.open("rb") as handle:
            data = handle.read()
    except OSError:
        return None
    if not data.startswith(b"\xff\xd8"):
        return None

    offset = 2
    data_length = len(data)
    while offset + 9 < data_length:
        if data[offset] != 0xFF:
            offset += 1
            continue
        marker = data[offset + 1]
        offset += 2
        if marker == 0xD9:
            break
        if marker in {0xD8, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if offset + 2 > data_length:
            break
        segment_length = int.from_bytes(data[offset : offset + 2], "big")
        if segment_length < 2 or offset + segment_length > data_length:
            break
        if marker in JPEG_SOF_MARKERS:
            if offset + 7 > data_length:
                break
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            return width, height
        offset += segment_length
    return None


def probe_raster_image_dimensions(image_path: Path) -> tuple[int, int] | None:
    suffix = image_path.suffix.lower()
    if suffix == ".png":
        return probe_png_dimensions(image_path)
    if suffix in {".jpg", ".jpeg"}:
        return probe_jpeg_dimensions(image_path)
    return None


def validate_podcast_show_cover_artwork(image_path: Path) -> tuple[int, int]:
    dimensions = probe_raster_image_dimensions(image_path)
    if dimensions is None:
        raise SystemExit(
            "Podcast manifest `artwork_path` must point to a readable PNG or JPEG show-cover asset."
        )
    width, height = dimensions
    if width != height:
        raise SystemExit(
            "Podcast manifest `artwork_path` must point to square show-cover artwork for podcast directories."
        )
    if not (PODCAST_SHOW_COVER_MIN_PIXELS <= width <= PODCAST_SHOW_COVER_MAX_PIXELS):
        raise SystemExit(
            "Podcast manifest `artwork_path` must be between 1400x1400 and 3000x3000 pixels."
        )
    return width, height


def parse_optional_duration_seconds(value: object, field_name: str) -> float | None:
    if value is None:
        return None
    if not isinstance(value, (int, float)) or float(value) < 0:
        raise SystemExit(f"Audiobook manifest `{field_name}` must be a number >= 0 when present.")
    return float(value)


def probe_audio_duration_seconds(audio_path: Path) -> float | None:
    if not FFPROBE_BIN or not audio_path.exists():
        return None
    result = subprocess.run(
        [
            str(FFPROBE_BIN),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        duration_seconds = float(result.stdout.strip())
    except ValueError:
        return None
    if duration_seconds < 0:
        return None
    return duration_seconds


def resolve_audio_duration_seconds(audio_path: Path, configured_duration_seconds: float | None) -> float | None:
    if configured_duration_seconds is not None:
        return configured_duration_seconds
    return probe_audio_duration_seconds(audio_path)


def load_audiobook_catalog(manifest_path: Path | None = DEFAULT_AUDIOBOOK_MANIFEST_PATH) -> AudiobookCatalog | None:
    if manifest_path is None:
        return None

    resolved_manifest_path = Path(manifest_path).expanduser().resolve()
    if not resolved_manifest_path.exists():
        return None

    payload = json.loads(resolved_manifest_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "onward_audiobook_manifest_v1":
        raise SystemExit("Audiobook manifest must use schema_version `onward_audiobook_manifest_v1`.")

    title = payload.get("title")
    if not isinstance(title, str) or not title.strip():
        raise SystemExit("Audiobook manifest requires a non-empty `title` string.")

    full_audiobook_payload = payload.get("full_audiobook")
    full_audiobook: FullAudiobookAsset | None = None
    if full_audiobook_payload is not None:
        if not isinstance(full_audiobook_payload, dict):
            raise SystemExit("Audiobook manifest `full_audiobook` must be an object when present.")
        full_title = full_audiobook_payload.get("title")
        full_audio_path = full_audiobook_payload.get("audio_path")
        full_silence_seconds = full_audiobook_payload.get("silence_between_tracks_seconds", 4)
        full_duration_seconds = parse_optional_duration_seconds(
            full_audiobook_payload.get("duration_seconds"),
            "full_audiobook.duration_seconds",
        )
        full_notes = full_audiobook_payload.get("notes")
        if not isinstance(full_title, str) or not full_title.strip():
            raise SystemExit("Audiobook manifest `full_audiobook.title` must be a non-empty string.")
        if not isinstance(full_audio_path, str) or not full_audio_path.strip():
            raise SystemExit("Audiobook manifest `full_audiobook.audio_path` must be a non-empty string.")
        if not isinstance(full_silence_seconds, (int, float)) or float(full_silence_seconds) < 0:
            raise SystemExit(
                "Audiobook manifest `full_audiobook.silence_between_tracks_seconds` must be a number >= 0."
            )
        if full_notes is not None and not isinstance(full_notes, str):
            raise SystemExit("Audiobook manifest `full_audiobook.notes` must be a string when present.")
        resolved_full_audio_path = (resolved_manifest_path.parent / full_audio_path).resolve()
        full_audiobook = FullAudiobookAsset(
            title=full_title.strip(),
            audio_source_path=resolved_full_audio_path,
            audio_output_path=f"{AUDIOBOOK_PUBLIC_ROOT}/{Path(full_audio_path).as_posix()}",
            silence_between_tracks_seconds=float(full_silence_seconds),
            notes=full_notes.strip() if isinstance(full_notes, str) and full_notes.strip() else None,
            is_available=resolved_full_audio_path.exists(),
            duration_seconds=resolve_audio_duration_seconds(resolved_full_audio_path, full_duration_seconds),
        )

    tracks_payload = payload.get("tracks")
    if not isinstance(tracks_payload, list) or not tracks_payload:
        raise SystemExit("Audiobook manifest requires a non-empty `tracks` array.")

    tracks: list[AudiobookTrack] = []
    seen_track_numbers: set[int] = set()
    seen_target_entry_ids: set[str] = set()

    for raw_track in tracks_payload:
        if not isinstance(raw_track, dict):
            raise SystemExit("Every audiobook manifest track must be an object.")

        track_number = raw_track.get("track_number")
        title_value = raw_track.get("title")
        audio_path = raw_track.get("audio_path")
        script_path = raw_track.get("script_path")
        target_entry_id = raw_track.get("target_entry_id")
        notes = raw_track.get("notes")
        duration_seconds = parse_optional_duration_seconds(
            raw_track.get("duration_seconds"),
            f"tracks[{track_number}].duration_seconds" if isinstance(track_number, int) else "tracks[].duration_seconds",
        )

        if not isinstance(track_number, int) or track_number < 1:
            raise SystemExit("Audiobook tracks require an integer `track_number` greater than 0.")
        if track_number in seen_track_numbers:
            raise SystemExit(f"Duplicate audiobook track number: {track_number}")
        if not isinstance(title_value, str) or not title_value.strip():
            raise SystemExit(f"Audiobook track {track_number} requires a non-empty `title`.")
        if not isinstance(audio_path, str) or not audio_path.strip():
            raise SystemExit(f"Audiobook track {track_number} requires a non-empty `audio_path`.")
        if not isinstance(script_path, str) or not script_path.strip():
            raise SystemExit(f"Audiobook track {track_number} requires a non-empty `script_path`.")
        if target_entry_id is not None and not isinstance(target_entry_id, str):
            raise SystemExit(f"Audiobook track {track_number} has an invalid `target_entry_id`.")
        if notes is not None and not isinstance(notes, str):
            raise SystemExit(f"Audiobook track {track_number} has an invalid `notes` value.")

        resolved_audio_path = (resolved_manifest_path.parent / audio_path).resolve()
        resolved_script_path = (resolved_manifest_path.parent / script_path).resolve()
        if not resolved_audio_path.exists():
            raise SystemExit(f"Audiobook audio file not found for track {track_number}: {resolved_audio_path}")
        if not resolved_script_path.exists():
            raise SystemExit(f"Audiobook script file not found for track {track_number}: {resolved_script_path}")

        normalized_target_entry_id = target_entry_id.strip() if isinstance(target_entry_id, str) else None
        if normalized_target_entry_id:
            if normalized_target_entry_id in seen_target_entry_ids:
                raise SystemExit(f"Duplicate audiobook target_entry_id: {normalized_target_entry_id}")
            seen_target_entry_ids.add(normalized_target_entry_id)

        seen_track_numbers.add(track_number)
        tracks.append(
            AudiobookTrack(
                track_number=track_number,
                title=title_value.strip(),
                audio_source_path=resolved_audio_path,
                audio_output_path=f"{AUDIOBOOK_PUBLIC_ROOT}/{Path(audio_path).as_posix()}",
                script_source_path=resolved_script_path,
                script_manifest_path=Path(script_path).as_posix(),
                target_entry_id=normalized_target_entry_id or None,
                notes=notes.strip() if isinstance(notes, str) and notes.strip() else None,
                duration_seconds=resolve_audio_duration_seconds(resolved_audio_path, duration_seconds),
            )
        )

    ordered_tracks = sorted(tracks, key=lambda track: track.track_number)
    if [track.track_number for track in ordered_tracks] != [track.track_number for track in tracks]:
        raise SystemExit("Audiobook manifest tracks must already be listed in listening order.")

    return AudiobookCatalog(
        title=title.strip(),
        manifest_path=resolved_manifest_path,
        tracks=tuple(ordered_tracks),
        full_audiobook=full_audiobook,
    )


def load_podcast_catalog(manifest_path: Path | None = DEFAULT_PODCAST_MANIFEST_PATH) -> PodcastCatalog | None:
    if manifest_path is None:
        return None

    resolved_manifest_path = Path(manifest_path).expanduser().resolve()
    if not resolved_manifest_path.exists():
        return None

    payload = json.loads(resolved_manifest_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "onward_podcast_manifest_v1":
        raise SystemExit("Podcast manifest must use schema_version `onward_podcast_manifest_v1`.")

    title = parse_non_empty_string(payload.get("title"), "title")
    prompt_path = parse_non_empty_string(payload.get("prompt_path"), "prompt_path")
    description = parse_non_empty_string(payload.get("description"), "description")
    subtitle = parse_optional_string(payload.get("subtitle"), "subtitle")
    site_url = validate_absolute_url(payload.get("site_url"), "site_url")
    page_path = validate_ascii_public_path(
        payload.get("page_path", DEFAULT_PODCAST_PAGE_PATH),
        "page_path",
    )
    if page_path != DEFAULT_PODCAST_PAGE_PATH:
        raise SystemExit(
            f"Podcast manifest `page_path` must currently remain `{DEFAULT_PODCAST_PAGE_PATH}`."
        )
    feed_path = validate_ascii_public_path(
        payload.get("feed_path", DEFAULT_PODCAST_FEED_PATH),
        "feed_path",
        required_prefix=PODCAST_PUBLIC_ROOT,
    )
    categories = parse_podcast_categories(payload.get("categories"))
    public_contact_email = parse_non_empty_string(payload.get("public_contact_email"), "public_contact_email")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", public_contact_email):
        raise SystemExit("Podcast manifest `public_contact_email` must look like an email address.")
    author_name = parse_optional_string(payload.get("author_name"), "author_name") or title
    owner_name = parse_optional_string(payload.get("owner_name"), "owner_name") or author_name
    language = parse_optional_string(payload.get("language"), "language") or "en-CA"
    artwork_path = parse_non_empty_string(payload.get("artwork_path"), "artwork_path")
    artwork_output_path = validate_ascii_public_path(
        payload.get("artwork_output_path", f"{PODCAST_PUBLIC_ROOT}/{Path(artwork_path).name}"),
        "artwork_output_path",
        required_prefix=PODCAST_PUBLIC_ROOT,
    )
    apple_podcasts_url = parse_optional_string(payload.get("apple_podcasts_url"), "apple_podcasts_url")
    if apple_podcasts_url is not None:
        apple_podcasts_url = validate_absolute_url(apple_podcasts_url, "apple_podcasts_url")
    spotify_url = parse_optional_string(payload.get("spotify_url"), "spotify_url")
    if spotify_url is not None:
        spotify_url = validate_absolute_url(spotify_url, "spotify_url")

    resolved_prompt_path = (resolved_manifest_path.parent / prompt_path).resolve()
    if not resolved_prompt_path.exists():
        raise SystemExit(f"Podcast prompt file not found: {resolved_prompt_path}")
    resolved_artwork_path = (resolved_manifest_path.parent / artwork_path).resolve()
    if not resolved_artwork_path.exists():
        raise SystemExit(f"Podcast artwork file not found: {resolved_artwork_path}")
    validate_podcast_show_cover_artwork(resolved_artwork_path)

    feed = PodcastFeedMetadata(
        description=description,
        subtitle=subtitle,
        site_url=site_url,
        page_path=page_path,
        feed_path=feed_path,
        categories=categories,
        public_contact_email=public_contact_email,
        author_name=author_name,
        owner_name=owner_name,
        language=language,
        artwork_source_path=resolved_artwork_path,
        artwork_manifest_path=Path(artwork_path).as_posix(),
        artwork_output_path=artwork_output_path,
        apple_podcasts_url=apple_podcasts_url,
        spotify_url=spotify_url,
    )

    full_book_payload = payload.get("full_book_episode")
    full_book_episode: FullBookPodcastEpisode | None = None
    if full_book_payload is not None:
        if not isinstance(full_book_payload, dict):
            raise SystemExit("Podcast manifest `full_book_episode` must be an object when present.")
        full_title = full_book_payload.get("title")
        full_audio_path = full_book_payload.get("audio_path")
        full_source_path = full_book_payload.get("source_path")
        full_notes = full_book_payload.get("notes")
        full_summary = parse_optional_string(full_book_payload.get("summary"), "full_book_episode.summary")
        full_published_at = parse_iso_date(full_book_payload.get("published_at"), "full_book_episode.published_at")
        full_public_audio_path = validate_ascii_public_path(
            full_book_payload.get("public_audio_path"),
            "full_book_episode.public_audio_path",
            required_prefix=PODCAST_PUBLIC_ROOT,
        )
        full_duration_seconds = parse_optional_duration_seconds(
            full_book_payload.get("duration_seconds"),
            "full_book_episode.duration_seconds",
        )
        if not isinstance(full_title, str) or not full_title.strip():
            raise SystemExit("Podcast manifest `full_book_episode.title` must be a non-empty string.")
        if not isinstance(full_audio_path, str) or not full_audio_path.strip():
            raise SystemExit("Podcast manifest `full_book_episode.audio_path` must be a non-empty string.")
        if not isinstance(full_source_path, str) or not full_source_path.strip():
            raise SystemExit("Podcast manifest `full_book_episode.source_path` must be a non-empty string.")
        if full_notes is not None and not isinstance(full_notes, str):
            raise SystemExit("Podcast manifest `full_book_episode.notes` must be a string when present.")
        resolved_full_audio_path = (resolved_manifest_path.parent / full_audio_path).resolve()
        resolved_full_source_path = (resolved_manifest_path.parent / full_source_path).resolve()
        if not resolved_full_audio_path.exists():
            raise SystemExit(f"Podcast audio file not found for full-book episode: {resolved_full_audio_path}")
        if not resolved_full_source_path.exists():
            raise SystemExit(f"Podcast source path not found for full-book episode: {resolved_full_source_path}")
        full_book_episode = FullBookPodcastEpisode(
            title=full_title.strip(),
            audio_source_path=resolved_full_audio_path,
            audio_output_path=full_public_audio_path,
            source_path=resolved_full_source_path,
            source_manifest_path=Path(full_source_path).as_posix(),
            notes=full_notes.strip() if isinstance(full_notes, str) and full_notes.strip() else None,
            summary=full_summary
            or (
                full_notes.strip()
                if isinstance(full_notes, str) and full_notes.strip()
                else f"Whole-book companion episode for {title}."
            ),
            published_at=full_published_at,
            duration_seconds=resolve_audio_duration_seconds(resolved_full_audio_path, full_duration_seconds),
        )

    episodes_payload = payload.get("episodes")
    if not isinstance(episodes_payload, list) or not episodes_payload:
        raise SystemExit("Podcast manifest requires a non-empty `episodes` array.")

    episodes: list[PodcastEpisode] = []
    seen_episode_numbers: set[int] = set()
    seen_target_entry_ids: set[str] = set()
    for raw_episode in episodes_payload:
        if not isinstance(raw_episode, dict):
            raise SystemExit("Every podcast manifest episode must be an object.")

        episode_number = raw_episode.get("episode_number")
        title_value = raw_episode.get("title")
        audio_path = raw_episode.get("audio_path")
        source_path = raw_episode.get("source_path")
        target_entry_id = raw_episode.get("target_entry_id")
        notes = raw_episode.get("notes")
        summary = parse_optional_string(
            raw_episode.get("summary"),
            (
                f"episodes[{episode_number}].summary"
                if isinstance(episode_number, int)
                else "episodes[].summary"
            ),
        )
        public_audio_path = validate_ascii_public_path(
            raw_episode.get("public_audio_path"),
            (
                f"episodes[{episode_number}].public_audio_path"
                if isinstance(episode_number, int)
                else "episodes[].public_audio_path"
            ),
            required_prefix=PODCAST_PUBLIC_ROOT,
        )
        published_at = parse_iso_date(
            raw_episode.get("published_at"),
            (
                f"episodes[{episode_number}].published_at"
                if isinstance(episode_number, int)
                else "episodes[].published_at"
            ),
        )
        duration_seconds = parse_optional_duration_seconds(
            raw_episode.get("duration_seconds"),
            (
                f"episodes[{episode_number}].duration_seconds"
                if isinstance(episode_number, int)
                else "episodes[].duration_seconds"
            ),
        )

        if not isinstance(episode_number, int) or episode_number < 1:
            raise SystemExit("Podcast episodes require an integer `episode_number` greater than 0.")
        if episode_number in seen_episode_numbers:
            raise SystemExit(f"Duplicate podcast episode number: {episode_number}")
        if not isinstance(title_value, str) or not title_value.strip():
            raise SystemExit(f"Podcast episode {episode_number} requires a non-empty `title`.")
        if not isinstance(audio_path, str) or not audio_path.strip():
            raise SystemExit(f"Podcast episode {episode_number} requires a non-empty `audio_path`.")
        if not isinstance(source_path, str) or not source_path.strip():
            raise SystemExit(f"Podcast episode {episode_number} requires a non-empty `source_path`.")
        if target_entry_id is not None and not isinstance(target_entry_id, str):
            raise SystemExit(f"Podcast episode {episode_number} has an invalid `target_entry_id`.")
        if notes is not None and not isinstance(notes, str):
            raise SystemExit(f"Podcast episode {episode_number} has an invalid `notes` value.")

        resolved_audio_path = (resolved_manifest_path.parent / audio_path).resolve()
        resolved_source_path = (resolved_manifest_path.parent / source_path).resolve()
        if not resolved_audio_path.exists():
            raise SystemExit(f"Podcast audio file not found for episode {episode_number}: {resolved_audio_path}")
        if not resolved_source_path.exists():
            raise SystemExit(f"Podcast source path not found for episode {episode_number}: {resolved_source_path}")

        normalized_target_entry_id = target_entry_id.strip() if isinstance(target_entry_id, str) else None
        if normalized_target_entry_id:
            if normalized_target_entry_id in seen_target_entry_ids:
                raise SystemExit(f"Duplicate podcast target_entry_id: {normalized_target_entry_id}")
            seen_target_entry_ids.add(normalized_target_entry_id)

        seen_episode_numbers.add(episode_number)
        episodes.append(
            PodcastEpisode(
                episode_number=episode_number,
                title=title_value.strip(),
                audio_source_path=resolved_audio_path,
                audio_output_path=public_audio_path,
                source_path=resolved_source_path,
                source_manifest_path=Path(source_path).as_posix(),
                target_entry_id=normalized_target_entry_id or None,
                notes=notes.strip() if isinstance(notes, str) and notes.strip() else None,
                summary=summary
                or (
                    notes.strip()
                    if isinstance(notes, str) and notes.strip()
                    else f"Companion podcast episode for {title_value.strip()}."
                ),
                published_at=published_at,
                duration_seconds=resolve_audio_duration_seconds(resolved_audio_path, duration_seconds),
            )
        )

    ordered_episodes = sorted(episodes, key=lambda episode: episode.episode_number)
    if [episode.episode_number for episode in ordered_episodes] != [episode.episode_number for episode in episodes]:
        raise SystemExit("Podcast manifest episodes must already be listed in listening order.")

    return PodcastCatalog(
        title=title.strip(),
        manifest_path=resolved_manifest_path,
        prompt_source_path=resolved_prompt_path,
        prompt_manifest_path=Path(prompt_path).as_posix(),
        feed=feed,
        episodes=tuple(ordered_episodes),
        full_book_episode=full_book_episode,
    )


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


def normalize_merge_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    without_marks = "".join(character for character in normalized if not unicodedata.combining(character))
    collapsed = WHITESPACE_PATTERN.sub(" ", without_marks).strip()
    return collapsed.casefold()


def attribute_value(attributes: str, attribute: str) -> str | None:
    pattern = re.compile(rf'\b{re.escape(attribute)}=(?:"([^"]*)"|\'([^\']*)\')', re.IGNORECASE)
    match = pattern.search(attributes)
    if not match:
        return None
    return unescape(match.group(1) or match.group(2) or "").strip() or None


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


def title_case_word(word: str, *, is_first: bool, is_last: bool) -> str:
    prefix_match = re.match(r"^\W*", word)
    suffix_match = re.search(r"\W*$", word)
    prefix = prefix_match.group(0) if prefix_match else ""
    suffix = suffix_match.group(0) if suffix_match else ""
    core_end = len(word) - len(suffix) if suffix else len(word)
    core = word[len(prefix) : core_end]
    if not core:
        return word

    core_lower = core.lower()
    if ROMAN_NUMERAL_PATTERN.fullmatch(core):
        transformed = core.upper()
    elif not is_first and not is_last and core_lower in TITLE_CASE_SMALL_WORDS:
        transformed = core_lower
    else:
        transformed = core_lower.title()
    return prefix + transformed + suffix


def soften_display_title(text: str) -> str:
    normalized = WHITESPACE_PATTERN.sub(" ", text).strip()
    if not normalized or not is_mostly_uppercase(normalized):
        return normalized

    words = normalized.split()
    softened = [
        title_case_word(word, is_first=index == 0, is_last=index == len(words) - 1)
        for index, word in enumerate(words)
    ]
    return " ".join(softened)


def derive_display_title(entry: BundleEntry, article_html: str) -> str:
    normalized_title = soften_display_title(entry.title)
    if entry.kind != "page" or not PLACEHOLDER_PAGE_TITLE_PATTERN.fullmatch(entry.title.strip()):
        return normalized_title

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
    return normalized_title


def add_class_to_tag(opening_tag: str, class_name: str) -> str:
    class_pattern = re.compile(r'\bclass=(?:"([^"]*)"|\'([^\']*)\')', re.IGNORECASE)
    match = class_pattern.search(opening_tag)
    if match:
        existing = match.group(1) or match.group(2) or ""
        classes = existing.split()
        if class_name in classes:
            return opening_tag
        updated = " ".join([*classes, class_name]).strip()
        quote = '"' if match.group(1) is not None else "'"
        replacement = f'class={quote}{updated}{quote}'
        return opening_tag[: match.start()] + replacement + opening_tag[match.end() :]
    closing = "/>" if opening_tag.endswith("/>") else ">"
    return opening_tag[: -len(closing)] + f' class="{class_name}"{closing}'


def set_attribute_on_tag(opening_tag: str, attribute: str, value: str) -> str:
    pattern = re.compile(rf'\b{re.escape(attribute)}=(?:"[^"]*"|\'[^\']*\')', re.IGNORECASE)
    replacement = f'{attribute}="{escape(value, quote=True)}"'
    match = pattern.search(opening_tag)
    if match:
        return opening_tag[: match.start()] + replacement + opening_tag[match.end() :]
    closing = "/>" if opening_tag.endswith("/>") else ">"
    return opening_tag[: -len(closing)] + f" {replacement}{closing}"


def extract_block_ids(html_fragment: str) -> tuple[str, ...]:
    block_ids: list[str] = []
    for match in ID_ATTR_PATTERN.finditer(html_fragment):
        block_id = match.group(1) or match.group(2) or ""
        if block_id.startswith("blk-"):
            block_ids.append(block_id)
    return tuple(block_ids)


def first_source_page_from_html(html_fragment: str) -> int | None:
    match = CROP_FILENAME_PATTERN.search(html_fragment)
    if not match:
        return None
    return int(match.group(1))


def article_blocks(article_html: str) -> list[str]:
    blocks = [match.group(0).strip() for match in ARTICLE_BLOCK_PATTERN.finditer(article_html)]
    if blocks:
        return blocks
    stripped = article_html.strip()
    return [stripped] if stripped else []


def block_merge_signature(block_html: str) -> str | None:
    image_sources = [
        src
        for image_match in IMG_TAG_PATTERN.finditer(block_html)
        if (src := attribute_value(image_match.group(1), "src"))
    ]
    caption = plain_text_from_html(FIGCAPTION_BLOCK_PATTERN.search(block_html).group(0)) if FIGCAPTION_BLOCK_PATTERN.search(block_html) else ""
    if image_sources:
        signature_parts = ["image", *image_sources]
        if caption:
            signature_parts.append(normalize_merge_text(caption))
        return "|".join(signature_parts)

    text = normalize_merge_text(plain_text_from_html(block_html))
    if not text:
        return None
    return f"text|{text}"


def merge_absorbed_article_html(
    primary_article_html: str,
    absorbed_articles: list[tuple[BundleEntry, str]],
) -> str:
    if not absorbed_articles:
        return primary_article_html

    seen_signatures = {
        signature
        for block_html in article_blocks(primary_article_html)
        if (signature := block_merge_signature(block_html))
    }
    merged_blocks = article_blocks(primary_article_html)
    absorbed_ids: list[str] = []
    for absorbed_entry, absorbed_html in absorbed_articles:
        absorbed_ids.append(absorbed_entry.entry_id)
        for block_html in article_blocks(absorbed_html):
            signature = block_merge_signature(block_html)
            if signature and signature in seen_signatures:
                continue
            if signature:
                seen_signatures.add(signature)
            merged_blocks.append(block_html)

    merged_comment = f"<!-- merged-entry-ids: {', '.join(absorbed_ids)} -->"
    return merged_comment + "\n" + "\n".join(merged_blocks)


def source_page_title(entry: BundleEntry, source_page: int) -> str:
    title = CHAPTER_024_PHOTO_TITLES.get(source_page)
    if title:
        return title
    return f"Archive Photos {source_page}"


def printed_page_for_source(entry: BundleEntry, source_page: int) -> int | None:
    if entry.printed_page_start is None or not entry.source_pages:
        return None
    return entry.printed_page_start + (source_page - entry.source_pages[0])


def split_chapter_024_fragments(
    entry: BundleEntry,
    article_html: str,
    *,
    source_entry_ids: tuple[str, ...],
) -> list[EntryFragment]:
    figure_matches = list(FIGURE_PATTERN.finditer(article_html))
    if not figure_matches:
        return [
            EntryFragment(
                entry=entry,
                raw_article_html=article_html,
                source_entry_ids=source_entry_ids,
                block_ids=extract_block_ids(article_html),
            )
        ]

    first_figure = figure_matches[0]
    poem_html = article_html[: first_figure.start()].strip()
    fragments = [
        EntryFragment(
            entry=entry,
            raw_article_html=poem_html,
            source_entry_ids=source_entry_ids,
            block_ids=extract_block_ids(poem_html),
        )
    ]

    grouped_figures: list[tuple[int, list[str], list[str]]] = []
    current_page: int | None = None
    for match in figure_matches:
        figure_html = match.group(0)
        source_page = first_source_page_from_html(figure_html) or current_page
        if source_page is None:
            continue
        current_page = source_page
        if grouped_figures and grouped_figures[-1][0] == source_page:
            grouped_figures[-1][1].append(figure_html)
            grouped_figures[-1][2].extend(extract_block_ids(figure_html))
        else:
            grouped_figures.append((source_page, [figure_html], list(extract_block_ids(figure_html))))

    for offset, (source_page, figure_htmls, block_ids) in enumerate(grouped_figures, start=1):
        printed_page = printed_page_for_source(entry, source_page)
        synthetic_entry = BundleEntry(
            entry_id=f"page-photo-{source_page}",
            kind="page",
            title=source_page_title(entry, source_page),
            path=f"page-photo-{source_page}.html",
            order=entry.order * 100 + offset,
            prev_entry_id=None,
            next_entry_id=None,
            source_pages=(source_page,),
            printed_pages=(printed_page,) if printed_page is not None else (),
            printed_page_start=printed_page,
            printed_page_end=printed_page,
        )
        fragments.append(
            EntryFragment(
                entry=synthetic_entry,
                raw_article_html=f'<h1>{escape(synthetic_entry.title)}</h1>' + "".join(figure_htmls),
                source_entry_ids=source_entry_ids,
                block_ids=tuple(block_ids),
            )
        )
    return fragments


def expand_entry_fragments(
    entry: BundleEntry,
    article_html: str,
    *,
    source_entry_ids: tuple[str, ...],
) -> list[EntryFragment]:
    if entry.entry_id == "chapter-024":
        return split_chapter_024_fragments(entry, article_html, source_entry_ids=source_entry_ids)
    return [
        EntryFragment(
            entry=entry,
            raw_article_html=article_html,
            source_entry_ids=source_entry_ids,
            block_ids=extract_block_ids(article_html),
        )
    ]


def decorate_genealogy_tables(article_html: str) -> str:
    def replace_table(match: re.Match[str]) -> str:
        table_html = match.group(0)
        table_probe = WHITESPACE_PATTERN.sub(" ", table_html.upper())
        if not all(f"<TH>{header}</TH>" in table_probe for header in GENEALOGY_TABLE_HEADERS):
            return table_html
        opening_tag_match = re.match(r"<table\b[^>]*>", table_html, re.IGNORECASE)
        if not opening_tag_match:
            return table_html
        opening_tag = opening_tag_match.group(0)
        return add_class_to_tag(opening_tag, "genealogy-table") + table_html[len(opening_tag) :]

    return TABLE_PATTERN.sub(replace_table, article_html)


def decorate_ancestry_table(entry: BundleEntry, article_html: str) -> str:
    if entry.entry_id != "chapter-001":
        return article_html
    match = TABLE_PATTERN.search(article_html)
    if not match:
        return article_html
    table_html = match.group(0)
    opening_tag_match = re.match(r"<table\b[^>]*>", table_html, re.IGNORECASE)
    if not opening_tag_match:
        return article_html
    opening_tag = opening_tag_match.group(0)
    replacement = add_class_to_tag(opening_tag, "ancestry-table") + table_html[len(opening_tag) :]
    replacement = replacement.replace(
        "<tr><td>\\</td><td>/</td></tr>",
        '<tr class="ancestry-final-row ancestry-connector-row"><td>\\</td><td>/</td></tr>',
    )
    replacement = re.sub(
        r'(<tr class="ancestry-final-row ancestry-connector-row"><td>\\</td><td>/</td></tr>)\s*'
        r"<tr><td>(.*?)</td></tr>\s*"
        r"<tr><td>(.*?)</td></tr>\s*"
        r"<tr><td>(.*?)</td></tr>",
        r'\1<tr class="ancestry-final-row"><td colspan="2">\2</td></tr>'
        r'<tr class="ancestry-final-row"><td colspan="2">\3</td></tr>'
        r'<tr class="ancestry-final-row"><td colspan="2">\4</td></tr>',
        replacement,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return article_html[: match.start()] + replacement + article_html[match.end() :]


def decorate_recipe_callout(entry: BundleEntry, article_html: str) -> str:
    if entry.entry_id != "chapter-005" or "recipe-callout" in article_html:
        return article_html
    return RECIPE_BLOCK_PATTERN.sub(r'<section class="recipe-callout">\1</section>', article_html, count=1)


def clean_index_paragraphs(entry: BundleEntry, article_html: str) -> str:
    if entry.entry_id != "page-008":
        return article_html

    items: list[tuple[str, str]] = []
    for match in PARAGRAPH_PATTERN.finditer(article_html):
        text = plain_text_from_html(match.group(1))
        dotted = re.match(r"^(.*?)\s*\.+\s*(\d+)$", text)
        if dotted:
            items.append((dotted.group(1).strip(), dotted.group(2)))

    if items:
        list_html = '<ul class="clean-index-list">' + "".join(
            f'<li><span>{escape(label)}</span><span>{escape(page)}</span></li>'
            for label, page in items
        ) + "</ul>"
        article_html = PARAGRAPH_PATTERN.sub("", article_html, count=len(items) + 1)
        insertion = article_html.find("</h1>")
        if insertion != -1:
            article_html = article_html[: insertion + len("</h1>")] + list_html + article_html[insertion + len("</h1>") :]

    def clean_table(match: re.Match[str]) -> str:
        table_html = match.group(0)
        if "summary-index-table" in table_html:
            return table_html
        opening_tag_match = re.match(r"<table\b[^>]*>", table_html, re.IGNORECASE)
        if not opening_tag_match:
            return table_html
        opening_tag = add_class_to_tag(opening_tag_match.group(0), "summary-index-table")
        cleaned = re.sub(r"([A-Za-z0-9])\s*\.+\s*", r"\1 ", table_html[len(opening_tag_match.group(0)) :])
        if "<th>Page</th>" not in cleaned:
            cleaned = cleaned.replace("</tr>", "<th>Page</th></tr>", 1)
        return opening_tag + cleaned

    return TABLE_PATTERN.sub(clean_table, article_html, count=1)


def should_inline_figure(entry: BundleEntry, article_html: str) -> bool:
    if entry.entry_id in {"chapter-003", "chapter-024"} or entry.entry_id.startswith("page-photo-"):
        return False
    if len(list(FIGURE_PATTERN.finditer(article_html))) > 2:
        return False
    return len(list(PARAGRAPH_PATTERN.finditer(article_html))) >= 4


def figure_variant(figure_html: str) -> str:
    texts = []
    for match in IMG_TAG_PATTERN.finditer(figure_html):
        alt = attribute_value(match.group(1), "alt")
        if alt:
            texts.append(alt.lower())
    caption_match = FIGCAPTION_BLOCK_PATTERN.search(figure_html)
    if caption_match:
        texts.append(plain_text_from_html(caption_match.group(0)).lower())
    combined = " ".join(texts)
    if any(keyword in combined for keyword in FIGURE_SIGNATURE_KEYWORDS):
        return "figure-signature"
    if any(keyword in combined for keyword in FIGURE_EMBLEM_KEYWORDS):
        return "figure-emblem"
    if any(keyword in combined for keyword in FIGURE_ILLUSTRATION_KEYWORDS):
        return "figure-illustration"
    if len(list(IMG_TAG_PATTERN.finditer(figure_html))) > 1:
        return "figure-gallery"
    return "figure-photo"


def render_figure_image(attributes: str) -> str | None:
    src = attribute_value(attributes, "src")
    if not src:
        return None

    image_tag = f"<img{attributes}>"
    image_tag = add_class_to_tag(image_tag, "figure-image")
    image_tag = set_attribute_on_tag(image_tag, "decoding", "async")
    return (
        f'<a class="figure-image-link" href="{escape(src)}" target="_blank" rel="noopener">'
        f"{image_tag}</a>"
    )


def decorate_figures(entry: BundleEntry, article_html: str) -> str:
    inline_figure = should_inline_figure(entry, article_html)

    def replace_figure(match: re.Match[str]) -> str:
        figure_html = match.group(0)
        opening_tag_match = re.match(r"<figure\b[^>]*>", figure_html, re.IGNORECASE)
        if not opening_tag_match:
            return figure_html
        opening_tag = opening_tag_match.group(0)
        variant = figure_variant(figure_html)
        opening_tag = add_class_to_tag(opening_tag, variant)
        if inline_figure and variant in {"figure-photo", "figure-illustration"}:
            opening_tag = add_class_to_tag(opening_tag, "figure-inline")

        image_htmls = [
            image_html
            for image_match in IMG_TAG_PATTERN.finditer(figure_html)
            if (image_html := render_figure_image(image_match.group(1)))
        ]
        if not image_htmls:
            return ""
        caption_match = FIGCAPTION_BLOCK_PATTERN.search(figure_html)
        media_html = image_htmls[0]
        if len(image_htmls) > 1:
            media_html = '<div class="figure-image-grid">' + "".join(image_htmls) + "</div>"
        caption_html = caption_match.group(0) if caption_match else ""
        return opening_tag + media_html + caption_html + "</figure>"

    return FIGURE_PATTERN.sub(replace_figure, article_html)


def should_skip_rendered_entry(entry: BundleEntry, article_html: str) -> bool:
    if entry.kind != "page":
        return False
    if IMG_TAG_PATTERN.search(article_html):
        return False
    if TABLE_PATTERN.search(article_html):
        return False
    return not plain_text_from_html(article_html)


def rewrite_primary_heading(article_html: str, display_title: str) -> str:
    match = PRIMARY_HEADING_PATTERN.search(article_html)
    if not match:
        return article_html
    current_heading = plain_text_from_html(match.group(2))
    if not current_heading or not is_mostly_uppercase(current_heading):
        return article_html
    if soften_display_title(current_heading) != display_title:
        return article_html
    replacement = f"{match.group(1)}{escape(display_title)}{match.group(3)}"
    return article_html[: match.start()] + replacement + article_html[match.end() :]


def enhance_article_html(entry: BundleEntry, article_html: str, display_title: str) -> str:
    enhanced = decorate_genealogy_tables(article_html)
    enhanced = decorate_ancestry_table(entry, enhanced)
    enhanced = clean_index_paragraphs(entry, enhanced)
    enhanced = decorate_recipe_callout(entry, enhanced)
    enhanced = decorate_figures(entry, enhanced)
    return rewrite_primary_heading(enhanced, display_title)


def first_image_details(article_html: str) -> tuple[str | None, str | None]:
    match = IMG_TAG_PATTERN.search(article_html)
    if not match:
        return None, None
    attributes = match.group(1)
    return attribute_value(attributes, "src"), attribute_value(attributes, "alt")


def card_thumbnail(entry: BundleEntry, group: EntryGroup, article_html: str) -> tuple[str | None, str | None]:
    if entry.kind != "page":
        return None, None
    src, alt = first_image_details(article_html)
    if not src:
        return None, None
    return src, alt


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


def select_provenance_rows(
    provenance_rows_by_entry_id: dict[str, list[dict]],
    source_entry_ids: tuple[str, ...],
    block_ids: tuple[str, ...],
) -> tuple[dict[str, object], ...]:
    selected_rows: list[dict[str, object]] = []
    for source_entry_id in source_entry_ids:
        selected_rows.extend(provenance_rows_by_entry_id.get(source_entry_id, []))
    if block_ids:
        allowed_ids = set(block_ids)
        selected_rows = [row for row in selected_rows if row.get("block_id") in allowed_ids]
    return tuple(selected_rows)


def repo_relative_or_abs(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def public_href(path: str) -> str:
    return "/".join(quote(part) for part in path.split("/"))


def absolute_public_url(site_url: str, path: str) -> str:
    return f"{site_url.rstrip('/')}/{public_href(path.lstrip('/'))}"


def format_rss_pub_date(published_at: date) -> str:
    return format_datetime(datetime.combine(published_at, time(12, 0, tzinfo=timezone.utc)))


def append_xml_text(parent: ET.Element, tag: str, text: str) -> ET.Element:
    child = ET.SubElement(parent, tag)
    child.text = text
    return child


def render_podcast_feed_item(
    channel: ET.Element,
    *,
    catalog: PodcastCatalog,
    title: str,
    summary: str,
    published_at: date,
    audio_source_path: Path,
    audio_output_path: str,
    item_url: str,
    episode_number: int | None = None,
) -> None:
    item = ET.SubElement(channel, "item")
    append_xml_text(item, "title", title)
    append_xml_text(item, "description", summary)
    append_xml_text(item, "link", item_url)
    guid = append_xml_text(item, "guid", item_url)
    guid.set("isPermaLink", "true")
    append_xml_text(item, "pubDate", format_rss_pub_date(published_at))
    ET.SubElement(
        item,
        "enclosure",
        {
            "url": absolute_public_url(catalog.feed.site_url, audio_output_path),
            "length": str(audio_source_path.stat().st_size),
            "type": "audio/mpeg",
        },
    )
    append_xml_text(item, f"{{{ITUNES_XML_NAMESPACE}}}author", catalog.feed.author_name)
    append_xml_text(item, f"{{{ITUNES_XML_NAMESPACE}}}summary", summary)
    append_xml_text(item, f"{{{ITUNES_XML_NAMESPACE}}}explicit", "false")
    if episode_number is not None:
        append_xml_text(item, f"{{{ITUNES_XML_NAMESPACE}}}episode", str(episode_number))


def render_podcast_feed(catalog: PodcastCatalog) -> str:
    ET.register_namespace("atom", ATOM_XML_NAMESPACE)
    ET.register_namespace("content", CONTENT_XML_NAMESPACE)
    ET.register_namespace("itunes", ITUNES_XML_NAMESPACE)

    feed_url = absolute_public_url(catalog.feed.site_url, catalog.feed.feed_path)
    page_url = absolute_public_url(catalog.feed.site_url, catalog.feed.page_path)
    artwork_url = absolute_public_url(catalog.feed.site_url, catalog.feed.artwork_output_path)
    all_published_dates = [episode.published_at for episode in catalog.episodes]
    if catalog.full_book_episode:
        all_published_dates.append(catalog.full_book_episode.published_at)
    last_build_date = format_rss_pub_date(max(all_published_dates)) if all_published_dates else format_rss_pub_date(date.today())

    rss = ET.Element(
        "rss",
        {
            "version": "2.0",
            "xmlns:content": CONTENT_XML_NAMESPACE,
        },
    )
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(
        channel,
        f"{{{ATOM_XML_NAMESPACE}}}link",
        {"href": feed_url, "rel": "self", "type": "application/rss+xml"},
    )
    append_xml_text(channel, "title", catalog.title)
    append_xml_text(channel, "link", page_url)
    append_xml_text(channel, "description", catalog.feed.description)
    append_xml_text(channel, "language", catalog.feed.language)
    append_xml_text(channel, "managingEditor", catalog.feed.public_contact_email)
    append_xml_text(channel, "webMaster", catalog.feed.public_contact_email)
    append_xml_text(channel, "lastBuildDate", last_build_date)
    append_xml_text(channel, "generator", "Onward to the Unknown family-site builder")
    append_xml_text(channel, f"{{{ITUNES_XML_NAMESPACE}}}author", catalog.feed.author_name)
    if catalog.feed.subtitle:
        append_xml_text(channel, f"{{{ITUNES_XML_NAMESPACE}}}subtitle", catalog.feed.subtitle)
    append_xml_text(channel, f"{{{ITUNES_XML_NAMESPACE}}}summary", catalog.feed.description)
    append_xml_text(channel, f"{{{ITUNES_XML_NAMESPACE}}}explicit", "false")
    for category in catalog.feed.categories:
        category_element = ET.SubElement(
            channel,
            f"{{{ITUNES_XML_NAMESPACE}}}category",
            {"text": category.name},
        )
        if category.subcategory:
            ET.SubElement(
                category_element,
                f"{{{ITUNES_XML_NAMESPACE}}}category",
                {"text": category.subcategory},
            )
    ET.SubElement(channel, f"{{{ITUNES_XML_NAMESPACE}}}image", {"href": artwork_url})
    owner = ET.SubElement(channel, f"{{{ITUNES_XML_NAMESPACE}}}owner")
    append_xml_text(owner, f"{{{ITUNES_XML_NAMESPACE}}}name", catalog.feed.owner_name)
    append_xml_text(owner, f"{{{ITUNES_XML_NAMESPACE}}}email", catalog.feed.public_contact_email)
    image = ET.SubElement(channel, "image")
    append_xml_text(image, "url", artwork_url)
    append_xml_text(image, "title", catalog.title)
    append_xml_text(image, "link", page_url)

    if catalog.full_book_episode:
        render_podcast_feed_item(
            channel,
            catalog=catalog,
            title=catalog.full_book_episode.title,
            summary=catalog.full_book_episode.summary,
            published_at=catalog.full_book_episode.published_at,
            audio_source_path=catalog.full_book_episode.audio_source_path,
            audio_output_path=catalog.full_book_episode.audio_output_path,
            item_url=f"{page_url}#full-book-podcast",
        )

    for episode in catalog.episodes:
        render_podcast_feed_item(
            channel,
            catalog=catalog,
            title=episode.title,
            summary=episode.summary,
            published_at=episode.published_at,
            audio_source_path=episode.audio_source_path,
            audio_output_path=episode.audio_output_path,
            item_url=f"{page_url}#{episode_fragment_id(episode)}",
            episode_number=episode.episode_number,
        )

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    return ET.tostring(rss, encoding="utf-8", xml_declaration=True).decode("utf-8")


def source_library_input_root(source_dir: Path) -> Path:
    if source_dir.parent.name == "doc-web-html":
        return source_dir.parent.parent
    if source_dir.parent.name == "input":
        return source_dir.parent
    return REPO_ROOT / "input"


def source_library_sort_key(path: Path) -> tuple[int, int, str]:
    featured_rank = 0 if path.name == FEATURED_BOOK_SOURCE_FILENAME else 1
    kind_rank = 0 if path.suffix.lower() == ".pdf" else 1
    return featured_rank, kind_rank, normalize_merge_text(path.stem)


def source_title_from_path(source_path: Path, *, title_override: str | None = None) -> str:
    if title_override:
        return title_override
    if source_path.name in SPECIAL_SOURCE_TITLE_OVERRIDES:
        return SPECIAL_SOURCE_TITLE_OVERRIDES[source_path.name]
    base_name = re.sub(r"[-_]+", " ", source_path.stem)
    base_name = WHITESPACE_PATTERN.sub(" ", base_name).strip()
    return soften_display_title(base_name) or source_path.stem


def source_summary_text(source_path: Path, *, title_override: str | None = None) -> str:
    if source_path.name in SPECIAL_SOURCE_SUMMARY_OVERRIDES:
        return SPECIAL_SOURCE_SUMMARY_OVERRIDES[source_path.name]
    if title_override:
        return f"Preserved source attachment for {title_override}."
    if source_path.suffix.lower() == ".pdf":
        return "Preserved family archive PDF."
    return "Preserved family archive image."


def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    units = ("KB", "MB", "GB")
    size = float(size_bytes)
    for unit in units:
        size /= 1024.0
        if size < 1024.0 or unit == units[-1]:
            return f"{size:.1f} {unit}"
    return f"{size_bytes} B"


def discover_published_source_assets(
    source_dir: Path,
    supplements: list[FamilyStorySupplement],
) -> tuple[PublishedSourceAsset, ...]:
    input_root = source_library_input_root(source_dir)
    if not input_root.exists():
        return ()

    title_overrides_by_path = {
        supplement.source_pdf.resolve(): supplement.title
        for supplement in supplements
    }
    assets: list[PublishedSourceAsset] = []
    for source_path in sorted(input_root.iterdir(), key=source_library_sort_key):
        if not source_path.is_file():
            continue
        kind_label = PUBLISHABLE_SOURCE_SUFFIX_LABELS.get(source_path.suffix.lower())
        if not kind_label:
            continue
        title_override = title_overrides_by_path.get(source_path.resolve())
        relative_input_path = f"{input_root.name}/{source_path.relative_to(input_root).as_posix()}"
        assets.append(
            PublishedSourceAsset(
                source_path=source_path.resolve(),
                relative_input_path=relative_input_path,
                public_output_path=f"{SOURCE_LIBRARY_PUBLIC_ROOT}/{source_path.name}",
                title=source_title_from_path(source_path, title_override=title_override),
                filename=source_path.name,
                kind_label=kind_label,
                summary_text=source_summary_text(source_path, title_override=title_override),
                size_bytes=source_path.stat().st_size,
                featured=source_path.name == FEATURED_BOOK_SOURCE_FILENAME,
            )
        )
    return tuple(assets)


def copy_published_source_assets(assets: tuple[PublishedSourceAsset, ...], output_dir: Path) -> None:
    for asset in assets:
        destination_path = output_dir / asset.public_output_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(asset.source_path, destination_path)


def serialize_source_library_manifest(assets: tuple[PublishedSourceAsset, ...]) -> str:
    featured_asset = next((asset for asset in assets if asset.featured), None)
    payload = {
        "schema_version": "onward_source_library_v1",
        "page_path": DEFAULT_SOURCE_LIBRARY_PAGE_PATH if assets else None,
        "published_count": len(assets),
        "featured_source": featured_asset.relative_input_path if featured_asset else None,
        "files": [
            {
                "title": asset.title,
                "filename": asset.filename,
                "kind_label": asset.kind_label,
                "summary_text": asset.summary_text,
                "source_path": asset.relative_input_path,
                "output_path": asset.public_output_path,
                "size_bytes": asset.size_bytes,
                "featured": asset.featured,
            }
            for asset in assets
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def copy_audiobook_public_assets(catalog: AudiobookCatalog, output_dir: Path) -> None:
    for track in catalog.tracks:
        destination_path = output_dir / track.audio_output_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(track.audio_source_path, destination_path)
    if catalog.full_audiobook and catalog.full_audiobook.is_available:
        destination_path = output_dir / catalog.full_audiobook.audio_output_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(catalog.full_audiobook.audio_source_path, destination_path)


def copy_podcast_public_assets(catalog: PodcastCatalog, output_dir: Path) -> None:
    for episode in catalog.episodes:
        destination_path = output_dir / episode.audio_output_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(episode.audio_source_path, destination_path)
    if catalog.full_book_episode:
        destination_path = output_dir / catalog.full_book_episode.audio_output_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(catalog.full_book_episode.audio_source_path, destination_path)
    artwork_destination_path = output_dir / catalog.feed.artwork_output_path
    artwork_destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(catalog.feed.artwork_source_path, artwork_destination_path)


def load_family_story_supplements(source_dir: Path) -> list[FamilyStorySupplement]:
    registry_path = source_dir.parent / SUPPLEMENT_REGISTRY_PATH.name
    if not registry_path.exists():
        return []

    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "onward_family_story_supplement_registry_v1":
        raise SystemExit(
            "Family story supplement registry must use schema_version "
            "`onward_family_story_supplement_registry_v1`."
        )
    supplements_payload = payload.get("supplements")
    if not isinstance(supplements_payload, list):
        raise SystemExit("Family story supplement registry must provide a `supplements` array.")

    supplements: list[FamilyStorySupplement] = []
    for raw_row in supplements_payload:
        if not isinstance(raw_row, dict):
            raise SystemExit("Every family story supplement registry row must be an object.")
        supplement_id = raw_row.get("supplement_id")
        title = raw_row.get("title")
        output_path = raw_row.get("output_path")
        bundle_dir = raw_row.get("bundle_dir")
        source_pdf = raw_row.get("source_pdf")
        preamble = raw_row.get("preamble")
        if not all(isinstance(value, str) and value.strip() for value in (
            supplement_id,
            title,
            output_path,
            bundle_dir,
            source_pdf,
            preamble,
        )):
            raise SystemExit(
                "Family story supplements require non-empty string values for "
                "`supplement_id`, `title`, `output_path`, `bundle_dir`, `source_pdf`, and `preamble`."
            )
        entry_ids = raw_row.get("entry_ids")
        if not isinstance(entry_ids, list) or not entry_ids or not all(isinstance(value, str) for value in entry_ids):
            raise SystemExit("Family story supplement `entry_ids` must be a non-empty string array.")
        absorbed_entry_ids = raw_row.get("absorbed_entry_ids", [])
        if not isinstance(absorbed_entry_ids, list) or not all(isinstance(value, str) for value in absorbed_entry_ids):
            raise SystemExit("Family story supplement `absorbed_entry_ids` must be a string array when present.")
        group_id = raw_row.get("group_id", "family-stories")
        if group_id not in ENTRY_GROUPS_BY_ID:
            raise SystemExit(f"Unknown family story supplement group_id: {group_id!r}")
        insert_after_entry_id = raw_row.get("insert_after_entry_id")
        if insert_after_entry_id is not None and not isinstance(insert_after_entry_id, str):
            raise SystemExit("Family story supplement `insert_after_entry_id` must be a string when present.")

        resolved_bundle_dir = (registry_path.parent / bundle_dir).resolve()
        resolved_source_pdf = (registry_path.parent / source_pdf).resolve()
        if not (resolved_bundle_dir / "manifest.json").exists():
            raise SystemExit(f"Family story supplement bundle is missing manifest.json: {resolved_bundle_dir}")
        if not resolved_source_pdf.exists():
            raise SystemExit(f"Family story supplement source PDF not found: {resolved_source_pdf}")

        supplements.append(
            FamilyStorySupplement(
                supplement_id=supplement_id.strip(),
                title=title.strip(),
                output_path=output_path.strip(),
                bundle_dir=resolved_bundle_dir,
                source_pdf=resolved_source_pdf,
                group=ENTRY_GROUPS_BY_ID[group_id],
                insert_after_entry_id=insert_after_entry_id.strip() if isinstance(insert_after_entry_id, str) else None,
                source_entry_ids=tuple(entry_ids),
                absorbed_entry_ids=tuple(absorbed_entry_ids),
                preamble=preamble.strip(),
            )
        )
    return supplements


def is_relative_asset_reference(raw_value: str) -> bool:
    return bool(raw_value) and not re.match(r"^(?:[a-z][a-z0-9+.-]*:|/|#)", raw_value, re.IGNORECASE)


def rewrite_relative_asset_references(article_html: str, prefix: str) -> str:
    normalized_prefix = prefix.strip("/")

    def replace(match: re.Match[str]) -> str:
        value = match.group("double") or match.group("single") or ""
        if not is_relative_asset_reference(value):
            return match.group(0)
        stripped = value.lstrip("./")
        if stripped.startswith(normalized_prefix + "/"):
            return match.group(0)
        quote = '"' if match.group("double") is not None else "'"
        return f'{match.group("attr")}={quote}{normalized_prefix}/{stripped}{quote}'

    return URL_ATTR_PATTERN.sub(replace, article_html)


def copy_supplement_public_assets(bundle_dir: Path, assets_dir: Path) -> None:
    copied_any = False
    for source_path in sorted(bundle_dir.rglob("*")):
        if not source_path.is_file():
            continue
        relative_path = source_path.relative_to(bundle_dir)
        if relative_path.parts and relative_path.parts[0] == "provenance":
            continue
        if relative_path.name == "manifest.json":
            continue
        if source_path.suffix.lower() == ".html":
            continue
        destination_path = assets_dir / relative_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)
        copied_any = True
    if not copied_any and assets_dir.exists():
        shutil.rmtree(assets_dir)


def demote_primary_heading(article_html: str) -> str:
    match = PRIMARY_HEADING_PATTERN.search(article_html)
    if not match:
        return article_html
    opening_tag = re.sub(r"<h1\b", "<h2", match.group(1), count=1, flags=re.IGNORECASE)
    opening_tag = add_class_to_tag(opening_tag, "supplement-source-title")
    closing_tag = re.sub(r"</h1>", "</h2>", match.group(3), count=1, flags=re.IGNORECASE)
    replacement = f"{opening_tag}{match.group(2)}{closing_tag}"
    return article_html[: match.start()] + replacement + article_html[match.end() :]


def render_supplement_article_html(
    supplement: FamilyStorySupplement,
    *,
    body_html: str,
    action_links: list[str],
) -> str:
    actions_html = "".join(action_links)
    return dedent(
        f"""\
        <section class="supplement-intro">
          <p class="supplement-kicker">Family archive supplement</p>
          <h1>{escape(supplement.title)}</h1>
          <p class="supplement-preamble">{escape(supplement.preamble)}</p>
          <div class="supplement-actions">
            {actions_html}
          </div>
        </section>
        <section id="supplement-body" class="supplement-body">
          {body_html}
        </section>
        """
    ).strip()


def build_supplement_rendered_entry(
    supplement: FamilyStorySupplement,
    *,
    output_dir: Path,
    internal_dir: Path,
    published_source_assets_by_path: dict[Path, PublishedSourceAsset],
) -> tuple[RenderedEntry, SupplementAuditRow]:
    bundle_manifest = load_manifest(supplement.bundle_dir)
    bundle_entries = [bundle_entry_from_manifest(row) for row in bundle_manifest.get("entries", [])]
    selected_entries = select_entries(bundle_entries, list(supplement.source_entry_ids))
    primary_entry = selected_entries[0]
    primary_text = (supplement.bundle_dir / primary_entry.path).read_text(encoding="utf-8")
    primary_article_html = extract_article_html(primary_text, supplement.bundle_dir / primary_entry.path)
    absorbed_articles: list[tuple[BundleEntry, str]] = []
    for absorbed_entry in selected_entries[1:]:
        absorbed_text = (supplement.bundle_dir / absorbed_entry.path).read_text(encoding="utf-8")
        absorbed_articles.append(
            (absorbed_entry, extract_article_html(absorbed_text, supplement.bundle_dir / absorbed_entry.path))
        )
    merged_article_html = merge_absorbed_article_html(primary_article_html, absorbed_articles)

    public_root = f"supplements/{supplement.supplement_id}"
    public_root_path = output_dir / "supplements" / supplement.supplement_id
    if public_root_path.exists():
        shutil.rmtree(public_root_path)
    copy_supplement_public_assets(supplement.bundle_dir, public_root_path / "assets")

    merged_article_html = rewrite_relative_asset_references(merged_article_html, f"{public_root}/assets")
    synthetic_entry = BundleEntry(
        entry_id=f"supplement-{supplement.supplement_id}",
        kind="chapter",
        title=supplement.title,
        path=supplement.output_path,
        order=0,
        prev_entry_id=None,
        next_entry_id=None,
        source_pages=tuple(page for entry in selected_entries for page in entry.source_pages),
        printed_pages=tuple(page for entry in selected_entries for page in entry.printed_pages),
        printed_page_start=None,
        printed_page_end=None,
    )
    enhanced_body_html = enhance_article_html(synthetic_entry, merged_article_html, supplement.title)
    enhanced_body_html = demote_primary_heading(enhanced_body_html)
    action_links = [render_nav_link("Read Memoir", "#supplement-body", primary=True)]
    published_source = published_source_assets_by_path.get(supplement.source_pdf.resolve())
    if published_source:
        source_href = public_href(published_source.public_output_path)
        action_links.append(render_nav_link("Open Original PDF", source_href))
    article_html = render_supplement_article_html(
        supplement,
        body_html=enhanced_body_html,
        action_links=action_links,
    )

    supplement_provenance_rows = load_provenance_rows(supplement.bundle_dir)
    provenance_rows = select_provenance_rows(
        supplement_provenance_rows,
        supplement.source_entry_ids,
        extract_block_ids(article_html),
    )
    write_text(
        internal_dir / "supplements" / supplement.supplement_id / "metadata.json",
        json.dumps(
            {
                "schema_version": "onward_family_story_supplement_v1",
                "supplement_id": supplement.supplement_id,
                "title": supplement.title,
                "output_path": supplement.output_path,
                "source_bundle_dir": repo_relative_or_abs(supplement.bundle_dir),
                "source_pdf": repo_relative_or_abs(supplement.source_pdf),
                "source_entry_ids": list(supplement.source_entry_ids),
                "absorbed_entry_ids": list(supplement.absorbed_entry_ids),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )

    rendered_entry = RenderedEntry(
        entry=synthetic_entry,
        group=supplement.group,
        article_html=article_html,
        display_title=supplement.title,
        summary_text=excerpt_text(supplement.preamble, LANDING_CARD_SUMMARY_LIMIT),
        thumbnail_src=first_image_details(article_html)[0],
        thumbnail_alt=first_image_details(article_html)[1],
        source_entry_ids=supplement.source_entry_ids,
        block_ids=extract_block_ids(article_html),
        provenance_rows=provenance_rows,
    )
    audit_row = SupplementAuditRow(
        supplement_id=supplement.supplement_id,
        title=supplement.title,
        group=supplement.group,
        status="rendered",
        output_path=supplement.output_path,
        bundle_root=repo_relative_or_abs(supplement.bundle_dir),
        source_pdf_path=repo_relative_or_abs(supplement.source_pdf),
        source_entry_ids=supplement.source_entry_ids,
        absorbed_entry_ids=supplement.absorbed_entry_ids,
        rationale="Rendered as a family-story supplement.",
    )
    return rendered_entry, audit_row


def insert_supplement_rendered_entries(
    rendered_entries: list[RenderedEntry],
    supplement_rows: list[tuple[FamilyStorySupplement, RenderedEntry]],
) -> list[RenderedEntry]:
    combined = list(rendered_entries)
    for supplement, rendered_entry in supplement_rows:
        insert_index = None
        if supplement.insert_after_entry_id:
            for index, existing in enumerate(combined):
                if existing.entry.entry_id == supplement.insert_after_entry_id:
                    insert_index = index + 1
        if insert_index is None and supplement.group.id == "family-stories":
            for index, existing in enumerate(combined):
                if existing.group.id == "closing-archive":
                    insert_index = index
                    break
        if insert_index is None:
            combined.append(rendered_entry)
        else:
            combined.insert(insert_index, rendered_entry)
    return combined


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
    if entry.entry_id.startswith("page-photo-") or entry.entry_id == "chapter-024" or entry.order >= 33:
        return ENTRY_GROUPS_BY_ID["closing-archive"]
    if entry.entry_id in DEFAULT_FAMILY_ENTRY_IDS:
        return ENTRY_GROUPS_BY_ID["family-stories"]
    return ENTRY_GROUPS_BY_ID["opening-pages"]


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


def absorbed_output_paths(entries: list[BundleEntry]) -> dict[str, str]:
    entries_by_id = {entry.entry_id: entry for entry in entries}
    absorbed: dict[str, str] = {}
    for absorbed_entry_id, target_entry_id in MERGED_ENTRY_TARGETS.items():
        absorbed_entry = entries_by_id.get(absorbed_entry_id)
        target_entry = entries_by_id.get(target_entry_id)
        if absorbed_entry and target_entry:
            absorbed[absorbed_entry_id] = target_entry.path
    return absorbed


def absorbed_entries_by_target(entries: list[BundleEntry]) -> dict[str, list[BundleEntry]]:
    entries_by_id = {entry.entry_id: entry for entry in entries}
    absorbed_by_target: dict[str, list[BundleEntry]] = defaultdict(list)
    for absorbed_entry_id, target_entry_id in MERGED_ENTRY_TARGETS.items():
        absorbed_entry = entries_by_id.get(absorbed_entry_id)
        target_entry = entries_by_id.get(target_entry_id)
        if absorbed_entry and target_entry:
            absorbed_by_target[target_entry_id].append(absorbed_entry)
    for absorbed_entries in absorbed_by_target.values():
        absorbed_entries.sort(key=lambda entry: entry.order)
    return dict(absorbed_by_target)


def build_rendered_entries(
    source_dir: Path,
    entries: list[BundleEntry],
    *,
    provenance_rows_by_entry_id: dict[str, list[dict]],
    absorbed_entry_ids: set[str] | None = None,
    absorbed_entries_by_target_id: dict[str, list[BundleEntry]] | None = None,
) -> list[RenderedEntry]:
    absorbed_entry_ids = absorbed_entry_ids or set()
    absorbed_entries_by_target_id = absorbed_entries_by_target_id or {}
    rendered: list[RenderedEntry] = []
    for entry in entries:
        if entry.entry_id in absorbed_entry_ids:
            continue
        document_path = source_dir / entry.path
        document_text = document_path.read_text(encoding="utf-8")
        raw_article_html = extract_article_html(document_text, document_path)
        absorbed_articles: list[tuple[BundleEntry, str]] = []
        for absorbed_entry in absorbed_entries_by_target_id.get(entry.entry_id, []):
            absorbed_path = source_dir / absorbed_entry.path
            absorbed_text = absorbed_path.read_text(encoding="utf-8")
            absorbed_articles.append((absorbed_entry, extract_article_html(absorbed_text, absorbed_path)))
        raw_article_html = merge_absorbed_article_html(raw_article_html, absorbed_articles)
        source_entry_ids = (entry.entry_id, *(absorbed_entry.entry_id for absorbed_entry, _html in absorbed_articles))
        for fragment in expand_entry_fragments(entry, raw_article_html, source_entry_ids=source_entry_ids):
            if should_skip_rendered_entry(fragment.entry, fragment.raw_article_html):
                continue
            group = group_for_entry(fragment.entry)
            display_title = derive_display_title(fragment.entry, fragment.raw_article_html)
            article_html = enhance_article_html(fragment.entry, fragment.raw_article_html, display_title)
            thumbnail_src, thumbnail_alt = card_thumbnail(fragment.entry, group, fragment.raw_article_html)
            rendered.append(
                RenderedEntry(
                    entry=fragment.entry,
                    group=group,
                    article_html=article_html,
                    display_title=display_title,
                    summary_text=build_summary_text(article_html, display_title),
                    thumbnail_src=thumbnail_src,
                    thumbnail_alt=thumbnail_alt,
                    source_entry_ids=fragment.source_entry_ids,
                    block_ids=fragment.block_ids,
                    provenance_rows=select_provenance_rows(
                        provenance_rows_by_entry_id,
                        fragment.source_entry_ids,
                        fragment.block_ids,
                    ),
                )
            )
    return rendered


def build_omission_audit(
    all_entries: list[BundleEntry],
    selected_entries: list[BundleEntry],
    skipped_entry_ids: set[str] | None = None,
    absorbed_entry_output_paths: dict[str, str] | None = None,
) -> list[AuditRow]:
    skipped_entry_ids = skipped_entry_ids or set()
    absorbed_entry_output_paths = absorbed_entry_output_paths or {}
    selected_ids = {entry.entry_id for entry in selected_entries}
    audit_rows: list[AuditRow] = []
    for entry in all_entries:
        group = group_for_entry(entry)
        if entry.entry_id in absorbed_entry_output_paths:
            audit_rows.append(
                AuditRow(
                    entry=entry,
                    group=group,
                    status="rendered",
                    surface="merged-entry-page",
                    output_path=absorbed_entry_output_paths[entry.entry_id],
                    rationale="Absorbed into the first opening page so the repeated title leaf does not appear as a separate reader-facing page.",
                )
            )
            continue
        if entry.entry_id in skipped_entry_ids:
            audit_rows.append(
                AuditRow(
                    entry=entry,
                    group=group,
                    status="intentionally_deferred",
                    surface="audit-only",
                    output_path=None,
                    rationale="Skipped in the surfaced site because the source page has no text, no image, and no table content to show.",
                )
            )
            continue
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
        <link rel="stylesheet" href="{SITE_STYLESHEET_HREF}">
        </head>
        <body>
        {body_html}
        </body>
        </html>
        """
    )


def render_entry_card(rendered: RenderedEntry) -> str:
    entry = rendered.entry
    card_classes = "story-card has-thumbnail" if rendered.thumbnail_src else "story-card"
    media_html = ""
    if rendered.thumbnail_src:
        media_html = dedent(
            f"""\
              <div class="story-card-media">
                <img src="{escape(rendered.thumbnail_src)}" alt="{escape(rendered.thumbnail_alt or rendered.display_title)}">
              </div>
            """
        )
    summary_html = f"\n  <p>{escape(rendered.summary_text)}</p>" if rendered.summary_text else ""
    title_html = f'<h3 class="story-title">{escape(rendered.display_title)}</h3>'
    return dedent(
        f"""\
        <a class="{card_classes}" href="{escape(entry.path)}">
          {media_html}{title_html}{summary_html}
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
            {render_section_title(group.label, icon_svg=SECTION_ICON_SVG_BY_ID.get(group.id))}
          </div>
          <div class="story-grid">
            {cards}
          </div>
        </section>
        """
    )


def render_source_library_card(asset: PublishedSourceAsset) -> str:
    kicker = "Featured book PDF" if asset.featured else asset.kind_label
    file_meta = f"{asset.kind_label} · {format_file_size(asset.size_bytes)}"
    source_href = public_href(asset.public_output_path)
    open_label = f"Open {'PDF' if asset.source_path.suffix.lower() == '.pdf' else 'Image'}"
    return dedent(
        f"""\
        <section class="panel source-card{' featured' if asset.featured else ''}">
          <p class="audio-kicker">{escape(kicker)}</p>
          <h2 class="section-title">{escape(asset.title)}</h2>
          <p class="audio-summary">{escape(asset.summary_text)}</p>
          <p class="source-meta">{escape(file_meta)}</p>
          <p class="source-meta"><code>{escape(asset.relative_input_path)}</code></p>
          {render_action_row([render_nav_link(open_label, source_href, primary=True)])}
        </section>
        """
    ).strip()


def render_index_book_panel(
    manifest: dict,
    rendered_entries: list[RenderedEntry],
    source_assets: tuple[PublishedSourceAsset, ...],
) -> str:
    summary = (
        f"Open the book page for the opening pages, family stories, and closing archive gathered from {manifest['title']}."
        if source_assets
        else "Open the book page for the opening pages, family stories, and closing archive."
    )
    return dedent(
        f"""\
        <section class="panel section-panel" id="book">
          <div class="section-header">
            <p class="audio-kicker">The Book</p>
            {render_section_title("The Book", icon_svg=BOOK_ICON_SVG)}
          </div>
          <p class="audio-summary">{escape(summary)}</p>
          {render_action_row([render_nav_link("Go to Book", DEFAULT_BOOK_PAGE_PATH, primary=True)])}
        </section>
        """
    ).strip()


def render_index_source_panel(assets: tuple[PublishedSourceAsset, ...]) -> str:
    if assets:
        item_label = "item" if len(assets) == 1 else "items"
        summary = (
            f"Browse the family documents and scans gathered here in one place. "
            f"The archive collection includes {len(assets)} {item_label}."
        )
    else:
        summary = "Open the archive shelf for the scanned book files, photographs, and companion documents collected with the family history."
    return dedent(
        f"""\
        <section class="panel section-panel source-overview" id="archive-sources">
          <div class="section-header">
            <p class="audio-kicker">Archive sources</p>
            {render_section_title("Archive Sources", icon_svg=BOOK_ICON_SVG)}
          </div>
          <p class="audio-summary">{escape(summary)}</p>
          {render_action_row([render_nav_link("Go to Archive Sources", DEFAULT_SOURCE_LIBRARY_PAGE_PATH, primary=True)])}
        </section>
        """
    ).strip()


def format_track_label(track: AudiobookTrack) -> str:
    return f"Track {track.track_number:02d}"


def track_fragment_id(track: AudiobookTrack) -> str:
    return f"track-{track.track_number:02d}"


def format_episode_label(episode: PodcastEpisode) -> str:
    return f"Episode {episode.episode_number:02d}"


def episode_fragment_id(episode: PodcastEpisode) -> str:
    return f"episode-{episode.episode_number:02d}"


def render_action_row(links: list[str]) -> str:
    if not links:
        return ""
    return '<div class="audio-actions">' + "".join(links) + "</div>"


def render_kicker(label: str, *, icon_svg: str | None = None) -> str:
    if not icon_svg:
        return f'<p class="audio-kicker">{escape(label)}</p>'
    return (
        '<p class="audio-kicker">'
        '<span class="kicker-row">'
        f'<span class="kicker-icon">{icon_svg}</span>'
        f'<span>{escape(label)}</span>'
        "</span>"
        "</p>"
    )


def format_audio_duration(duration_seconds: float | None) -> str | None:
    if duration_seconds is None:
        return None
    total_seconds = max(0, int(round(duration_seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def render_audio_runtime(duration_seconds: float | None) -> str:
    duration_label = format_audio_duration(duration_seconds)
    if duration_label is None:
        return ""
    return f'<p class="audio-runtime">Run time {escape(duration_label)}</p>'


def render_ai_attribution(tool_name: str, tool_url: str) -> str:
    return (
        '<p class="audio-note audio-attribution">'
        f'<span class="audio-attribution-icon">{AI_ICON_SVG}</span>'
        "<span>"
        "These recordings were generated by AI using "
        f'<a href="{escape(tool_url)}" target="_blank" rel="noopener noreferrer">{escape(tool_name)}</a>.'
        "</span>"
        "</p>"
    )


def decorate_primary_heading_with_icon(article_html: str, icon_svg: str) -> str:
    match = PRIMARY_HEADING_PATTERN.search(article_html)
    if not match:
        return article_html
    replacement = (
        f"{match.group(1)}"
        '<span class="article-heading-row">'
        f'<span class="article-heading-icon">{icon_svg}</span>'
        f'<span class="article-heading-text">{match.group(2)}</span>'
        "</span>"
        f"{match.group(3)}"
    )
    return article_html[: match.start()] + replacement + article_html[match.end() :]


def render_audio_player(audio_output_path: str) -> str:
    return dedent(
        f"""\
        <audio class="audio-player" controls preload="none">
          <source src="{escape(audio_output_path)}" type="audio/mpeg">
          <a href="{escape(audio_output_path)}" download>Download MP3</a>
        </audio>
        """
    ).strip()


def render_full_audiobook_player(full_audiobook: FullAudiobookAsset) -> str:
    return render_audio_player(full_audiobook.audio_output_path)


def render_index_audiobook_panel(catalog: AudiobookCatalog) -> str:
    track_count = len(catalog.tracks)
    actions = render_action_row([render_nav_link("Go to Audiobook", DEFAULT_AUDIOBOOK_PAGE_PATH, primary=True)])
    return dedent(
        f"""\
        <section class="panel section-panel audiobook-overview" id="audiobook">
          <div class="section-header">
            <p class="audio-kicker">Audiobook</p>
            {render_section_title("Audiobook", icon_svg=AUDIOBOOK_ICON_SVG)}
          </div>
          <p class="audio-summary">Listen chapter by chapter in your browser or download any MP3 for later. The current set includes {track_count} tracks, including the memoir supplement and closing poem.</p>
          {actions}
        </section>
        """
    ).strip()


def render_index_podcast_panel(catalog: PodcastCatalog) -> str:
    episode_count = len(catalog.episodes) + (1 if catalog.full_book_episode else 0)
    return dedent(
        f"""\
        <section class="panel section-panel" id="podcast">
          <div class="section-header">
            <p class="audio-kicker">Podcast</p>
            {render_section_title("Podcast", icon_svg=PODCAST_ICON_SVG)}
          </div>
          <p class="audio-summary">Listen to the whole-book episode or open chapter episodes as they are added. The current set includes {episode_count} episodes.</p>
          {render_action_row([render_nav_link("Go to Podcast", DEFAULT_PODCAST_PAGE_PATH, primary=True)])}
        </section>
        """
    ).strip()


def render_entry_audio_disclosure(
    *,
    summary_label: str,
    title: str,
    summary_text: str,
    audio_output_path: str,
    duration_seconds: float | None,
    notes: str | None,
    actions: list[str],
) -> str:
    note_html = f'<p class="audio-note">{escape(notes)}</p>' if notes else ""
    runtime_label = format_audio_duration(duration_seconds)
    meta_text = f"Run time {runtime_label}" if runtime_label else "Open player"
    return dedent(
        f"""\
        <details class="panel entry-audio-panel">
          <summary class="entry-audio-summary">
            <span class="entry-audio-summary-copy">
              <span class="entry-audio-summary-label">{escape(summary_label)}</span>
              <span class="entry-audio-summary-title">{escape(title)}</span>
              <span class="entry-audio-summary-meta">{escape(meta_text)}</span>
            </span>
          </summary>
          <div class="entry-audio-panel-body">
            <p class="audio-summary">{escape(summary_text)}</p>
            {render_audio_runtime(duration_seconds)}
            {note_html}
            {render_audio_player(audio_output_path)}
            {render_action_row(actions)}
          </div>
        </details>
        """
    ).strip()


def render_entry_audiobook_panel(track: AudiobookTrack) -> str:
    return render_entry_audio_disclosure(
        summary_label=f"Audiobook / {format_track_label(track)}",
        title=track.title,
        summary_text=f"This page matches {format_track_label(track).lower()} of the current audiobook.",
        audio_output_path=track.audio_output_path,
        duration_seconds=track.duration_seconds,
        notes=track.notes,
        actions=[
            render_nav_link("Open Full Audiobook", DEFAULT_AUDIOBOOK_PAGE_PATH, primary=True),
            render_nav_link("Download MP3", track.audio_output_path, download=True),
        ],
    )


def render_entry_podcast_panel(episode: PodcastEpisode) -> str:
    return render_entry_audio_disclosure(
        summary_label=f"Podcast / {format_episode_label(episode)}",
        title=episode.title,
        summary_text="This page also has a companion podcast episode.",
        audio_output_path=episode.audio_output_path,
        duration_seconds=episode.duration_seconds,
        notes=episode.notes,
        actions=[
            render_nav_link("Open Podcast Page", DEFAULT_PODCAST_PAGE_PATH, primary=True),
            render_nav_link("Download MP3", episode.audio_output_path, download=True),
        ],
    )


def render_audiobook_track_card(
    track: AudiobookTrack,
    rendered_entries_by_id: dict[str, RenderedEntry],
) -> str:
    matching_entry = rendered_entries_by_id.get(track.target_entry_id or "")
    notes_html = f'<p class="audio-note">{escape(track.notes)}</p>' if track.notes else ""
    actions = [
        render_nav_link("Download MP3", track.audio_output_path, download=True, icon_svg=DOWNLOAD_ICON_SVG),
    ]
    if matching_entry:
        actions.insert(0, render_nav_link("Read this section", matching_entry.entry.path, icon_svg=BOOK_ICON_SVG))

    return dedent(
        f"""\
        <section class="panel audio-track-card" id="{escape(track_fragment_id(track))}">
          <div class="audio-track-copy">
            {render_kicker(format_track_label(track))}
            <h2 class="section-title">{escape(track.title)}</h2>
            {render_audio_runtime(track.duration_seconds)}
            {notes_html}
          </div>
          {render_audio_player(track.audio_output_path)}
          {render_action_row(actions)}
        </section>
        """
    ).strip()


def render_podcast_episode_card(
    episode: PodcastEpisode,
    rendered_entries_by_id: dict[str, RenderedEntry],
) -> str:
    matching_entry = rendered_entries_by_id.get(episode.target_entry_id or "")
    notes_html = f'<p class="audio-note">{escape(episode.notes)}</p>' if episode.notes else ""
    actions = [
        render_nav_link("Download MP3", episode.audio_output_path, download=True, icon_svg=DOWNLOAD_ICON_SVG),
    ]
    if matching_entry:
        actions.insert(0, render_nav_link("Read this chapter", matching_entry.entry.path, icon_svg=BOOK_ICON_SVG))
    return dedent(
        f"""\
        <section class="panel audio-track-card" id="{escape(episode_fragment_id(episode))}">
          <div class="audio-track-copy">
            {render_kicker(format_episode_label(episode), icon_svg=PODCAST_ICON_SVG)}
            <h2 class="section-title">{escape(episode.title)}</h2>
            {render_audio_runtime(episode.duration_seconds)}
            {notes_html}
          </div>
          {render_audio_player(episode.audio_output_path)}
          {render_action_row(actions)}
        </section>
        """
    ).strip()


def render_podcast_app_handoff(catalog: PodcastCatalog) -> str:
    app_links = [render_nav_link("Podcast RSS Feed", catalog.feed.feed_path, icon_svg=PODCAST_ICON_SVG)]
    if catalog.feed.apple_podcasts_url:
        app_links.append(render_nav_link("Listen in Apple Podcasts", catalog.feed.apple_podcasts_url))
    if catalog.feed.spotify_url:
        app_links.append(render_nav_link("Listen in Spotify", catalog.feed.spotify_url))
    subtitle_html = (
        f'<p class="audio-note">{escape(catalog.feed.subtitle)}</p>'
        if catalog.feed.subtitle
        else ""
    )
    return dedent(
        f"""\
        <section class="panel section-panel audio-feature-card">
          <div class="section-header">
            {render_section_title("Use a Podcast App", icon_svg=PODCAST_ICON_SVG)}
          </div>
          <p class="audio-summary">This page stays the easiest place to listen here. If you already use a podcast app, use the feed or app links below and the same episodes will still point back to this site.</p>
          {subtitle_html}
          {render_action_row(app_links)}
        </section>
        """
    ).strip()


def render_audiobook_page(
    site_title: str,
    catalog: AudiobookCatalog,
    rendered_entries: list[RenderedEntry],
) -> str:
    rendered_entries_by_id = {rendered.entry.entry_id: rendered for rendered in rendered_entries}
    track_cards = "\n".join(
        render_audiobook_track_card(track, rendered_entries_by_id)
        for track in catalog.tracks
    )
    full_audiobook_html = ""
    if catalog.full_audiobook:
        full_notes_html = f'<p class="audio-note">{escape(catalog.full_audiobook.notes)}</p>' if catalog.full_audiobook.notes else ""
        full_player_html = ""
        full_actions_html = ""
        full_summary = (
            "Start here if you want the full reading in one place, then use the individual tracks below whenever you want to return to a single section."
            if catalog.full_audiobook.is_available
            else "The individual tracks below are ready now, and the complete audiobook will appear here as one continuous listening option."
        )
        if catalog.full_audiobook.is_available:
            full_player_html = render_full_audiobook_player(catalog.full_audiobook)
            full_actions_html = render_action_row(
                [
                    render_nav_link(
                        "Download Full Audiobook",
                        catalog.full_audiobook.audio_output_path,
                        download=True,
                        icon_svg=DOWNLOAD_ICON_SVG,
                    )
                ]
            )
        full_audiobook_html = dedent(
            f"""\
            <section class="panel section-panel audio-feature-card" id="full-audiobook">
              <div class="section-header">
                {render_kicker("Full Audiobook")}
                <h2 class="section-title">{escape(catalog.full_audiobook.title)}</h2>
              </div>
              <p class="audio-summary">{escape(full_summary)}</p>
              {render_audio_runtime(catalog.full_audiobook.duration_seconds)}
              {full_notes_html}
              {full_player_html}
              {full_actions_html}
            </section>
            """
        ).strip()
    tracks_section_html = dedent(
        f"""\
        <section class="panel section-panel audio-section">
          <div class="section-header">
            {render_section_title("Individual Tracks", icon_svg=AUDIOBOOK_ICON_SVG)}
          </div>
          <p class="audio-summary">Choose a single section below if you would rather listen chapter by chapter.</p>
          <div class="audio-track-grid">
            {track_cards}
          </div>
        </section>
        """
    ).strip()
    body = dedent(
        f"""\
        <main class="site-shell">
          {render_site_header(site_title, current_section="audiobook")}

          <section class="hero audio-hero">
            {render_kicker("Whole-book listening", icon_svg=AUDIOBOOK_ICON_SVG)}
            <h1>{escape(catalog.title)}</h1>
            <p class="audio-summary">Start with the full audiobook just below, or choose any individual track farther down the page to revisit one section at a time.</p>
            {render_ai_attribution("ElevenLabs", "https://elevenlabs.io/")}
          </section>

          {full_audiobook_html}

          {tracks_section_html}
        </main>
        """
    )
    return render_layout(title=f"Audiobook — {site_title}", body_html=body)


def render_podcast_page(
    site_title: str,
    catalog: PodcastCatalog,
    rendered_entries: list[RenderedEntry],
) -> str:
    rendered_entries_by_id = {rendered.entry.entry_id: rendered for rendered in rendered_entries}
    episode_cards = "\n".join(
        render_podcast_episode_card(episode, rendered_entries_by_id)
        for episode in catalog.episodes
    )
    full_book_html = ""
    if catalog.full_book_episode:
        full_notes_html = (
            f'<p class="audio-note">{escape(catalog.full_book_episode.notes)}</p>'
            if catalog.full_book_episode.notes
            else ""
        )
        full_book_html = dedent(
            f"""\
            <section class="panel audio-track-card" id="full-book-podcast">
              <div class="audio-track-copy">
                {render_kicker("Whole-Book Episode", icon_svg=PODCAST_ICON_SVG)}
                <h2 class="section-title">{escape(catalog.full_book_episode.title)}</h2>
                {render_audio_runtime(catalog.full_book_episode.duration_seconds)}
                {full_notes_html}
              </div>
              {render_audio_player(catalog.full_book_episode.audio_output_path)}
              {render_action_row([render_nav_link("Download Whole-Book Episode", catalog.full_book_episode.audio_output_path, download=True, icon_svg=DOWNLOAD_ICON_SVG)])}
            </section>
            """
        ).strip()
    body = dedent(
        f"""\
        <main class="site-shell">
          {render_site_header(site_title, current_section="podcast")}

          <section class="hero audio-hero">
            {render_kicker("Family podcast", icon_svg=PODCAST_ICON_SVG)}
            <h1>{escape(catalog.title)}</h1>
            <p class="audio-summary">Press play on the whole-book episode or any chapter episode below, or download an MP3 to listen later on your phone, tablet, or computer.</p>
            {render_ai_attribution("NotebookLM", "https://notebooklm.google.com/")}
          </section>

          {render_podcast_app_handoff(catalog)}

          <section class="audio-track-grid">
            {full_book_html}
            {episode_cards}
          </section>
        </main>
        """
    )
    return render_layout(title=f"Podcast — {site_title}", body_html=body)


def render_source_library_page(
    site_title: str,
    assets: tuple[PublishedSourceAsset, ...],
) -> str:
    featured_asset = next((asset for asset in assets if asset.featured), None)
    supporting_assets = tuple(asset for asset in assets if not asset.featured)
    hero_actions: list[str] = []
    if featured_asset:
        featured_href = public_href(featured_asset.public_output_path)
        hero_actions.append(render_nav_link("Open Book PDF", featured_href, primary=True))
    page_title_html = (
        '<h1 class="section-title source-page-title">'
        '<span class="section-title-row">'
        f'<span class="section-title-icon">{BOOK_ICON_SVG}</span>'
        '<span>Archive Sources</span>'
        "</span>"
        "</h1>"
    )
    featured_section_html = ""
    if featured_asset:
        featured_section_html = dedent(
            f"""\
            <section class="panel section-panel source-section">
              <div class="section-header">
                {render_section_title("Onward to the Unknown", icon_svg=BOOK_ICON_SVG)}
              </div>
              <div class="source-library-grid">
                {render_source_library_card(featured_asset)}
              </div>
            </section>
            """
        ).strip()
    supporting_section_html = ""
    if supporting_assets:
        supporting_cards = "\n".join(render_source_library_card(asset) for asset in supporting_assets)
        supporting_section_html = dedent(
            f"""\
            <section class="panel section-panel source-section">
              <div class="section-header">
                {render_section_title("Photocopied Archive Documents", icon_svg=BOOK_ICON_SVG)}
              </div>
              <p class="source-section-note">{escape(PHOTOCOPY_SECTION_NOTE)}</p>
              <div class="source-library-grid">
                {supporting_cards}
              </div>
            </section>
            """
        ).strip()
    if not assets:
        supporting_section_html = dedent(
            """\
            <section class="panel section-panel source-section">
              <div class="section-header">
                <h2 class="section-title">Archive Shelf</h2>
              </div>
              <p class="audio-summary">This page is set aside for the original scans, photographs, and companion documents that belong with the family archive.</p>
            </section>
            """
        ).strip()
    body = dedent(
        f"""\
        <main class="site-shell">
          {render_site_header(site_title, current_section="archive-sources")}

          <section class="hero source-hero">
            <p class="audio-kicker">Original archive files</p>
            {page_title_html}
            <p class="audio-summary">These are the original book and family documents gathered with the archive. Open any item in your browser and take your time with it there.</p>
            {render_action_row(hero_actions)}
          </section>

          {featured_section_html}

          {supporting_section_html}
        </main>
        """
    )
    return render_layout(title=f"Archive Sources — {site_title}", body_html=body)


def render_home_hero_stat(value: str, label: str) -> str:
    return (
        '<div class="home-hero-stat">'
        f'<span class="home-hero-stat-value">{escape(value)}</span>'
        f'<span class="home-hero-stat-label">{escape(label)}</span>'
        "</div>"
    )


def render_book_page(
    site_title: str,
    manifest: dict,
    rendered_entries: list[RenderedEntry],
    source_assets: tuple[PublishedSourceAsset, ...],
) -> str:
    sections = {
        group.id: [rendered for rendered in rendered_entries if rendered.group.id == group.id]
        for group in ENTRY_GROUPS
    }
    featured_asset = next((asset for asset in source_assets if asset.featured), None)
    hero_actions = ""
    if featured_asset:
        hero_actions = render_action_row(
            [render_nav_link("Open the Book PDF", public_href(featured_asset.public_output_path), primary=True)]
        )
    section_html = "\n".join(
        render_index_section(group, sections[group.id])
        for group in ENTRY_GROUPS
        if sections[group.id]
    )
    body = dedent(
        f"""\
        <main class="site-shell">
          {render_site_header(site_title, current_section="book")}

          <section class="hero home-hero">
            <div class="home-hero-grid">
              <div class="home-hero-copy">
                <p class="audio-kicker">The Book</p>
                <h1>{escape(manifest["title"])}</h1>
                <p class="home-hero-summary">Read through the opening pages, move through the family stories, and finish with the closing archive at your own pace.</p>
                <p class="home-hero-note">Take your time and follow the names, memories, and places that feel familiar to you.</p>
                {hero_actions}
              </div>
            </div>
          </section>

          {section_html}
        </main>
        """
    )
    return render_layout(title=f"Book — {site_title}", body_html=body)


def render_index_page(
    site_title: str,
    manifest: dict,
    rendered_entries: list[RenderedEntry],
    *,
    audiobook_catalog: AudiobookCatalog | None = None,
    podcast_catalog: PodcastCatalog | None = None,
    source_assets: tuple[PublishedSourceAsset, ...] = (),
) -> str:
    family_story_count = len([rendered for rendered in rendered_entries if rendered.group.id == "family-stories"])
    book_section_count = len(rendered_entries) - family_story_count
    archive_file_count = len(source_assets)
    audio_track_count = len(audiobook_catalog.tracks) if audiobook_catalog else 0
    podcast_episode_count = 0
    if podcast_catalog:
        podcast_episode_count = len(podcast_catalog.episodes) + (1 if podcast_catalog.full_book_episode else 0)
    archive_file_count = len(source_assets)
    hero_summary = "Begin here, then choose the book, archive sources, audiobook, or podcast."
    hero_stats_items = [
        render_home_hero_stat(str(book_section_count), "Book pages and chapters"),
        render_home_hero_stat(str(family_story_count), "Family stories"),
        render_home_hero_stat(str(audio_track_count), "Audiobook tracks"),
        render_home_hero_stat(str(podcast_episode_count), "Podcast episodes"),
        render_home_hero_stat(str(archive_file_count), "Archive documents"),
    ]
    hero_stats = "".join(hero_stats_items)
    feature_panels = [
        render_index_book_panel(manifest, rendered_entries, source_assets),
        render_index_source_panel(source_assets),
        render_index_audiobook_panel(audiobook_catalog) if audiobook_catalog else "",
        render_index_podcast_panel(podcast_catalog) if podcast_catalog else "",
    ]
    home_feature_html = '<div class="home-feature-grid">' + "".join(panel for panel in feature_panels if panel) + "</div>"

    body = dedent(
        f"""\
        <main class="site-shell">
          {render_site_header(site_title, current_section="home")}

          <section class="hero home-hero">
            <div class="home-hero-grid">
              <div class="home-hero-copy">
                <p class="audio-kicker">A family keepsake</p>
                <h1>{escape(manifest["title"])}</h1>
                <p class="home-hero-summary">{escape(hero_summary)}</p>
                <p class="home-hero-note">Take your time and follow the names, memories, and places that feel familiar to you.</p>
              </div>
              <aside class="home-hero-aside" aria-label="Family collection summary">
                <p class="audio-kicker">What you'll find here</p>
                <div class="home-hero-stat-grid">{hero_stats}</div>
              </aside>
            </div>
          </section>

          {home_feature_html}
        </main>
        """
    )
    return render_layout(title=site_title, body_html=body)


def render_nav_link(
    label: str,
    href: str | None,
    *,
    primary: bool = False,
    download: bool = False,
    icon_svg: str | None = None,
) -> str:
    if href is None:
        return f'<span class="nav-placeholder">{escape(label)}</span>'
    class_name = "nav-button primary" if primary else "nav-button secondary"
    download_attr = " download" if download else ""
    label_html = escape(label)
    if icon_svg:
        label_html = (
            f'<span class="nav-button-content">'
            f'<span class="nav-button-icon">{icon_svg}</span>'
            f'<span class="nav-button-label">{label_html}</span>'
            f"</span>"
        )
    return f'<a class="{class_name}" href="{escape(href)}"{download_attr}>{label_html}</a>'


def render_section_title(label: str, *, icon_svg: str | None = None) -> str:
    label_html = escape(label)
    if not icon_svg:
        return f'<h2 class="section-title">{label_html}</h2>'
    return (
        '<h2 class="section-title">'
        '<span class="section-title-row">'
        f'<span class="section-title-icon">{icon_svg}</span>'
        f'<span>{label_html}</span>'
        "</span>"
        "</h2>"
    )


def render_directional_nav_link(label: str, href: str | None, *, direction: str) -> str:
    if direction == "back":
        directional_label = f"← {label}"
    elif direction == "next":
        directional_label = f"{label} →"
    else:
        raise ValueError(f"Unsupported navigation direction: {direction}")
    return render_nav_link(directional_label, href)


def render_home_nav_link(href: str = "index.html") -> str:
    return (
        f'<a class="nav-button primary home-button" href="{escape(href)}" '
        f'aria-label="Home" title="Home">{HOME_ICON_SVG}</a>'
    )


def render_site_title_link(site_title: str, href: str = "index.html") -> str:
    return f'<a class="site-title site-title-link" href="{escape(href)}">{escape(site_title)}</a>'


def render_site_menu(current_section: str | None = None) -> str:
    items = (
        ("home", "Home", "index.html", HOME_ICON_SVG),
        ("book", "The Book", DEFAULT_BOOK_PAGE_PATH, BOOK_ICON_SVG),
        ("archive-sources", "Archive Sources", DEFAULT_SOURCE_LIBRARY_PAGE_PATH, ARCHIVE_ICON_SVG),
        ("audiobook", "Audiobook", DEFAULT_AUDIOBOOK_PAGE_PATH, AUDIOBOOK_ICON_SVG),
        ("podcast", "Podcast", DEFAULT_PODCAST_PAGE_PATH, PODCAST_ICON_SVG),
    )
    links: list[str] = []
    for section_key, label, href, icon_svg in items:
        class_name = "site-menu-link"
        current_attr = ""
        if current_section == section_key:
            class_name += " is-current"
            current_attr = ' aria-current="page"'
        label_html = (
            '<span class="site-menu-link-content">'
            f'<span class="site-menu-link-icon">{icon_svg}</span>'
            f'<span>{escape(label)}</span>'
            "</span>"
        )
        links.append(f'<a class="{class_name}" href="{escape(href)}"{current_attr}>{label_html}</a>')
    return '<nav class="site-menu" aria-label="Site sections">' + "".join(links) + "</nav>"


def render_site_header(site_title: str, *, current_section: str | None = None) -> str:
    return (
        '<header class="site-header">'
        f"{render_site_title_link(site_title)}"
        f"{render_site_menu(current_section)}"
        "</header>"
    )


def entry_css_class(entry_id: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", entry_id.lower()).strip("-")
    return f"entry-{slug}" if slug else "entry-page"


def render_entry_page(
    site_title: str,
    rendered_entries: list[RenderedEntry],
    index: int,
    *,
    audiobook_track_by_entry_id: dict[str, AudiobookTrack] | None = None,
    podcast_episode_by_entry_id: dict[str, PodcastEpisode] | None = None,
) -> str:
    rendered = rendered_entries[index]
    previous_rendered = rendered_entries[index - 1] if index > 0 else None
    next_rendered = rendered_entries[index + 1] if index + 1 < len(rendered_entries) else None
    audiobook_track = (audiobook_track_by_entry_id or {}).get(rendered.entry.entry_id)
    audiobook_panel = render_entry_audiobook_panel(audiobook_track) if audiobook_track else ""
    podcast_episode = (podcast_episode_by_entry_id or {}).get(rendered.entry.entry_id)
    podcast_panel = render_entry_podcast_panel(podcast_episode) if podcast_episode else ""
    audio_panels = [panel for panel in (audiobook_panel, podcast_panel) if panel]
    audio_panel_html = ""
    if audio_panels:
        grid_class = "entry-audio-grid has-multiple" if len(audio_panels) > 1 else "entry-audio-grid has-single"
        audio_panel_html = f'<div class="{grid_class}">' + "".join(audio_panels) + "</div>"
    article_html = rendered.article_html
    if rendered.entry.kind == "chapter":
        article_html = decorate_primary_heading_with_icon(article_html, BOOK_ICON_SVG)

    body = dedent(
        f"""\
        <main class="site-shell">
          {render_site_header(site_title, current_section="book")}

          <nav class="page-nav" aria-label="Book entry navigation">
            {render_directional_nav_link(previous_rendered.display_title if previous_rendered else "Previous", previous_rendered.entry.path if previous_rendered else None, direction="back")}
            {render_home_nav_link()}
            {render_directional_nav_link(next_rendered.display_title if next_rendered else "Next", next_rendered.entry.path if next_rendered else None, direction="next")}
          </nav>

          {audio_panel_html}

          <article class="article-card {entry_css_class(rendered.entry.entry_id)}">
            {article_html}
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
    supplement_rows: list[SupplementAuditRow],
    source_assets: tuple[PublishedSourceAsset, ...],
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
        "supplement_count": len(supplement_rows),
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
        "supplements": [
            {
                "supplement_id": row.supplement_id,
                "title": row.title,
                "group_id": row.group.id,
                "group_label": row.group.label,
                "status": row.status,
                "output_path": row.output_path,
                "bundle_root": row.bundle_root,
                "source_pdf_path": row.source_pdf_path,
                "source_entry_ids": list(row.source_entry_ids),
                "absorbed_entry_ids": list(row.absorbed_entry_ids),
                "rationale": row.rationale,
            }
            for row in supplement_rows
        ],
        "source_library": {
            "page_path": DEFAULT_SOURCE_LIBRARY_PAGE_PATH if source_assets else None,
            "published_count": len(source_assets),
            "files": [
                {
                    "title": asset.title,
                    "filename": asset.filename,
                    "kind_label": asset.kind_label,
                    "source_path": asset.relative_input_path,
                    "output_path": asset.public_output_path,
                    "size_bytes": asset.size_bytes,
                    "featured": asset.featured,
                }
                for asset in source_assets
            ],
        },
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def build_family_site(
    source_dir: Path,
    output_dir: Path,
    *,
    entry_ids: list[str] | None = None,
    site_title: str = DEFAULT_SITE_TITLE,
    audiobook_manifest_path: Path | None = DEFAULT_AUDIOBOOK_MANIFEST_PATH,
    podcast_manifest_path: Path | None = DEFAULT_PODCAST_MANIFEST_PATH,
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
    supplements = load_family_story_supplements(source_dir)
    published_source_assets = discover_published_source_assets(source_dir, supplements)
    published_source_assets_by_path = {
        asset.source_path.resolve(): asset
        for asset in published_source_assets
    }
    copy_published_source_assets(published_source_assets, output_dir)
    write_text(internal_dir / "source-library.json", serialize_source_library_manifest(published_source_assets))
    absorbed_entry_output_map = absorbed_output_paths(selected_entries)
    absorbed_entries_by_target_id = absorbed_entries_by_target(selected_entries)
    rendered_entries = build_rendered_entries(
        source_dir,
        selected_entries,
        provenance_rows_by_entry_id=provenance_rows,
        absorbed_entry_ids=set(absorbed_entry_output_map),
        absorbed_entries_by_target_id=absorbed_entries_by_target_id,
    )
    supplement_rendered_rows: list[tuple[FamilyStorySupplement, RenderedEntry, SupplementAuditRow]] = []
    for supplement in supplements:
        rendered_entry, audit_row = build_supplement_rendered_entry(
            supplement,
            output_dir=output_dir,
            internal_dir=internal_dir,
            published_source_assets_by_path=published_source_assets_by_path,
        )
        supplement_rendered_rows.append((supplement, rendered_entry, audit_row))
    rendered_entries = insert_supplement_rendered_entries(
        rendered_entries,
        [(supplement, rendered_entry) for supplement, rendered_entry, _audit_row in supplement_rendered_rows],
    )
    rendered_manifest_ids = {
        source_entry_id
        for rendered in rendered_entries
        for source_entry_id in rendered.source_entry_ids
        if source_entry_id in {entry.entry_id for entry in selected_entries}
    }
    skipped_entry_ids = {entry.entry_id for entry in selected_entries if entry.entry_id not in rendered_manifest_ids}
    skipped_entry_ids -= set(absorbed_entry_output_map)
    audit_rows = build_omission_audit(
        all_entries,
        selected_entries,
        skipped_entry_ids=skipped_entry_ids,
        absorbed_entry_output_paths=absorbed_entry_output_map,
    )
    audiobook_catalog = load_audiobook_catalog(audiobook_manifest_path)
    audiobook_track_by_entry_id: dict[str, AudiobookTrack] = {}
    if audiobook_catalog:
        rendered_entry_ids = {rendered.entry.entry_id for rendered in rendered_entries}
        missing_target_entry_ids = sorted(
            {
                track.target_entry_id
                for track in audiobook_catalog.tracks
                if track.target_entry_id and track.target_entry_id not in rendered_entry_ids
            }
        )
        if missing_target_entry_ids:
            raise SystemExit(
                "Audiobook manifest target_entry_id value(s) do not match the rendered site: "
                + ", ".join(missing_target_entry_ids)
            )
        audiobook_track_by_entry_id = {
            track.target_entry_id: track
            for track in audiobook_catalog.tracks
            if track.target_entry_id
        }
        copy_audiobook_public_assets(audiobook_catalog, output_dir)
        write_text(
            internal_dir / "audiobook" / "manifest.json",
            audiobook_catalog.manifest_path.read_text(encoding="utf-8"),
        )
    podcast_catalog = load_podcast_catalog(podcast_manifest_path)
    podcast_episode_by_entry_id: dict[str, PodcastEpisode] = {}
    if podcast_catalog:
        rendered_entry_ids = {rendered.entry.entry_id for rendered in rendered_entries}
        missing_target_entry_ids = sorted(
            {
                episode.target_entry_id
                for episode in podcast_catalog.episodes
                if episode.target_entry_id and episode.target_entry_id not in rendered_entry_ids
            }
        )
        if missing_target_entry_ids:
            raise SystemExit(
                "Podcast manifest target_entry_id value(s) do not match the rendered site: "
                + ", ".join(missing_target_entry_ids)
            )
        podcast_episode_by_entry_id = {
            episode.target_entry_id: episode
            for episode in podcast_catalog.episodes
            if episode.target_entry_id
        }
        copy_podcast_public_assets(podcast_catalog, output_dir)
        write_text(
            internal_dir / "podcast" / "manifest.json",
            podcast_catalog.manifest_path.read_text(encoding="utf-8"),
        )
        write_text(
            internal_dir / "podcast" / Path(podcast_catalog.prompt_manifest_path).name,
            podcast_catalog.prompt_source_path.read_text(encoding="utf-8"),
        )
        write_text(
            output_dir / podcast_catalog.feed.feed_path,
            render_podcast_feed(podcast_catalog),
        )
    supplement_audit_rows = [audit_row for _supplement, _rendered_entry, audit_row in supplement_rendered_rows]
    omission_audit_path = internal_dir / "omission-audit.json"

    write_text(
        omission_audit_path,
        serialize_omission_audit(
            manifest,
            site_title,
            audit_rows,
            supplement_audit_rows,
            published_source_assets,
        ),
    )

    for rendered in rendered_entries:
        write_text(
            internal_dir / "provenance" / "entries" / f"{rendered.entry.entry_id}.json",
            json.dumps(list(rendered.provenance_rows), indent=2, sort_keys=True) + "\n",
        )

    for index, rendered in enumerate(rendered_entries):
        write_text(
            output_dir / rendered.entry.path,
            render_entry_page(
                site_title=site_title,
                rendered_entries=rendered_entries,
                index=index,
                audiobook_track_by_entry_id=audiobook_track_by_entry_id,
                podcast_episode_by_entry_id=podcast_episode_by_entry_id,
            ),
        )

    if audiobook_catalog:
        write_text(
            output_dir / DEFAULT_AUDIOBOOK_PAGE_PATH,
            render_audiobook_page(
                site_title=site_title,
                catalog=audiobook_catalog,
                rendered_entries=rendered_entries,
            ),
        )

    write_text(
        output_dir / DEFAULT_SOURCE_LIBRARY_PAGE_PATH,
        render_source_library_page(
            site_title=site_title,
            assets=published_source_assets,
        ),
    )

    write_text(
        output_dir / DEFAULT_BOOK_PAGE_PATH,
        render_book_page(
            site_title=site_title,
            manifest=manifest,
            rendered_entries=rendered_entries,
            source_assets=published_source_assets,
        ),
    )

    if podcast_catalog:
        write_text(
            output_dir / podcast_catalog.feed.page_path,
            render_podcast_page(
                site_title=site_title,
                catalog=podcast_catalog,
                rendered_entries=rendered_entries,
            ),
        )

    write_text(
        output_dir / "index.html",
        render_index_page(
            site_title=site_title,
            manifest=manifest,
            rendered_entries=rendered_entries,
            audiobook_catalog=audiobook_catalog,
            podcast_catalog=podcast_catalog,
            source_assets=published_source_assets,
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
