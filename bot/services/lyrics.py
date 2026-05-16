import lyricsgenius
from bot.config import Config
from bot.utils.logger import log
import asyncio

class LyricsService:
    """
    Service de recherche de paroles via Genius API.
    """
    def __init__(self):
        self.genius = None
        if Config.GENIUS_TOKEN:
            try:
                self.genius = lyricsgenius.Genius(Config.GENIUS_TOKEN)
                self.genius.verbose = False
                self.genius.remove_section_headers = True
            except Exception as e:
                log.error(f"Erreur d'initialisation Genius: {e}")

    async def get_lyrics(self, query: str) -> str | None:
        """
        Recherche les paroles pour un titre donné.
        """
        if not self.genius:
            return "API Genius non configurée."
            
        try:
            # Exécuter dans un thread car lyricsgenius est bloquant
            loop = asyncio.get_event_loop()
            song = await loop.run_in_executor(None, self.genius.search_song, query)
            
            if song:
                return song.lyrics
            return None
        except Exception as e:
            log.error(f"Erreur recherche paroles: {e}")
            return None

# Instance globale
lyrics_service = LyricsService()
