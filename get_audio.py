import os
import yt_dlp as youtube_dl
from dotenv import load_dotenv
import re

def sanitize_filename(filename):
    # Remove any invalid characters and replace with underscore
    sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)
    # Remove any double underscores or trailing underscores
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    return sanitized

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
        'nocheckcertificate': True,  # Ignore SSL certificate errors
    }

    # Extract video information without downloading
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get('title', 'audio')
        sanitized_title = sanitize_filename(title)
        audio_file_path = os.path.join(output_path, f"{sanitized_title}")
        ydl_opts['outtmpl'] = audio_file_path

    # Download the audio using the sanitized file name
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    return audio_file_path + '.mp3'