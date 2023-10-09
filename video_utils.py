import requests
import subprocess
from moviepy.editor import *
from utils import *
import warnings
import aiohttp
import asyncio
warnings.filterwarnings("ignore")


async def download_video(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)


def concatenate_videos(video_files):
    clips = []
    for video_file in video_files:
        clip = VideoFileClip(video_file)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    return final_clip


async def convert_video(input_path, output_path):
    loop = asyncio.get_running_loop()
    # Obtenez les dimensions de la vidéo d'origine
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        input_path
    ]
    result = await run_command_async(cmd)
    width, height = map(int, [x for x in result.stdout.strip().split(',') if x])

    # Déterminez si l'arrière-plan flou est nécessaire
    if width != 1080 or height != 1920:
        filter_complex = (
            "[0:v]split=2[bg][fg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "boxblur=10:10[background];[fg]scale=1080:1920:force_original_aspect_ratio=decrease[foreground];["
            "background][foreground]overlay=(W-w)/2:(H-h)/2"
        )
    else:
        filter_complex = "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"

    # Exécutez la commande FFmpeg
    command = [
        'ffmpeg',
        '-hide_banner',
        '-loglevel', 'error',
        '-y',
        '-i', input_path,
        '-vf', filter_complex,
        '-acodec', 'aac',  # copier l'audio tel quel; retirez cette ligne si vous ne voulez pas d'audio
        output_path
    ]
    await loop.run_in_executor(None, run_ffmpeg_command, command)


async def add_watermark(input_path, output_path):
    loop = asyncio.get_running_loop()
    command = [
        'ffmpeg',
        '-hide_banner',
        '-loglevel', 'error',
        '-y',
        '-i', input_path,
        '-i', "data/logo.png",
        '-filter_complex', '[1:v]format=rgba,colorchannelmixer=aa=0.5[logo];[0:v][logo]overlay=(main_w-overlay_w)/2:main_h-overlay_h-120',
        '-codec:a', 'copy',
        output_path
    ]
    await loop.run_in_executor(None, run_ffmpeg_command, command)


async def add_subscribe_voice(input_path, output_path):
    loop = asyncio.get_running_loop()
    command = [
        'ffmpeg',
        '-hide_banner',
        '-loglevel', 'error',
        '-y',
        '-i', input_path,
        '-i', "data/subscribe_voice.mp3",
        '-filter_complex', '[1:a]adelay=500|500[a1];[a1]apad[apadded];[0:a][apadded]amerge=inputs=2[a]',
        '-map', '0:v',
        '-map', '[a]',
        '-c:v', 'copy',
        '-ac', '2',
        '-b:a', '128k',
        output_path
    ]
    await loop.run_in_executor(None, run_ffmpeg_command, command)



