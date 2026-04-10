from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.doc_web_import import (
    BundleSummary,
    DocWebImportError,
    RuntimeManifest,
    build_runtime_paths,
    import_bundle,
    validate_bundle_contract,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests/fixtures/doc_web_bundle_minimal"


class DocWebImportTests(unittest.TestCase):
    def test_validate_bundle_contract_returns_summary(self) -> None:
        summary = validate_bundle_contract(FIXTURE_ROOT)
        self.assertEqual(
            summary,
            BundleSummary(
                document_id="fixture-book",
                title="Fixture Book",
                entry_count=1,
                provenance_row_count=3,
                reading_order=["chapter-001"],
                entry_ids=["chapter-001"],
            ),
        )

    def test_validate_bundle_contract_rejects_missing_block_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_text:
            temp_root = Path(temp_dir_text) / "bundle"
            shutil.copytree(FIXTURE_ROOT, temp_root)
            html_path = temp_root / "chapter-001.html"
            html_path.write_text(
                html_path.read_text(encoding="utf-8").replace(
                    'id="blk-chapter-001-0002"',
                    'id="wrong-id"',
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(DocWebImportError, "missing from chapter-001.html"):
                validate_bundle_contract(temp_root)

    def test_import_bundle_writes_snapshot_and_active_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_text:
            temp_root = Path(temp_dir_text)
            doc_web_root = temp_root / "doc-web"
            doc_web_root.mkdir()
            runtime_manifest = RuntimeManifest(
                source_path=str(doc_web_root),
                python_executable="python",
                default_recipe="configs/recipes/recipe-onward-pdf-html-mvp.yaml",
                default_input_pdf="input/Onward to the Unknown.pdf",
                source_runs_root="output/runs",
                snapshot_root=str(temp_root / "runtime-imports"),
            )
            paths = build_runtime_paths(runtime_manifest, repo_root=REPO_ROOT)

            import scripts.doc_web_import as module

            original_contract = module.fetch_doc_web_contract
            try:
                module.fetch_doc_web_contract = lambda *_args, **_kwargs: {  # type: ignore[assignment]
                    "contract_name": "doc-web",
                    "schema_fingerprint": "sha256:test",
                }
                result = import_bundle(
                    paths,
                    bundle_root=FIXTURE_ROOT,
                    snapshot_id="fixture-import",
                )
            finally:
                module.fetch_doc_web_contract = original_contract  # type: ignore[assignment]

            metadata = json.loads(result.metadata_path.read_text(encoding="utf-8"))
            active = json.loads(result.active_import_path.read_text(encoding="utf-8"))

            self.assertEqual(metadata["snapshotId"], "fixture-import")
            self.assertEqual(metadata["bundle"]["document_id"], "fixture-book")
            self.assertEqual(metadata["source"]["contract"]["schema_fingerprint"], "sha256:test")
            self.assertEqual(active["snapshotId"], "fixture-import")
            self.assertTrue((result.bundle_root / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
