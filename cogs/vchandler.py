import os
import discord
from discord.ext import commands
import cogs.CoggieLibs.vchannel

class VCHandler(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # function handles all updates to users joining and leaving channels
    # including moving between channels
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        hypo_channel_name = member.display_name + '\'s Team Channel'
        if after.channel and after.channel.name == 'Team Channel Creator':
            new_channel = await guild.create_voice_channel(hypo_channel_name)
            await member.move_to(new_channel)
            self.client.log_temp_channel(guild, new_channel)
        elif before.channel and (before.channel in self.client.created_channels[guild.id]) and (not before.channel.members):
            self.client.created_channels[guild.id].remove(before.channel)
            await before.channel.delete()

def setup(client):
    client.add_cog(VCHandler(client))