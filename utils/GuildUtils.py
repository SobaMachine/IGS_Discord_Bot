import discord.utils
from enum import Enum

class Guild_Attributes(Enum):
    roles = 0
    channels = 1

def get_guild(ctx):
    return ctx.author.guild

# Returns the guild and the ID of an attribute given a name (role or channel)
async def get_id(ctx,name,type):
    guild = get_guild(ctx)
    if type == Guild_Attributes.roles:
        new_id = discord.utils.get(guild.roles, name=name).id
    elif type == Guild_Attributes.channels:
        new_id = discord.utils.get(guild.channels, name=name).id
    return guild, new_id