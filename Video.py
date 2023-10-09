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
        initial_embed = Embed(title="Building video", description="Initializing...", color=0x00ff00)
        await self.interaction.edit_original_response(embed=initial_embed)

        for i, url in enumerate(urls):
            converted_url = convert_pinkbike_url(url)
            filename = f"Downloaded/video_{i}.mp4"
            self.video_files.append(filename)

            # Update the embed
            progress_embed = Embed(title="Building video", description=f"Downloading video {i + 1}/{len(urls)}",
                                   color=0x00ff00)
            await self.interaction.edit_original_response(embed=progress_embed)

            # Download the video
            await download_video(converted_url, filename)

            # Update the embed again
            success_embed = Embed(title="Building video",
                                  description=f"Successfully downloaded video {i + 1}/{len(urls)}", color=0x00ff00)
            await self.interaction.edit_original_response(embed=success_embed)

            # Check if the file is empty
            if os.path.getsize(filename) == 0:
                raise ValueError(f"The file {filename} is empty!")

            # Get the converted filename
            converted_filename = "Converted/" + get_converted_filename(filename.split("/")[1].split(".")[0] + ".mp4")

            # Convert the video
            converting_embed = Embed(title="Building video", description=f"Converting video {i + 1}/{len(urls)}",
                                     color=0x00ff00)
            await self.interaction.edit_original_response(embed=converting_embed)
            await convert_video(filename, converted_filename)

            # Successfully converted video
            converted_embed = Embed(title="Building video",
                                    description=f"Successfully converted video {i + 1}/{len(urls)}", color=0x00ff00)
            await self.interaction.edit_original_response(embed=converted_embed)

            # Add the converted file to the list
            self.converted_files.append(converted_filename)

        # Combining videos
        combining_embed = Embed(title="Building video", description="Combining the videos...", color=0x00ff00)
        await self.interaction.edit_original_response(embed=combining_embed)
        combined_clip = concatenate_videos(self.converted_files)

        # Writing the final video
        writing_embed = Embed(title="Building video", description="Writing the final video...", color=0x00ff00)
        await self.interaction.edit_original_response(embed=writing_embed)
        combined_clip.write_videofile("Result/result.mp4", preset="ultrafast", codec="libx264",
                                      ffmpeg_params=['-profile:v', 'high', '-level', '4.2', '-pix_fmt', 'yuv420p',
                                                     '-hide_banner', '-loglevel', 'error'])

        # Adding watermark
        watermark_embed = Embed(title="Building video", description="Adding watermark to the final video...",
                                color=0x00ff00)
        await self.interaction.edit_original_response(embed=watermark_embed)
        await add_watermark("Result/result.mp4", "Result/result_watermark.mp4")

        # Adding audio
        audio_embed = Embed(title="Building video", description="Adding audio to the final video...", color=0x00ff00)
        await self.interaction.edit_original_response(embed=audio_embed)
        await add_subscribe_voice("Result/result_watermark.mp4", f"C:/PublicDownloads/result{self.date_and_time}.mp4")

        # Done
        done_embed = Embed(title="Done!", description="Your video is ready!", color=0x00ff00)
        await self.interaction.edit_original_response(embed=done_embed)

    delete_video_files()
