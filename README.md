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

# Features

## 1. Download Audio From YouTube URLs

Download and extract high-quality MP3 audio locally.

Script:
```bash
python scripts/transcribe_url.py "YOUTUBE_URL"
```

Outputs:
```text
output/audio/
```

Use cases:
- podcast archiving
- creator research
- offline listening
- transcript preparation
- future AI workflows

---

## 2. Transcribe Downloaded Audio

Generate local transcripts using Faster Whisper.

Script:
```bash
python scripts/transcribe_audio.py
```

Outputs:
```text
output/transcripts/
```

Generated files:
- `.txt` → human-readable transcript
- `.json` → structured machine-readable transcript

JSON includes:
- raw seconds
- formatted timestamps
- transcript segments

Example:
```json
{
  "start_seconds": 741.14,
  "end_seconds": 743.70,
  "start_timestamp": "00:12:21",
  "end_timestamp": "00:12:23",
  "text": "So, I'm writing a book right now,"
}
```

---

## 3. Full Pipeline

Download audio + transcribe automatically.

Script:
```bash
python scripts/transcribe_full.py "YOUTUBE_URL"
```

Outputs:
```text
output/audio/
output/transcripts/
```

---

## 4. Transcript Analysis

Analyse transcript structure using OpenAI models.

Script:
```bash
python scripts/analyse_transcript.py "TRANSCRIPT_JSON_PATH"
```

Example:
```bash
python scripts/analyse_transcript.py "output/transcripts/video.json"
```

Outputs:
```text
output/analysis/
```

Analysis includes:
- hook analysis
- persuasion patterns
- content opportunities
- structure breakdowns
- remix ideas
- content strategy insights

---

# Project Structure

```text
creative-signal/
│
├── scripts/
│   ├── transcribe_audio.py
│   ├── transcribe_url.py
│   ├── transcribe_full.py
│   └── analyse_transcript.py
│
├── output/
│   ├── audio/
│   ├── transcripts/
│   └── analysis/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Setup

## 1. Clone Repo

```bash
git clone https://github.com/YOUR_USERNAME/creative-signal.git

cd creative-signal
```

##Quickstart

After cloning repo,

```bash
cd creative-signal
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. Create Virtual Environment

This project uses a Python virtual environment (`.venv`) to keep project dependencies isolated from the rest of the machine.

A virtual environment is a local Python workspace. It means packages like `yt-dlp`, `faster-whisper`, `openai`, and `python-dotenv` are installed only for this project, rather than globally across the computer.

Do not commit `.venv` to GitHub.

The `.venv/` folder is ignored by `.gitignore`.

---

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

## Python Packages

Defined in:
```text
requirements.txt
```

Current packages:
```text
faster-whisper
openai
python-dotenv
yt-dlp
```

---

# FFmpeg Installation

FFmpeg is required for audio extraction.

Check installation:
```bash
ffmpeg -version
```

If FFmpeg is not installed:
https://ffmpeg.org/download.html

---

# OpenAI API Setup

Create:
```text
.env
```

Example:
```env
OPENAI_API_KEY=your_api_key_here
```

Do NOT commit `.env` to GitHub.

---

# Whisper Models

Supported models:
- tiny
- base
- small
- medium
- large-v3

Example:
```bash
python scripts/transcribe_full.py "YOUTUBE_URL" --model small
```

Larger models:
- better quality
- slower processing

---

# Notes

## Transcript Formats

TXT:
- human readable
- easier manual review

JSON:
- structured AI workflows
- semantic analysis
- future vector indexing
- clip extraction
- retrieval systems

---

## Why Separate Scripts?

The pipeline is intentionally modular.

### `transcribe_url.py`
Handles:
```text
URL → MP3
```

Useful independently for:
- offline listening
- audio collection
- dataset building
- future workflows

### `transcribe_audio.py`
Handles:
```text
MP3 → Transcript
```

### `transcribe_full.py`
Handles:
```text
URL → MP3 → Transcript
```

This modular structure allows:
- reusable workflows
- easier debugging
- future scalability
- interchangeable pipeline stages

---

# Future Directions

Potential future layers:
- hook classification
- persuasion analysis
- semantic chunking
- embeddings
- vector search
- creator fingerprinting
- clip extraction
- viral structure analysis
- AI remix generation

---

# Disclaimer

This project is for educational and research purposes.

Ensure you comply with:
- platform terms of service
- copyright laws
- creator rights
- content licensing requirements