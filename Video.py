import warnings
from datetime import datetime
import asyncio
import discord

from discord import Embed
from video_utils import *

console = Console()
warnings.filterwarnings("ignore")


class Video:

    def __init__(self, interaction: discord.Interaction = None):
        self.date_and_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.video_files = []
        self.converted_files = []
        self.interaction = interaction

    async def build_video(self, urls):
        delete_video_files()

        # Embed initial
        initial_embed = Embed(
            title="Building video...",
            description="Initializing...",
            color=0xFF5733,
            timestamp=datetime.now()
        )
        initial_embed.set_footer(text="Pinkbike Video Builder", icon_url=self.interaction.user.avatar.url)
        await self.interaction.edit_original_response(embed=initial_embed)

        for i, url in enumerate(urls):
            converted_url = convert_pinkbike_url(url)
            filename = f"Downloaded/video_{i}.mp4"
            self.video_files.append(filename)

            # Update the embed
            initial_embed.title = "Building video..."
            initial_embed.description = f"Downloading video {i + 1}/{len(urls)}"
            await self.interaction.edit_original_response(embed=initial_embed)

            # Download the video
            await download_video(converted_url, filename)

            # Update the embed again
            initial_embed.title = "Building video..."
            initial_embed.description = f"Successfully downloaded video {i + 1}/{len(urls)}"
            await self.interaction.edit_original_response(embed=initial_embed)

            # Check if the file is empty
            if os.path.getsize(filename) == 0:
                raise ValueError(f"The file {filename} is empty!")

            # Get the converted filename
            converted_filename = "Converted/" + get_converted_filename(filename.split("/")[1].split(".")[0] + ".mp4")

            # Convert the video
            initial_embed.title = "Building video..."
            initial_embed.description = f"Converting video {i + 1}/{len(urls)}"
            await self.interaction.edit_original_response(embed=initial_embed)
            await convert_video(filename, converted_filename)

            # Successfully converted video
            initial_embed.title = "Building video..."
            initial_embed.description = f"Successfully converted video {i + 1}/{len(urls)}"
            await self.interaction.edit_original_response(embed=initial_embed)

            # Add the converted file to the list
            self.converted_files.append(converted_filename)

        # Combining videos
        initial_embed.title = "Building video..."
        initial_embed.description = "Combining the videos..."
        await self.interaction.edit_original_response(embed=initial_embed)
        combined_clip = concatenate_videos(self.converted_files)

        # Writing the final video
        initial_embed.title = "Building video..."
        initial_embed.description = "Writing the final video..."
        await self.interaction.edit_original_response(embed=initial_embed)
        combined_clip.write_videofile("Result/result.mp4", preset="ultrafast", codec="libx264",
                                      ffmpeg_params=['-profile:v', 'high', '-level', '4.2', '-pix_fmt', 'yuv420p',
                                                     '-hide_banner', '-loglevel', 'error'])

        # Adding watermark
        initial_embed.title = "Building video..."
        initial_embed.description = "Adding watermark to the final video..."
        await self.interaction.edit_original_response(embed=initial_embed)
        await add_watermark("Result/result.mp4", "Result/result_watermark.mp4")

        # Adding audio
        initial_embed.title = "Building video..."
        initial_embed.description = "Adding audio to the final video..."
        await self.interaction.edit_original_response(embed=initial_embed)
        await add_subscribe_voice("Result/result_watermark.mp4", f"C:/PublicDownloads/result{self.date_and_time}.mp4")

        # Done
        initial_embed.title = "Done!"
        initial_embed.description = "Your video is ready!"
        await self.interaction.edit_original_response(embed=initial_embed)

    delete_video_files()
