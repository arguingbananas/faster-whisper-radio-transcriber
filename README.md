# Faster Whisper Radio Transcriber

This project transcribes audio from **internet radio streams (HLS/m3u8)** or **local/direct MP3 files/streams** using the Faster Whisper transcription model. It supports real-time streaming, chunked transcription, and can automatically detect the input type (HLS or MP3) without any flags.

---

## Project Structure

```
faster-whisper-radio-transcriber
├── src
│   ├── main.py          # Entry point of the application
│   ├── transcriber.py   # Transcriber class for audio transcription (with chunk overlap support)
│   ├── radio_stream.py  # RadioStream class for fetching HLS streams, MP3 streams, or local MP3 files
│   └── utils.py         # Utility functions for logging and audio handling
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

---

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) (must be installed and in your PATH for audio decoding)
- See `requirements.txt` for Python dependencies:
  - faster-whisper
  - torch
  - requests
  - pydub
  - numpy
  - soundfile
  - m3u8

Install dependencies with:

```bash
pip install -r requirements.txt
```

Install ffmpeg (Linux example):

```bash
sudo apt-get install ffmpeg
```

---

## Usage

To start the transcription process, run:

```bash
python src/main.py <input>
```

Where `<input>` can be:
- An HLS stream URL (ending with `.m3u8` or containing `m3u8`)
- A direct MP3 stream URL
- A path to a local MP3 file

**Examples:**

```bash
python src/main.py https://ample-a.revma.ihrhls.com/zc7729/72_1u78k3rrpowz902/playlist.m3u8?streamid=7729
python src/main.py https://somesite.com/live.mp3
python src/main.py myfile.mp3
```

The program will automatically detect the input type and process accordingly.

---

## Features

- **Automatic Input Detection:** No flags needed—just provide the URL or file path.
- **Supports HLS (m3u8) and MP3:** Handles both streaming and local files.
- **Real-time Streaming:** Buffers and transcribes audio in parallel for low latency.
- **Chunk Overlap (optional):** Improves transcription accuracy at chunk boundaries.
- **Audio Normalization:** Light normalization for improved transcription quality.
- **Threaded Transcription:** Uses a queue and worker thread for efficient processing.
- **Logging:** Logs transcription activity to `transcriber.log`.

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for enhancements or bug fixes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.