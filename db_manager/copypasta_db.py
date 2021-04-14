from typing import List, Union
import discord

from models.copypasta import CopypastaIn, CopypastaOut, CopypastaTable


async def insert_one_copypasta(copypasta_input: CopypastaIn) -> None:
    """Inserts one copypasta into the copypastas table"""
    inserted_copypasta = await CopypastaTable.objects.create(**copypasta_input.dict())
    return CopypastaOut(
        id = inserted_copypasta.id,
        name = inserted_copypasta.name,
        content = inserted_copypasta.content,
        guild_id = inserted_copypasta.guild_id,
    )


async def get_copypastas_by_guild(guild: discord.Guild) -> List[CopypastaOut]:
    """Gets a list of copypastas from the copypastas table based on the guild id"""
    retrieved_copypastas = await CopypastaTable.objects.filter(guild_id=str(guild.id)).all()
    return [
        CopypastaOut(**dict(copypasta)) for copypasta in retrieved_copypastas
    ]

async def get_copypasta_by_name_and_guild(copypasta_name: str, guild: discord.Guild) -> Union[CopypastaOut, None]:
    """Gets a list of copypastas from the copypastas table based on both the guild id and copypasta_name"""
    retrieved_copypastas = await CopypastaTable.objects.filter(name=copypasta_name).filter(guild_id=str(guild.id)).all()
    return [
        CopypastaOut(**dict(copypasta)) for copypasta in retrieved_copypastas
    ][0]
