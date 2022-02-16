from ext.FileUtils import delete_created_channel, add_created_channel,is_duplicate
created_channels = set()

# Creates or destroys a channel when called
async def edit_channel(member, before, after, voice_channel):
    # if we join the create-a voice channel, clone the channel and give it a name
    new_voice = None  # temp storage for our newly created channel
    voice_channels = member.guild.voice_channels

    # TODO: the normal delete stuff is pretty redundant to this, maybe rework it?
    # check if there are any channels we've created with 0 members in it
    for chan in voice_channels:
        if check_created_channel(chan) and check_remaining_members(chan):
            await delete_channel(chan)

    # Creates new channel
    if after.channel is not None:
        if after.channel.name == voice_channel:
            await create_channel(member, after)

    # Note:  We check against new_voice to avoid trying to delete the channel when joining.
    if before.channel is not None and before.channel.name is not voice_channel and (after.channel is None or after.channel is not new_voice):
        if check_created_channel(before.channel) and check_remaining_members(before.channel):
            await delete_channel(before.channel)


# check if member has a nickname set, else return their discord username
def check_member_name(_member):
    if _member.nick is not None:
        return _member.nick
    else:
        return _member.name


# Keeps script from deleting channels it didn't create.
def check_created_channel(_channel):
    # just uses FileUtil's is_duplicate to check if the channel exists in the list. Reopens file to get latest version
    return is_duplicate(_channel.id, True)


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
    new_voice = await _after.channel.clone(name=f"{check_member_name(_member)}'s Voice Channel")
    # offsets the new channel by 2 from the top of the voice category so it appears just below create-a-chat
    await new_voice.move(after=_after.channel)
    await _member.move_to(new_voice)  # moves the member to their voice channel
    # created_channels.add(new_voice.id)  # add channel id to our set of created channels to check before deletion
    await add_created_channel(new_voice.id)


# Deletes the given channel
async def delete_channel(_channel):
    await delete_created_channel(_channel.id)
    await _channel.delete()
