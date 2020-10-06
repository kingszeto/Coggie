import os
import config
import discord
from discord.ext import commands

client =  commands.Bot(command_prefix='.')
client.created_channels = {}

def log_temp_channel(guild, cv):
    if not guild.id in client.created_channels:
        client.created_channels[guild.id] = set()
    client.created_channels[guild.id].add(cv)
client.log_temp_channel = log_temp_channel

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(config.bot_token)

