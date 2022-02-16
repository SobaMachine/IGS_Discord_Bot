from discord.utils import get



async def single_post(_message, _discord_channel, _role_name):
    if _message.channel.name == _discord_channel:
        member = _message.author  # get the member who triggered the on_message event
        role = get(member.guild.roles, name=_role_name)  # sets the role that will be given to the member
        await member.add_roles(role, reason="Made their introduction post")  # adds the role to the member and adds reason to audit log

def set_birthday():
    pass