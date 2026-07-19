from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
from PIL import Image

from modules.reunion_flyer import (
    DEFAULT_CONTRACT_PATH,
    ReunionFlyerError,
    build_artifacts,
    load_contract,
    validate_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]


def _write_contract(tmp_path: Path, mutate=None) -> tuple[Path, Path, dict]:
    repo_root = tmp_path / "repo"
    contract_path = repo_root / "outreach" / "reunion-flyer.json"
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.loads(DEFAULT_CONTRACT_PATH.read_text(encoding="utf-8"))
    cover_path = repo_root / "input" / "fixture-cover.jpg"
    cover_path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (800, 1063), (111, 46, 29)).save(cover_path, format="JPEG", quality=92)
    payload["cover"].update(
        {
            "source_path": "input/fixture-cover.jpg",
            "width_pixels": 800,
            "height_pixels": 1063,
            "sha256": hashlib.sha256(cover_path.read_bytes()).hexdigest(),
        }
    )
    if mutate is not None:
        mutate(payload)
    contract_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return contract_path, repo_root, payload


def test_real_contract_uses_canonical_onward_sources_and_copy() -> None:
    contract = load_contract()
    book = contract.section("book")
    assert book["title"] == "Onward to the Unknown"
    assert book["subtitle"] == "A Genealogy and Biography of the L'Heureux Family"
    assert book["canonical_url"] == "https://onward.copper-dog.com/"
    assert book["display_hostname"] == "onward.copper-dog.com"
    assert book["actions"] == [
        "Read the book online",
        "Open the searchable PDF",
        "Get eBook or audiobook",
        "Listen chapter by chapter",
    ]
    assert book["family_name_rows"] == [
        "Alma • Arthur • Leonidas • Josephine • Paul",
        "George • Joe • Mathilda • Marie-Louise • Roseanna",
        "Antoinette • Emilie • Wilfred • Pierre • Antoine",
    ]
    assert contract.section("cover")["source_path"].endswith("images/page-001-000.jpg")
    assert contract.section("palette")["paper"] == "#ffffff"


def test_contract_rejects_hostname_that_differs_from_encoded_url(tmp_path: Path) -> None:
    contract_path, repo_root, _ = _write_contract(
        tmp_path, lambda payload: payload["book"].__setitem__("display_hostname", "example.com")
    )
    with pytest.raises(ReunionFlyerError, match="display hostname"):
        load_contract(contract_path, repo_root=repo_root)


def test_contract_rejects_prohibited_reader_copy(tmp_path: Path) -> None:
    contract_path, repo_root, _ = _write_contract(
        tmp_path,
        lambda payload: payload["book"].__setitem__("free_headline", "No cost. No account needed."),
    )
    with pytest.raises(ReunionFlyerError, match="prohibited wording"):
        load_contract(contract_path, repo_root=repo_root)


def test_contract_rejects_cover_hash_drift(tmp_path: Path) -> None:
    contract_path, repo_root, _ = _write_contract(
        tmp_path, lambda payload: payload["cover"].__setitem__("sha256", "0" * 64)
    )
    with pytest.raises(ReunionFlyerError, match="cover SHA-256"):
        load_contract(contract_path, repo_root=repo_root)


def test_contract_rejects_small_type_and_qr_geometry(tmp_path: Path) -> None:
    contract_path, repo_root, _ = _write_contract(
        tmp_path, lambda payload: payload["typography"]["print"].__setitem__("actions", 17)
    )
    with pytest.raises(ReunionFlyerError, match="essential 18-point floor"):
        load_contract(contract_path, repo_root=repo_root)

    contract_path, repo_root, _ = _write_contract(
        tmp_path, lambda payload: payload["qr"].__setitem__("quiet_zone_modules", 3)
    )
    with pytest.raises(ReunionFlyerError, match="four-module quiet zone"):
        load_contract(contract_path, repo_root=repo_root)


def test_contract_rejects_incomplete_output_inventory(tmp_path: Path) -> None:
    contract_path, repo_root, _ = _write_contract(
        tmp_path, lambda payload: payload["outputs"].pop("phone_png")
    )
    with pytest.raises(ReunionFlyerError, match="outputs must contain exactly"):
        load_contract(contract_path, repo_root=repo_root)


def test_longer_book_substitution_still_respects_slots(tmp_path: Path) -> None:
    def mutate(payload: dict) -> None:
        payload["book"]["title"] = "Across the Prairies and Into the Foothills"
        payload["book"]["title_lines"] = ["Across the Prairies", "Into the Foothills"]
        payload["book"]["canonical_url"] = "https://family-archive.example/"
        payload["book"]["display_hostname"] = "family-archive.example"
        payload["book"]["free_headline"] = "Family stories online — free to explore"
        payload["book"]["family_name_rows"] = [
            "Alexandra • Benjamin • Charlotte",
            "Dominique • Evangeline • Frederick",
            "Genevieve • Henrietta • Isabelle",
        ]

    contract_path, repo_root, _ = _write_contract(tmp_path, mutate)
    contract = load_contract(contract_path, repo_root=repo_root)
    assert contract.section("book")["display_hostname"] == "family-archive.example"


def test_builder_and_validator_produce_exact_artifact_family(tmp_path: Path) -> None:
    contract_path, repo_root, payload = _write_contract(tmp_path)
    first_report = build_artifacts(contract_path, repo_root=repo_root)
    evidence = validate_artifacts(contract_path, repo_root=repo_root, decode=False)
    for key, relative in payload["outputs"].items():
        assert (repo_root / relative).is_file(), key
    assert first_report["qr"]["version"] == 4
    assert evidence["pdf"]["media_box_points"] == [612.0, 792.0]
    assert evidence["pdf"]["embedded_images"] == [
        {"resource": evidence["pdf"]["embedded_images"][0]["resource"], "width": 800, "height": 1063}
    ]
    assert evidence["rasters"]["letter_preview_png"]["pixel_dimensions"] == [2550, 3300]
    assert evidence["rasters"]["phone_png"]["pixel_dimensions"] == [1080, 1920]
    assert evidence["qr_master"]["pixel_dimensions"] == [1640, 1640]
    assert evidence["qr_master"]["module_pixels"] == 40

    first_hashes = copy.deepcopy(first_report["artifacts"])
    second_report = build_artifacts(contract_path, repo_root=repo_root)
    assert second_report["artifacts"] == first_hashes
