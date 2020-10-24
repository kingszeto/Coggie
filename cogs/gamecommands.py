import discord
from discord.ext import commands
from .CoggieLibs import CoggieVoice, VoiceChannelLL
class GameCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def amongus(self, ctx, limit=0):
        if not ctx.author.voice:
            await ctx.send("Must be in a Voice Channel to use this command")
            return
        cw_guild = ctx.guild
        hypo_channel_name = ctx.author.display_name + '\'s Among Us Game'
        new_channel = await cw_guild.create_voice_channel(hypo_channel_name, user_limit=limit)
        await ctx.author.move_to(new_channel)
        await ctx.send("Lobby Created! The channel will disappear once everyone leaves. Have fun :)")
        self.client.log_temp_channel(cw_guild, CoggieVoice(ctx.author, new_channel))

def setup(client):
    client.add_cog(GameCommands(client))