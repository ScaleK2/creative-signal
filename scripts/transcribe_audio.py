import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"


def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"


def find_video_folders(output_dir: Path) -> list[Path]:
    folders = []

    for folder in sorted(output_dir.iterdir()):
        if not folder.is_dir():
            continue

        if folder.name.startswith("_"):
            continue

        if any(folder.glob("*.mp3")):
            folders.append(folder)

    return folders




def find_audio_file(video_dir: Path) -> Path:
    mp3_files = sorted(video_dir.glob("*.mp3"))

    if not mp3_files:
        raise FileNotFoundError(f"No MP3 file found in: {video_dir}")

    return mp3_files[0]


def transcript_exists(video_dir: Path) -> bool:
    return (video_dir / "transcript.txt").exists() and (video_dir / "transcript.json").exists()


def load_metadata(video_dir: Path) -> dict:
    metadata_path = video_dir / "metadata.info.json"

    if not metadata_path.exists():
        return {}

    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def extract_metadata_fields(metadata: dict) -> dict:
    if not metadata:
        return {}

    return {
        "source_title": metadata.get("title"),
        "source_url": metadata.get("webpage_url") or metadata.get("original_url"),
        "original_url": metadata.get("original_url"),
        "webpage_url": metadata.get("webpage_url"),
        "video_id": metadata.get("id"),
        "channel": metadata.get("channel") or metadata.get("uploader"),
        "channel_id": metadata.get("channel_id") or metadata.get("uploader_id"),
        "duration_seconds": metadata.get("duration"),
        "upload_date": metadata.get("upload_date"),
    }


def transcribe_video_folder(video_dir: Path, model: WhisperModel, model_size: str) -> None:
    audio_path = find_audio_file(video_dir)
    metadata = load_metadata(video_dir)
    source_metadata = extract_metadata_fields(metadata)

    print(f"\nTranscribing: {video_dir.name}")

    segments, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        vad_filter=True,
    )

    transcript_segments = []
    plain_lines = []

    for segment in segments:
        text = segment.text.strip()

        if not text:
            continue

        start_timestamp = format_timestamp(segment.start)
        end_timestamp = format_timestamp(segment.end)

        transcript_segments.append({
            "start_seconds": round(segment.start, 2),
            "end_seconds": round(segment.end, 2),
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "text": text,
        })

        line = f"[{start_timestamp} - {end_timestamp}] {text}"
        plain_lines.append(line)
        print(line)

    result = {
        "video_folder": str(video_dir),
        "audio_file": str(audio_path),
        "model": model_size,
        "language": info.language,
        "language_probability": info.language_probability,
        "source_metadata": source_metadata,
        "full_transcript": "\n".join(plain_lines),
        "segments": transcript_segments,
    }

    txt_path = video_dir / "transcript.txt"
    json_path = video_dir / "transcript.json"

    txt_path.write_text(result["full_transcript"], encoding="utf-8")
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"\nTranscript TXT saved: {txt_path}")
    print(f"Transcript JSON saved: {json_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio.mp3 files inside output/video folders."
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Optional custom output folder. Default: project-root/output",
    )

    parser.add_argument(
        "--folder",
        default=None,
        help="Optional specific video folder name to transcribe",
    )

    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model size: tiny, base, small, medium, large-v3",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-transcribe even if transcript files already exist",
    )

    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Output folder: {output_dir}")

    if not output_dir.exists():
        raise FileNotFoundError(f"Output folder does not exist: {output_dir}")

    if args.folder:
        video_folders = [output_dir / args.folder]
    else:
        video_folders = find_video_folders(output_dir)

    video_folders = [folder for folder in video_folders if folder.exists()]

    if not video_folders:
        raise FileNotFoundError("No video folders with MP3 files found.")

    pending_folders = []

    for folder in video_folders:
        if args.force or not transcript_exists(folder):
            pending_folders.append(folder)
        else:
            print(f"Skipping existing transcript: {folder.name}")

    if not pending_folders:
        print("\nNo new audio files to transcribe.")
        return

    print(f"\nLoading Whisper model: {args.model}")
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    for video_dir in pending_folders:
        transcribe_video_folder(video_dir, model, args.model)

    print("\nDone.")


if __name__ == "__main__":
    main()