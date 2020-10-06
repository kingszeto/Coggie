import discord
from discord.ext import commands

class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            self.client.created_channels[guild.id] = set()
        # print(self.client.guilds)
        print(f"Bot is loaded, running in {len(self.client.guilds)} servers")

def setup(client):
    client.add_cog(Setup(client))
