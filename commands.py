import discord
from discord import Embed
from datetime import datetime
from utils import get_download_url


class Commands:

    def __init__(self, tree, client, config):
        self.tree = tree
        self.client = client
        self.config = config
        self._register_commands()

    def _register_commands(self):
        @self.tree.command(name="pinkbike", description="Get a compiled video from pinkbike links",
                           guild=discord.Object(id=self.config.guild_id))
        async def pinkbike(interaction: discord.Interaction, urls: str):
            from Video import Video

            initial_embed = Embed(title="Building video...", description="Your video is being processed.",
                                  color=0x00ff00)
            await interaction.response.send_message(embed=initial_embed, ephemeral=True)

            video = Video(interaction=interaction)
            await video.build_video(urls.split(","))

            upload_embed = Embed(title="Uploading the video!", description="Your video is being uploaded.",
                                 color=0x00ff00)
            await interaction.edit_original_response(embed=upload_embed)

            date_and_time = video.date_and_time
            download_url = get_download_url(f"result{date_and_time}.mp4")

            download_embed = Embed(title="Download Video", description=f"[Click here to download]({download_url})",
                                   color=0x0000ff)
            await interaction.followup.send(embed=download_embed)

            success_embed = Embed(title="Success!", description="Your video has been successfully uploaded.",
                                  color=0x00ff00)
            await interaction.edit_original_response(embed=success_embed)
