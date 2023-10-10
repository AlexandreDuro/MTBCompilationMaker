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

            initial_embed = Embed(
                title="Building video...",
                description="Your video is being processed.",
                color=0xFF5733,
                timestamp=datetime.now()
            )
            initial_embed.set_footer(text="Pinkbike Video Builder", icon_url=self.client.user.avatar.url)
            await interaction.response.send_message(embed=initial_embed, ephemeral=True)

            video = Video(interaction=interaction)
            await video.build_video(urls.split(","))

            initial_embed.title = "Uploading the video..."
            initial_embed.description = "Your video is being uploaded."
            await interaction.edit_original_response(embed=initial_embed)

            date_and_time = video.date_and_time
            download_url = get_download_url(f"result{date_and_time}.mp4")

            download_embed = Embed(
                title="Download Video",
                description=f"[Click here to download]({download_url})",
                color=0xDADADA,
                timestamp=datetime.now()
            )
            await interaction.followup.send(embed=download_embed)

            initial_embed.title = "Success!"
            initial_embed.description = "Your video has been successfully uploaded."
            await interaction.edit_original_response(embed=initial_embed)
