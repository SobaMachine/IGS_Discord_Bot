import os
from dotenv import load_dotenv
from ext import CreateAVoice, FileUtils
from ext.FileUtils import edit_guild_config, read_guild_config
import discord
from discord.commands import slash_command, Option
from discord.ext import commands

bot = discord.Bot()

slash = None
token = None
discord_guild = None
role_name = None
discord_channel = None
voice_channel = None

list_voice_channels=[]
list_text_channels=[]

intro_role_config = "Single_Post_Role"
intro_channel_config = "Single_Post_Channel"
voice_channel_config = "Create-A-Voice_Channel"


# load our environment variables from the .env file
def load_environment():
    global token
    global discord_guild
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    discord_guild = os.getenv('DISCORD_GUILD')


# Load config variables kept in config.json file
def load_configs(_guild_id):
    global role_name
    global discord_channel
    global voice_channel
    # sets variables based on the json config
    #role_name = read_configs()[intro_role_config]
    #discord_channel = read_configs()[intro_channel_config]
    #voice_channel = read_configs()[voice_channel_config]
    #discord_channel, role_name, voice_channel = read_guild_config(_guild_id)
    read_guild_config(_guild_id)


# actually load our environment first using main()
if __name__ == '__main__':
    load_environment()


@bot.event
async def on_ready():
    load_configs(852958354677694474)
    bot.add_cog(EditConfigCommands(bot))
    bot.add_cog(BotHelpCommands(bot))
    bot.add_cog((CreateAVoiceCommands(bot)))
    # bot.add_cog(SlashCommands(bot))
    print(f"Bot user {bot.user} is Ready!")


# TODO DO NOT DELETE
# Sets user role if they post in the given chat
# @bot.event  # Do things when a message is received
# async def on_message(_message):
#     await SinglePostChannel.single_post(_message, discord_channel, role_name)
#     await bot.process_commands(_message)


# Create or destroy channels as user joins / leaves


# class SlashCommands(interactions.Extension):
#     def __init__(self,slash):
#         self.slash = slash
#
#     @interactions.command(
#         name="my_first_command",
#         description="This is the first command I made!",
#         scope=discord_guild,
#     )
#     async def my_first_command(ctx: interactions.CommandContext):
#         await ctx.send("Hi there!")


# cog for handling create-a-voice bot things
class CreateAVoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.event  # Runs when users join and leave voice channels.
    async def on_voice_state_update(member, before, after):
        load_configs(member.guild.id)
       # print(member.guild.id)
        #print(voice_channel, role_name, discord_channel)

        #print(after.channel)

         # reload this config before doing anything.  it was acting weird without this.
        #await CreateAVoice.edit_channel(member, before, after, voice_channel)


# cog for editing settings present in json files
class EditConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[discord_guild], description="test description", name="introchannel")
    async def intro_channel(self, ctx, arg):
        print("Intro channel slash command ran")
        #try_update(ctx, intro_channel_config, arg)
        # await ctx.send(f"Introduction channel config updated to: {arg}")

    @slash_command(guild_ids=[discord_guild])
    async def intro_role(self, ctx, arg):
        try_update(ctx, intro_role_config,arg)
        # await ctx.send(f"Single post restricted role config updated to: {arg}")

    @slash_command(guild_ids=[discord_guild])
    async def voice_channel(self, ctx, arg):
        try_update(ctx, voice_channel_config,arg)
        # await ctx.send(f"Create-a-Voice channel config updated to: {arg}")


# cog for replying with help related information
class BotHelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def h(self, ctx, *, member):
        member = member or ctx.author
        await ctx.send("HOW COOL IS THIS")

async def try_update(ctx, _config_name, arg):
    print(f"Running edit on {_config_name} to {arg}")

    try:
        await edit_guild_config(_config_name,arg)
        await ctx.send(f"Updated {_config_name} to {arg}")
    except:
        await ctx.send(f"Failed to update {_config_name}")
        # TODO: optionally, maybe send an alert to me to figure out why?

# Actually run the bot
bot.run(token)

# slash.run(token)
