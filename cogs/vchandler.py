import os
import discord
from discord.ext import commands

class VCHandler(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # function handles all updates to users joining and leaving channels
    # including moving between channels
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        hypo_channel_name = member.display_name + '\'s Team Channel'
        channel_names = [channel.name for channel in guild.voice_channels]
        if after.channel and after.channel.name == 'Team Channel Creator' and hypo_channel_name not in channel_names:
            new_channel = await guild.create_voice_channel(hypo_channel_name)
            await member.move_to(new_channel)
        elif before.channel and (before.channel.name == hypo_channel_name) and (after.channel is None or after.channel.name != hypo_channel_name):
            channel = discord.utils.get(guild.voice_channels, name=hypo_channel_name)
            await before.channel.delete()

def setup(client):
    client.add_cog(VCHandler(client))