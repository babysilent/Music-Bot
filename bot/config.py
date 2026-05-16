import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration de l'application gérée via les variables d'environnement.
    """
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    # Spotify
    SPOTIFY_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    # Genius (Lyrics)
    GENIUS_TOKEN = os.getenv("GENIUS_API_TOKEN")
    
    # Bot Settings
    PREFIX = os.getenv("COMMAND_PREFIX", "/")
    DEFAULT_VOLUME = int(os.getenv("DEFAULT_VOLUME", 50))
    MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", 100))
    
    # Colors for Embeds
    COLOR_SUCCESS = 0x2ecc71
    COLOR_ERROR = 0xe74c3c
    COLOR_INFO = 0x3498db
    COLOR_MUSIC = 0x9b59b6
    
    # FFmpeg options
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }
    
    # YTDL options
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
