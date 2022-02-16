import os
from dotenv import load_dotenv
from ext import CreateAVoice, FileUtils
from ext.FileUtils import edit_guild_config, read_guild_config, Data, get_config_value
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from discord.types.channel import VoiceChannel

bot = discord.Bot()


slash = None
token = None
discord_guild = None
role_name = None
discord_channel = None
voice_channel = None


# load our environment variables from the .env file
def load_environment():
    global token
    global discord_guild
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    discord_guild = os.getenv('DISCORD_GUILD')


# Load config variables kept in config.json file
async def load_configs(_guild_id):
    global role_name
    global discord_channel
    global voice_channel
    discord_channel, role_name, voice_channel = await read_guild_config(_guild_id)


# actually load our environment first using main()
if __name__ == '__main__':
    load_environment()

def setup(bot):
    bot.add_cog(Example(bot))
    bot.add_cog(EditConfigCommands(bot))
    bot.add_cog((CreateAVoiceCommands(bot)))
    print(f"Bot user {bot.user} is Ready!")

@bot.event
async def on_ready():
    await load_configs(852958354677694474)
    setup(bot)

def get_guild(ctx):
    return ctx.author.guild


class Example(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

        @slash_command(guild_ids=[852958354677694474])
        async def hello (ctx):
            print("WOWEE")
            await ctx.respond("YOU DID IT!")

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

    @bot.command()
    async def testcommand(ctx):
        channels = discord.utils.get(ctx.author.voice.channel)
        print(channels)

    @bot.event  # Runs when users join and leave voice channels.
    async def on_voice_state_update(member, before, after):
        # reload this config before doing anything.  it was acting weird without this.
        await load_configs(member.guild.id)
        voice_channel = await get_config_value(Data.col_voice_chan, Data.guilds_table, Data.col_guild, member.guild.id)
        await CreateAVoice.edit_channel(member, before, after, voice_channel)


# cog for editing settings present in json files
class EditConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# TODO: I still need to figure out why i can't get voice or text channel lists
    # async def get_voice_channels(ctx: discord.AutocompleteContext):
    #     print(ctx.interaction.guild.voice_channels)
    #     return ['0','1','2']#[voice_channel for voice_channel in guild.channels]

    @bot.slash_command(guild_ids=[852958354677694474], description="Updates the channel to be monitored for introductions")
    async def intro_channel(ctx, channel_name):
        guild = get_guild(ctx)
        new_id = discord.utils.get(guild.channels, name=role_name)
        await edit_guild_config(guild.id, Data.col_intro_chan_id, new_id)
        await ctx.respond(await edit_guild_config(guild.id, Data.col_intro_chan, channel_name))

    @bot.slash_command(guild_ids=[852958354677694474], description="Updates the role used to restrict writing to introduction channel")
    async def intro_role(ctx, role_name):
        guild = get_guild(ctx)
        new_id = discord.utils.get(guild.roles, name=role_name)
        await edit_guild_config(guild.id, Data.col_intro_role_id, new_id)
        await ctx.respond(await edit_guild_config(guild.id, Data.col_intro_role, role_name))

    @bot.slash_command(guild_ids=[852958354677694474], description="Updates the channel to be used as base create-a-voice channel")
    async def voice_channel(ctx: discord.ApplicationContext, channel_name: Option(str, "Pick a channel")):
        guild=get_guild(ctx)
        new_id = discord.utils.get(guild.channels, name=role_name)
        await edit_guild_config(guild.id, Data.col_voice_chan_id, new_id)
        await ctx.respond(await edit_guild_config(guild.id, Data.col_voice_chan, channel_name))





# Actually run the bot
bot.run(token)

