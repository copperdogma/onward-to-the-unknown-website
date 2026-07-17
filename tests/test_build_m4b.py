from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
from PIL import Image

from modules.build_family_site import load_audiobook_catalog
from modules.build_m4b import build_m4b, m4b_chapters, validate_m4b
from modules.portable_editions import PortableEditionError, load_portable_catalog


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")

pytestmark = pytest.mark.skipif(
    not FFMPEG or not FFPROBE, reason="ffmpeg and ffprobe are required"
)


def synthesize_mp3(path: Path, frequency: int, duration_seconds: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(FFMPEG),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-t",
            f"{duration_seconds:g}",
            "-i",
            f"sine=frequency={frequency}:sample_rate=44100",
            "-ac",
            "1",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "64k",
            str(path),
        ],
        check=True,
    )


def write_audio_manifest(root: Path) -> Path:
    tracks = []
    for number, title, frequency, duration in (
        (1, "One", 440, 0.35),
        (2, "Two", 660, 0.40),
    ):
        audio_path = root / "tracks" / f"{number:02d}-{title.lower()}.mp3"
        script_path = root / "script" / f"{number:02d}-{title.lower()}.md"
        synthesize_mp3(audio_path, frequency, duration)
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(f"# {title}\n", encoding="utf-8")
        tracks.append(
            {
                "track_number": number,
                "title": title,
                "script_path": str(script_path.relative_to(root)),
                "audio_path": str(audio_path.relative_to(root)),
            }
        )
    manifest = root / "audiobook-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "onward_audiobook_manifest_v1",
                "title": "Fixture Audiobook",
                "full_audiobook": {
                    "title": "Fixture Complete Audiobook",
                    "audio_path": "generated/fixture.mp3",
                    "silence_between_tracks_seconds": 0.2,
                },
                "tracks": tracks,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def write_portable_manifest(root: Path, cover: Path) -> Path:
    relative_root = root.relative_to(ROOT).as_posix()
    manifest = root / "portable-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "onward_portable_editions_v1",
                "publication": {
                    "identifier": "urn:uuid:fixture",
                    "title": "Fixture",
                    "subtitle": "Fixture",
                    "language": "en-CA",
                    "author": "Fixture Family",
                    "publisher": "Fixture Family",
                    "original_publication_year": "1987",
                    "modified": "2026-07-17T20:00:00Z",
                    "description": "Fixture",
                    "source_url": "https://example.test/",
                    "cover_source_path": cover.relative_to(ROOT).as_posix(),
                    "cover_output_path": f"{relative_root}/generated-cover.jpg",
                },
                "epub": {
                    "output_path": f"{relative_root}/fixture.epub",
                    "public_path": "downloads/fixture.epub",
                    "media_type": "application/epub+zip",
                },
                "m4b": {
                    "output_path": f"{relative_root}/fixture.m4b",
                    "public_path": "audiobook/fixture.m4b",
                    "media_type": "audio/mp4",
                    "codec": "aac",
                    "profile": "AAC Low Complexity",
                    "bit_rate": "64k",
                    "sample_rate_hz": 44100,
                    "channels": 1,
                    "narrator": "Fixture Narrator",
                    "expected_chapter_count": 2,
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def test_build_m4b_has_cover_metadata_and_exact_chapters() -> None:
    (ROOT / "build").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "build") as tmp:
        root = Path(tmp)
        audiobook_manifest = write_audio_manifest(root)
        cover = root / "cover.jpg"
        Image.new("RGB", (400, 600), "#38584f").save(cover, "JPEG")
        portable_manifest = write_portable_manifest(root, cover)

        output = build_m4b(audiobook_manifest, portable_manifest)
        audiobook = load_audiobook_catalog(audiobook_manifest)
        assert audiobook is not None
        portable = load_portable_catalog(portable_manifest)
        validation = validate_m4b(output, audiobook, portable)
        chapters = m4b_chapters(audiobook)

        assert validation.ok, validation.errors
        assert [chapter.title for chapter in chapters] == ["One", "Two"]
        assert chapters[0].start_ms == 0
        assert chapters[0].end_ms == chapters[1].start_ms
        assert output.stat().st_size > 1_000
        with pytest.raises(PortableEditionError, match="Refusing to overwrite"):
            build_m4b(audiobook_manifest, portable_manifest)
