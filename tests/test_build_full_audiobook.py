from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from modules.build_full_audiobook import build_full_audiobook


FFMPEG_BIN = shutil.which("ffmpeg")
FFPROBE_BIN = shutil.which("ffprobe")


pytestmark = pytest.mark.skipif(
    not FFMPEG_BIN or not FFPROBE_BIN,
    reason="ffmpeg and ffprobe are required for merged audiobook build tests",
)


def synthesize_mp3(path: Path, duration_seconds: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(FFMPEG_BIN),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-t",
            f"{duration_seconds:g}",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-c:a",
            "libmp3lame",
            "-q:a",
            "9",
            str(path),
        ],
        check=True,
    )


def test_build_full_audiobook_writes_merged_mp3_with_configured_silence(tmp_path: Path) -> None:
    audiobook_root = tmp_path / "audiobook"
    synthesize_mp3(audiobook_root / "tracks" / "01.mp3", 0.25)
    synthesize_mp3(audiobook_root / "tracks" / "02.mp3", 0.25)
    (audiobook_root / "script").mkdir(parents=True)
    (audiobook_root / "script" / "01.md").write_text("# One\n", encoding="utf-8")
    (audiobook_root / "script" / "02.md").write_text("# Two\n", encoding="utf-8")

    manifest_path = audiobook_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "onward_audiobook_manifest_v1",
                "title": "Fixture Audiobook",
                "full_audiobook": {
                    "title": "Full Audiobook",
                    "audio_path": "tracks/full.mp3",
                    "silence_between_tracks_seconds": 0.2,
                },
                "tracks": [
                    {
                        "track_number": 1,
                        "title": "One",
                        "audio_path": "tracks/01.mp3",
                        "script_path": "script/01.md",
                    },
                    {
                        "track_number": 2,
                        "title": "Two",
                        "audio_path": "tracks/02.mp3",
                        "script_path": "script/02.md",
                    },
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    output_path = build_full_audiobook(manifest_path=manifest_path)

    assert output_path.exists()
    duration_probe = subprocess.run(
        [
            str(FFPROBE_BIN),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    duration_seconds = float(duration_probe.stdout.strip())
    assert duration_seconds >= 0.65
