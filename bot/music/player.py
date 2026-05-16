import asyncio
import discord
from bot.music.queue import MusicQueue
from bot.music.ytdl import YTDLSource
from bot.utils.logger import log
from bot.utils.embeds import MusicEmbed
from bot.config import Config

class MusicPlayer:
    def __init__(self, bot, guild: discord.Guild):
        self.bot = bot
        self.guild = guild
        self.queue = MusicQueue()
        self.voice_client: discord.VoiceClient | None = None
        self.current_track = None
        self.next_event = asyncio.Event()
        self.volume = Config.DEFAULT_VOLUME / 100
        self.loop = bot.loop
        self.task = self.loop.create_task(self.player_loop())
        self.filter = None

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next_event.clear()

            if not self.queue.is_empty() or self.queue.loop_mode == 2:
                track = await self.get_next_track()
                if track:
                    await self.play_track(track)
                    await self.next_event.wait()
            else:
                try:
                    await asyncio.wait_for(self.next_event.wait(), timeout=300) 
                except asyncio.TimeoutError:
                    log.info(f"😴 Inactivité sur {self.guild.name}. Déconnexion.")
                    await self.cleanup()
                    return

    async def get_next_track(self):
        if self.queue.loop_mode == 1 and self.current_track:
            return self.current_track
        
        next_track = self.queue.get_next()
        
        if self.queue.loop_mode == 2 and self.current_track:
            self.queue.add(self.current_track)
            
        return next_track

    async def play_track(self, track_data):
        try:
            source = await YTDLSource.create_source(
                None, 
                track_data['webpage_url'], 
                loop=self.loop, 
                requester=track_data['requester']
            )
            
            self.current_track = track_data
            self.voice_client.play(
                source, 
                after=lambda e: self.loop.call_soon_threadsafe(self.next_event.set)
            )
            self.voice_client.source.volume = self.volume
            
            log.info(f"🎵 Lecture : {source.title} ({self.guild.name})")
            
        except Exception as e:
            log.error(f"❌ Erreur lecture {self.guild.name}: {e}")
            self.next_event.set()

    async def cleanup(self):
        if self.voice_client:
            await self.voice_client.disconnect()
        
        if self.task:
            self.task.cancel()
        
        cog = self.bot.get_cog("Music")
        if cog and self.guild.id in cog.players:
            del cog.players[self.guild.id]
        
        log.info(f"🧹 Nettoyage {self.guild.name}")

    def stop(self):
        self.queue.clear()
        if self.voice_client:
            self.voice_client.stop()

    def pause(self):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()

    def resume(self):
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()

    def skip(self):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()


