import discord
from .schemas import channels
from .db_utilities import build_query
from sqlalchemy.schema import CreateTable

from .db_connector import db
from models.channel import ChannelIn, ChannelOut

async def create_channels_table() -> None:
    await db.connect()
    sql_statement = str(CreateTable(channels))
    await db.execute(sql_statement)
    await db.disconnect()

async def insert_one_channel(raw_discord_channel: discord.TextChannel) -> None:
    channel_input = ChannelIn(
        channel_id=str(raw_discord_channel.id),
        guild_id=str(raw_discord_channel.guild.id)
    )
    query = channels.insert()
    await db.connect()
    await db.execute(query=query, values=channel_input.to_dict())
    await db.disconnect()

async def get_bot_channel_by_guild(guild: discord.Guild) -> ChannelOut:
    query, values = build_query(channels, {
        "equalTo": {
            "guild_id": str(guild.id)
        }
    })
    await db.connect()
    row = await db.fetch_one(query=query, values=values)
    designated_channel = ChannelOut(
        channel_record_id=int(row[0]),
        channel_id=str(row[1]),
        guild_id=str(row[2])
    )
    await db.disconnect()
    return designated_channel


