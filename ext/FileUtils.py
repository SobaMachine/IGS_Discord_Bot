import json
import logging
import sqlite3
from os import path
import sqlite3 as sql

file_data = None
sql.paramstyle = 'qmark'

class Data:
    folder = "./configs"
    filename = "./config.json"
    guild = "Guild"
    guild_id = "Guild_ID"
    channel = "Channel_ID"
    configs = "Configs"

    col_created_chan = 'created_channel'
    col_guild = 'guild_id'
    col_intro_role = 'intro_role'
    col_intro_chan = 'intro_channel'
    col_voice_chan = 'voice_channel'

    db_location = './configs/guild_configs.db'
    channel_table = "CREATED_CHANNELS"
    guilds_table = "GUILD_CONFIGS"
    birthday_table = "BIRTHDAYS"


async def init_guild(_guild_id):
    db = sql.connect(Data.db_location)
    try:
        db.execute(f"INSERT INTO GUILD_CONFIGS VALUES({_guild_id}, '', '', '');")
        db.commit()
    except sqlite3.IntegrityError:
        print(f"The Guild you are trying to add ({_guild_id}) already exists as a unique key in the database")
    db.close()


# async def get_db_data():
#     db = sql.connect(Data.db_location)
#     with db:
#         cursor = db.execute("SELECT guild_id FROM CREATED_CHANNELS;")
#         for row in cursor:
#             print("guild_id = ", row[0])
#     db.close()




# Adds channel to the created channel DB along with the guild it is associated with
# Lead with channel_id since it is the unique key in the DB
async def add_created_channel(_channel_id, _guild_id):
    db = sql.connect(Data.db_location)
    db. execute(f'''INSERT INTO {Data.channel_table} 
                    ({Data.col_created_chan}, {Data.col_guild}) 
                    VALUES ({_channel_id}, {_guild_id});''', (Data.channel_table, Data.col_created_chan, Data.col_guild, _channel_id, _guild_id))
    db.commit()
    db.close()

# Removes channel from the list of created channels
async def delete_created_channel(_channel_id):
    db = sql.connect(Data.db_location)
    db. execute(f'''DELETE from {Data.channel_table} 
                    where {Data.col_created_chan} = '{_channel_id}';''')
    db.commit()
    db.close()




# Update the database config with new values
async def edit_guild_config(_guild_id, _option, _data):
    db = sql.connect(Data.db_location)
    db.execute('''UPDATE ?
                  SET ? = '?'
                  WHERE ?=?;''', (Data.guilds_table, _option, _data, Data.col_guild, _guild_id))
    db.commit()
    db.close()

# Reads the configs for the given guild
# Returns:[0] = intro_channel || [1] = intro_role || [2] = voice channel
def read_guild_config(_guild_id):


    db = sql.connect(Data.db_location)
    cur = db.cursor()
    configs = cur.execute(f"SELECT {Data.col_intro_chan}, {Data.col_intro_role}, {Data.col_voice_chan} FROM {Data.guilds_table} WHERE {Data.col_guild} = {_guild_id}")
    #configs= cur.execute("SELECT :1 FROM :2 WHERE :3 = :4", (Data.col_intro_role, Data.guilds_table, Data.col_guild, _guild_id))
    # print (configs.fetchone())
    rows = configs.fetchone()
    print(rows)
    db.close()
    return rows

def is_duplicate(_guild_id,_channel_id):

    pass



# region Old JSON oriented code that is replaced with database oriented code
# TODO: Replace add_json_channel with add_created_channel() where used.
# async def add_json_channel(_id):
#     load_json(Data.filename)
#     new_data = {Data.channel: _id}
#     if not is_duplicate(_id, True):
#         file_data[Data.created].append(new_data)
#         await write_json(file_data, Data.filename)


# TODO: Replace delete_json_channel with delete_created_channel in any references
# async def delete_json_channel(_id):
#     load_json(Data.filename)
#     if is_duplicate(_id, True):
#         for i in file_data[Data.created]:
#             if i[Data.channel] == _id:
#                 file_data[Data.created].remove(i)
#                 await write_json(file_data, Data.filename)

# TODO Replace edit_config with edit_guild_config
# async def edit_config(_option, _data):
#     load_json(Data.filename)  # get latest data from file
#     file_data[Data.configs][_option] = _data  # replace the option with the new data
#     print(file_data[Data.configs])
#     await write_json(file_data, Data.filename)


# TODO: remove write_json from any references. Replace with edit_guild_config
# async def write_json(_new_data, _filename):
#     file = open(_filename, "w")
#     json.dump(_new_data, file, indent=4)
#     file.truncate
#     file.close()


# TODO: Remove load_json from any references. this is replaced by just loading the database up when we need it.
# loads json data from file into our file_data
# def load_json(_filename):
#     global file_data
#     file = open(_filename, "r")
#     file_data = json.load(file)
#     file.close()

# TODO: Remove read_configs from any references
# def read_configs():
#     load_json(Data.filename)
#     return file_data[Data.configs]

# TODO: Replace is_duplicate with a SQLite versiona and remove from any references
# def is_duplicate(_channel_id, reopen_file):
#     if reopen_file:  # maybe sometimes we don't want to have to touch the actual file for data
#         load_json(Data.filename)
#     for i in file_data[Data.created]:
#         if i[Data.channel] == _channel_id:
#             return True

# TODO: Remove make_server_config from any references
# def make_server_config():
#     load_json(Data.filename)
#     _id = "852958354677694474"  # TODO: remove this and just pass our guild ID when needed.
#     # determine if the file for this guild exists
#     if path.exists(f"./configs/852958354677694474.json"):
#         print("Guild config exists, loading it!")
#     else:
#         print("Guild config does not exist, creating now")
#         # if file exists
#         # read file
#         # else if file does not exist
#         # create file from template
# endregion

