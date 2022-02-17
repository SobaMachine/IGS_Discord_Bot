import logging
import sqlite3 as sql


# stores strings and stuff for interacting with DB to make it easy to rename things in the future
class Data:
    db_location = './configs/guild_configs.db'
    channel_table = "CREATED_CHANNELS"
    guilds_table = "GUILD_CONFIGS"
    birthday_table = "BIRTHDAYS"

    col_created_chan_id = 'created_channel_id'
    col_guild_id = 'guild_id'
    col_intro_role = 'intro_role'
    col_intro_chan = 'intro_channel'
    col_voice_chan = 'voice_channel'
    col_intro_role_id = 'intro_role_id'
    col_intro_chan_id = 'intro_channel_id'
    col_voice_chan_id = 'voice_channel_id'


# adds guild to the guild_configs DB with default values
async def init_guild(_guild_id):
    db = sql.connect(Data.db_location)
    try:
        db.execute(f"INSERT INTO GUILD_CONFIGS VALUES({_guild_id}, '', '', '');")
        db.commit()
    except sql.IntegrityError:
        print(f"The Guild you are trying to add ({_guild_id}) already exists as a unique key in the database")
    db.close()


# Adds channel to the created channel DB along with the guild it is associated with
# Lead with channel_id since it is the unique key in the DB
async def add_created_channel(_channel_id, _guild_id):
    await db_execute(f"INSERT INTO {Data.channel_table} ({Data.col_created_chan_id}, {Data.col_guild_id}) VALUES ({_channel_id}, {_guild_id});", True)


# Removes channel from the list of created channels. called from CreateAVoice.delete_channel()
async def delete_created_channel(_channel_id):
    await db_execute(f"DELETE from {Data.channel_table} where {Data.col_created_chan_id} = '{_channel_id}';", True)


# Update the database config with new values
async def edit_guild_config(_guild_id, _option, _data):
    try:
        await db_execute(f"UPDATE {Data.guilds_table} SET {_option} = '{_data}' WHERE {Data.col_guild_id}={_guild_id};", True)
        # return for output to respond to member
        return (f"Updated {_option} to {_data}")
    except:
        return (f"Failed to update {_option}")


# Reads the configs for the given guild
# Returns:[0] = intro_channel || [1] = intro_role || [2] = voice channel
async def read_guild_config(_guild_id):
    rows = await db_execute(f"SELECT {Data.col_intro_chan_id}, {Data.col_intro_role_id}, {Data.col_voice_chan_id} "
                          f"FROM {Data.guilds_table} "
                          f"WHERE {Data.col_guild_id} = {_guild_id};", False, True)
   # rows=rows.fetchone()
    return rows

async def get_all_values(_col, _table):
    value = await db_execute(f"SELECT {_col} FROM {_table}",False,False,True)
    return value
# get value of single config
async def get_config_value(_col, _table, _key, _key_val):
    value = await db_execute(f"SELECT {_col} FROM {_table} where {_key} = {_key_val}",False,True)
   # value = value.fetchone()
    return value[0]


# Check if item already exists in the database, returns true if it does.
async def is_duplicate(_table, _col, _id):
    exists = await db_execute(f"SELECT {_col} from {_table} WHERE {_col} = {_id};",False, True)
    # exists = exists.fetchone()
    if exists is not None:

        return True
    else:
        #print(f"ID {_id} does not exist in '{_col}' in table {_table}")
        return False
    pass


# Opens the database
def open_db():
    try:
        #print("opened database")
        return sql.connect(Data.db_location)
    except sql.Error as error:
        debug_log("Encountered Error opening database",error)
        pass


# Executes a string in the database.  optionally commits or runs fetchone() on results
async def db_execute(_execute_string, _needs_commit=False, _fetchone=False, _fetchall=False):
    try:
        db = open_db()
        if _fetchall:
            db = db.cursor()
        else:
            db = db
        ex = db.execute(_execute_string)
        #print(f"executed '{_execute_string}")
        if _fetchone:
            ex = ex.fetchone()
        if _fetchall:
            ex = ex.fetchall()
        if _needs_commit:
            db.commit()
        db.close()
        return ex
    except sql.Error as error:
        debug_log(f"An error occurred when executing {_execute_string}", error)
    except sql.IntegrityError as error:
        debug_log("The channel you are trying to add already exists as a unique key in the database", error)
    except sql.DatabaseError as error:
        debug_log(f"A database error has occurred.", error)


# simplify some debugging junk
def debug_log(_string, _error=None):
    print(_string)
    logging.WARN(_error)