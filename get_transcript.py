import logging
import os
import tempfile
import google.auth.transport.requests
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pytube import YouTube


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Path to the OAuth 2.0 credentials file
CLIENT_SECRETS_FILE = "credentials.json"

# The scopes required for accessing the YouTube Data API and downloading age-restricted videos
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_authenticated_service():
    """
    Authenticates the user using OAuth 2.0 and returns an authorized YouTube API client.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)

def get_video_metadata(url: str) -> dict:
    """
    Fetches the metadata of the YouTube video using YouTube Data API.

    Args:
        url (str): The YouTube video URL.

    Returns:
        dict: The metadata of the video if available, otherwise None.
    """
    try:
        video_id = url.split('v=')[-1].split('&')[0]
        youtube = get_authenticated_service()
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        metadata = response['items'][0]['snippet'] if 'items' in response and response['items'] else None
        logger.debug(f"Fetched metadata: {metadata}")
        return metadata
    except Exception as e:
        logger.error(f"Error fetching video metadata: {e}")
        return None

def download_youtube_audio(url: str) -> BinaryIO:
    """
    Downloads the audio stream of a YouTube video to a temporary file and returns a file object.

    Args:
        url (str): The URL of the YouTube video from which the audio stream is to be downloaded.

    Returns:
        BinaryIO: The temporary file containing the downloaded audio stream.
    """
    temp_file = None  # Initialize the temp_file variable

    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream is None:
            raise Exception("No audio stream found")

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

        # Download the audio stream and write to the temporary file
        audio_stream.stream_to_buffer(temp_file)
        temp_file.close()  # Close the file to finalize writing
        logger.debug(f"Audio file downloaded to {temp_file.name}")
        
        # Reopen the temporary file in binary read mode
        return open(temp_file.name, 'rb')
    except Exception as e:
        logger.error(f"Error downloading audio from YouTube: {e}")
        if temp_file:
            os.unlink(temp_file.name)  # Ensure to delete the temp file in case of error
        raise
    finally:
        # Ensure to delete the temp file once done
        if temp_file and not temp_file.closed:
            os.unlink(temp_file.name)

if __name__ == "__main__":
    try:
        # Test fetching metadata
        url = "https://youtu.be/xrbyI-Cuze4"
        metadata = get_video_metadata(url)
        logger.info(f"Video metadata: {metadata}")
        
        # Test downloading audio
        audio_file = download_youtube_audio(url)
        logger.info("Downloaded audio file successfully.")
        # Do something with the audio_file
        audio_file.close()  # Remember to close the file when done
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")