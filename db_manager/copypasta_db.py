from typing import List, Union
import discord
from .schemas import copypastas
from .db_utilities import build_query
from sqlalchemy.schema import CreateTable

from .db_connector import db
from models.copypasta import CopypastaIn, CopypastaOut


async def create_copypastas_table() -> None:
    await db.connect()
    sql_statement = str(CreateTable(copypastas))
    await db.execute(sql_statement)
    await db.disconnect()

async def insert_one_copypasta(copypasta: CopypastaIn) -> None:
    query = copypastas.insert()
    await db.connect()
    await db.execute(query=query, values=copypasta.to_dict())
    await db.disconnect()

async def get_copypastas_by_guild(guild: discord.Guild) -> List[CopypastaOut]:
    query, values = build_query(copypastas, {
        "equalTo": {
            "guild_id": str(guild.id)
        }
    })
    await db.connect()
    mapped_copypastas: List[CopypastaOut] = []

    async for row in db.iterate(query=query, values=values):
        mapped_copypasta = CopypastaOut(
            id=int(row[0]),
            name=str(row[1]),
            content=str(row[2]),
            guild_id=str(row[3])
        )
        mapped_copypastas.append(mapped_copypasta)
        
    await db.disconnect()
    return mapped_copypastas

async def get_copypasta_by_name_and_guild(copypasta_name: str, guild: discord.Guild) -> Union[CopypastaOut, None]:
    query, values = build_query(copypastas, {
        "equalTo": {
            "name": str(copypasta_name),
            "guild_id": str(guild.id)
        }
    })
    await db.connect()
    row = await db.fetch_one(query=query, values=values)
    if not row:
        await db.disconnect()
        return
    copypasta_output = CopypastaOut(
        id=int(row[0]),
        name=str(row[1]),
        content=str(row[2]),
        guild_id=str(row[3])
    )
    await db.disconnect()
    return copypasta_output