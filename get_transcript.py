import whisper

def transcribe_audio_to_text(audio_path):
    # Load the whisper model
    model = whisper.load_model("small")

    # Transcribe the audio file
    result = model.transcribe(audio_path)

    return result["text"]