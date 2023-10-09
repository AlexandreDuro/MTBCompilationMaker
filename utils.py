import asyncio
import os
import subprocess
from functools import partial

import requests
import json
from rich.console import Console
console = Console()


# Fonction pour exécuter la commande ffmpeg sans afficher les logs
def run_ffmpeg_command(command):
    with open(os.devnull, 'w') as null_file:
        subprocess.run(command, stdout=null_file, stderr=null_file)


def delete_video_files():
    for filename in os.listdir('./Downloaded'):
        if "video" in filename:
            os.remove("./Downloaded/" + filename)
            console.print(f"Successfully deleted : {filename}", style="italic purple")
    for filename in os.listdir('./Converted'):
        if "converted" in filename:
            os.remove("./Converted/" + filename)
            console.print(f"Successfully deleted : {filename}", style="italic purple")


def convert_pinkbike_url(original_url):
    video_id = original_url.split("/")[4]
    two_digit = video_id[:2]

    # Vérifiez la disponibilité de la résolution 1080p
    url = f"https://ev1.pinkbike.org/v1920/{two_digit}/pbvid-{video_id}.mp4"
    if check_high_quality(url):
        return url

    # Vérifiez la disponibilité de la résolution 720p
    url = f"https://ev1.pinkbike.org/v1280/{two_digit}/pbvid-{video_id}.mp4"
    if check_high_quality(url):
        return url

    # Si aucune des résolutions haute qualité n'est disponible, utilisez la résolution par défaut (480p)
    return f"https://ev1.pinkbike.org/vf/{two_digit}/pbvid-{video_id}.mp4"


def check_high_quality(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return True
    else:
        return False


def get_converted_filename(original_filename):
    return f"converted_{original_filename}"


def get_download_url(filename):
    base_url = "http://202.61.194.180:8080/"
    return base_url + filename


async def run_command_async(cmd):
    loop = asyncio.get_event_loop()
    partial_run = partial(subprocess.run, cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = await loop.run_in_executor(None, partial_run)
    return result


class Config:
    def __init__(self, config_file):
        self.config_file = config_file

    def _load_config(self):
        with open(self.config_file, "r") as file:
            return json.load(file)

    @property
    def bot_token(self):
        return self._load_config()["token"]

    @property
    def guild_id(self):
        return self._load_config()["guild_id"]
