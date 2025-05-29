import sys
from transcriber import Transcriber
from radio_stream import RadioStream
from utils import setup_logging
import time
import threading
from queue import Queue, Empty

def transcription_worker(audio_queue, transcriber, stop_event):
    while not stop_event.is_set():
        try:
            audio_wav = audio_queue.get(timeout=1)
            if audio_wav:
                transcription = transcriber.transcribe_audio(audio_wav)
                print(transcription)
            audio_queue.task_done()
        except Empty:
            continue

def main():
    setup_logging()

    if len(sys.argv) < 2:
        print("Usage: python main.py <input>")
        print("  <input> can be one of the following:")
        print("    - HLS stream URL (e.g., https://example.com/stream.m3u8)")
        print("    - Direct MP3 stream URL (e.g., https://example.com/live.mp3)")
        print("    - Path to a local MP3 file (e.g., myfile.mp3)")
        sys.exit(1)

    stream_url = sys.argv[1]
    radio_stream = RadioStream(stream_url)
    transcriber = Transcriber(model_name="base.en", chunk_overlap_sec=0)

    # Initialize the audio queue and worker thread for transcription
    audio_queue = Queue(maxsize=5)
    stop_event = threading.Event()
    worker_thread = threading.Thread(target=transcription_worker, args=(audio_queue, transcriber, stop_event), daemon=True)

    radio_stream.fetch_stream()
    worker_thread.start()

    try:
        while True:
            time.sleep(10)  # Buffer for (n) seconds
            audio_wav = radio_stream.get_audio_wav()
            if audio_wav:
                try:
                    audio_queue.put(audio_wav, timeout=2)
                except:
                    print("Transcription queue is full, dropping audio chunk.")
            else:
                print("No audio buffered yet.")
    except KeyboardInterrupt:
        radio_stream.stop_stream()
        stop_event.set()
        worker_thread.join()

if __name__ == "__main__":
    main()