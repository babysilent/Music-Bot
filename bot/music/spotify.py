import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bot.config import Config
from bot.utils.logger import log
import re

class SpotifyClient:
    """
    Client pour interagir avec l'API Spotify.
    """
    def __init__(self):
        self.client = None
        if Config.SPOTIFY_ID and Config.SPOTIFY_SECRET:
            try:
                auth_manager = SpotifyClientCredentials(
                    client_id=Config.SPOTIFY_ID,
                    client_secret=Config.SPOTIFY_SECRET
                )
                self.client = spotipy.Spotify(auth_manager=auth_manager)
            except Exception as e:
                log.error(f"Erreur d'initialisation Spotify: {e}")

    def is_spotify_url(self, url: str) -> bool:
        """Vérifie si l'URL est une URL Spotify valide."""
        return "open.spotify.com" in url

    async def get_track_info(self, url: str):
        """Récupère les informations d'une piste Spotify."""
        if not self.client:
            return None
            
        try:
            track = self.client.track(url)
            return f"{track['name']} {track['artists'][0]['name']}"
        except Exception as e:
            log.error(f"Erreur Spotify track: {e}")
            return None

    async def get_playlist_tracks(self, url: str):
        """Récupère les pistes d'une playlist Spotify."""
        if not self.client:
            return []
            
        try:
            results = self.client.playlist_items(url)
            tracks = results['items']
            while results['next']:
                results = self.client.next(results)
                tracks.extend(results['items'])
            
            return [f"{item['track']['name']} {item['track']['artists'][0]['name']}" for item in tracks if item['track']]
        except Exception as e:
            log.error(f"Erreur Spotify playlist: {e}")
            return []

    async def get_album_tracks(self, url: str):
        """Récupère les pistes d'un album Spotify."""
        if not self.client:
            return []
            
        try:
            results = self.client.album_tracks(url)
            tracks = results['items']
            while results['next']:
                results = self.client.next(results)
                tracks.extend(results['items'])
            
            return [f"{track['name']} {track['artists'][0]['name']}" for track in tracks]
        except Exception as e:
            log.error(f"Erreur Spotify album: {e}")
            return []

# Instance globale
spotify = SpotifyClient()
