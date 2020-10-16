import discord
from random import randint
from discord.ext import commands
from .CoggieLibs import CoggieVoice
from .CoggieLibs import VoiceChannelLL

class OrgCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.split_ready = False

    @commands.command()
    async def create_chain(self, ctx, key, num_servers=2, prefix=None, member_limit=0):
        # make sure pre-reqs achieved in making server chain
        if not ctx.author.guild_permissions.manage_channels:
            raise commands.MissingPermissions([discord.Permissions.manage_channels])
        if num_servers >= 20:
            ctx.send("Limit 20, I'm but a weak bot.")
        if not ctx.author.voice:
            await ctx.send("You must be in a Voice Channel to use this command.")
            return
        ### prefix here for channel name
        channel_prefix = ""
        if prefix:
            prefix = prefix.replace("_", " ")
            channel_prefix = prefix + " Room ({}/'+str(num_servers)+')"
        else:
            channel_prefix = ctx.author.display_name + '\'s Cog Room ({}/'+str(num_servers)+')'

        category = await ctx.guild.create_category(prefix if prefix else ctx.author.display_name\
            + '\'s Voice Channel Chain')

        cv = CoggieVoice(ctx.author, await category.create_voice_channel(channel_prefix.format(1)), key)
        current = cv.channels
        for i in range(1, num_servers):
            current.next = VoiceChannelLL(await category.create_voice_channel(channel_prefix.format(str(i + 1)), user_limit=member_limit))
            current = current.next
        current = cv.channels
        self.client.log_temp_channel(ctx.guild, cv)
        await ctx.author.move_to(cv.channels.voice_channel)

    # arrival should be a CoggieVoice.key
    @commands.command()
    async def all_split(self, ctx, departure, arrive_key, role=None):
        if not ctx.author.guild_permissions.manage_channels:
            raise commands.MissingPermissions([discord.Permissions.manage_channels])
        guild = ctx.guild
        voice_channel = discord.utils.get(guild.voice_channels, name=departure)
        if not voice_channel:
            await ctx.send("Channel not found")
            return
        arrival = self.client.get_cogvoice_key(guild, arrive_key)
        if not arrival:
            await ctx.send("Destination chain-key not found.")
            return
        current = arrival.channels
        while voice_channel.members:
            eject = choice(voice_channel.members)
            await eject.move_to(current.voice_channel)
            current = current.next
            if not current:
                current = arrival.channels
    
    @commands.command()
    async def split(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_channels:
            raise commands.MissingPermissions([discord.Permissions.manage_channels])
        
        # make sure there's a destination
        arrival = self.client.get_cogvoice_key(ctx.guild, args[-1])
        if not arrival:
            await ctx.send("Destination chain-key not found.")
            return
        vc = discord.utils.get(ctx.guild.voice_channels, name="Lounge")
        
        #get all the servers until "to"
        people = [member for server in [discord.utils.get(ctx.guild.voice_channels, name=vcname.replace("_", " ")).members for vcname in args[:-2]] for member in server]

        #split randomly
        current = arrival.channels
        while people:
            eject = randint(0, len(people) - 1)
            eject = people.pop(eject)
            await eject.move_to(current.voice_channel)
            current = current.next
            if not current:
                current = arrival.channels
    
    # # fix dis, but carl-bot maybe a better way to do role assignments
    # @commands.command()
    # async def make_mass_groups(self, ctx, *args):
    #     await ctx.send("Called")
    #     i = 0
    #     role_name = []
    #     while i < len(args):
    #         if not(args[i][0] == '<' and args[i][-1] == '>'):
    #             role_name.append(args[i])
    #             i += 1
    #         else: 
    #             role = await ctx.guild.create_role(name=" ".join(role_name))
    #             print(args[i])
    #             while args[i][0] == '<' and args[i][-1] == '>':
    #                 member = int(args[i].strip("<!@>"))
    #                 for m in ctx.guild.members:
    #                     if m.id == member:
    #                         await member.add_roles(role)
    #                         break
    #                 i += 1
    #             role_name = []
    #     await ctx.send("Done")

            
    
        
        
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     await ctx.send("You don't have permissions to do that.")

def setup(client):
    client.add_cog(OrgCommands(client))
