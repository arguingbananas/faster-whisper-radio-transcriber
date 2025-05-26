from faster_whisper import WhisperModel
from pydub import AudioSegment
from io import BytesIO

class Transcriber:
    def __init__(self, model_name="base.en", chunk_overlap_sec=0):
        # self.model = WhisperModel(model_name)
        self.model = WhisperModel(
            model_name,
            device="auto",           # or "cpu", "cuda:0", "auto"
            compute_type="default",  # or "int8", "float16", "float32", "int8_float16"
            # cpu_threads=4,           # for CPU inference
            # num_workers=1            # for parallel decoding
        )
        self.chunk_overlap_sec = chunk_overlap_sec
        self.prev_audio = None

    def transcribe_audio(self, audio_data):
        if self.model is None:
            raise ValueError("Model not loaded.")

        # Only apply chunk overlap if chunk_overlap_sec > 0
        if self.chunk_overlap_sec > 0 and self.prev_audio is not None:
            audio_data.seek(0)
            prev_audio = AudioSegment.from_file(self.prev_audio, format="wav")
            curr_audio = AudioSegment.from_file(audio_data, format="wav")
            overlap = prev_audio[-self.chunk_overlap_sec * 1000:]
            combined = overlap + curr_audio
            buf = BytesIO()
            combined.export(buf, format="wav")
            buf.seek(0)
            audio_data = buf

        # Save current audio for next overlap (if enabled)
        if self.chunk_overlap_sec > 0:
            audio_data.seek(0)
            self.prev_audio = BytesIO(audio_data.read())
            self.prev_audio.seek(0)

        audio = AudioSegment.from_file(audio_data, format="wav")
        audio = audio.normalize()
        buf = BytesIO()
        audio.export(buf, format="wav")
        buf.seek(0)
        segments, _ = self.model.transcribe(buf, language="en")
        return " ".join(segment.text for segment in segments)