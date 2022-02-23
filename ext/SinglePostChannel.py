from discord.utils import get
from ext.FileUtils import get_config_value, Data

# Changes user role on sending a message in specified channel
async def single_post(_message):
    _discord_channel = await get_config_value(Data.col_voice_chan_id,Data.guilds_table,Data.col_guild_id,_message.author.guild.id)
    _role = await get_config_value(Data.col_intro_role_id,Data.guilds_table,Data.col_guild_id,_message.author.guild.id)
    if _message.channel.name == _discord_channel:
        member = _message.author  # get the member who triggered the on_message event
        role = get(member.guild.roles, id=_role)  # sets the role that will be given to the member
        await member.add_roles(role, reason="Made their introduction post")  # adds the role to the member and adds reason to audit log

# Logic for getting birthday from user's post and adding it to our database for birthday reminders
def set_birthday():
    pass

# Logic for getting birthday from database
def get_birthday():
    pass