from __future__ import annotations

import importlib.util
from pathlib import Path


def load_deploy_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "scripts" / "deploy_static_site.py"
    spec = importlib.util.spec_from_file_location("deploy_static_site", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_collect_source_state_ignores_manifest_and_tracks_dirs(tmp_path):
    deploy = load_deploy_module()
    (tmp_path / "index.html").write_text("index", encoding="utf-8")
    (tmp_path / ".deploy-manifest.json").write_text("{}", encoding="utf-8")
    (tmp_path / "_internal").mkdir()
    (tmp_path / "_internal" / "omission-audit.json").write_text("{}", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "chapter-001.html").write_text("chapter", encoding="utf-8")

    state = deploy.collect_source_state(tmp_path)

    assert state["files"] == ["index.html", "nested/chapter-001.html"]
    assert state["dirs"] == ["nested"]
    assert state["top_level"] == ["index.html", "nested"]


def test_build_sync_plan_deletes_stale_paths():
    deploy = load_deploy_module()
    previous = {
        "files": ["index.html", "old-page.html", "nested/old.txt"],
        "dirs": ["nested"],
    }
    current = {
        "files": ["index.html"],
        "dirs": [],
        "top_level": ["index.html"],
    }

    plan = deploy.build_sync_plan(previous=previous, current=current)

    assert plan["stale_files"] == ["nested/old.txt", "old-page.html"]
    assert plan["stale_dirs"] == ["nested"]
    assert plan["pre_delete_files"] == []
    assert plan["pre_delete_dirs"] == []


def test_build_sync_plan_handles_file_directory_replacement():
    deploy = load_deploy_module()
    previous = {
        "files": ["assets/logo.txt"],
        "dirs": ["assets"],
    }
    current = {
        "files": ["assets"],
        "dirs": [],
        "top_level": ["assets"],
    }

    plan = deploy.build_sync_plan(previous=previous, current=current)

    assert plan["pre_delete_files"] == ["assets/logo.txt"]
    assert plan["pre_delete_dirs"] == ["assets"]
