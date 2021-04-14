import discord
from models.channel import ChannelIn, ChannelOut, ChannelTable

async def insert_one_channel(raw_discord_channel: discord.TextChannel) -> None:
    """Inserts one channel into the channels table"""
    channel_input = ChannelIn(
        channel_id=str(raw_discord_channel.id),
        guild_id=str(raw_discord_channel.guild.id)
    )
    inserted_channel = await ChannelTable.objects.create(**channel_input.dict())
    return ChannelOut(
        channel_record_id = inserted_channel.channel_record_id,
        channel_id = inserted_channel.channel_id,
        guild_id = inserted_channel.guild_id,
    )

async def get_bot_channel_by_guild(guild: discord.Guild) -> ChannelOut:
    """Retrieves one channel based on the guild id"""
    retrieved_channel = await ChannelTable.objects.get(guild_id=str(guild.id))
    return ChannelOut(
        **dict(retrieved_channel)
    )
