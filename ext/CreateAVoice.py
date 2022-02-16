import ext.FileUtils as db
from ext.FileUtils import Data
import sqlite3 as sql
import logging
import utils.MemberUtils as MemberUtils

#cleans voice chat and DB of channels orphaned from both

async def clean_channels(member, voice_channel):
    voice_channels = member.guild.voice_channels
    for chan in voice_channels:
        if await check_created_channel(chan) and check_remaining_members(chan):
            await delete_channel(chan, voice_channel)
        else:
            pass


# Creates or destroys a channel when called
async def edit_channel(member, before, after, voice_channel):
    # if we join the create-a voice channel, clone the channel and give it a name
    new_voice = None  # temp storage for our newly created channel
    voice_channels = member.guild.voice_channels
    # TODO: the normal delete stuff is pretty redundant to this, maybe rework it?
    # check if there are any channels we've created with 0 members in it


    # Creates new channel
    if after.channel is not None:
        if after.channel.name == voice_channel:
            new_voice = await create_channel(member, after)

    # Note:  We check against new_voice to avoid trying to delete the channel when joining.
    if before.channel is not None and before.channel.name is not voice_channel and (after.channel is None or after.channel is not new_voice):
        if await check_created_channel(before.channel) and check_remaining_members(before.channel):
            await delete_channel(before.channel, voice_channel)
            pass



# # Keeps script from deleting channels it didn't create.
async def check_created_channel(_channel):
    # just uses FileUtil's is_duplicate to check if the channel exists in the list. Reopens file to get latest version
    return await db.is_duplicate(Data.channel_table,Data.col_created_chan, _channel.id)


# checks if there is nobody remaining in the chat
def check_remaining_members(_channel):
    try:
        if len(_channel.members) == 0:
            return True
        else:
            return False
    except:
        return True


# creates channel and adds it to json
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


# Deletes the given channel
async def delete_channel(_channel, voice_channel):
    if _channel == voice_channel:
        pass
    else:
        await db.delete_created_channel(_channel.id)
        await _channel.delete()
        #print("the channel has been deleted!")
