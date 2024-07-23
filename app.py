import streamlit as st
import os
from get_audio import download_audio_from_youtube
from get_transcript import transcribe_audio_to_text

st.title("YouTube Audio Transcription")

youtube_url = st.text_input("Enter YouTube URL:")
if st.button("Transcribe"):
    if youtube_url:
        try:
            audio_file_path = download_audio_from_youtube(youtube_url, output_path='.')

            if os.path.exists(audio_file_path):
                transcription = transcribe_audio_to_text(audio_file_path)
                st.subheader("Transcription")
                st.write(transcription)
            else:
                st.error(f"Error: File {audio_file_path} does not exist.")
        except Exception as e:
            st.error(f"Error: {e}")