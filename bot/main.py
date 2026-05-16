import asyncio
import discord
from discord.ext import commands
from bot.config import Config
from bot.utils.logger import log
import os
import sys

class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.voice_states = True

        super().__init__(
            command_prefix=Config.PREFIX,
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        log.info("🚀 Initialisation des modules...")
        
        for filename in os.listdir('./bot/cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'bot.cogs.{filename[:-3]}')
                    log.info(f"✅ Module chargé : {filename}")
                except Exception as e:
                    log.error(f"❌ Erreur chargement {filename}: {e}")

        log.info("🔄 Synchronisation des commandes slash...")
        try:
            synced = await self.tree.sync()
            log.info(f"✨ {len(synced)} commandes synchronisées.")
        except Exception as e:
            log.error(f"⚠️ Erreur synchronisation : {e}")

    async def on_ready(self):
        log.info(f"🌟 Connecté : {self.user} ({self.user.id})")
        log.info(f"🌍 Serveurs : {len(self.guilds)}")
        
        activity = discord.Activity(
            type=discord.ActivityType.listening, 
            name=f"{Config.PREFIX}help | Musique Premium 🎵"
        )
        await self.change_presence(activity=activity)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        log.error(f"🔥 Erreur : {error}")

async def main():
    if not Config.TOKEN:
        log.critical("🛑 Token Discord manquant dans le fichier .env")
        sys.exit(1)

    bot = MusicBot()
    
    async with bot:
        try:
            await bot.start(Config.TOKEN)
        except discord.LoginFailure:
            log.critical("🔑 Token invalide")
        except Exception as e:
            log.error(f"💥 Erreur fatale : {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("👋 Fermeture du bot.")
    except Exception as e:
        log.error(f"💀 Crash : {e}")

