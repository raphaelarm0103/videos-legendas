import whisper


class AudioProcessor:
    def __init__(self, model_size="medium"):
        self.model = whisper.load_model(model_size)

    def transcribe_audio(self, audio_file):
        result = self.model.transcribe(audio_file, language='pt', temperature=0.0, word_timestamps=True)
        return result['segments']
