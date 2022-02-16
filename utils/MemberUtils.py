import discord.member

# check if member has a nickname set, else return their discord username
def check_nick(_member):
    if _member.nick is not None:
        return _member.nick
    else:
        return _member.name