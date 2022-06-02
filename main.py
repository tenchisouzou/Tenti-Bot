import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


class Mybot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="./",
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=True, users=True
            ),
        )

    async def on_ready(self):
        print("ready")
        print(self.guilds)


if __name__ == "__main__":
    load_dotenv()
    bot = Mybot()
    bot.run(os.environ["TOKEN"])
