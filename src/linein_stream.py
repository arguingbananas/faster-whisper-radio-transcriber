import sounddevice as sd
import threading
from io import BytesIO
from pydub import AudioSegment
import numpy as np

class LineInStream:
    def __init__(self, samplerate=16000, channels=1, chunk_duration=10):
        self.samplerate = samplerate
        self.channels = channels
        self.chunk_duration = chunk_duration  # seconds
        self.audio_buffer = BytesIO()
        self.streaming = False
        self.thread = None

    def fetch_stream(self):
        self.streaming = True
        self.thread = threading.Thread(target=self._record, daemon=True)
        self.thread.start()

    def _record(self):
        def callback(indata, frames, time, status):
            if not self.streaming:
                raise sd.CallbackStop()
            # Convert to int16 and write to buffer
            audio = (indata * 32767).astype(np.int16).tobytes()
            self.audio_buffer.write(audio)

        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype='float32', callback=callback):
            while self.streaming:
                sd.sleep(int(self.chunk_duration * 1000))

    def get_audio_wav(self):
        self.audio_buffer.seek(0)
        raw = self.audio_buffer.read()
        if not raw:
            return None
        # Convert raw PCM to WAV using pydub
        audio = AudioSegment(
            data=raw,
            sample_width=2,
            frame_rate=self.samplerate,
            channels=self.channels
        )
        wav_buffer = BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        self.audio_buffer = BytesIO()  # Clear buffer
        return wav_buffer

    def stop_stream(self):
        self.streaming = False
        if self.thread:
            self.thread.join()