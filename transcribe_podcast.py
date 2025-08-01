import numpy as np
from faster_whisper import WhisperModel
import json
import argparse
import os
import sys
import wave
import struct


def simple_speaker_detection(segments, n_speakers=2):
    """
    Simple speaker detection based on speech patterns and pauses.
    This is a heuristic approach that works reasonably well for podcasts.
    """
    print(f"Applying simple speaker detection for {n_speakers} speakers...")

    # Calculate pause durations between segments
    pauses = []
    for i in range(1, len(segments)):
        pause_duration = segments[i].start - segments[i - 1].end
        pauses.append(pause_duration)

    # Use pause duration and segment length patterns to detect speaker changes
    speaker_changes = [0]  # First segment is always speaker 0
    current_speaker = 0

    for i, segment in enumerate(segments[1:], 1):
        prev_segment = segments[i - 1]
        pause_duration = segment.start - prev_segment.end

        # Heuristics for speaker change detection:
        # 1. Long pause (> 1 second) suggests speaker change
        # 2. Very short segments followed by longer ones
        # 3. Significant change in segment duration patterns

        change_score = 0

        # Long pause indicator
        if pause_duration > 1.0:
            change_score += 2
        elif pause_duration > 0.5:
            change_score += 1

        # Segment length pattern changes
        if len(prev_segment.text) < 50 and len(segment.text) > 100:
            change_score += 1
        elif len(prev_segment.text) > 100 and len(segment.text) < 50:
            change_score += 1

        # Apply speaker change if score is high enough
        if change_score >= 2:
            current_speaker = (current_speaker + 1) % n_speakers

        speaker_changes.append(current_speaker)

    return speaker_changes


def transcribe_with_speakers(audio_file, n_speakers=2):
    print("Loading Faster Whisper model...")
    model = WhisperModel("base", device="cpu", compute_type="int8")

    print("Transcribing audio...")
    segments, info = model.transcribe(audio_file, beam_size=5)
    segments = list(segments)

    print(
        f"Detected language: {info.language} (probability: {info.language_probability:.2f})"
    )

    # Apply simple speaker detection
    speaker_assignments = simple_speaker_detection(segments, n_speakers)

    # Create result segments with speaker information
    result_segments = []

    for i, segment in enumerate(segments):
        result_segments.append(
            {
                "start": segment.start,
                "end": segment.end,
                "speaker": f"SPEAKER_{speaker_assignments[i]:02d}",
                "text": segment.text,
            }
        )

    return result_segments


def format_output(segments):
    output = []
    current_speaker = None
    current_text = []

    for segment in segments:
        if segment["speaker"] != current_speaker:
            if current_text:
                output.append(f"\n{current_speaker}: {' '.join(current_text)}\n")
            current_speaker = segment["speaker"]
            current_text = [segment["text"].strip()]
        else:
            current_text.append(segment["text"].strip())

    # Add the last segment
    if current_text:
        output.append(f"\n{current_speaker}: {' '.join(current_text)}\n")

    return "".join(output)


def format_output_with_timestamps(segments):
    """Alternative format with timestamps"""
    output = []

    for segment in segments:
        start_min = int(segment["start"] // 60)
        start_sec = int(segment["start"] % 60)
        timestamp = f"[{start_min:02d}:{start_sec:02d}]"
        output.append(f"{timestamp} {segment['speaker']}: {segment['text'].strip()}\n")

    return "".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio file with simple speaker detection"
    )
    parser.add_argument("audio_file", help="Path to the audio file (MP3, WAV, etc.)")
    parser.add_argument("--output", "-o", help="Output transcript file path (optional)")
    parser.add_argument(
        "--speakers", "-s", type=int, default=2, help="Number of speakers (default: 2)"
    )
    parser.add_argument(
        "--timestamps", "-t", action="store_true", help="Include timestamps in output"
    )

    args = parser.parse_args()

    # Check if audio file exists
    if not os.path.exists(args.audio_file):
        print(f"Error: Audio file '{args.audio_file}' not found.")
        sys.exit(1)

    # Get base filename for output files
    base_name = os.path.splitext(os.path.basename(args.audio_file))[0]

    # Clean up base name (remove problematic characters)
    base_name = "".join(
        c for c in base_name if c.isalnum() or c in (" ", "-", "_")
    ).rstrip()
    base_name = base_name.replace(" ", "_")

    # Set output file path
    if args.output:
        output_file = args.output
    else:
        output_file = f"{base_name}_transcript.txt"

    json_file = f"{base_name}_segments.json"

    print(f"Processing {args.audio_file}...")
    print(f"Detecting {args.speakers} speakers...")

    try:
        segments = transcribe_with_speakers(args.audio_file, n_speakers=args.speakers)

        # Format output
        if args.timestamps:
            formatted_output = format_output_with_timestamps(segments)
        else:
            formatted_output = format_output(segments)

        # Save transcript to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_output)

        print(f"Transcript saved to {output_file}")

        # Also save raw segments as JSON for further processing
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(segments, f, indent=2, ensure_ascii=False)

        print(f"Raw segments saved to {json_file}")
        print(f"\nProcessed {len(segments)} segments")
        print("\nFirst few lines:")
        print(formatted_output[:500] + "...")

    except Exception as e:
        print(f"Error processing audio file: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
