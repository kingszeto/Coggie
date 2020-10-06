import discord
from discord.ext import commands

class GeneralCommannds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
         await ctx.send(f'Pong! Latency: {round(self.client.latency * 1000)} ms')

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=["pattis", "pyvaluate"])
    async def _eval(self, ctx, *args):
        print(args)
        if len(args) != 1:
            response = 'I evaluate snippets of Python! Surround \" (quotation marks) '\
                'around the markdown format for code blocking. Example: \n.pyvaluate \"code here\"'
            await ctx.send(response)
        elif len(args) == 1:
                code = args[0].replace('`', "")
                try:
                    answer = eval(code)
                    await ctx.send(answer)
                except:
                    await ctx.send("Your one-liner isn't working, Pattis sad")



def setup(client):
    client.add_cog(GeneralCommannds(client))
