import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"
DEFAULT_MODEL = "gpt-4.1-mini"


MODEL_PRICING = {
    "gpt-5.5": {"input": 5.00, "cached_input": 0.50, "output": 30.00},
    "gpt-5.4": {"input": 2.50, "cached_input": 0.25, "output": 15.00},
    "gpt-5.4-mini": {"input": 0.75, "cached_input": 0.075, "output": 4.50},
    "gpt-4.1": {"input": 2.00, "cached_input": 0.50, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "cached_input": 0.10, "output": 1.60},
}


def find_transcript(transcript_input: str, output_dir: Path) -> Path:
    input_path = Path(transcript_input)

    if input_path.is_absolute() and input_path.exists():
        return input_path

    direct_path = PROJECT_ROOT / input_path
    if direct_path.exists():
        return direct_path

    if input_path.suffix == ".json":
        matches = list(output_dir.glob(f"*/{input_path.name}")) + list(output_dir.glob(f"*/transcript.json"))
    else:
        candidate = output_dir / input_path / "transcript.json"
        if candidate.exists():
            return candidate

        matches = [
            path for path in output_dir.glob("*/transcript.json")
            if path.parent.name == transcript_input
        ]

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        print("\nMultiple transcript matches found:")
        for index, match in enumerate(matches, start=1):
            print(f"{index}. {match}")

        choice = input("\nChoose transcript number: ").strip()

        if choice.isdigit():
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(matches):
                return matches[selected_index]

    raise FileNotFoundError(f"Transcript not found for input: {transcript_input}")


def load_transcript(transcript_path: Path) -> dict:
    with transcript_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_transcript_text(transcript_data: dict) -> str:
    segments = transcript_data.get("segments", [])

    if not segments:
        return transcript_data.get("full_transcript", "")

    lines = []

    for segment in segments:
        start = segment.get("start_timestamp", "")
        end = segment.get("end_timestamp", "")
        text = segment.get("text", "")

        if text:
            lines.append(f"[{start} - {end}] {text}")

    return "\n".join(lines)


def build_prompt(transcript_data: dict, transcript_text: str) -> str:
    source_metadata = transcript_data.get("source_metadata", {})
    source_title = source_metadata.get("source_title", "Unknown title")
    source_url = source_metadata.get("source_url", "Unknown URL")
    channel = source_metadata.get("channel", "Unknown channel")

    return f"""
You are a senior creative strategist, content analyst, and performance marketer.

Your task is to analyse the following video transcript to help develop better content.

Be specific. Avoid generic advice. Use the timestamps where useful.

Source:
- Title: {source_title}
- Channel: {channel}
- URL: {source_url}

Return the response in markdown using this exact structure:

# Content Intelligence Report

## 1. Executive Summary
- What this video is about
- Why this content works or does not work
- Best use case for this content

## 2. Core Message
- Main idea
- Supporting ideas
- Strongest claim
- Most reusable insight

## 3. Hook Analysis
Analyse the first 30 seconds.
- Hook type
- Opening promise
- Curiosity gap
- Emotional trigger
- Hook strength score out of 10
- Why it works or fails
- How to improve the hook

## 4. Structure Breakdown
Break the transcript into logical sections.

For each section include:
- Timestamp range
- Section purpose
- Key points
- Viewer emotion or belief shift

## 5. Persuasion Patterns
Identify:
- Authority signals
- Fear/desire triggers
- Status appeals
- Identity framing
- Contrast framing
- Repetition
- Memorable phrases

## 6. Content Opportunities
Generate:
- 10 LinkedIn post angles
- 10 short-form video hooks
- 5 carousel ideas
- 5 newsletter angles

## 7. Remix Ideas
Create:
- 3 TikTok/Reels script concepts
- 3 LinkedIn post concepts
- 3 ad angle concepts

## 8. Strategic Takeaway
What can a creator, marketer, or founder learn from this transcript?

Transcript:
{transcript_text}
"""


def calculate_estimated_cost(model: str, usage) -> dict:
    input_tokens = getattr(usage, "input_tokens", 0) or 0
    output_tokens = getattr(usage, "output_tokens", 0) or 0
    total_tokens = getattr(usage, "total_tokens", input_tokens + output_tokens) or 0

    pricing = MODEL_PRICING.get(model)

    if not pricing:
        return {
            "model": model,
            "pricing_found": False,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "estimated_total_cost_usd": None,
        }

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return {
        "model": model,
        "pricing_found": True,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "input_price_per_1m": pricing["input"],
        "output_price_per_1m": pricing["output"],
        "estimated_input_cost_usd": round(input_cost, 6),
        "estimated_output_cost_usd": round(output_cost, 6),
        "estimated_total_cost_usd": round(input_cost + output_cost, 6),
    }


def print_usage_report(cost_report: dict) -> None:
    print("\n=== OpenAI Usage ===")
    print(f"Model: {cost_report['model']}")
    print(f"Input tokens: {cost_report['input_tokens']:,}")
    print(f"Output tokens: {cost_report['output_tokens']:,}")
    print(f"Total tokens: {cost_report['total_tokens']:,}")

    print("\n=== Estimated Cost ===")
    if not cost_report["pricing_found"]:
        print("Pricing not found for this model.")
        return

    print(f"Input cost: ${cost_report['estimated_input_cost_usd']:.6f}")
    print(f"Output cost: ${cost_report['estimated_output_cost_usd']:.6f}")
    print(f"Total cost: ${cost_report['estimated_total_cost_usd']:.6f}")


def run_analysis(prompt: str, model: str) -> tuple[str, dict]:
    client = OpenAI()

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    cost_report = calculate_estimated_cost(model, response.usage)
    print_usage_report(cost_report)

    return response.output_text, cost_report


def save_analysis(
    analysis_text: str,
    prompt: str,
    transcript_path: Path,
    model: str,
    cost_report: dict,
) -> None:
    video_dir = transcript_path.parent
    analysis_root = video_dir / "analysis"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = analysis_root / timestamp

    run_dir.mkdir(parents=True, exist_ok=True)

    analysis_path = run_dir / "analysis.md"
    prompt_path = run_dir / "prompt.txt"
    metadata_path = run_dir / "metadata.json"

    metadata = {
        "video_folder": str(video_dir),
        "source_transcript": str(transcript_path),
        "analysis_file": str(analysis_path),
        "prompt_file": str(prompt_path),
        "model": model,
        "created_at": timestamp,
        "usage": cost_report,
    }

    analysis_path.write_text(analysis_text, encoding="utf-8")
    prompt_path.write_text(prompt, encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"\nAnalysis folder: {run_dir}")


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY not found in project-root .env file.")

    parser = argparse.ArgumentParser(
        description="Analyse a transcript.json file inside an output video folder."
    )

    parser.add_argument(
        "transcript",
        help="Video folder name, transcript.json path, or transcript filename",
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model to use. Default: {DEFAULT_MODEL}",
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Optional custom output root. Default: project-root/output",
    )

    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR

    transcript_path = find_transcript(args.transcript, output_dir)

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Transcript file: {transcript_path}")
    print(f"Model: {args.model}")

    print("\nLoading transcript...")
    transcript_data = load_transcript(transcript_path)

    print("Building prompt...")
    transcript_text = build_transcript_text(transcript_data)
    prompt = build_prompt(transcript_data, transcript_text)

    print("Running analysis...")
    analysis_text, cost_report = run_analysis(prompt, args.model)

    save_analysis(
        analysis_text=analysis_text,
        prompt=prompt,
        transcript_path=transcript_path,
        model=args.model,
        cost_report=cost_report,
    )

    print("\nDone.")


if __name__ == "__main__":
    main()