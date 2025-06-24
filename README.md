# Faster Whisper Radio Transcriber

This tool streams audio from various sources, transcribes it using Faster Whisper, and can extract trivia questions from the transcription using a local Ollama LLM instance.

## Features

- **Input Sources:**
  - HLS stream URL (e.g., `https://example.com/stream.m3u8`)
  - Direct MP3 stream URL (e.g., `https://example.com/live.mp3`)
  - Local MP3 file (e.g., `myfile.mp3`)
  - System audio input ("linein" for microphone or line-in)
- **Real-time transcription** using [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- **Optional output to file:** Save the latest transcription to a file (overwrites each time)
- **Trivia question extraction** from transcription using a local [Ollama](https://ollama.com/) LLM instance
- **Graceful shutdown** with Ctrl+C

## Usage

```bash
python src/main.py <input> [output_file]
```

- `<input>`:  
  - HLS stream URL (e.g., `https://example.com/stream.m3u8`)
  - Direct MP3 stream URL (e.g., `https://example.com/live.mp3`)
  - Path to a local MP3 file (e.g., `myfile.mp3`)
  - `linein` (use system audio input)
- `[output_file]` (optional):  
  - If provided, the latest transcription will be saved to this file (overwritten each time).

### Example

```bash
python src/main.py https://example.com/stream.m3u8
python src/main.py myfile.mp3 transcript.txt
python src/main.py linein
```

## Requirements

- Python 3.8+
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- torch
- requests
- pydub
- numpy
- soundfile
- m3u8
- sounddevice (for line-in audio)
- PortAudio library (for sounddevice; install with `sudo apt-get install libportaudio2 portaudio19-dev` on Debian/Ubuntu)

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

## Ollama Integration

- The program sends each transcription chunk to a local Ollama LLM instance (default: `http://localhost:11434/api/generate`) to extract trivia questions.
- Make sure Ollama is running and a suitable model (e.g., `qwen3`) is available.

## Output

- Transcriptions are printed to the console as they are generated.
- If `[output_file]` is specified, the latest transcription chunk overwrites the file.
- Extracted questions (if any) are printed to the console.

## License

MIT