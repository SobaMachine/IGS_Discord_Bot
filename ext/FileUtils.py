import json
import logging
import sqlite3
from os import path
import sqlite3 as sql

file_data = None

class Data:
    folder = "./configs"
    filename = "./config.json"
    guild = "Guild"
    guild_id = "Guild_ID"
    channel = "Channel_ID"
    configs = "Configs"

    col_created_chan = "created_channel"
    col_guild = "guild_id"
    col_role = "intro_role"
    col_intro_chan = "intro_channel"
    col_voice_chan = "voice_channel"

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
    db. execute('''INSERT INTO ? 
                    (?, ?) 
                    VALUES (?, ?);''', (Data.channel_table, Data.col_created_chan, Data.col_guild, _channel_id, _guild_id))
    db.commit()
    db.close()

# Removes channel from the list of created channels
async def delete_created_channel(_channel_id):
    db = sql.connect(Data.db_location)
    db. execute('''DELETE from ? 
                    where ? = '?';''', (Data.channel_table, Data.col_created_chan, _channel_id))
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
    configs = db.execute('''SELECT ?, ?, ? FROM ? WHERE ? = ?''', (Data.col_intro_chan, Data.col_role, Data.col_voice_chan, Data.guilds_table, Data.col_guild,_guild_id))
    print (configs.fetchone())
    rows = configs.fetchone()
    db.close()
    return rows

def is_duplicate(_guild_id,_channel_id):

    pass





