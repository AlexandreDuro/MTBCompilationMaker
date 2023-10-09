import discord
from datetime import datetime
from utils import get_download_url


class Commands:

    def __init__(self, tree, client, config):
        self.tree = tree
        self.client = client
        self.config = config
        self._register_commands()

    def _register_commands(self):
        @self.tree.command(name="pinkbike", description="Get a compiled video from pinkbike links", guild=discord.Object(id=self.config.guild_id))
        async def pinkbike(interaction: discord.Interaction, urls: str):
            from Video import Video
            await interaction.response.send_message("Building video...", ephemeral=True)
            original_message = await interaction.original_response()
            video = Video()
            await video.build_video(urls.split(","))
            await interaction.followup.send("Uploading the video!", ephemeral=True)
            date_and_time = video.date_and_time
            download_url = get_download_url(f"result{date_and_time}.mp4")
            await interaction.followup.send(download_url)
            await interaction.followup.send("Video built successfully!", ephemeral=True)
