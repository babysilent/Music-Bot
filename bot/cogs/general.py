import discord
from discord import app_commands
from discord.ext import commands
from bot.utils.embeds import MusicEmbed
import time

class General(commands.Cog):
    """
    Commandes générales et utilitaires.
    """
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="ping", description="Affiche la latence du bot")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = MusicEmbed.info(f"Latence : **{latency}ms** 🏓")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stats", description="Affiche les statistiques du bot")
    async def stats(self, interaction: discord.Interaction):
        uptime = time.time() - self.start_time
        hours, rem = divmod(uptime, 3600)
        minutes, seconds = divmod(rem, 60)
        
        embed = MusicEmbed.info(
            f"Serveurs : **{len(self.bot.guilds)}**\n"
            f"Utilisateurs : **{len(self.bot.users)}**\n"
            f"Uptime : **{int(hours)}h {int(minutes)}m {int(seconds)}s**\n"
            f"Version Python : **3.12**\n"
            f"Bibliothèque : **discord.py**"
        , title="📊 Statistiques du Bot")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Affiche la liste des commandes")
    async def help(self, interaction: discord.Interaction):
        commands_list = (
            "**/play** - Joue une musique ou ajoute à la queue\n"
            "**/pause** - Met en pause\n"
            "**/resume** - Reprend la lecture\n"
            "**/stop** - Arrête tout\n"
            "**/skip** - Passe au suivant\n"
            "**/queue** - Voir la file d'attente\n"
            "**/nowplaying** - Musique actuelle\n"
            "**/volume** - Régler le volume\n"
            "**/loop** - Boucler la musique/queue\n"
            "**/shuffle** - Mélanger la queue\n"
            "**/clear** - Vider la queue\n"
            "**/disconnect** - Quitter le vocal\n"
            "**/lyrics** - Voir les paroles\n"
            "**/filter** - Appliquer un effet"
        )
        embed = MusicEmbed.info(commands_list, title="📜 Liste des Commandes")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
