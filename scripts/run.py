import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"


def run_command(command: list[str]) -> None:
    print("\nRunning:")
    print(" ".join(command))
    print()

    subprocess.run(command, cwd=PROJECT_ROOT)


def pause() -> None:
    input("\nPress Enter to return to menu...")


def download_audio() -> None:
    url = input("\nPaste YouTube URL or playlist URL: ").strip()

    if not url:
        print("No URL provided.")
        return

    force = input("Force overwrite existing matching folder? (y/n): ").strip().lower() == "y"

    command = ["python", "scripts/transcribe_url.py", url]

    if force:
        command.append("--force")

    run_command(command)


def transcribe_audio() -> None:
    model = input("\nWhisper model [base/small/medium/large-v3] (default: base): ").strip()
    folder = input("Specific video folder name? Leave blank to transcribe all pending: ").strip()
    force = input("Force re-transcribe existing files? (y/n): ").strip().lower() == "y"

    command = ["python", "scripts/transcribe_audio.py"]

    if model:
        command.extend(["--model", model])

    if folder:
        command.extend(["--folder", folder])

    if force:
        command.append("--force")

    run_command(command)


def full_pipeline() -> None:
    url = input("\nPaste YouTube URL or playlist URL: ").strip()

    if not url:
        print("No URL provided.")
        return

    model = input("Whisper model [base/small/medium/large-v3] (default: base): ").strip()
    force = input("Force overwrite/re-transcribe? (y/n): ").strip().lower() == "y"

    command = ["python", "scripts/transcribe_full.py", url]

    if model:
        command.extend(["--model", model])

    if force:
        command.append("--force")

    run_command(command)


def list_video_folders_with_transcripts() -> list[Path]:
    if not OUTPUT_DIR.exists():
        return []

    folders = []

    for folder in sorted(OUTPUT_DIR.iterdir()):
        if not folder.is_dir():
            continue

        if folder.name.startswith("_"):
            continue

        if (folder / "transcript.json").exists():
            folders.append(folder)

    return folders


def analyse_transcript() -> None:
    folders = list_video_folders_with_transcripts()

    if not folders:
        print("\nNo video folders with transcript.json found.")
        print(f"Expected structure: {OUTPUT_DIR}\\video_folder\\transcript.json")
        return

    print("\nAvailable video folders:")

    for index, folder in enumerate(folders, start=1):
        print(f"{index}. {folder.name}")

    choice = input("\nChoose video folder number: ").strip()

    if not choice.isdigit():
        print("Invalid choice.")
        return

    selected_index = int(choice) - 1

    if selected_index < 0 or selected_index >= len(folders):
        print("Choice out of range.")
        return

    selected_folder = folders[selected_index].name

    model = input("OpenAI model (default: gpt-4.1-mini): ").strip()

    command = ["python", "scripts/analyse_transcript.py", selected_folder]

    if model:
        command.extend(["--model", model])

    run_command(command)


def show_menu() -> None:
    print("\n==============================")
    print("Creative Signal")
    print("==============================")
    print("1. Download audio from URL")
    print("2. Transcribe downloaded audio")
    print("3. Download + transcribe")
    print("4. Analyse transcript")
    print("5. Exit")


def main() -> None:
    while True:
        show_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            download_audio()
            pause()

        elif choice == "2":
            transcribe_audio()
            pause()

        elif choice == "3":
            full_pipeline()
            pause()

        elif choice == "4":
            analyse_transcript()
            pause()

        elif choice == "5":
            print("\nExiting.")
            break

        else:
            print("\nInvalid option.")
            pause()


if __name__ == "__main__":
    main()