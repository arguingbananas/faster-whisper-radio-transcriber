import sys
from transcriber import Transcriber
from radio_stream import RadioStream
from utils import setup_logging
import time

def main():
    setup_logging()

    if len(sys.argv) < 2:
        print("Usage: python main.py <stream_url>")
        sys.exit(1)

    stream_url = sys.argv[1]
    radio_stream = RadioStream(stream_url)
    transcriber = Transcriber()

    radio_stream.fetch_stream()
    try:
        while True:
            time.sleep(8)  # Buffer for (n) seconds
            audio_wav = radio_stream.get_audio_wav()
            if audio_wav:
                transcription = transcriber.transcribe_audio(audio_wav)
                print(transcription)
            else:
                print("No audio buffered yet.")
    except KeyboardInterrupt:
        radio_stream.stop_stream()

if __name__ == "__main__":
    main()