#!/usr/bin/env python3
"""Run and import bundles from the sibling doc-web checkout."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_MANIFEST_PATH = REPO_ROOT / "doc-web-runtime.json"
MANIFEST_SCHEMA_VERSION = "doc_web_bundle_manifest_v1"
PROVENANCE_SCHEMA_VERSION = "doc_web_provenance_block_v1"


class DocWebImportError(RuntimeError):
    """Base error for doc-web integration failures."""


@dataclass(frozen=True)
class RuntimeManifest:
    source_path: str
    python_executable: str
    default_recipe: str
    default_input_pdf: str
    source_runs_root: str
    snapshot_root: str


@dataclass(frozen=True)
class RuntimePaths:
    source_root: Path
    python_executable: str
    default_recipe_path: Path
    default_input_pdf_path: Path
    source_runs_root: Path
    snapshot_root: Path
    active_import_path: Path


@dataclass(frozen=True)
class BundleSummary:
    document_id: str
    title: str
    entry_count: int
    provenance_row_count: int
    reading_order: list[str]
    entry_ids: list[str]


@dataclass(frozen=True)
class ImportedSnapshot:
    snapshot_id: str
    metadata_path: Path
    bundle_root: Path
    active_import_path: Path


class _TrackedHtmlParser(HTMLParser):
    """Collect DOM ids and image references from bundle HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.dom_ids: set[str] = set()
        self.image_paths: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        element_id = attrs_dict.get("id")
        if element_id:
            self.dom_ids.add(element_id)
        if tag == "img":
            src = attrs_dict.get("src")
            if src:
                self.image_paths.append(src)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def load_runtime_manifest(path: Path = RUNTIME_MANIFEST_PATH) -> RuntimeManifest:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DocWebImportError(f"Runtime manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DocWebImportError(f"Runtime manifest is not valid JSON: {exc}") from exc

    required_fields = {
        "sourcePath": "source_path",
        "pythonExecutable": "python_executable",
        "defaultRecipe": "default_recipe",
        "defaultInputPdf": "default_input_pdf",
        "sourceRunsRoot": "source_runs_root",
        "snapshotRoot": "snapshot_root",
    }
    missing = [field for field in required_fields if not isinstance(payload.get(field), str)]
    if missing:
        raise DocWebImportError(
            f"{path} is missing required string fields: {', '.join(sorted(missing))}"
        )

    return RuntimeManifest(
        source_path=payload["sourcePath"],
        python_executable=payload["pythonExecutable"],
        default_recipe=payload["defaultRecipe"],
        default_input_pdf=payload["defaultInputPdf"],
        source_runs_root=payload["sourceRunsRoot"],
        snapshot_root=payload["snapshotRoot"],
    )


def build_runtime_paths(manifest: RuntimeManifest, repo_root: Path = REPO_ROOT) -> RuntimePaths:
    source_root = _resolve_config_path(repo_root, manifest.source_path)
    source_runs_root = _resolve_config_path(source_root, manifest.source_runs_root)
    snapshot_root = _resolve_config_path(repo_root, manifest.snapshot_root)
    active_import_path = snapshot_root / "active-import.json"
    return RuntimePaths(
        source_root=source_root,
        python_executable=manifest.python_executable,
        default_recipe_path=_resolve_config_path(source_root, manifest.default_recipe),
        default_input_pdf_path=_resolve_config_path(repo_root, manifest.default_input_pdf),
        source_runs_root=source_runs_root,
        snapshot_root=snapshot_root,
        active_import_path=active_import_path,
    )


def _resolve_config_path(base: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def run_command(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "unknown error"
        raise DocWebImportError(f"{' '.join(args)} failed with exit code {proc.returncode}: {detail}")
    return proc


def fetch_doc_web_contract(paths: RuntimePaths, python_executable: str | None = None) -> dict[str, Any]:
    python_bin = python_executable or paths.python_executable
    proc = run_command(
        [python_bin, "-c", "from doc_web.cli import main; main()", "contract", "--json"],
        cwd=paths.source_root,
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise DocWebImportError(f"doc-web contract payload is not valid JSON: {exc}") from exc


def run_onward_recipe(
    paths: RuntimePaths,
    *,
    run_id: str,
    recipe_path: Path | None = None,
    input_pdf_path: Path | None = None,
    python_executable: str | None = None,
    force: bool = False,
    allow_run_id_reuse: bool = False,
    start_from: str | None = None,
    end_at: str | None = None,
    dry_run: bool = False,
    extra_args: list[str] | None = None,
) -> Path:
    recipe = (recipe_path or paths.default_recipe_path).resolve()
    input_pdf = (input_pdf_path or paths.default_input_pdf_path).resolve()
    python_bin = python_executable or paths.python_executable

    if not recipe.exists():
        raise DocWebImportError(f"Recipe not found: {recipe}")
    if not input_pdf.exists():
        raise DocWebImportError(f"Input PDF not found: {input_pdf}")

    args = [
        python_bin,
        "driver.py",
        "--recipe",
        str(recipe),
        "--input-pdf",
        str(input_pdf),
        "--run-id",
        run_id,
    ]
    if allow_run_id_reuse:
        args.append("--allow-run-id-reuse")
    if force:
        args.append("--force")
    if start_from:
        args.extend(["--start-from", start_from])
    if end_at:
        args.extend(["--end-at", end_at])
    if dry_run:
        args.append("--dry-run")
    if extra_args:
        args.extend(extra_args)

    run_command(args, cwd=paths.source_root)
    return paths.source_runs_root / run_id / "output" / "html"


def import_run_bundle(
    paths: RuntimePaths,
    *,
    run_id: str,
    snapshot_id: str | None = None,
    recipe_path: Path | None = None,
    python_executable: str | None = None,
    force: bool = False,
) -> ImportedSnapshot:
    bundle_root = paths.source_runs_root / run_id / "output" / "html"
    if not bundle_root.exists():
        raise DocWebImportError(f"Bundle output not found for run '{run_id}': {bundle_root}")
    source_payload = {
        "runId": run_id,
        "recipePath": _rel_or_abs(recipe_path or paths.default_recipe_path),
    }
    return import_bundle(
        paths,
        bundle_root=bundle_root,
        snapshot_id=snapshot_id or run_id,
        python_executable=python_executable,
        force=force,
        source_payload=source_payload,
    )


def import_bundle(
    paths: RuntimePaths,
    *,
    bundle_root: Path,
    snapshot_id: str,
    python_executable: str | None = None,
    force: bool = False,
    source_payload: dict[str, Any] | None = None,
) -> ImportedSnapshot:
    bundle_root = bundle_root.resolve()
    if not bundle_root.exists():
        raise DocWebImportError(f"Bundle root not found: {bundle_root}")

    summary = validate_bundle_contract(bundle_root)
    contract_payload = fetch_doc_web_contract(paths, python_executable=python_executable)

    snapshot_dir = (paths.snapshot_root / snapshot_id).resolve()
    bundle_snapshot_dir = snapshot_dir / "bundle"
    metadata_path = snapshot_dir / "import-metadata.json"

    if snapshot_dir.exists():
        if not force:
            raise DocWebImportError(
                f"Snapshot '{snapshot_id}' already exists at {snapshot_dir}. Use --force to replace it."
            )
        shutil.rmtree(snapshot_dir)

    bundle_snapshot_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(bundle_root, bundle_snapshot_dir)

    imported_at = _iso_now()
    payload = {
        "schemaVersion": "onward_doc_web_import_v1",
        "snapshotId": snapshot_id,
        "importedAt": imported_at,
        "source": {
            "docWebRoot": _rel_or_abs(paths.source_root),
            "bundleRoot": _rel_or_abs(bundle_root),
            "contract": contract_payload,
        },
        "bundle": {
            **asdict(summary),
            "snapshotRoot": _rel_or_abs(bundle_snapshot_dir),
            "manifestPath": _rel_or_abs(bundle_snapshot_dir / "manifest.json"),
            "provenancePath": _rel_or_abs(bundle_snapshot_dir / "provenance" / "blocks.jsonl"),
        },
    }
    if source_payload:
        payload["source"].update(source_payload)

    write_json(metadata_path, payload)
    write_json(
        paths.active_import_path,
        {
            "schemaVersion": "onward_doc_web_active_import_v1",
            "updatedAt": imported_at,
            "snapshotId": snapshot_id,
            "metadataPath": _rel_or_abs(metadata_path),
            "bundleRoot": _rel_or_abs(bundle_snapshot_dir),
        },
    )

    return ImportedSnapshot(
        snapshot_id=snapshot_id,
        metadata_path=metadata_path,
        bundle_root=bundle_snapshot_dir,
        active_import_path=paths.active_import_path,
    )


def validate_bundle_contract(bundle_root: Path) -> BundleSummary:
    bundle_root = bundle_root.resolve()
    manifest_path = _resolve_bundle_member(bundle_root, "manifest.json", "manifest")
    manifest = _load_json_object(manifest_path, label="manifest")

    schema_version = manifest.get("schema_version")
    if schema_version != MANIFEST_SCHEMA_VERSION:
        raise DocWebImportError(
            f"Bundle manifest schema_version must be {MANIFEST_SCHEMA_VERSION}, got {schema_version!r}"
        )

    required_top_level = {
        "document_id": str,
        "title": str,
        "source_artifact": str,
        "index_path": str,
        "entries": list,
        "reading_order": list,
        "provenance_path": str,
    }
    for field_name, expected_type in required_top_level.items():
        value = manifest.get(field_name)
        if not isinstance(value, expected_type):
            raise DocWebImportError(
                f"Bundle manifest field '{field_name}' must be {expected_type.__name__}"
            )

    index_path = _resolve_bundle_member(bundle_root, manifest["index_path"], "index_path")
    if index_path.suffix.lower() != ".html":
        raise DocWebImportError("index_path must point to an HTML file")

    provenance_path = _resolve_bundle_member(
        bundle_root,
        manifest["provenance_path"],
        "provenance_path",
    )

    entry_map: dict[str, dict[str, Any]] = {}
    for entry in manifest["entries"]:
        if not isinstance(entry, dict):
            raise DocWebImportError("Every manifest entry must be an object")
        _validate_manifest_entry(bundle_root, entry, entry_map)

    reading_order = manifest["reading_order"]
    if not all(isinstance(item, str) for item in reading_order):
        raise DocWebImportError("reading_order must contain only string entry ids")
    entry_ids = list(entry_map)
    if sorted(reading_order) != sorted(entry_ids):
        raise DocWebImportError("reading_order must list every entry exactly once")
    if len(set(reading_order)) != len(reading_order):
        raise DocWebImportError("reading_order contains duplicate entry ids")

    ordered_entries = [entry_map[entry_id] for entry_id in reading_order]
    for index, entry in enumerate(ordered_entries):
        expected_prev = ordered_entries[index - 1]["entry_id"] if index > 0 else None
        expected_next = ordered_entries[index + 1]["entry_id"] if index + 1 < len(ordered_entries) else None
        if entry.get("prev_entry_id") != expected_prev:
            raise DocWebImportError(
                f"Entry '{entry['entry_id']}' prev_entry_id does not match reading_order"
            )
        if entry.get("next_entry_id") != expected_next:
            raise DocWebImportError(
                f"Entry '{entry['entry_id']}' next_entry_id does not match reading_order"
            )

    blocks_by_entry = _load_provenance_rows(provenance_path, entry_map)

    for entry_id, entry in entry_map.items():
        html_path = _resolve_bundle_member(bundle_root, entry["path"], f"entry:{entry_id}")
        parser = _TrackedHtmlParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        parser.close()
        for block_id in blocks_by_entry.get(entry_id, []):
            if block_id not in parser.dom_ids:
                raise DocWebImportError(
                    f"Bundle provenance block '{block_id}' is missing from {entry['path']}"
                )
        for image_path in parser.image_paths:
            _resolve_bundle_member(bundle_root, image_path, f"image:{image_path}")

    return BundleSummary(
        document_id=manifest["document_id"],
        title=manifest["title"],
        entry_count=len(entry_ids),
        provenance_row_count=sum(len(block_ids) for block_ids in blocks_by_entry.values()),
        reading_order=list(reading_order),
        entry_ids=list(reading_order),
    )


def _validate_manifest_entry(
    bundle_root: Path,
    entry: dict[str, Any],
    entry_map: dict[str, dict[str, Any]],
) -> None:
    required_fields = {
        "entry_id": str,
        "kind": str,
        "title": str,
        "path": str,
        "order": int,
    }
    for field_name, expected_type in required_fields.items():
        value = entry.get(field_name)
        if not isinstance(value, expected_type):
            raise DocWebImportError(
                f"Bundle entry field '{field_name}' must be {expected_type.__name__}"
            )

    entry_id = entry["entry_id"]
    if entry_id in entry_map:
        raise DocWebImportError(f"Bundle manifest contains duplicate entry_id '{entry_id}'")
    if entry["kind"] not in {"chapter", "page"}:
        raise DocWebImportError(f"Unsupported entry kind for '{entry_id}': {entry['kind']!r}")

    html_path = _resolve_bundle_member(bundle_root, entry["path"], f"entry:{entry_id}")
    if html_path.suffix.lower() != ".html":
        raise DocWebImportError(f"Entry '{entry_id}' path must point to HTML: {entry['path']}")
    if html_path.stem != entry_id:
        raise DocWebImportError(
            f"Entry '{entry_id}' path stem must match entry_id, got {html_path.stem!r}"
        )

    for link_field in ("prev_entry_id", "next_entry_id"):
        value = entry.get(link_field)
        if value is not None and not isinstance(value, str):
            raise DocWebImportError(f"Entry '{entry_id}' field '{link_field}' must be a string or null")

    entry_map[entry_id] = entry


def _load_provenance_rows(
    provenance_path: Path,
    entry_map: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    blocks_by_entry: dict[str, list[str]] = {entry_id: [] for entry_id in entry_map}
    lines = provenance_path.read_text(encoding="utf-8").splitlines()
    for line_number, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            continue
        try:
            payload = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise DocWebImportError(
                f"Provenance row {line_number} is not valid JSON: {exc}"
            ) from exc
        if payload.get("schema_version") != PROVENANCE_SCHEMA_VERSION:
            raise DocWebImportError(
                f"Provenance row {line_number} schema_version must be {PROVENANCE_SCHEMA_VERSION}"
            )
        required_fields = {
            "block_id": str,
            "entry_id": str,
            "block_kind": str,
            "source_element_ids": list,
        }
        for field_name, expected_type in required_fields.items():
            value = payload.get(field_name)
            if not isinstance(value, expected_type):
                raise DocWebImportError(
                    f"Provenance row {line_number} field '{field_name}' must be {expected_type.__name__}"
                )
        entry_id = payload["entry_id"]
        if entry_id not in entry_map:
            raise DocWebImportError(
                f"Provenance row {line_number} references unknown entry_id '{entry_id}'"
            )
        if not all(isinstance(item, str) for item in payload["source_element_ids"]):
            raise DocWebImportError(
                f"Provenance row {line_number} source_element_ids must contain only strings"
            )
        block_id = payload["block_id"]
        if not block_id.startswith(f"blk-{entry_id}-"):
            raise DocWebImportError(
                f"Provenance block '{block_id}' must use the stable blk-<entry-id>-NNNN format"
            )
        blocks_by_entry[entry_id].append(block_id)
    return blocks_by_entry


def _resolve_bundle_member(bundle_root: Path, relative_path: str, label: str) -> Path:
    candidate = (bundle_root / PurePosixPath(relative_path)).resolve()
    if not candidate.is_relative_to(bundle_root):
        raise DocWebImportError(f"{label} escapes bundle root: {relative_path}")
    if not candidate.exists():
        raise DocWebImportError(f"{label} not found: {relative_path}")
    return candidate


def _load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DocWebImportError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise DocWebImportError(f"{label} must be a JSON object")
    return payload


def _iso_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _rel_or_abs(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _print_json(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run and import bundles from the sibling doc-web checkout.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract_parser = subparsers.add_parser("contract", help="Emit the local doc-web contract payload.")
    contract_parser.add_argument("--python", help="Override the Python executable used for doc-web commands.")

    run_parser = subparsers.add_parser("run-onward", help="Run the maintained Onward recipe in the sibling doc-web checkout.")
    run_parser.add_argument("--run-id", required=True, help="Run id to use in the sibling doc-web checkout.")
    run_parser.add_argument("--recipe", help="Override the doc-web recipe path.")
    run_parser.add_argument("--input-pdf", help="Override the PDF path from this repo.")
    run_parser.add_argument("--python", help="Override the Python executable used for doc-web commands.")
    run_parser.add_argument("--force", action="store_true", help="Pass --force to doc-web driver.py.")
    run_parser.add_argument(
        "--allow-run-id-reuse",
        action="store_true",
        help="Pass --allow-run-id-reuse to doc-web driver.py.",
    )
    run_parser.add_argument("--start-from", help="Resume doc-web from a specific stage id.")
    run_parser.add_argument("--end-at", help="Stop doc-web after a specific stage id.")
    run_parser.add_argument("--dry-run", action="store_true", help="Validate the recipe graph without executing it.")
    run_parser.add_argument(
        "extra_args",
        nargs=argparse.REMAINDER,
        help="Additional args to pass to doc-web driver.py after '--'.",
    )

    import_run_parser = subparsers.add_parser("import-run", help="Import the output/html bundle from a doc-web run id.")
    import_run_parser.add_argument("--run-id", required=True, help="Source doc-web run id.")
    import_run_parser.add_argument("--snapshot-id", help="Snapshot id inside .runtime/doc-web-imports/; defaults to the run id.")
    import_run_parser.add_argument("--recipe", help="Override the doc-web recipe path recorded in metadata.")
    import_run_parser.add_argument("--python", help="Override the Python executable used for doc-web commands.")
    import_run_parser.add_argument("--force", action="store_true", help="Replace an existing snapshot if present.")

    import_bundle_parser = subparsers.add_parser("import-bundle", help="Import an existing doc-web bundle directory.")
    import_bundle_parser.add_argument("--bundle-path", required=True, help="Path to a doc-web bundle root containing manifest.json.")
    import_bundle_parser.add_argument("--snapshot-id", required=True, help="Snapshot id inside .runtime/doc-web-imports/.")
    import_bundle_parser.add_argument("--python", help="Override the Python executable used for doc-web commands.")
    import_bundle_parser.add_argument("--force", action="store_true", help="Replace an existing snapshot if present.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    manifest = load_runtime_manifest()
    paths = build_runtime_paths(manifest)

    if args.command == "contract":
        _print_json(fetch_doc_web_contract(paths, python_executable=args.python))
        return 0

    if args.command == "run-onward":
        extra_args = list(args.extra_args or [])
        if extra_args and extra_args[0] == "--":
            extra_args = extra_args[1:]
        bundle_root = run_onward_recipe(
            paths,
            run_id=args.run_id,
            recipe_path=_resolve_config_path(paths.source_root, args.recipe) if args.recipe else None,
            input_pdf_path=_resolve_config_path(REPO_ROOT, args.input_pdf) if args.input_pdf else None,
            python_executable=args.python,
            force=args.force,
            allow_run_id_reuse=args.allow_run_id_reuse,
            start_from=args.start_from,
            end_at=args.end_at,
            dry_run=args.dry_run,
            extra_args=extra_args,
        )
        _print_json(
            {
                "schemaVersion": "onward_doc_web_run_v1",
                "runId": args.run_id,
                "bundleRoot": _rel_or_abs(bundle_root),
                "dryRun": args.dry_run,
            }
        )
        return 0

    if args.command == "import-run":
        snapshot = import_run_bundle(
            paths,
            run_id=args.run_id,
            snapshot_id=args.snapshot_id,
            recipe_path=_resolve_config_path(paths.source_root, args.recipe) if args.recipe else None,
            python_executable=args.python,
            force=args.force,
        )
        _print_json(
            {
                "schemaVersion": "onward_doc_web_import_result_v1",
                "snapshotId": snapshot.snapshot_id,
                "metadataPath": _rel_or_abs(snapshot.metadata_path),
                "bundleRoot": _rel_or_abs(snapshot.bundle_root),
                "activeImportPath": _rel_or_abs(snapshot.active_import_path),
            }
        )
        return 0

    if args.command == "import-bundle":
        snapshot = import_bundle(
            paths,
            bundle_root=_resolve_config_path(REPO_ROOT, args.bundle_path),
            snapshot_id=args.snapshot_id,
            python_executable=args.python,
            force=args.force,
        )
        _print_json(
            {
                "schemaVersion": "onward_doc_web_import_result_v1",
                "snapshotId": snapshot.snapshot_id,
                "metadataPath": _rel_or_abs(snapshot.metadata_path),
                "bundleRoot": _rel_or_abs(snapshot.bundle_root),
                "activeImportPath": _rel_or_abs(snapshot.active_import_path),
            }
        )
        return 0

    parser.error(f"Unhandled command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
