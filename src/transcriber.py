from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self, model_name="base.en"):
        self.model = WhisperModel(model_name)

    def transcribe_audio(self, audio_data):
        if self.model is None:
            raise ValueError("Model not loaded.")
        segments, _ = self.model.transcribe(audio_data)
        return " ".join(segment.text for segment in segments)