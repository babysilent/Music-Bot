import discord
from discord import app_commands
from discord.ext import commands
import asyncio

from bot.music.player import MusicPlayer
from bot.music.ytdl import YTDLSource
from bot.music.spotify import spotify
from bot.music.filters import AudioFilters
from bot.utils.embeds import MusicEmbed
from bot.utils.formatting import format_duration, create_progress_bar
from bot.utils.logger import log
from bot.services.lyrics import lyrics_service

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    def get_player(self, guild: discord.Guild) -> MusicPlayer:
        if guild.id not in self.players:
            self.players[guild.id] = MusicPlayer(self.bot, guild)
        return self.players[guild.id]

    async def ensure_voice(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(
                embed=MusicEmbed.error("Vous devez être dans un salon vocal."),
                ephemeral=True
            )
            return False
        
        if interaction.guild.voice_client:
            if interaction.guild.voice_client.channel != interaction.user.voice.channel:
                await interaction.response.send_message(
                    embed=MusicEmbed.error("Je suis déjà dans un autre salon vocal."),
                    ephemeral=True
                )
                return False
        
        return True

    @app_commands.command(name="play", description="Lancer une musique ou une recherche")
    @app_commands.describe(search="Lien YouTube/Spotify ou recherche texte")
    async def play(self, interaction: discord.Interaction, search: str):
        if not await self.ensure_voice(interaction):
            return

        await interaction.response.defer()
        player = self.get_player(interaction.guild)
        
        if not interaction.guild.voice_client:
            player.voice_client = await interaction.user.voice.channel.connect()
        else:
            player.voice_client = interaction.guild.voice_client

        if spotify.is_spotify_url(search):
            if "track" in search:
                track_name = await spotify.get_track_info(search)
                if track_name:
                    search = track_name
                else:
                    return await interaction.followup.send(embed=MusicEmbed.error("Impossible de lire ce lien Spotify."))
            elif "playlist" in search or "album" in search:
                tracks = await spotify.get_playlist_tracks(search) if "playlist" in search else await spotify.get_album_tracks(search)
                if not tracks:
                    return await interaction.followup.send(embed=MusicEmbed.error("Playlist vide ou privée."))
                
                for t in tracks:
                    data = {'webpage_url': t, 'requester': interaction.user, 'title': t}
                    player.queue.add(data)
                
                player.next_event.set()
                return await interaction.followup.send(embed=MusicEmbed.success(f"**{len(tracks)}** musiques ajoutées depuis Spotify."))

        try:
            data = await YTDLSource.from_url(search, loop=self.bot.loop, stream=True)
            
            if 'entries' in data:
                for entry in data['entries']:
                    entry['requester'] = interaction.user
                    player.queue.add(entry)
                await interaction.followup.send(embed=MusicEmbed.success(f"**{len(data['entries'])}** musiques ajoutées à la file d'attente."))
            else:
                data['requester'] = interaction.user
                player.queue.add(data)
                await interaction.followup.send(embed=MusicEmbed.success(f"Ajouté : **{data['title']}** 🎵"))
            
            player.next_event.set()
            
        except Exception as e:
            log.error(f"Erreur /play: {e}")
            await interaction.followup.send(embed=MusicEmbed.error(f"Erreur technique : {e}"))

    @app_commands.command(name="pause", description="Mettre la musique en pause")
    async def pause(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        player.pause()
        await interaction.response.send_message(embed=MusicEmbed.music("Pause ⏸️"))

    @app_commands.command(name="resume", description="Reprendre la lecture")
    async def resume(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        player.resume()
        await interaction.response.send_message(embed=MusicEmbed.music("Reprise ▶️"))

    @app_commands.command(name="skip", description="Passer au morceau suivant")
    async def skip(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        player.skip()
        await interaction.response.send_message(embed=MusicEmbed.music("Passé ⏭️"))

    @app_commands.command(name="stop", description="Arrêter tout et vider la queue")
    async def stop(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        player.stop()
        await interaction.response.send_message(embed=MusicEmbed.music("Arrêté ⏹️"))

    @app_commands.command(name="queue", description="Voir la file d'attente")
    async def queue(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        if player.queue.is_empty:
            return await interaction.response.send_message(embed=MusicEmbed.info("La file d'attente est vide."))
        
        queue_list = player.queue.get_queue_list()
        description = ""
        for i, track in enumerate(queue_list[:10], 1):
            description += f"{i}. **{track['title']}**\n"
        
        if len(queue_list) > 10:
            description += f"\n*... et {len(queue_list) - 10} autres.*"
            
        embed = MusicEmbed.music(description, title=f"📋 File d'attente ({len(queue_list)})")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="nowplaying", description="Voir le morceau actuel")
    async def nowplaying(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        if not player.current_track or not interaction.guild.voice_client:
            return await interaction.response.send_message(embed=MusicEmbed.info("Rien n'est en cours de lecture."))
        
        track = player.current_track
        progress = create_progress_bar(30, track.get('duration', 100))
        
        embed = MusicEmbed.music(
            f"🎶 **[{track['title']}]({track.get('webpage_url')})**\n"
            f"👤 Demandé par : {track['requester'].mention}\n\n"
            f"{progress} `{format_duration(track.get('duration', 0))}`"
        )
        if track.get('thumbnail'):
            embed.set_thumbnail(url=track['thumbnail'])
            
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="volume", description="Régler le volume (0-100)")
    @app_commands.describe(value="Niveau sonore")
    async def volume(self, interaction: discord.Interaction, value: app_commands.Range[int, 0, 100]):
        player = self.get_player(interaction.guild)
        player.volume = value / 100
        if interaction.guild.voice_client and interaction.guild.voice_client.source:
            interaction.guild.voice_client.source.volume = player.volume
        
        emoji = "🔈" if value < 30 else "🔉" if value < 70 else "🔊"
        await interaction.response.send_message(embed=MusicEmbed.music(f"Volume : **{value}%** {emoji}"))

    @app_commands.command(name="loop", description="Mode de répétition")
    @app_commands.choices(mode=[
        app_commands.Choice(name="Désactivé", value=0),
        app_commands.Choice(name="Titre actuel", value=1),
        app_commands.Choice(name="File d'attente", value=2),
    ])
    async def loop(self, interaction: discord.Interaction, mode: app_commands.Choice[int]):
        player = self.get_player(interaction.guild)
        player.queue.loop_mode = mode.value
        await interaction.response.send_message(embed=MusicEmbed.music(f"Répétition : **{mode.name}** 🔁"))

    @app_commands.command(name="shuffle", description="Mélanger la file d'attente")
    async def shuffle(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        player.queue.shuffle()
        await interaction.response.send_message(embed=MusicEmbed.music("File mélangée 🔀"))

    @app_commands.command(name="clear", description="Vider la file d'attente")
    async def clear(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        player.queue.clear()
        await interaction.response.send_message(embed=MusicEmbed.music("File vidée 🧹"))

    @app_commands.command(name="disconnect", description="Quitter le salon vocal")
    async def disconnect(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        await player.cleanup()
        await interaction.response.send_message(embed=MusicEmbed.music("Déconnecté 👋"))

    @app_commands.command(name="lyrics", description="Paroles du morceau actuel")
    async def lyrics(self, interaction: discord.Interaction):
        player = self.get_player(interaction.guild)
        if not player.current_track:
            return await interaction.response.send_message(embed=MusicEmbed.error("Rien ne joue actuellement."))
        
        await interaction.response.defer()
        lyrics_text = await lyrics_service.get_lyrics(player.current_track['title'])
        
        if not lyrics_text:
            return await interaction.followup.send(embed=MusicEmbed.error("Paroles introuvables."))
        
        if len(lyrics_text) > 4000:
            lyrics_text = lyrics_text[:4000] + "..."
            
        embed = MusicEmbed.music(lyrics_text, title=f"🎤 Paroles : {player.current_track['title']}")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="filter", description="Appliquer un effet sonore")
    @app_commands.describe(name="Effet")
    @app_commands.choices(name=[
        app_commands.Choice(name="Bassboost", value="bassboost"),
        app_commands.Choice(name="Nightcore", value="nightcore"),
        app_commands.Choice(name="Reverb", value="reverb"),
        app_commands.Choice(name="Vaporwave", value="vaporwave"),
        app_commands.Choice(name="Aucun", value="none"),
    ])
    async def filter(self, interaction: discord.Interaction, name: str):
        player = self.get_player(interaction.guild)
        if name == "none":
            player.filter = None
            msg = "Effets désactivés."
        else:
            player.filter = AudioFilters.get_filter(name)
            msg = f"Effet **{name}** activé pour la prochaine musique."
        
        await interaction.response.send_message(embed=MusicEmbed.music(f"{msg} ✨"))


async def setup(bot):
    await bot.add_cog(Music(bot))
