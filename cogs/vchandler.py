import os
import discord
from discord.ext import commands
from .CoggieLibs import CoggieVoice

def checkInCogVoice(channel: discord.VoiceChannel, created_channels: set()):
    for cogvoice in created_channels:
        if channel in cogvoice.channels:
            return cogvoice
    return
    
class VCHandler(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # function handles all updates to users joining and leaving channels
    # including moving between channels
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        hypo_channel_name = member.display_name + '\'s Team Channel'
        if before.channel:
            cv = checkInCogVoice(before.channel, self.client.created_channels[guild.id])
            if cv and not cv.has_members():
                self.client.created_channels[guild.id].remove(cv)
            ### delete the VC LinkedList ###
                head = cv.channels
                category = cv.channels.voice_channel.category
                current = cv.channels
                while head:
                    current = current.next
                    await head.voice_channel.delete()
                    head = current
                if category and not "Creator" in category.name:
                    await category.delete()
            ### end of delete the VC LinkedList ###
        
        # separate function to add teams
        if after.channel and after.channel.name == 'Team Channel Creator':
            # if it's in a category, make the new channel under the category section, else do the same thing but
            # else do the same thing but not in a category section
            if after.channel.category:
                new_channel = await after.channel.category.create_voice_channel(hypo_channel_name)
                await member.move_to(new_channel)
                self.client.log_temp_channel(guild, CoggieVoice(member, new_channel))
            else:
                new_channel = await guild.create_voice_channel(hypo_channel_name)
                await member.move_to(new_channel)
                self.client.log_temp_channel(guild, CoggieVoice(member, new_channel))

def setup(client):
    client.add_cog(VCHandler(client))