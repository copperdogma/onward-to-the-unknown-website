from __future__ import annotations

import subprocess
from pathlib import Path

from modules.build_family_site import DEFAULT_AUDIOBOOK_MANIFEST_PATH, AudiobookCatalog, load_audiobook_catalog

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNEL_LAYOUT = "stereo"
DEFAULT_MP3_QUALITY = "2"


def resolve_output_path(catalog: AudiobookCatalog, output: str | Path | None = None) -> Path:
    if output is not None:
        return Path(output).expanduser().resolve()
    if catalog.full_audiobook is None:
        raise SystemExit("Audiobook manifest does not declare a `full_audiobook` output.")
    return catalog.full_audiobook.audio_source_path


def build_full_audiobook(
    manifest_path: str | Path | None = DEFAULT_AUDIOBOOK_MANIFEST_PATH,
    *,
    output: str | Path | None = None,
    force: bool = False,
    ffmpeg_bin: str = "ffmpeg",
) -> Path:
    catalog = load_audiobook_catalog(Path(manifest_path) if manifest_path is not None else None)
    if catalog is None:
        raise SystemExit(f"Audiobook manifest not found: {manifest_path}")
    if catalog.full_audiobook is None:
        raise SystemExit("Audiobook manifest does not declare `full_audiobook` metadata.")

    output_path = resolve_output_path(catalog, output)
    if output_path.exists() and not force:
        raise SystemExit(
            "Refusing to overwrite existing full audiobook without --force: "
            f"{output_path}"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    silence_seconds = catalog.full_audiobook.silence_between_tracks_seconds
    command: list[str] = [
        ffmpeg_bin,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if force else "-n",
    ]
    filter_parts: list[str] = []
    concat_inputs: list[str] = []
    input_index = 0

    for track_index, track in enumerate(catalog.tracks):
        command.extend(["-i", str(track.audio_source_path)])
        filter_parts.append(
            f"[{input_index}:a]aresample={DEFAULT_SAMPLE_RATE},"
            f"aformat=sample_fmts=fltp:channel_layouts={DEFAULT_CHANNEL_LAYOUT}[a{input_index}]"
        )
        concat_inputs.append(f"[a{input_index}]")
        input_index += 1
        if track_index == len(catalog.tracks) - 1 or silence_seconds <= 0:
            continue
        command.extend(
            [
                "-f",
                "lavfi",
                "-t",
                f"{silence_seconds:g}",
                "-i",
                f"anullsrc=channel_layout={DEFAULT_CHANNEL_LAYOUT}:sample_rate={DEFAULT_SAMPLE_RATE}",
            ]
        )
        filter_parts.append(
            f"[{input_index}:a]aformat=sample_fmts=fltp:channel_layouts={DEFAULT_CHANNEL_LAYOUT}[a{input_index}]"
        )
        concat_inputs.append(f"[a{input_index}]")
        input_index += 1

    filter_parts.append(f"{''.join(concat_inputs)}concat=n={len(concat_inputs)}:v=0:a=1[outa]")
    command.extend(
        [
            "-filter_complex",
            ";".join(filter_parts),
            "-map",
            "[outa]",
            "-ar",
            str(DEFAULT_SAMPLE_RATE),
            "-ac",
            "2",
            "-c:a",
            "libmp3lame",
            "-q:a",
            DEFAULT_MP3_QUALITY,
            str(output_path),
        ]
    )

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        raise SystemExit(
            "Missing required `ffmpeg` binary. Install ffmpeg to build the merged audiobook."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"ffmpeg failed while building the merged audiobook: {exc}") from exc

    return output_path


def cli_main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Build a merged full-audiobook MP3 from the ordered track set in audiobook/manifest.json."
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_AUDIOBOOK_MANIFEST_PATH),
        help="Path to the audiobook manifest JSON.",
    )
    parser.add_argument(
        "--output",
        help="Override the full audiobook output path. Defaults to manifest full_audiobook.audio_path.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the existing full audiobook if it already exists.",
    )
    args = parser.parse_args(argv)

    output_path = build_full_audiobook(
        manifest_path=args.manifest,
        output=args.output,
        force=args.force,
    )
    print(f"Built merged full audiobook: {output_path}")
    return 0
