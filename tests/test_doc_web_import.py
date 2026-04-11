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
    run_scanned_supplement_recipe,
    validate_bundle_contract,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests/fixtures/doc_web_bundle_minimal"


class DocWebImportTests(unittest.TestCase):
    def test_build_runtime_paths_falls_back_to_primary_checkout_paths_for_worktrees(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_text:
            temp_root = Path(temp_dir_text)
            primary_repo = temp_root / "projects" / "onward-to-the-unknown-website"
            worktree_repo = temp_root / "worktrees" / "5ede" / "onward-to-the-unknown-website"
            doc_web_root = temp_root / "projects" / "doc-web"
            input_pdf = primary_repo / "input" / "Onward to the Unknown.pdf"

            primary_repo.mkdir(parents=True)
            worktree_repo.mkdir(parents=True)
            doc_web_root.mkdir(parents=True)
            input_pdf.parent.mkdir(parents=True)
            input_pdf.write_text("fixture pdf", encoding="utf-8")

            runtime_manifest = RuntimeManifest(
                source_path="../doc-web",
                python_executable="python",
                default_recipe="configs/recipes/recipe-onward-pdf-html-mvp.yaml",
                default_input_pdf="input/Onward to the Unknown.pdf",
                source_runs_root="output/runs",
                snapshot_root=".runtime/doc-web-imports",
            )

            import scripts.doc_web_import as module

            original_primary_root = module.primary_git_checkout_root
            try:
                module.primary_git_checkout_root = lambda _repo_root: primary_repo  # type: ignore[assignment]
                paths = build_runtime_paths(runtime_manifest, repo_root=worktree_repo)
            finally:
                module.primary_git_checkout_root = original_primary_root  # type: ignore[assignment]

            self.assertEqual(paths.source_root, doc_web_root.resolve())
            self.assertEqual(paths.default_input_pdf_path, input_pdf.resolve())
            self.assertEqual(
                paths.snapshot_root,
                (worktree_repo / ".runtime" / "doc-web-imports").resolve(),
            )

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

    def test_run_scanned_supplement_recipe_builds_standard_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_text:
            temp_root = Path(temp_dir_text)
            repo_root = temp_root / "repo"
            doc_web_root = temp_root / "doc-web"
            input_pdf = repo_root / "input" / "memoir.pdf"
            recipe_path = doc_web_root / "configs" / "recipes" / "recipe-pdf-ocr-html-mvp.yaml"
            run_root = doc_web_root / "output" / "runs" / "memoir-run"
            pages_path = run_root / "05_extract_page_numbers_html_v1" / "pages_html_with_page_numbers.jsonl"
            illustration_path = run_root / "03_crop_illustrations_guided_v1" / "illustration_manifest.jsonl"

            input_pdf.parent.mkdir(parents=True)
            input_pdf.write_text("fixture pdf", encoding="utf-8")
            recipe_path.parent.mkdir(parents=True)
            recipe_path.write_text("fixture recipe", encoding="utf-8")
            pages_path.parent.mkdir(parents=True, exist_ok=True)
            pages_path.write_text("[]\n", encoding="utf-8")
            illustration_path.parent.mkdir(parents=True, exist_ok=True)
            illustration_path.write_text("[]\n", encoding="utf-8")

            runtime_manifest = RuntimeManifest(
                source_path=str(doc_web_root),
                python_executable="python",
                default_recipe="configs/recipes/recipe-onward-pdf-html-mvp.yaml",
                default_input_pdf="input/Onward to the Unknown.pdf",
                source_runs_root="output/runs",
                snapshot_root=str(temp_root / "runtime-imports"),
            )
            paths = build_runtime_paths(runtime_manifest, repo_root=repo_root)

            import scripts.doc_web_import as module

            recorded_calls: list[list[str]] = []
            original_run_command = module.run_command
            try:
                def fake_run_command(args: list[str], *, cwd: Path | None = None):  # type: ignore[override]
                    del cwd
                    recorded_calls.append(args)
                    if args[:3] == ["python", "-m", "modules.build.build_chapter_html_v1.main"]:
                        output_dir = run_root / "output" / "html"
                        output_dir.mkdir(parents=True, exist_ok=True)
                        (output_dir / "manifest.json").write_text("{}", encoding="utf-8")
                    return None

                module.run_command = fake_run_command  # type: ignore[assignment]
                result = run_scanned_supplement_recipe(
                    paths,
                    run_id="memoir-run",
                    bundle_title="Rolland Alain Memoir Family Story",
                    input_pdf_path=input_pdf,
                    recipe_path=recipe_path,
                    force=True,
                )
            finally:
                module.run_command = original_run_command  # type: ignore[assignment]

            self.assertEqual(result, (run_root / "output" / "html").resolve())
            self.assertEqual(recorded_calls[0][:9], [
                "python",
                "driver.py",
                "--recipe",
                str(recipe_path.resolve()),
                "--input-pdf",
                str(input_pdf.resolve()),
                "--run-id",
                "memoir-run",
                "--end-at",
            ])
            self.assertEqual(recorded_calls[0][9], "extract_page_numbers")
            self.assertIn("modules.portionize.portionize_headings_html_v1.main", recorded_calls[1])
            self.assertIn("--fallback-title", recorded_calls[1])
            self.assertIn("Rolland Alain Memoir Family Story", recorded_calls[1])
            self.assertIn("modules.build.build_chapter_html_v1.main", recorded_calls[2])
            self.assertIn("--illustration-manifest", recorded_calls[2])
            self.assertTrue((result / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
