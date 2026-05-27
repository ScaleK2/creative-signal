# Creative Signal

Creative Signal is a local AI-powered media intelligence pipeline for:

- Downloading audio from YouTube URLs
- Generating local transcripts using Whisper
- Analysing transcript structure and persuasion patterns using LLMs

The goal is to build structured content intelligence workflows for:
- creator analysis
- hook breakdowns
- persuasion analysis
- content strategy
- remix generation
- semantic indexing

---

## Recommended Usage (Menu-First)

The **primary way to use this project** is the interactive menu:

```bash
python scripts/run.py
```

You can then choose:
1. Download audio from URL
2. Transcribe downloaded audio
3. Download + transcribe
4. Analyse transcript
5. Exit

Why this is recommended:
- Easier day-to-day workflow
- Guided prompts for required inputs
- Uses the same active Python interpreter for all subprocess calls

---

## Setup

### 1) Clone repo

```bash
git clone https://github.com/YOUR_USERNAME/creative-signal.git
cd creative-signal
```

### 2) Create virtual environment

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure OpenAI key

Create a `.env` file in project root:

```env
OPENAI_API_KEY=your_api_key_here
```

Do **not** commit `.env`.

### 5) Verify FFmpeg

```bash
ffmpeg -version
```

If missing, install from: https://ffmpeg.org/download.html

---

## Direct Script Usage (Advanced)

You can still run each script directly when needed.

### 1) Download audio (`scripts/transcribe_url.py`)

Download and extract MP3 audio from a YouTube URL or playlist URL.

**Git Bash**
```bash
python scripts/transcribe_url.py "YOUTUBE_URL"
```

Options:
- `--force` overwrite existing matching video folder
- `--output PATH` custom output directory

Creates one folder per video under `output/` with:
- `<video_title>.mp3`
- `metadata.info.json` (if available)

---

### 2) Transcribe downloaded audio (`scripts/transcribe_audio.py`)

Transcribe existing MP3 files inside `output/<video_folder>/`.

```bash
python scripts/transcribe_audio.py
```

Useful options:
- `--model tiny|base|small|medium|large-v3`
- `--folder VIDEO_FOLDER_NAME` (transcribe one folder)
- `--force` (re-transcribe even if transcript files exist)
- `--output PATH`

Outputs in each video folder:
- `transcript.txt`
- `transcript.json`

`transcript.json` includes segment timestamps and source metadata fields.

---

### 3) Full pipeline (`scripts/transcribe_full.py`)

Download + transcribe in one command.

```bash
python scripts/transcribe_full.py "YOUTUBE_URL"
```

Useful options:
- `--model tiny|base|small|medium|large-v3`
- `--force`
- `--output PATH`

---

### 4) Transcript analysis (`scripts/analyse_transcript.py`)

Generate a structured content-intelligence report from a transcript.

```bash
python scripts/analyse_transcript.py "VIDEO_FOLDER_NAME"
```

Also accepts transcript file path/name as input.

Useful options:
- `--model MODEL_NAME` (default: `gpt-4.1-mini`)
- `--output PATH`

Analysis output is saved under each video folder in:
- `analysis/<timestamp>/analysis.md`
- `analysis/<timestamp>/prompt.txt`
- `analysis/<timestamp>/metadata.json`

Includes:
- Executive summary
- Core message
- Hook analysis
- Structure breakdown
- Persuasion patterns
- Content opportunities
- Remix ideas
- Strategic takeaway

---

## Project Structure

```text
creative-signal/
├── scripts/
│   ├── run.py
│   ├── transcribe_url.py
│   ├── transcribe_audio.py
│   ├── transcribe_full.py
│   └── analyse_transcript.py
├── output/
│   └── <video_folder>/
│       ├── <video_title>.mp3
│       ├── metadata.info.json
│       ├── transcript.txt
│       ├── transcript.json
│       └── analysis/
├── .env.example
├── requirements.txt
└── README.md
```

---

## Requirements

From `requirements.txt`:

- faster-whisper
- openai
- python-dotenv
- yt-dlp

