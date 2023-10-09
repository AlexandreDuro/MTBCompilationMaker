import warnings
from datetime import datetime
import asyncio
from rich.console import Console

from video_utils import *

console = Console()
warnings.filterwarnings("ignore")


class Video:

    def __init__(self):
        self.date_and_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.video_files = []
        self.converted_files = []

    async def build_video(self, urls):
        delete_video_files()
        for i, url in enumerate(urls):
            converted_url = convert_pinkbike_url(url)
            filename = f"Downloaded/video_{i}.mp4"
            self.video_files.append(filename)

            console.print(f"Downloading video {i + 1}/{len(urls)}", style="italic blue")
            await download_video(converted_url, filename)
            console.print(f"Successfully downloaded video {i + 1}/{len(urls)}", style="italic green")

            if os.path.getsize(filename) == 0:
                raise ValueError(f"The file {filename} is empty!")

            converted_filename = "Converted/" + get_converted_filename(filename.split("/")[1].split(".")[0] + ".mp4")
            console.print(f"Converting video {i + 1}/{len(urls)}", style="italic blue")
            await convert_video(filename, converted_filename)
            console.print(f"Successfully converted video {i + 1}/{len(urls)}", style="italic green")

            self.converted_files.append(converted_filename)

        console.print("Combining the videos...", style="italic blue")
        combined_clip = concatenate_videos(self.converted_files)

        console.print("Writing the final video...", style="italic blue")
        combined_clip.write_videofile("Result/result.mp4", preset="ultrafast", codec="libx264",
                                      ffmpeg_params=['-profile:v', 'high', '-level', '4.2', '-pix_fmt', 'yuv420p',
                                                     '-hide_banner', '-loglevel', 'error'])

        console.print("Adding watermark to the final video...", style="italic blue")
        await add_watermark("Result/result.mp4", "Result/result_watermark.mp4")

        console.print("Adding audio to the final video...", style="italic blue")
        await add_subscribe_voice("Result/result_watermark.mp4", f"C:/PublicDownloads/result{self.date_and_time}.mp4")
        console.print("Done!", style="bold green")
    delete_video_files()

