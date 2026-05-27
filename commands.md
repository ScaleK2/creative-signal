# Creative Signal Commands

## Activate Environment

```bash
cd C:\Projects\creative-signal

.venv\Scripts\activate
```

---

# Audio Downloading

## Download Single YouTube Audio

```bash
python scripts/transcribe_url.py "YOUTUBE_URL"
```

Example:

```bash
python scripts/transcribe_url.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Output:

```text
output/audio/
```

---

## Download Full YouTube Playlist Audio

```bash
python scripts/transcribe_url.py "PLAYLIST_URL"
```

Example:

```bash
python scripts/transcribe_url.py "https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID"
```

Output:

```text
output/audio/
```

---

## Force Re-download / Overwrite Existing Audio

```bash
python scripts/transcribe_url.py "YOUTUBE_URL" --force
```

---

## Custom Audio Output Folder

```bash
python scripts/transcribe_url.py "YOUTUBE_URL" --output "custom/folder/path"
```

---

# Audio Transcription

## Transcribe Existing Downloaded Audio

```bash
python scripts/transcribe_audio.py
```

Outputs:

```text
output/transcripts/
```

Generated files:

- .txt → Human-readable transcript
- .json → Structured machine-readable transcript

---

## Transcribe Using Better Whisper Model

```bash
python scripts/transcribe_audio.py --model small
```

Supported models:

- tiny
- base
- small
- medium
- large-v3

Notes:

- Larger models = better quality
- Larger models = slower processing

---

# Full Pipeline

## Download + Transcribe Automatically

```bash
python scripts/transcribe_full.py "YOUTUBE_URL"
```

Outputs:

```text
output/audio/
output/transcripts/
```

---

## Full Pipeline With Better Model

```bash
python scripts/transcribe_full.py "YOUTUBE_URL" --model small
```

---

# Transcript Analysis

## Analyse Transcript JSON

```bash
python scripts/analyse_transcript.py "output/transcripts/FILE_NAME.json"
```

Example:

```bash
python scripts/analyse_transcript.py "output/transcripts/The_Psychology_of_Making_People_Respect_You_Instantly.json"
```

Outputs:

```text
output/analysis/
```

Generated analysis includes:

- Executive summary
- Hook analysis
- Structure breakdown
- Persuasion patterns
- Content opportunities
- Remix ideas
- Strategic takeaways

---

# Dependency Installation

## Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

## Create `.env`

```env
OPENAI_API_KEY=your_api_key_here
```

Do NOT commit `.env` to GitHub.

---

# Verification Commands

## Check FFmpeg Installation

```bash
ffmpeg -version
```

---

## Check Node.js Installation

```bash
node -v

npm -v
```

---

## Check Python Version

```bash
python --version
```

---

# Git Commands

## Initialise Git Repo

```bash
git init
```

---

## Add Files

```bash
git add .
```

---

## Commit Changes

```bash
git commit -m "Initial commit"
```

---

## Connect GitHub Repo

```bash
git remote add origin https://github.com/YOUR_USERNAME/creative-signal.git
```

---

## Push To GitHub

```bash
git branch -M main

git push -u origin main
```

---

# Recommended Project Structure

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
├── docs/
│   └── COMMANDS.md
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Notes

## TXT vs JSON Outputs

### TXT
Human-readable transcript.

Best for:
- manual review
- reading
- prompting LLMs

### JSON
Structured transcript.

Best for:
- AI pipelines
- semantic search
- embeddings
- clip extraction
- future analysis systems

---

# Future Ideas

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
- content intelligence dashboards
- retrieval-augmented generation (RAG)

```