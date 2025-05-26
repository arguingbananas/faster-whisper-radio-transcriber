import threading
import requests
from io import BytesIO
import m3u8
import time
from urllib.parse import urljoin
from pydub import AudioSegment

class RadioStream:
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.audio_buffer = BytesIO()
        self.buffer_lock = threading.Lock()
        self.streaming = False
        self.thread = None
        self.seen_segments = set()

    def fetch_stream(self, poll_interval=2):
        def stream_worker():
            while self.streaming:
                try:
                    playlist = m3u8.load(self.stream_url)
                    for segment in playlist.segments:
                        if segment.uri not in self.seen_segments:
                            self.seen_segments.add(segment.uri)
                            segment_url = urljoin(self.stream_url, segment.uri)
                            resp = requests.get(segment_url, stream=True)
                            resp.raise_for_status()
                            with self.buffer_lock:
                                self.audio_buffer.write(resp.content)
                    time.sleep(poll_interval)
                except Exception as e:
                    print(f"Error fetching HLS stream: {e}")
                    time.sleep(poll_interval)
        self.streaming = True
        self.thread = threading.Thread(target=stream_worker, daemon=True)
        self.thread.start()

    def stop_stream(self):
        self.streaming = False
        if self.thread:
            self.thread.join()

    def get_audio(self):
        with self.buffer_lock:
            self.audio_buffer.seek(0)
            data = self.audio_buffer.read()
            self.audio_buffer = BytesIO()  # Clear buffer after reading
        return data

    def get_audio_wav(self):
        """
        Returns the audio buffer as WAV bytes, suitable for Whisper.
        """
        mpegts_data = self.get_audio()
        if not mpegts_data:
            return None
        
        # Decode MPEG-TS to AudioSegment
        audio = AudioSegment.from_file(BytesIO(mpegts_data), format="aac")
        wav_buffer = BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        return wav_buffer