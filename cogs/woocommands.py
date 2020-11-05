import discord
import requests
from discord.ext import commands

class WooCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def leetAll(self, ctx):
        r = requests.get('https://leetcode.com/problems/random-one-question/all')
        await ctx.send(f'Here is your random Leetcode problem!\n {r.url}')

    @commands.command()
    async def leetAlgo(self, ctx):
        r = requests.get('https://leetcode.com/problems/random-one-question/algorithms')
        await ctx.send(f'Here is your random Leetcode algorithm problem!\n {r.url}')
    
    @commands.command()
    async def leetData(self, ctx):
        r = requests.get('https://leetcode.com/problems/random-one-question/database')
        await ctx.send(f'Here is your random Leetcode database problem!\n {r.url}')
    

def setup(client):
    client.add_cog(WooCommands(client))