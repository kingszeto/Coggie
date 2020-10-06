import discord
from discord.ext import commands

class GameCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def amongus(self, ctx, limit=0):
        if not ctx.author.voice.channel:
            await ctx.send("Must be in a Voice Channel to use this command")
            return
        cw_guild = ctx.guild
        channel_names = {channel.name for channel in cw_guild.voice_channels}
        hypo_channel_name = ctx.author.display_name + '\'s Among Us Game'
        if not hypo_channel_name in channel_names:
            new_channel = await cw_guild.create_voice_channel(hypo_channel_name, user_limit=limit)
            await ctx.author.move_to(new_channel)
            await ctx.send("Lobby Created! The channel will disappear once everyone leaves. Have fun :)")
        else:
            "Something's wrong... probably on my end cause my human creator really sucks at programming :("

    @commands.command()
    async def league(self, ctx, *args):
        if len(args) >= 2:
            ctx.send("Max two args. Example\n.league 5 custom\nThis creates two league lobbies with a limit of 5. Use .league for a new temporary league channel")
            return
        cw_guild = ctx.guild
        channel_names = {channel.name for channel in cw_guild.voice_channels}
        hypo_channel_name = ctx.author.display_name + '\'s League Game'

        if not ctx.author.voice.channel:
            await ctx.send("Must be in a Voice Channel to use this command")
        try:
            if len(args) == 2:
                amount, lobby_type = args
                if not isinstance(amount, int): raise TypeError
                if lobby_type == 'custom':
                    new_channel = await cw_guild.create_voice_channel(hypo_channel_name + ' (1/2)', user_limit=amount)
                    await ctx.author.move_to(new_channel)
                    await cw_guild.create_voice_channel(hypo_channel_name + ' (2/2)', user_limit=amount)
                else:
                    raise TypeError
            elif len(args) == 1:
                args = args[0]
                if isinstance(args, int):
                    new_channel = await cw_guild.create_voice_channel(hypo_channel_name, user_limit=args)
                    await ctx.author.move_to(new_channel)
                elif isinstance(args, str) and args == "custom":
                    new_channel = await cw_guild.create_voice_channel(hypo_channel_name + ' (1/2)')
                    await ctx.author.move_to(new_channel)
                    await cw_guild.create_voice_channel(hypo_channel_name + ' (2/2)')
            else:
                raise TypeError
        except TypeError:
            await ctx.send("Format is .league optionally followed by [size] [type]\nAdditionally, only custom League lobbies are supported at the moment for lobby types")
            return


def setup(client):
    client.add_cog(GameCommands(client))