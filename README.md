# Faster Whisper Radio Transcriber

This tool streams audio from a radio source (HLS, direct MP3, or local MP3 file), transcribes it using Faster Whisper, and outputs the transcription.

## Usage

```bash
python src/main.py <input> [output_file]
```

- `<input>`:  
  - HLS stream URL (e.g., `https://example.com/stream.m3u8`)
  - Direct MP3 stream URL (e.g., `https://example.com/live.mp3`)
  - Path to a local MP3 file (e.g., `myfile.mp3`)
- `[output_file]` (optional):  
  - If provided, transcriptions will be appended to this file in addition to being printed to the console.

## Example

```bash
python src/main.py https://example.com/stream.m3u8 transcription.txt
```

This will print transcriptions to the console and also save them to `transcription.txt`.

## Features

- Real-time radio/audio stream transcription
- Optional output to a file
- Graceful shutdown with Ctrl+C

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## License

MIT