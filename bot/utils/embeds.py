import discord
from bot.config import Config
from datetime import datetime

class MusicEmbed(discord.Embed):
    def __init__(self, **kwargs):
        color = kwargs.pop('color', Config.COLOR_MUSIC)
        super().__init__(color=color, timestamp=datetime.now(), **kwargs)
        self.set_footer(text="Harmonie Musicale")

    @classmethod
    def success(cls, message: str, title: str = "✨"):
        return cls(title=title, description=message, color=Config.COLOR_SUCCESS)

    @classmethod
    def error(cls, message: str, title: str = "⚠️"):
        return cls(title=title, description=message, color=Config.COLOR_ERROR)

    @classmethod
    def info(cls, message: str, title: str = "ℹ️"):
        return cls(title=title, description=message, color=Config.COLOR_INFO)

    @classmethod
    def music(cls, message: str, title: str = "🎶"):
        return cls(title=title, description=message, color=Config.COLOR_MUSIC)


