"""Build and validate a chaptered M4B from the reviewed audiobook tracks."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from modules.build_family_site import (
    DEFAULT_AUDIOBOOK_MANIFEST_PATH,
    AudiobookCatalog,
    load_audiobook_catalog,
)
from modules.portable_editions import (
    DEFAULT_MANIFEST_PATH as PORTABLE_MANIFEST_PATH,
    PortableCatalog,
    PortableEditionError,
    ensure_portable_cover,
    load_portable_catalog,
)


@dataclass(frozen=True)
class M4BChapter:
    number: int
    title: str
    start_ms: int
    end_ms: int


@dataclass
class M4BValidation:
    errors: list[str]
    notes: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_audiobook_catalog(path: str | Path) -> AudiobookCatalog:
    try:
        catalog = load_audiobook_catalog(Path(path))
    except SystemExit as exc:
        raise PortableEditionError(str(exc)) from exc
    if catalog is None or catalog.full_audiobook is None:
        raise PortableEditionError("Audiobook manifest requires a full_audiobook contract.")
    return catalog


def m4b_chapters(catalog: AudiobookCatalog) -> list[M4BChapter]:
    if catalog.full_audiobook is None:
        raise PortableEditionError("Audiobook manifest requires full-audiobook pause metadata.")
    chapters: list[M4BChapter] = []
    cursor_ms = 0
    pause_ms = round(catalog.full_audiobook.silence_between_tracks_seconds * 1000)
    for index, track in enumerate(catalog.tracks):
        if track.duration_seconds is None:
            raise PortableEditionError(
                f"Track {track.track_number:02d} cannot be probed for M4B chapter math."
            )
        track_ms = round(track.duration_seconds * 1000)
        end_ms = cursor_ms + track_ms + (pause_ms if index < len(catalog.tracks) - 1 else 0)
        chapters.append(M4BChapter(track.track_number, track.title, cursor_ms, end_ms))
        cursor_ms = end_ms
    return chapters


def _ffmetadata_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("=", "\\=")
        .replace(";", "\\;")
        .replace("#", "\\#")
        .replace("\n", "\\\n")
    )


def chapter_metadata(
    audiobook: AudiobookCatalog,
    portable: PortableCatalog,
    chapters: list[M4BChapter],
) -> str:
    narrator = str(portable.m4b.settings.get("narrator") or "ElevenLabs narration")
    lines = [
        ";FFMETADATA1",
        f"title={_ffmetadata_escape(portable.publication.title)}",
        f"album={_ffmetadata_escape(portable.publication.title)}",
        f"artist={_ffmetadata_escape(portable.publication.author)}",
        f"comment={_ffmetadata_escape('Narrated with ' + narrator)}",
        "genre=Audiobook",
    ]
    for chapter in chapters:
        lines.extend(
            [
                "[CHAPTER]",
                "TIMEBASE=1/1000",
                f"START={chapter.start_ms}",
                f"END={chapter.end_ms}",
                f"title={_ffmetadata_escape(f'{chapter.number:02d}. {chapter.title}')}",
            ]
        )
    return "\n".join(lines) + "\n"


def probe_media(path: str | Path, *, ffprobe_bin: str | None = None) -> dict[str, object]:
    executable = ffprobe_bin or shutil.which("ffprobe")
    if not executable:
        raise PortableEditionError("Missing required `ffprobe` binary.")
    completed = subprocess.run(
        [
            executable,
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-show_chapters",
            "-of",
            "json",
            str(Path(path)),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise PortableEditionError(f"ffprobe failed for {path}: {completed.stderr.strip()}")
    return json.loads(completed.stdout)


def preflight_tracks(catalog: AudiobookCatalog) -> None:
    errors: list[str] = []
    hashes: dict[str, int] = {}
    for track in catalog.tracks:
        label = f"Track {track.track_number:02d}"
        if not track.audio_source_path.is_file():
            errors.append(f"{label} is missing: {track.audio_source_path}")
            continue
        if track.duration_seconds is None or track.duration_seconds <= 0:
            errors.append(f"{label} has no usable duration.")
        digest = hash_file(track.audio_source_path)
        duplicate = hashes.get(digest)
        if duplicate is not None:
            errors.append(f"{label} duplicates track {duplicate:02d} byte-for-byte.")
        hashes[digest] = track.track_number
    if errors:
        raise PortableEditionError(
            "M4B track preflight failed:\n" + "\n".join(f"- {error}" for error in errors)
        )


def validate_m4b(
    path: str | Path,
    audiobook_catalog: AudiobookCatalog,
    portable_catalog: PortableCatalog,
    *,
    ffprobe_bin: str | None = None,
) -> M4BValidation:
    m4b = Path(path)
    validation = M4BValidation([], [])
    validation.require(m4b.is_file() and m4b.stat().st_size > 0, f"M4B is missing or empty: {m4b}")
    if not m4b.is_file():
        return validation
    try:
        payload = probe_media(m4b, ffprobe_bin=ffprobe_bin)
    except PortableEditionError as exc:
        validation.errors.append(str(exc))
        return validation
    streams = payload.get("streams") if isinstance(payload.get("streams"), list) else []
    audio_streams = [
        stream
        for stream in streams
        if isinstance(stream, dict) and stream.get("codec_type") == "audio"
    ]
    cover_streams = [
        stream
        for stream in streams
        if isinstance(stream, dict)
        and stream.get("codec_type") == "video"
        and int((stream.get("disposition") or {}).get("attached_pic") or 0) == 1
    ]
    validation.require(len(audio_streams) == 1, f"M4B has {len(audio_streams)} audio streams, expected 1.")
    validation.require(len(cover_streams) == 1, f"M4B has {len(cover_streams)} attached covers, expected 1.")
    if audio_streams:
        audio = audio_streams[0]
        validation.require(
            audio.get("codec_name") == portable_catalog.m4b.settings.get("codec"),
            f"M4B audio codec is {audio.get('codec_name')!r}.",
        )
        validation.require(
            int(audio.get("sample_rate") or 0)
            == int(portable_catalog.m4b.settings.get("sample_rate_hz") or 0),
            "M4B sample rate is wrong.",
        )
        validation.require(
            int(audio.get("channels") or 0)
            == int(portable_catalog.m4b.settings.get("channels") or 0),
            "M4B channel count is wrong.",
        )
        profile = str(audio.get("profile") or "")
        validation.require(
            "LC" in profile or "Low Complexity" in profile,
            f"M4B AAC profile is not LC: {profile!r}",
        )
    chapters = payload.get("chapters") if isinstance(payload.get("chapters"), list) else []
    expected = m4b_chapters(audiobook_catalog)
    validation.require(
        len(chapters) == len(expected),
        f"M4B has {len(chapters)} chapters, expected {len(expected)}.",
    )
    for actual, wanted in zip(chapters, expected):
        tags = actual.get("tags") if isinstance(actual, dict) else {}
        if not isinstance(tags, dict):
            tags = {}
        title = str(tags.get("title") or "")
        expected_title = f"{wanted.number:02d}. {wanted.title}"
        validation.require(
            title == expected_title,
            f"M4B chapter {wanted.number:02d} title is {title!r}, expected {expected_title!r}.",
        )
        actual_start = round(float(actual.get("start_time") or 0) * 1000)
        actual_end = round(float(actual.get("end_time") or 0) * 1000)
        validation.require(
            abs(actual_start - wanted.start_ms) <= 2,
            f"M4B chapter {wanted.number:02d} starts at {actual_start} ms, expected {wanted.start_ms}.",
        )
        validation.require(
            abs(actual_end - wanted.end_ms) <= 2,
            f"M4B chapter {wanted.number:02d} ends at {actual_end} ms, expected {wanted.end_ms}.",
        )
    format_payload = payload.get("format") if isinstance(payload.get("format"), dict) else {}
    duration = float(format_payload.get("duration") or 0)
    expected_duration = expected[-1].end_ms / 1000 if expected else 0
    validation.require(
        abs(duration - expected_duration) <= 2.0,
        f"M4B duration is {duration:.3f}s, expected {expected_duration:.3f}s.",
    )
    tags = format_payload.get("tags") if isinstance(format_payload.get("tags"), dict) else {}
    tag_map = {str(key).lower(): str(value) for key, value in tags.items()}
    publication = portable_catalog.publication
    for key, wanted in (
        ("title", publication.title),
        ("album", publication.title),
        ("artist", publication.author),
    ):
        validation.require(
            tag_map.get(key) == wanted,
            f"M4B metadata {key} is {tag_map.get(key)!r}, expected {wanted!r}.",
        )
    narrator = str(portable_catalog.m4b.settings.get("narrator") or "")
    validation.require(
        narrator in tag_map.get("comment", ""),
        "M4B metadata does not identify the narration.",
    )
    validation.notes.append(
        f"M4B contains {len(chapters)} chapters, {len(streams)} streams, "
        f"{duration:.3f} seconds, and {m4b.stat().st_size} bytes."
    )
    return validation


def build_m4b(
    audiobook_manifest_path: str | Path = DEFAULT_AUDIOBOOK_MANIFEST_PATH,
    portable_manifest_path: str | Path = PORTABLE_MANIFEST_PATH,
    *,
    output: str | Path | None = None,
    force: bool = False,
    ffmpeg_bin: str | None = None,
) -> Path:
    audiobook = require_audiobook_catalog(audiobook_manifest_path)
    portable = load_portable_catalog(portable_manifest_path)
    expected_count = int(portable.m4b.settings.get("expected_chapter_count") or 0)
    if len(audiobook.tracks) != expected_count:
        raise PortableEditionError(
            f"Audiobook has {len(audiobook.tracks)} tracks, expected {expected_count} for M4B."
        )
    preflight_tracks(audiobook)
    chapters = m4b_chapters(audiobook)
    output_path = Path(output).expanduser().resolve() if output else portable.m4b.output_path
    if output_path.exists() and not force:
        raise PortableEditionError(
            f"Refusing to overwrite existing M4B without --force: {output_path}"
        )
    executable = ffmpeg_bin or shutil.which("ffmpeg")
    if not executable:
        raise PortableEditionError("Missing required `ffmpeg` binary.")
    cover = ensure_portable_cover(portable.publication, force=force)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="onward-m4b-") as tmp:
        metadata_path = Path(tmp) / "chapters.ffmeta"
        metadata_path.write_text(
            chapter_metadata(audiobook, portable, chapters), encoding="utf-8"
        )
        command = [executable, "-hide_banner", "-loglevel", "error", "-y" if force else "-n"]
        for track in audiobook.tracks:
            command.extend(["-i", str(track.audio_source_path)])
        cover_index = len(audiobook.tracks)
        metadata_index = cover_index + 1
        command.extend(["-i", str(cover), "-f", "ffmetadata", "-i", str(metadata_path)])
        sample_rate = int(portable.m4b.settings.get("sample_rate_hz") or 44100)
        channels = int(portable.m4b.settings.get("channels") or 1)
        layout = "mono" if channels == 1 else "stereo"
        pause = audiobook.full_audiobook.silence_between_tracks_seconds
        filter_parts: list[str] = []
        concat_inputs: list[str] = []
        for index, _track in enumerate(audiobook.tracks):
            filters = (
                f"[{index}:a]aresample={sample_rate},"
                f"aformat=sample_fmts=fltp:channel_layouts={layout}"
            )
            if index < len(audiobook.tracks) - 1 and pause > 0:
                filters += f",apad=pad_dur={pause:g}"
            filters += f"[a{index}]"
            filter_parts.append(filters)
            concat_inputs.append(f"[a{index}]")
        filter_parts.append(
            f"{''.join(concat_inputs)}concat=n={len(concat_inputs)}:v=0:a=1[outa]"
        )
        narrator = str(portable.m4b.settings.get("narrator") or "ElevenLabs narration")
        command.extend(
            [
                "-filter_complex",
                ";".join(filter_parts),
                "-map",
                "[outa]",
                "-map",
                f"{cover_index}:v:0",
                "-map_metadata",
                str(metadata_index),
                "-map_chapters",
                str(metadata_index),
                "-c:a",
                "aac",
                "-profile:a",
                "aac_low",
                "-b:a",
                str(portable.m4b.settings.get("bit_rate") or "64k"),
                "-ar",
                str(sample_rate),
                "-ac",
                str(channels),
                "-c:v",
                "mjpeg",
                "-disposition:v:0",
                "attached_pic",
                "-metadata:s:v:0",
                "title=Cover",
                "-metadata:s:v:0",
                "comment=Cover (front)",
                "-metadata",
                f"title={portable.publication.title}",
                "-metadata",
                f"album={portable.publication.title}",
                "-metadata",
                f"artist={portable.publication.author}",
                "-metadata",
                f"comment=Narrated with {narrator}",
                "-metadata",
                "genre=Audiobook",
                "-metadata",
                f"date={portable.publication.original_publication_year}",
                "-movflags",
                "+faststart",
                str(output_path),
            ]
        )
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            output_path.unlink(missing_ok=True)
            raise PortableEditionError(
                f"ffmpeg failed while building M4B (exit {completed.returncode})."
            )
    validation = validate_m4b(output_path, audiobook, portable)
    if not validation.ok:
        output_path.unlink(missing_ok=True)
        raise PortableEditionError(
            "Built M4B failed validation:\n"
            + "\n".join(f"- {error}" for error in validation.errors)
        )
    return output_path


def cli_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--audiobook-manifest", default=str(DEFAULT_AUDIOBOOK_MANIFEST_PATH))
    build_parser.add_argument("--portable-manifest", default=str(PORTABLE_MANIFEST_PATH))
    build_parser.add_argument("--output")
    build_parser.add_argument("--force", action="store_true")
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--audiobook-manifest", default=str(DEFAULT_AUDIOBOOK_MANIFEST_PATH))
    validate_parser.add_argument("--portable-manifest", default=str(PORTABLE_MANIFEST_PATH))
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            output = build_m4b(
                args.audiobook_manifest,
                args.portable_manifest,
                output=args.output,
                force=args.force,
            )
            print(f"Built M4B: {output}")
            print(f"Size: {output.stat().st_size} bytes")
            return 0
        audiobook = require_audiobook_catalog(args.audiobook_manifest)
        portable = load_portable_catalog(args.portable_manifest)
        validation = validate_m4b(portable.m4b.output_path, audiobook, portable)
    except PortableEditionError as exc:
        print(f"FAILED: {exc}")
        return 1
    for note in validation.notes:
        print(note)
    if validation.errors:
        print("FAILED M4B validation")
        for error in validation.errors:
            print(f"- {error}")
        return 1
    print("PASS: M4B validation is clean")
    return 0
