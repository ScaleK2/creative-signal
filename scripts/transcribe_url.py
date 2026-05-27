import argparse
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"


def slugify(value: str) -> str:
    value = value.strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", "_", value)
    return value[:120]


def unique_folder(base_dir: Path, folder_name: str) -> Path:
    target = base_dir / folder_name

    if not target.exists():
        return target

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return base_dir / f"{folder_name}_{timestamp}"


def download_to_staging(url: str, staging_dir: Path, force: bool = False) -> None:
    staging_dir.mkdir(parents=True, exist_ok=True)

    output_template = str(staging_dir / "%(title).120s.%(ext)s")

    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--write-info-json",
        "--no-clean-info-json",
        "-o",
        output_template,
    ]

    if force:
        command.append("--force-overwrites")
    else:
        command.append("--no-overwrites")

    command.append(url)

    subprocess.run(command, check=True)


def organise_downloads(staging_dir: Path, output_dir: Path, force: bool = False) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_files = sorted(staging_dir.glob("*.mp3"))

    if not audio_files:
        raise FileNotFoundError("No MP3 files were created.")

    video_folders = []

    for audio_file in audio_files:
        base_name = slugify(audio_file.stem)
        video_dir = output_dir / base_name

        if video_dir.exists() and force:
            shutil.rmtree(video_dir)

        if video_dir.exists() and not force:
            video_dir = unique_folder(output_dir, base_name)

        video_dir.mkdir(parents=True, exist_ok=True)

        target_audio_path = video_dir / "audio.mp3"
        shutil.move(str(audio_file), str(target_audio_path))

        metadata_source = staging_dir / f"{audio_file.stem}.info.json"
        metadata_target = video_dir / "metadata.info.json"

        if metadata_source.exists():
            shutil.move(str(metadata_source), str(metadata_target))

        video_folders.append(video_dir)

        print(f"\nCreated video folder: {video_dir}")
        print(f"Audio saved: {target_audio_path}")

        if metadata_target.exists():
            print(f"Metadata saved: {metadata_target}")
        else:
            print("Metadata not found.")

    return video_folders


def clean_staging(staging_dir: Path) -> None:
    if staging_dir.exists():
        shutil.rmtree(staging_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube audio into one output folder per video."
    )

    parser.add_argument("url", help="YouTube URL or playlist URL")

    parser.add_argument(
        "--output",
        default=None,
        help="Optional custom output folder. Default: project-root/output",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing matching video folder",
    )

    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR
    staging_dir = output_dir / "_staging_download"

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Output folder: {output_dir}")

    clean_staging(staging_dir)

    print("\nDownloading audio...")
    download_to_staging(args.url, staging_dir, args.force)

    print("\nOrganising downloads...")
    organise_downloads(staging_dir, output_dir, args.force)

    clean_staging(staging_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()