#/pinkbike urls:https://www.pinkbike.com/video/577795/,https://www.pinkbike.com/video/577806/
import discord
from discord import app_commands
from commands import Commands
from utils import Config

config = Config("data/config.json")


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.tree = app_commands.CommandTree(self)
        self.commands = Commands(self.tree, self, config)

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync(guild=discord.Object(id=config.guild_id))
            self.synced = True
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Big crashes..."))
        print(f"{client.user} is ready.")


client = Client()

if __name__ == "__main__":
    client.run(config.bot_token)
