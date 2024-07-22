import os
from get_audio import download_audio_from_youtube
from get_transcript import transcribe_audio_to_text

def main():
    # URL of the YouTube video
    youtube_url = 'https://youtu.be/hZqaoISyNpg'
    
    # Download audio from YouTube and get the file path
    audio_file_path = download_audio_from_youtube(youtube_url, output_path='.')

    # Transcribe the downloaded audio
    transcription = transcribe_audio_to_text(audio_file_path)
    
    # Print the transcription
    print(transcription)

if __name__ == '__main__':
    main()