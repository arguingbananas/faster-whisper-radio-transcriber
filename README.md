# Faster Whisper Radio Transcriber

This project is designed to transcribe audio input from internet talk radio using the Faster Whisper transcription model. It captures audio from a specified radio stream and processes it for transcription.

## Project Structure

```
faster-whisper-radio-transcriber
├── src
│   ├── main.py          # Entry point of the application
│   ├── transcriber.py   # Contains the Transcriber class for audio transcription
│   ├── radio_stream.py   # Contains the RadioStream class for fetching audio streams
│   └── utils.py         # Utility functions for logging and audio handling
├── requirements.txt     # Lists the project dependencies
└── README.md            # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd faster-whisper-radio-transcriber
pip install -r requirements.txt
```

## Usage

To start the transcription process, run the main application:

```bash
python src/main.py
```

## Functionality

- **Transcriber Class**: Handles the loading of the Faster Whisper model and transcribes audio input.
- **RadioStream Class**: Fetches audio from an internet talk radio source and provides audio data for transcription.
- **Utility Functions**: Includes functions for logging setup and downloading audio segments if necessary.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.