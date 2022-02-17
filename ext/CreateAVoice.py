import ext.FileUtils as db
from ext.FileUtils import Data
import sqlite3 as sql
import logging, discord
import utils.MemberUtils as MemberUtils


# Creates or destroys a channel when called
async def edit_channel(member, before, after, voice_channel):
    new_voice = None  # temp storage for our newly created channel

    # Creates new channel if user joins defined voice_channel
    if after.channel is not None:
        if after.channel.id == voice_channel:
            new_voice = await create_channel(member, after)

    # Note:  We check against new_voice to avoid trying to delete the channel when joining.
    if before.channel is not None and before.channel.id is not voice_channel and (after.channel is None or after.channel is not new_voice):
        if await check_created_channel(before.channel.id) and check_remaining_members(before.channel.id):
            await clean_channels(member, voice_channel)
            pass


# Clones the create-a-voice channel
async def create_channel(_member, _after):
    # clones the create-a-voice channel and gives it the member's name
    new_voice = await _after.channel.clone(name=f"{MemberUtils.check_nick(_member)}'s Voice Channel")
    # offsets the new channel by 2 from the top of the voice category so it appears just below create-a-chat
    await new_voice.move(after=_after.channel)
    await _member.move_to(new_voice)  # moves the member to their voice channel
    # created_channels.add(new_voice.id)  # add channel id to our set of created channels to check before deletion
    try:
        await db.add_created_channel(new_voice.id, _member.guild.id)
        #print("the channel has been added to the database!")
    except sql.IntegrityError as error:
        #print(f"The channel you are trying to add ({_after}) already exists as a unique key in the database")
        logging.WARN(error)
        pass
    return new_voice


# # Keeps script from deleting channels it didn't create.
async def check_created_channel(_channel):
    # just uses FileUtil's is_duplicate to check if the channel exists in the list. Reopens file to get latest version
    return await db.is_duplicate(Data.channel_table, Data.col_created_chan_id, _channel)


# checks if there is nobody remaining in the chat
def check_remaining_members(_channel):
    try:
        if len(_channel.members) == 0:
            return True
        else:
            return False
    except:
        return True


# cleans voice chat and DB of channels orphaned from both
async def clean_channels(member, voice_channel):
    print(voice_channel)
    #voice_channels = member.guild.voice_channels

    voice_channels = []
    for chan in member.guild.voice_channels:
        voice_channels.append(chan.id)

    db_channels = await db.get_all_values(Data.col_created_chan_id, Data.channel_table)

    # Finds and deletes any created channels in the guild that have no remaining members
    for chan in voice_channels:
        if await check_created_channel(chan) and check_remaining_members(chan) and chan is not None:
            await delete_channel(member, chan, voice_channel)
        else:
            pass

    # finds and deletes orphaned channels in the DB that do not have an associated voice channel
    if db_channels is not None:
        for chan in db_channels:
            if chan not in voice_channels and chan is not None:
                await delete_channel(member, chan, voice_channel)
            else:
                pass


# Deletes the given channel
async def delete_channel(member, _channel, voice_channel):
    if _channel == voice_channel:
        pass
    elif _channel is not None:
        await db.delete_created_channel(_channel)
        chan = discord.utils.get(member.guild.voice_channels, id=_channel)
        if chan is not None:
            await chan.delete()
        else:
            pass
        #print("the channel has been deleted!")


# just returns the id if the channel isn't None
def get_id(channel):
    try:
        return channel.channel.id
    except:
        return None
