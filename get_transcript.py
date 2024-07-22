import whisper

def transcribe_audio_to_text(audio_path):
    # Load the whisper model
    model = whisper.load_model("small")

    # Transcribe the audio file
    result = model.transcribe(audio_path)

    # Print the transcribed text
    print("Transcription: ", result["text"])
    return result["text"]

if __name__ == '__main__':
    audio_file_path = 'BREATHE Trailer German Deutsch (2024) Milla Jovovich.mp3'  # Replace with the path to your downloaded audio file
    transcribe_audio_to_text(audio_file_path)