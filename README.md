# podcast_transcriber

## Getting Started

1. Clone this repo.
2. Run `uv sync` in the cloned directory.

## Usage

`uv run transcribe_podcast.py "41 Harsh Truths for People Who Actually Want to Change - Alex Hormozi (4K) [ky1oHHJ5Ne8].mp3" --output 41.txt`

Or with timestamps:

`uv run transcribe_podcast.py "41 Harsh Truths for People Who Actually Want to Change - Alex Hormozi (4K) [ky1oHHJ5Ne8].mp3" --output 41.txt --timestamps`

Then, postprocess the transcript, if you want:

```
sed -i '' 's/SPEAKER_00/Host/g' $1
sed -i '' 's/SPEAKER_01/Guest/g' $1
```

## Options

## Downloading A YouTube Video As Audio With `yt-dlp`

`yt-dlp -x --audio-format mp3 -o "audio/%(title)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"`
