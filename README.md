# Jake's Podcast Transcriber

A Python script that aims to accurately transcribe my favorite podcast episodes. 
I haven't found anything else that I liked and worked well, so I created this.

It uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper). This script
uses local models, so you'll need a computer with decent GPU, like Apple Silicon
 or Nvidia.

On my Apple Silicon Mac, it runs roughly 20-25x faster than real-time.

## Getting Started

1. Clone this repo.
2. Run `uv sync` in the cloned directory.

## Usage

`uv run transcribe_podcast.py "41 Harsh Truths for People Who Actually Want to Change - Alex Hormozi (4K) [ky1oHHJ5Ne8].mp3" --output 41.txt`

Or with timestamps:

`uv run transcribe_podcast.py "41 Harsh Truths for People Who Actually Want to Change - Alex Hormozi (4K) [ky1oHHJ5Ne8].mp3" --output 41.txt --timestamps`

### More options:

- `--output` or `-o`: Output transcript file path (optional)
- `--speakers` or `-s`: Number of speakers (default: 2, optional)
- `--timestamps` or `-t`: Include timestamps in output

Then, postprocess the transcript, if you want:

```
sed -i '' 's/SPEAKER_00/Host/g' $1
sed -i '' 's/SPEAKER_01/Guest/g' $1
```

## Downloading A YouTube Video As Audio With `yt-dlp`

`yt-dlp -x --audio-format mp3 -o "audio/%(title)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"`

### Getting `yt-dlp`:

- **macOS**: `brew install yt-dlp`

- **Linux**: Install the `yt-dlp` with your distribution's package manager.

- **Windows**: I don't use Windows. If you get it to work, let me 
know and I will update this documentation!


## Privacy Statement

All data stays on your computer. No data is sent externally.
