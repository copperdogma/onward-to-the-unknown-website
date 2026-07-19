from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import reportlab
from PIL import Image, ImageEnhance, ImageFilter
from pypdf import PdfReader
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT_PATH = REPO_ROOT / "outreach" / "reunion-flyer.json"
FONT_REGULAR_NAME = "OnwardVera"
FONT_BOLD_NAME = "OnwardVeraBold"
REQUIRED_OUTPUT_KEYS = (
    "letter_pdf",
    "letter_preview_png",
    "phone_png",
    "qr_png",
    "build_report_json",
)
HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


class ReunionFlyerError(RuntimeError):
    pass


@dataclass(frozen=True)
class FlyerContract:
    path: Path
    repo_root: Path
    payload: dict[str, Any]

    def section(self, name: str) -> dict[str, Any]:
        value = self.payload.get(name)
        if not isinstance(value, dict):
            raise ReunionFlyerError(f"Flyer contract requires a `{name}` object.")
        return value

    def output_path(self, key: str) -> Path:
        value = self.section("outputs").get(key)
        if not isinstance(value, str) or not value.strip():
            raise ReunionFlyerError(f"Flyer contract requires output path `{key}`.")
        return self.repo_root / value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _require_string(payload: dict[str, Any], key: str, context: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ReunionFlyerError(f"{context} requires a non-empty `{key}` string.")
    return value.strip()


def _require_number(payload: dict[str, Any], key: str, context: str) -> float:
    value = payload.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ReunionFlyerError(f"{context} requires numeric `{key}`.")
    return float(value)


def _require_strings(payload: dict[str, Any], key: str, context: str, *, count: int | None = None) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        raise ReunionFlyerError(f"{context} requires a non-empty `{key}` string list.")
    if count is not None and len(value) != count:
        raise ReunionFlyerError(f"{context} requires exactly {count} values in `{key}`.")
    return [item.strip() for item in value]


def _font_paths() -> tuple[Path, Path, Path]:
    font_dir = Path(reportlab.__file__).resolve().parent / "fonts"
    return font_dir / "Vera.ttf", font_dir / "VeraBd.ttf", font_dir / "bitstream-vera-license.txt"


def _register_fonts() -> tuple[Path, Path, Path]:
    regular, bold, license_path = _font_paths()
    for path in (regular, bold, license_path):
        if not path.is_file():
            raise ReunionFlyerError(f"Required ReportLab font resource is missing: {path}")
    if FONT_REGULAR_NAME not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT_REGULAR_NAME, regular))
    if FONT_BOLD_NAME not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT_BOLD_NAME, bold))
    return regular, bold, license_path


def _validate_text_width(text: str, font: str, size: float, maximum: float, label: str) -> None:
    width = pdfmetrics.stringWidth(text, font, size)
    if width > maximum:
        raise ReunionFlyerError(f"{label} is {width:.2f} points wide and exceeds the {maximum:.2f}-point slot.")


def _validate_layout_capacity(contract: FlyerContract) -> None:
    _register_fonts()
    book = contract.section("book")
    typography = contract.section("typography")
    print_type = typography.get("print")
    phone_type = typography.get("phone")
    if not isinstance(print_type, dict) or not isinstance(phone_type, dict):
        raise ReunionFlyerError("Flyer typography requires `print` and `phone` objects.")
    letter = contract.section("surfaces").get("letter")
    phone = contract.section("surfaces").get("phone")
    if not isinstance(letter, dict) or not isinstance(phone, dict):
        raise ReunionFlyerError("Flyer surfaces require `letter` and `phone` objects.")

    print_width = _require_number(letter, "width_points", "Letter surface")
    print_margin = _require_number(letter, "safe_margin_points", "Letter surface")
    print_slot = print_width - 2 * print_margin
    title_lines = _require_strings(book, "title_lines", "Book", count=2)
    for index, line in enumerate(title_lines, start=1):
        _validate_text_width(
            line,
            FONT_BOLD_NAME,
            _require_number(print_type, "title", "Print typography"),
            print_slot,
            f"Print title line {index}",
        )
    for key, font_key, font_name in (
        ("subtitle", "subtitle", FONT_REGULAR_NAME),
        ("free_headline", "free_headline", FONT_BOLD_NAME),
        ("camera_instruction", "camera_instruction", FONT_REGULAR_NAME),
        ("display_hostname", "hostname", FONT_BOLD_NAME),
    ):
        _validate_text_width(
            _require_string(book, key, "Book"),
            font_name,
            _require_number(print_type, font_key, "Print typography"),
            print_slot,
            f"Print {key}",
        )
    for index, action in enumerate(_require_strings(book, "actions", "Book", count=4), start=1):
        _validate_text_width(
            action,
            FONT_REGULAR_NAME,
            _require_number(print_type, "actions", "Print typography"),
            250,
            f"Print action {index}",
        )
    for index, row in enumerate(_require_strings(book, "family_name_rows", "Book", count=3), start=1):
        _validate_text_width(
            row,
            FONT_REGULAR_NAME,
            _require_number(print_type, "family_names", "Print typography"),
            print_slot,
            f"Family-name row {index}",
        )

    phone_width = _require_number(phone, "width_pixels", "Phone surface")
    phone_margin = _require_number(phone, "safe_margin_pixels", "Phone surface")
    phone_slot = phone_width - 2 * phone_margin
    for index, line in enumerate(title_lines, start=1):
        _validate_text_width(
            line,
            FONT_BOLD_NAME,
            _require_number(phone_type, "title", "Phone typography"),
            phone_slot,
            f"Phone title line {index}",
        )
    _validate_text_width(
        _require_string(book, "subtitle", "Book"),
        FONT_REGULAR_NAME,
        _require_number(phone_type, "subtitle", "Phone typography"),
        phone_slot,
        "Phone subtitle",
    )
    for index, line in enumerate(_phone_headline_lines(_require_string(book, "free_headline", "Book")), start=1):
        _validate_text_width(
            line,
            FONT_BOLD_NAME,
            _require_number(phone_type, "free_headline", "Phone typography"),
            phone_slot,
            f"Phone free-headline line {index}",
        )


def load_contract(path: Path = DEFAULT_CONTRACT_PATH, *, repo_root: Path | None = None) -> FlyerContract:
    resolved_path = path.resolve()
    root = (repo_root or REPO_ROOT).resolve()
    try:
        payload = json.loads(resolved_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReunionFlyerError(f"Flyer contract is missing: {resolved_path}") from exc
    except json.JSONDecodeError as exc:
        raise ReunionFlyerError(f"Flyer contract is invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReunionFlyerError("Flyer contract root must be an object.")
    if payload.get("schema_version") != "onward_reunion_flyer_v1":
        raise ReunionFlyerError("Flyer contract has an unsupported `schema_version`.")

    contract = FlyerContract(resolved_path, root, payload)
    book = contract.section("book")
    for key in (
        "title",
        "subtitle",
        "eyebrow",
        "free_headline",
        "camera_instruction",
        "canonical_url",
        "display_hostname",
        "family_heading",
        "phone_availability",
    ):
        _require_string(book, key, "Book")
    _require_strings(book, "title_lines", "Book", count=2)
    _require_strings(book, "actions", "Book", count=4)
    _require_strings(book, "family_name_rows", "Book", count=3)
    prohibited = _require_strings(book, "prohibited_wording", "Book")
    all_copy = " ".join(str(value) for value in book.values()).casefold()
    for phrase in prohibited:
        occurrences = all_copy.count(phrase.casefold())
        if occurrences > 1:
            raise ReunionFlyerError(f"Flyer reader copy contains prohibited wording: {phrase}")

    parsed_url = urlparse(_require_string(book, "canonical_url", "Book"))
    if parsed_url.scheme != "https" or not parsed_url.hostname or parsed_url.query or parsed_url.fragment:
        raise ReunionFlyerError("Flyer canonical URL must be a plain first-party HTTPS URL.")
    if parsed_url.hostname != _require_string(book, "display_hostname", "Book"):
        raise ReunionFlyerError("Flyer display hostname must exactly match the canonical URL hostname.")

    cover = contract.section("cover")
    cover_path = root / _require_string(cover, "source_path", "Cover")
    expected_width = int(_require_number(cover, "width_pixels", "Cover"))
    expected_height = int(_require_number(cover, "height_pixels", "Cover"))
    expected_hash = _require_string(cover, "sha256", "Cover")
    if not cover_path.is_file():
        raise ReunionFlyerError(f"Canonical cover is missing: {cover_path}")
    with Image.open(cover_path) as image:
        if image.size != (expected_width, expected_height):
            raise ReunionFlyerError(
                f"Canonical cover dimensions are {image.size}, expected {(expected_width, expected_height)}."
            )
    actual_hash = _sha256(cover_path)
    if actual_hash != expected_hash:
        raise ReunionFlyerError(f"Canonical cover SHA-256 is {actual_hash}, expected {expected_hash}.")

    palette = contract.section("palette")
    for key in ("paper", "ink", "muted", "light_rule", "deep", "secondary_deep", "accent", "secondary_accent", "qr"):
        value = _require_string(palette, key, "Palette")
        if not HEX_COLOR_PATTERN.fullmatch(value):
            raise ReunionFlyerError(f"Palette `{key}` must be a six-digit hex color.")
    if palette["paper"].casefold() != "#ffffff" or palette["qr"].casefold() != "#000000":
        raise ReunionFlyerError("Flyer paper must be #ffffff and QR modules must be #000000.")

    typography = contract.section("typography")
    print_type = typography.get("print")
    phone_type = typography.get("phone")
    if not isinstance(print_type, dict) or not isinstance(phone_type, dict):
        raise ReunionFlyerError("Flyer typography requires `print` and `phone` objects.")
    minimum_print = _require_number(typography, "minimum_essential_print_points", "Typography")
    minimum_host = _require_number(typography, "minimum_hostname_print_points", "Typography")
    for key in ("camera_instruction", "actions", "family_names"):
        if _require_number(print_type, key, "Print typography") < minimum_print:
            raise ReunionFlyerError(f"Print `{key}` is below the essential {minimum_print:g}-point floor.")
    if _require_number(print_type, "hostname", "Print typography") < minimum_host:
        raise ReunionFlyerError(f"Print hostname is below the {minimum_host:g}-point floor.")
    for key in ("eyebrow", "title", "subtitle", "free_headline", "family_heading"):
        if _require_number(print_type, key, "Print typography") <= 0:
            raise ReunionFlyerError(f"Print `{key}` must be positive.")
    for key in ("eyebrow", "title", "subtitle", "free_headline", "camera_instruction", "hostname", "availability"):
        if _require_number(phone_type, key, "Phone typography") <= 0:
            raise ReunionFlyerError(f"Phone `{key}` must be positive.")

    qr = contract.section("qr")
    version = int(_require_number(qr, "version", "QR"))
    data_modules = int(_require_number(qr, "data_modules", "QR"))
    quiet_modules = int(_require_number(qr, "quiet_zone_modules", "QR"))
    total_modules = int(_require_number(qr, "total_modules", "QR"))
    if qr.get("error_correction") != "Q" or version != 4 or quiet_modules != 4:
        raise ReunionFlyerError("Flyer QR must use version 4, Q correction, and a four-module quiet zone.")
    if data_modules != 21 + 4 * (version - 1) or total_modules != data_modules + 2 * quiet_modules:
        raise ReunionFlyerError("Flyer QR module geometry is inconsistent with its version and quiet zone.")
    module_pixels = int(_require_number(qr, "standalone_module_pixels", "QR"))
    if int(_require_number(qr, "standalone_size_pixels", "QR")) != total_modules * module_pixels:
        raise ReunionFlyerError("Standalone QR size must be an integer multiple of the total module count.")
    if _require_number(qr, "print_size_points", "QR") != _require_number(cover, "print_height_points", "Cover"):
        raise ReunionFlyerError("Printed cover and QR heights must match exactly.")

    surfaces = contract.section("surfaces")
    letter = surfaces.get("letter")
    phone = surfaces.get("phone")
    if not isinstance(letter, dict) or not isinstance(phone, dict):
        raise ReunionFlyerError("Flyer surfaces require `letter` and `phone` objects.")
    exact_values = {
        "letter.width_points": (_require_number(letter, "width_points", "Letter surface"), 612),
        "letter.height_points": (_require_number(letter, "height_points", "Letter surface"), 792),
        "letter.preview_width_pixels": (_require_number(letter, "preview_width_pixels", "Letter surface"), 2550),
        "letter.preview_height_pixels": (_require_number(letter, "preview_height_pixels", "Letter surface"), 3300),
        "letter.preview_dpi": (_require_number(letter, "preview_dpi", "Letter surface"), 300),
        "phone.width_pixels": (_require_number(phone, "width_pixels", "Phone surface"), 1080),
        "phone.height_pixels": (_require_number(phone, "height_pixels", "Phone surface"), 1920),
    }
    for label, (actual, expected) in exact_values.items():
        if actual != expected:
            raise ReunionFlyerError(f"{label} must be {expected:g}, got {actual:g}.")
    if not 0 < _require_number(letter, "maximum_non_white_ratio", "Letter surface") <= 0.27:
        raise ReunionFlyerError("Letter non-white ceiling must be positive and no higher than 0.27.")
    if not 0 < _require_number(phone, "maximum_non_white_ratio", "Phone surface") <= 0.2:
        raise ReunionFlyerError("Phone non-white ceiling must be positive and no higher than 0.2.")

    outputs = contract.section("outputs")
    if set(outputs) != set(REQUIRED_OUTPUT_KEYS):
        raise ReunionFlyerError(f"Flyer outputs must contain exactly: {', '.join(REQUIRED_OUTPUT_KEYS)}.")
    for key in REQUIRED_OUTPUT_KEYS:
        relative = Path(_require_string(outputs, key, "Outputs"))
        if relative.is_absolute() or relative.parts[:2] != ("output", "outreach"):
            raise ReunionFlyerError(f"Output `{key}` must be a relative path under output/outreach/.")

    cover_width = _cover_print_width(contract)
    row_width = cover_width + _require_number(letter, "cover_qr_gap_points", "Letter surface") + _require_number(
        qr, "print_size_points", "QR"
    )
    available = _require_number(letter, "width_points", "Letter surface") - 2 * _require_number(
        letter, "safe_margin_points", "Letter surface"
    )
    if row_width > available:
        raise ReunionFlyerError(f"Cover/QR row is {row_width:.2f} points wide and exceeds the {available:.2f}-point safe area.")

    _validate_layout_capacity(contract)
    return contract


def _cover_print_width(contract: FlyerContract) -> float:
    cover = contract.section("cover")
    return (
        _require_number(cover, "print_height_points", "Cover")
        * _require_number(cover, "width_pixels", "Cover")
        / _require_number(cover, "height_pixels", "Cover")
    )


def _phone_headline_lines(headline: str) -> list[str]:
    if " — " in headline:
        left, right = headline.split(" — ", 1)
        return [left, right]
    return [headline]


def _draw_centered(page: canvas.Canvas, text: str, y: float, font: str, size: float, color: str, width: float) -> None:
    page.setFillColor(HexColor(color))
    page.setFont(font, size)
    page.drawCentredString(width / 2, y, text)


def _qr_widget(contract: FlyerContract) -> QrCodeWidget:
    book = contract.section("book")
    qr = contract.section("qr")
    widget = QrCodeWidget(
        _require_string(book, "canonical_url", "Book"),
        barLevel=_require_string(qr, "error_correction", "QR"),
        qrVersion=int(_require_number(qr, "version", "QR")),
        barBorder=int(_require_number(qr, "quiet_zone_modules", "QR")),
        barFillColor=black,
    )
    widget.getBounds()
    if widget.qr.version != int(_require_number(qr, "version", "QR")) or len(widget.qr.modules) != int(
        _require_number(qr, "data_modules", "QR")
    ):
        raise ReunionFlyerError("ReportLab QR encoder did not produce the declared version/module geometry.")
    return widget


def _draw_qr(page: canvas.Canvas, contract: FlyerContract, x: float, y: float, size: float) -> None:
    widget = _qr_widget(contract)
    x1, y1, x2, y2 = widget.getBounds()
    scale = size / max(x2 - x1, y2 - y1)
    drawing = Drawing(size, size, transform=[scale, 0, 0, scale, -x1 * scale, -y1 * scale])
    drawing.add(widget)
    renderPDF.draw(drawing, page, x, y)


def _base_canvas(path: Path, size: tuple[float, float], title: str) -> canvas.Canvas:
    path.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(path), pagesize=size, pageCompression=1, invariant=1)
    page.setTitle(title)
    page.setAuthor("The L'Heureux Family")
    page.setSubject("Printable family-book reunion flyer")
    page.setFillColor(white)
    page.rect(0, 0, size[0], size[1], stroke=0, fill=1)
    return page


def _build_letter_pdf(contract: FlyerContract, path: Path) -> dict[str, float]:
    book = contract.section("book")
    palette = contract.section("palette")
    typography = contract.section("typography")["print"]
    cover = contract.section("cover")
    qr = contract.section("qr")
    letter = contract.section("surfaces")["letter"]
    width = _require_number(letter, "width_points", "Letter surface")
    height = _require_number(letter, "height_points", "Letter surface")
    page = _base_canvas(path, (width, height), f"{book['title']} reunion flyer")

    page.setStrokeColor(HexColor(palette["accent"]))
    page.setLineWidth(2.4)
    page.line(36, 766, 576, 766)
    page.setStrokeColor(HexColor(palette["secondary_accent"]))
    page.setLineWidth(1.2)
    page.line(36, 760, 576, 760)
    _draw_centered(page, book["eyebrow"], 742, FONT_BOLD_NAME, typography["eyebrow"], palette["accent"], width)
    _draw_centered(page, book["title_lines"][0], 696, FONT_BOLD_NAME, typography["title"], palette["deep"], width)
    _draw_centered(page, book["title_lines"][1], 649, FONT_BOLD_NAME, typography["title"], palette["deep"], width)
    _draw_centered(page, book["subtitle"], 617, FONT_REGULAR_NAME, typography["subtitle"], palette["ink"], width)
    _draw_centered(
        page, book["free_headline"], 590, FONT_BOLD_NAME, typography["free_headline"], palette["secondary_deep"], width
    )
    _draw_centered(
        page, book["camera_instruction"], 565, FONT_REGULAR_NAME, typography["camera_instruction"], palette["ink"], width
    )

    cover_width = _cover_print_width(contract)
    cover_height = _require_number(cover, "print_height_points", "Cover")
    qr_size = _require_number(qr, "print_size_points", "QR")
    gap = _require_number(letter, "cover_qr_gap_points", "Letter surface")
    row_width = cover_width + gap + qr_size
    row_x = (width - row_width) / 2
    row_y = _require_number(letter, "cover_qr_y_points", "Letter surface")
    cover_path = contract.repo_root / cover["source_path"]
    page.drawImage(
        str(cover_path),
        row_x,
        row_y,
        width=cover_width,
        height=cover_height,
        preserveAspectRatio=True,
        anchor="c",
        mask=None,
    )
    qr_x = row_x + cover_width + gap
    _draw_qr(page, contract, qr_x, row_y, qr_size)

    _draw_centered(page, book["display_hostname"], 226, FONT_BOLD_NAME, typography["hostname"], palette["accent"], width)
    action_x = (49, 313)
    action_y = (188, 160)
    page.setFont(FONT_REGULAR_NAME, typography["actions"])
    page.setFillColor(HexColor(palette["ink"]))
    page.setStrokeColor(HexColor(palette["secondary_accent"]))
    for index, action in enumerate(book["actions"]):
        column = index // 2
        row = index % 2
        x = action_x[column]
        y = action_y[row]
        page.setFillColor(HexColor(palette["secondary_accent"]))
        page.circle(x - 13, y + 5, 2.4, stroke=0, fill=1)
        page.setFillColor(HexColor(palette["ink"]))
        page.drawString(x, y, action)

    _draw_centered(
        page, book["family_heading"], 128, FONT_BOLD_NAME, typography["family_heading"], palette["muted"], width
    )
    for name_row, y in zip(book["family_name_rows"], (98, 71, 44), strict=True):
        _draw_centered(page, name_row, y, FONT_REGULAR_NAME, typography["family_names"], palette["deep"], width)
    page.setStrokeColor(HexColor(palette["light_rule"]))
    page.setLineWidth(1)
    page.line(36, 27, 576, 27)
    page.setStrokeColor(HexColor(palette["secondary_accent"]))
    page.setLineWidth(1.2)
    page.line(246, 21, 366, 21)
    page.showPage()
    page.save()
    return {
        "cover_x_points": row_x,
        "cover_y_points": row_y,
        "cover_width_points": cover_width,
        "cover_height_points": cover_height,
        "cover_effective_ppi": cover["height_pixels"] / (cover_height / 72),
        "cover_qr_gap_points": gap,
        "qr_x_points": qr_x,
        "qr_y_points": row_y,
        "qr_size_points": qr_size,
        "row_width_points": row_width,
    }


def _build_phone_pdf(contract: FlyerContract, path: Path) -> None:
    book = contract.section("book")
    palette = contract.section("palette")
    typography = contract.section("typography")["phone"]
    qr = contract.section("qr")
    phone = contract.section("surfaces")["phone"]
    width = _require_number(phone, "width_pixels", "Phone surface")
    height = _require_number(phone, "height_pixels", "Phone surface")
    page = _base_canvas(path, (width, height), f"{book['title']} phone QR card")
    page.setStrokeColor(HexColor(palette["accent"]))
    page.setLineWidth(8)
    page.line(72, 1845, 1008, 1845)
    page.setStrokeColor(HexColor(palette["secondary_accent"]))
    page.setLineWidth(4)
    page.line(72, 1827, 1008, 1827)
    _draw_centered(page, book["eyebrow"], 1755, FONT_BOLD_NAME, typography["eyebrow"], palette["accent"], width)
    _draw_centered(page, book["title_lines"][0], 1655, FONT_BOLD_NAME, typography["title"], palette["deep"], width)
    _draw_centered(page, book["title_lines"][1], 1555, FONT_BOLD_NAME, typography["title"], palette["deep"], width)
    _draw_centered(page, book["subtitle"], 1470, FONT_REGULAR_NAME, typography["subtitle"], palette["ink"], width)
    for line, y in zip(_phone_headline_lines(book["free_headline"]), (1410, 1355), strict=True):
        _draw_centered(page, line, y, FONT_BOLD_NAME, typography["free_headline"], palette["secondary_deep"], width)
    _draw_centered(
        page, book["camera_instruction"], 1295, FONT_REGULAR_NAME, typography["camera_instruction"], palette["ink"], width
    )
    qr_size = _require_number(qr, "phone_size_pixels", "QR")
    _draw_qr(page, contract, (width - qr_size) / 2, 430, qr_size)
    _draw_centered(page, book["display_hostname"], 335, FONT_BOLD_NAME, typography["hostname"], palette["accent"], width)
    _draw_centered(
        page, book["phone_availability"], 255, FONT_BOLD_NAME, typography["availability"], palette["ink"], width
    )
    page.setStrokeColor(HexColor(palette["light_rule"]))
    page.setLineWidth(3)
    page.line(72, 132, 1008, 132)
    page.setStrokeColor(HexColor(palette["secondary_accent"]))
    page.setLineWidth(4)
    page.line(390, 112, 690, 112)
    page.showPage()
    page.save()


def _build_standalone_qr(contract: FlyerContract, path: Path) -> None:
    qr = contract.section("qr")
    widget = _qr_widget(contract)
    modules = widget.qr.modules
    quiet = int(_require_number(qr, "quiet_zone_modules", "QR"))
    module_pixels = int(_require_number(qr, "standalone_module_pixels", "QR"))
    total = len(modules) + 2 * quiet
    image = Image.new("RGB", (total * module_pixels, total * module_pixels), (255, 255, 255))
    pixels = image.load()
    for row_index, row in enumerate(modules):
        for column_index, enabled in enumerate(row):
            if not enabled:
                continue
            left = (column_index + quiet) * module_pixels
            top = (row_index + quiet) * module_pixels
            for y in range(top, top + module_pixels):
                for x in range(left, left + module_pixels):
                    pixels[x, y] = (0, 0, 0)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=False)


def _render_pdf(pdf_path: Path, output_path: Path, dpi: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = output_path.with_suffix("")
    completed = subprocess.run(
        ["pdftocairo", "-png", "-singlefile", "-r", str(dpi), str(pdf_path), str(prefix)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise ReunionFlyerError(f"Poppler failed to render {pdf_path}: {completed.stderr.strip()}")
    generated = prefix.with_suffix(".png")
    if generated != output_path:
        generated.replace(output_path)


def _artifact_record(path: Path) -> dict[str, Any]:
    record: dict[str, Any] = {"path": str(path.relative_to(REPO_ROOT)) if path.is_relative_to(REPO_ROOT) else str(path)}
    record["bytes"] = path.stat().st_size
    record["sha256"] = _sha256(path)
    if path.suffix.casefold() == ".png":
        with Image.open(path) as image:
            record["pixel_dimensions"] = list(image.size)
            record["mode"] = image.mode
    return record


def _tool_version(command: list[str]) -> str:
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    output = (completed.stdout or completed.stderr).strip().splitlines()
    return output[0] if output else "unavailable"


def build_artifacts(contract_path: Path = DEFAULT_CONTRACT_PATH, *, repo_root: Path | None = None) -> dict[str, Any]:
    contract = load_contract(contract_path, repo_root=repo_root)
    regular, bold, license_path = _register_fonts()
    for key in REQUIRED_OUTPUT_KEYS:
        contract.output_path(key).parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = contract.repo_root / "tmp" / "pdfs" / "outreach"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    letter_pdf = contract.output_path("letter_pdf")
    phone_pdf = tmp_dir / "onward-to-the-unknown-phone-qr.pdf"
    layout = _build_letter_pdf(contract, letter_pdf)
    _build_phone_pdf(contract, phone_pdf)
    _render_pdf(letter_pdf, contract.output_path("letter_preview_png"), 300)
    _render_pdf(phone_pdf, contract.output_path("phone_png"), 72)
    _build_standalone_qr(contract, contract.output_path("qr_png"))

    artifact_keys = ("letter_pdf", "letter_preview_png", "phone_png", "qr_png")
    report = {
        "schema_version": "onward_reunion_flyer_build_report_v1",
        "contract_path": str(contract.path.relative_to(contract.repo_root)),
        "contract_sha256": _sha256(contract.path),
        "canonical_url": contract.section("book")["canonical_url"],
        "cover": {
            "source_path": contract.section("cover")["source_path"],
            "source_dimensions": [contract.section("cover")["width_pixels"], contract.section("cover")["height_pixels"]],
            "source_sha256": contract.section("cover")["sha256"],
            "treatment": contract.section("cover")["treatment"],
        },
        "layout": layout,
        "qr": contract.section("qr"),
        "tools": {
            "python_packages": {
                "opencv-contrib-python": package_version("opencv-contrib-python"),
                "Pillow": package_version("Pillow"),
                "pypdf": package_version("pypdf"),
                "reportlab": package_version("reportlab"),
            },
            "pdftocairo": _tool_version(["pdftocairo", "-v"]),
        },
        "fonts": {
            "regular": {"path": str(regular), "sha256": _sha256(regular)},
            "bold": {"path": str(bold), "sha256": _sha256(bold)},
            "license": {"path": str(license_path), "sha256": _sha256(license_path)},
        },
        "artifacts": {key: _artifact_record(contract.output_path(key)) for key in artifact_keys},
    }
    report_path = contract.output_path("build_report_json")
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def _pdf_evidence(contract: FlyerContract) -> dict[str, Any]:
    pdf_path = contract.output_path("letter_pdf")
    reader = PdfReader(str(pdf_path))
    if len(reader.pages) != 1:
        raise ReunionFlyerError(f"Flyer PDF has {len(reader.pages)} pages; expected one.")
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    if abs(width - 612) > 0.01 or abs(height - 792) > 0.01:
        raise ReunionFlyerError(f"Flyer PDF media size is {width} × {height}, expected 612 × 792 points.")
    text = page.extract_text() or ""
    book = contract.section("book")
    required_text = [book["title_lines"][0], book["title_lines"][1], book["display_hostname"], *book["actions"]]
    missing_text = [item for item in required_text if item not in text]
    if missing_text:
        raise ReunionFlyerError(f"Flyer PDF selectable text is missing: {missing_text}")

    resources = page["/Resources"].get_object()
    fonts = resources.get("/Font", {}).get_object()
    embedded_fonts: list[dict[str, Any]] = []
    for name, reference in fonts.items():
        font = reference.get_object()
        descriptor_ref = font.get("/FontDescriptor")
        descriptor = descriptor_ref.get_object() if descriptor_ref else None
        embedded = bool(descriptor and any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")))
        embedded_fonts.append({"resource": str(name), "base_font": str(font.get("/BaseFont")), "embedded": embedded})
    embedded_vera = [
        item for item in embedded_fonts if item["embedded"] and "BitstreamVeraSans" in item["base_font"]
    ]
    if len(embedded_vera) != 2 or not any("Bold" in item["base_font"] for item in embedded_vera):
        raise ReunionFlyerError(f"Flyer PDF does not embed Vera regular and bold: {embedded_fonts}")

    xobjects_ref = resources.get("/XObject")
    xobjects = xobjects_ref.get_object() if xobjects_ref else {}
    images = []
    for name, reference in xobjects.items():
        item = reference.get_object()
        if item.get("/Subtype") == "/Image":
            images.append({"resource": str(name), "width": int(item["/Width"]), "height": int(item["/Height"])})
    cover = contract.section("cover")
    expected_image = (int(cover["width_pixels"]), int(cover["height_pixels"]))
    if len(images) != 1 or (images[0]["width"], images[0]["height"]) != expected_image:
        raise ReunionFlyerError(f"Flyer PDF embedded images are {images}, expected one {expected_image} cover.")
    if "/ExtGState" in resources:
        raise ReunionFlyerError("Flyer PDF unexpectedly contains an ExtGState/transparency resource.")
    return {
        "pages": 1,
        "media_box_points": [width, height],
        "selectable_text_characters": len(text),
        "embedded_fonts": embedded_fonts,
        "embedded_vera_fonts": embedded_vera,
        "embedded_images": images,
        "transparency_resources": 0,
    }


def _non_white_ratio(path: Path) -> float:
    with Image.open(path) as image:
        histogram = image.convert("L").histogram()
        return (image.width * image.height - histogram[255]) / (image.width * image.height)


def _validate_qr_master(contract: FlyerContract) -> dict[str, Any]:
    qr_path = contract.output_path("qr_png")
    qr = contract.section("qr")
    total = int(qr["total_modules"])
    module_pixels = int(qr["standalone_module_pixels"])
    expected_size = (total * module_pixels, total * module_pixels)
    with Image.open(qr_path) as image:
        rgb = image.convert("RGB")
        if rgb.size != expected_size or image.mode != "RGB":
            raise ReunionFlyerError(f"Standalone QR is {image.mode} {image.size}, expected RGB {expected_size}.")
        colors = set(rgb.getdata())
        if not colors.issubset({(0, 0, 0), (255, 255, 255)}):
            raise ReunionFlyerError("Standalone QR contains colors other than pure black and white.")
        quiet_pixels = int(qr["quiet_zone_modules"]) * module_pixels
        edges = (
            rgb.crop((0, 0, rgb.width, quiet_pixels)),
            rgb.crop((0, rgb.height - quiet_pixels, rgb.width, rgb.height)),
            rgb.crop((0, 0, quiet_pixels, rgb.height)),
            rgb.crop((rgb.width - quiet_pixels, 0, rgb.width, rgb.height)),
        )
        if any(set(edge.getdata()) != {(255, 255, 255)} for edge in edges):
            raise ReunionFlyerError("Standalone QR quiet zone is not four pure-white modules on every edge.")
    return {"pixel_dimensions": list(expected_size), "module_pixels": module_pixels, "colors": ["#000000", "#ffffff"]}


def _validate_raster_surfaces(contract: FlyerContract) -> dict[str, Any]:
    letter = contract.section("surfaces")["letter"]
    phone = contract.section("surfaces")["phone"]
    checks = {
        "letter_preview_png": (
            (int(letter["preview_width_pixels"]), int(letter["preview_height_pixels"])),
            float(letter["maximum_non_white_ratio"]),
        ),
        "phone_png": ((int(phone["width_pixels"]), int(phone["height_pixels"])), float(phone["maximum_non_white_ratio"])),
    }
    evidence: dict[str, Any] = {}
    for key, (expected_size, maximum_ratio) in checks.items():
        path = contract.output_path(key)
        with Image.open(path) as image:
            if image.mode != "RGB" or image.size != expected_size:
                raise ReunionFlyerError(f"{key} is {image.mode} {image.size}, expected RGB {expected_size}.")
            corners = (image.getpixel((0, 0)), image.getpixel((image.width - 1, 0)), image.getpixel((0, image.height - 1)), image.getpixel((image.width - 1, image.height - 1)))
            if any(pixel != (255, 255, 255) for pixel in corners):
                raise ReunionFlyerError(f"{key} does not retain a true-white page at every corner: {corners}")
        ratio = _non_white_ratio(path)
        if ratio > maximum_ratio:
            raise ReunionFlyerError(f"{key} non-white ratio {ratio:.6f} exceeds the {maximum_ratio:.6f} ceiling.")
        evidence[key] = {"pixel_dimensions": list(expected_size), "mode": "RGB", "non_white_ratio": ratio}
    return evidence


def _make_stress_images(contract: FlyerContract) -> list[Path]:
    stress_dir = contract.repo_root / "tmp" / "pdfs" / "outreach" / "stress"
    stress_dir.mkdir(parents=True, exist_ok=True)
    preview_path = contract.output_path("letter_preview_png")
    phone_path = contract.output_path("phone_png")
    paths: list[Path] = []
    with Image.open(preview_path) as source:
        source = source.convert("RGB")
        preview_50 = source.resize((source.width // 2, source.height // 2), Image.Resampling.LANCZOS)
        path_50 = stress_dir / "flyer-50-percent.png"
        preview_50.save(path_50)
        paths.append(path_50)
        preview_25 = source.resize((source.width // 4, source.height // 4), Image.Resampling.LANCZOS)
        path_25 = stress_dir / "flyer-25-percent.png"
        preview_25.save(path_25)
        paths.append(path_25)
        path_gray = stress_dir / "flyer-25-percent-grayscale.png"
        preview_25.convert("L").convert("RGB").save(path_gray)
        paths.append(path_gray)
        camera_proxy = preview_50.filter(ImageFilter.GaussianBlur(radius=0.8))
        path_camera = stress_dir / "flyer-camera-proxy.jpg"
        camera_proxy.save(path_camera, format="JPEG", quality=55)
        paths.append(path_camera)
    with Image.open(phone_path) as source:
        source = source.convert("RGB")
        for brightness in (0.8, 0.65):
            path = stress_dir / f"phone-{int(brightness * 100)}-percent-brightness.png"
            ImageEnhance.Brightness(source).enhance(brightness).save(path)
            paths.append(path)
    return paths


def _decode_qr_images(contract: FlyerContract, paths: list[Path]) -> dict[str, Any]:
    script = contract.repo_root / "scripts" / "decode_qr_vision.swift"
    if not script.is_file():
        raise ReunionFlyerError(f"Independent QR decoder is missing: {script}")
    cache = contract.repo_root / "tmp" / "swift-module-cache" / "onward-reunion-flyer"
    cache.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        ["swift", "-module-cache-path", str(cache), str(script), *(str(path) for path in paths)],
        check=False,
        capture_output=True,
        text=True,
    )
    decoded: dict[str, str] = {}
    decoder = "macOS Core Image / Vision"
    primary_error = completed.stderr.strip() if completed.returncode != 0 else ""
    if completed.returncode == 0:
        for line in completed.stdout.splitlines():
            path_text, separator, value = line.partition("\t")
            if separator:
                decoded[str(Path(path_text).resolve())] = value.strip()
    if completed.returncode != 0 or len(decoded) != len(paths):
        try:
            import cv2
        except ImportError as exc:
            raise ReunionFlyerError(
                f"macOS QR decode failed and OpenCV fallback is unavailable: {primary_error}"
            ) from exc
        decoded = {}
        detector = cv2.QRCodeDetector()
        for path in paths:
            image = cv2.imread(str(path))
            value, points, _ = detector.detectAndDecode(image)
            if value and points is not None:
                decoded[str(path.resolve())] = value
        decoder = f"OpenCV QRCodeDetector {cv2.__version__} (macOS decoder fallback)"
    expected = contract.section("book")["canonical_url"]
    missing = []
    wrong = []
    for path in paths:
        actual = decoded.get(str(path.resolve()))
        if actual is None:
            missing.append(str(path))
        elif actual != expected:
            wrong.append({"path": str(path), "decoded": actual})
    if missing or wrong:
        raise ReunionFlyerError(f"QR decode mismatch; missing={missing}, wrong={wrong}, expected={expected}")
    result: dict[str, Any] = {
        "decoder": decoder,
        "results": {str(path.relative_to(contract.repo_root)): decoded[str(path.resolve())] for path in paths},
    }
    if primary_error:
        result["macos_decoder_error"] = primary_error
    return result


def validate_artifacts(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    *,
    repo_root: Path | None = None,
    decode: bool = True,
) -> dict[str, Any]:
    contract = load_contract(contract_path, repo_root=repo_root)
    missing = [str(contract.output_path(key)) for key in REQUIRED_OUTPUT_KEYS if not contract.output_path(key).is_file()]
    if missing:
        raise ReunionFlyerError(f"Flyer output inventory is incomplete: {missing}")
    report = json.loads(contract.output_path("build_report_json").read_text(encoding="utf-8"))
    if report.get("contract_sha256") != _sha256(contract.path):
        raise ReunionFlyerError("Flyer build report does not match the current contract hash.")
    for key in ("letter_pdf", "letter_preview_png", "phone_png", "qr_png"):
        recorded = report.get("artifacts", {}).get(key, {})
        actual_hash = _sha256(contract.output_path(key))
        if recorded.get("sha256") != actual_hash:
            raise ReunionFlyerError(f"Flyer build report hash for `{key}` does not match the current artifact.")

    evidence: dict[str, Any] = {
        "pdf": _pdf_evidence(contract),
        "rasters": _validate_raster_surfaces(contract),
        "qr_master": _validate_qr_master(contract),
        "artifact_hashes": {key: _sha256(contract.output_path(key)) for key in REQUIRED_OUTPUT_KEYS},
    }
    if decode:
        stress_paths = _make_stress_images(contract)
        decode_paths = [
            contract.output_path("letter_preview_png"),
            contract.output_path("phone_png"),
            contract.output_path("qr_png"),
            *stress_paths,
        ]
        evidence["decoded_qr"] = _decode_qr_images(contract, decode_paths)
    return evidence
