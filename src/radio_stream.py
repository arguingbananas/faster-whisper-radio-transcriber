import threading
import requests
from io import BytesIO
import m3u8
import time
from urllib.parse import urljoin
from pydub import AudioSegment
import os

class RadioStream:
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.audio_buffer = BytesIO()
        self.buffer_lock = threading.Lock()
        self.streaming = False
        self.thread = None
        self.seen_segments = set()
        self.is_file = os.path.isfile(stream_url)
        self.is_hls = (".m3u8" in stream_url or "m3u8" in stream_url) and not self.is_file

    def fetch_stream(self, poll_interval=2):
        if self.is_file:
            with open(self.stream_url, "rb") as f:
                with self.buffer_lock:
                    self.audio_buffer.write(f.read())
        elif self.is_hls:
            self._fetch_hls_stream(poll_interval)
        else:
            self._fetch_mp3_stream()

    def _fetch_hls_stream(self, poll_interval=2):
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
        raw_data = self.get_audio()
        if not raw_data:
            return None

        # Choose format based on input type
        if self.is_file:
            # Assume local file is mp3
            audio = AudioSegment.from_file(BytesIO(raw_data), format="mp3")
        elif self.is_hls:
            # Try AAC first, then fallback to mp3 or mpegts if needed
            try:
                audio = AudioSegment.from_file(BytesIO(raw_data), format="aac")
            except Exception:
                try:
                    audio = AudioSegment.from_file(BytesIO(raw_data), format="mp3")
                except Exception:
                    audio = AudioSegment.from_file(BytesIO(raw_data), format="mpegts")
        else:
            # Assume direct mp3 stream
            audio = AudioSegment.from_file(BytesIO(raw_data), format="mp3")

        wav_buffer = BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        return wav_buffer