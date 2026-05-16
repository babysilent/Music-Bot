import asyncio
import functools
import discord
import yt_dlp
from bot.config import Config
from bot.utils.logger import log

# Désactiver les avertissements de yt-dlp
yt_dlp.utils.bug_reports_message = lambda: ''

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')
        self.thumbnail = data.get('thumbnail')
        self.requester = data.get('requester')
        self.webpage_url = data.get('webpage_url')

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop=None, requester=None):
        loop = loop or asyncio.get_event_loop()
        ytdl = yt_dlp.YoutubeDL(Config.YTDL_OPTIONS)
        
        log.info(f"🔍 Recherche : {search}")
        partial = functools.partial(ytdl.extract_info, search, download=False)
        data = await loop.run_in_executor(None, partial)

        if 'entries' in data:
            data = data['entries'][0]

        data['requester'] = requester
        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **Config.FFMPEG_OPTIONS), data=data)

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        ytdl = yt_dlp.YoutubeDL(Config.YTDL_OPTIONS)
        
        partial = functools.partial(ytdl.extract_info, url, download=not stream)
        return await loop.run_in_executor(None, partial)


