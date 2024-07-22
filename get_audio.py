import os
import yt_dlp as youtube_dl
from dotenv import load_dotenv

def download_audio_from_youtube(youtube_url, output_path='.'):
    load_dotenv('.env')

    ydl_opts = {
        'username': os.getenv('YOUTUBE_EMAIL'), 
        'password': os.getenv('YOUTUBE_PASSWORD'),  
        'format': 'bestaudio/best',  
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',  # Convert audio to mp3
            'preferredquality': '192',  # Use a bitrate of 192 kbps
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'nocheckcertificate': True,  # Ignore SSL certificate errors
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([youtube_url])
    
    # Find the output file
    info_dict = ydl.extract_info(youtube_url, download=False)
    audio_file_path = f"{output_path}/{info_dict['title']}.mp3"

    return audio_file_path