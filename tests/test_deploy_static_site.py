from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import patch

import pytest


def load_deploy_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "scripts" / "deploy_static_site.py"
    spec = importlib.util.spec_from_file_location("deploy_static_site", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeSftpChild:
    def __init__(self, *, exitstatus: int | None, transcript: str) -> None:
        self._final_exitstatus = exitstatus
        self.before = transcript
        self.after = ""
        self.exitstatus: int | None = None
        self.signalstatus: int | None = None
        self.closed = False

    def expect(self, _patterns: list[object]) -> int:
        return 2

    def sendline(self, _value: str) -> None:
        raise AssertionError("The EOF-only fixture should not prompt for input.")

    def close(self) -> None:
        self.closed = True
        self.exitstatus = self._final_exitstatus


def test_run_sftp_rejects_connection_failure_after_eof():
    deploy = load_deploy_module()
    child = FakeSftpChild(
        exitstatus=255,
        transcript="ssh: Could not resolve hostname example.test\nConnection closed\n",
    )
    with patch.object(deploy.pexpect, "spawn", return_value=child):
        with pytest.raises(SystemExit, match="SFTP exited with 255"):
            deploy.run_sftp("ls\n", "example.test", "reader", "secret")
    assert child.closed


def test_run_sftp_accepts_zero_exit_after_waiting_for_child():
    deploy = load_deploy_module()
    child = FakeSftpChild(exitstatus=0, transcript="sftp> ls index.html\nindex.html\n")
    with patch.object(deploy.pexpect, "spawn", return_value=child):
        transcript = deploy.run_sftp("ls\n", "example.test", "reader", "secret")
    assert child.closed
    assert "index.html" in transcript


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
