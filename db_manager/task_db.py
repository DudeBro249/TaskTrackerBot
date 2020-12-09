import discord
from models.task import TaskIn, TaskOut
from typing import Any, Dict, List
from .schemas import tasks
from .db_utilities import build_query
from .db_connector import db
from sqlalchemy.schema import CreateTable

async def create_tasks_table() -> None:
    await db.connect()
    sql_statement = str(CreateTable(tasks))
    await db.execute(sql_statement)
    await db.disconnect()
        


async def delete_one_task(task: TaskOut) -> None:
    query = str(tasks.delete().where(tasks.c.id == 'id_1'))
    values = {
        'id_1': task.task_id
    }
    await db.connect()
    await db.execute(query=str(query), values=values)
    await db.disconnect()

async def get_guild_tasks(guild: discord.Guild, role: discord.Role=None) -> List[TaskOut]:
    role_id: str = ''
    if role != None:
        role_id = str(role.id)
    
    query, values = build_query(tasks, {
        "equalTo": {
            "guild_id": str(guild.id),
            "role_id": str(role_id)
        }
    })

    print(query)
    print(values)

    return await get_tasks(query=query, values=values)


async def get_tasks(query: str, values=None) -> List[TaskOut]:
    await db.connect()
    mapped_tasks: List[TaskOut] = []
    async for row in db.iterate(query=query, values=values):
        mapped_tasks.append(TaskOut(
            task_id=row[0],
            title=row[1],
            content=row[2],
            deadline=row[3],
            date_assigned=row[4],
            guild_id=row[5],
            role_id=row[6]
        ))
    await db.disconnect()
    return mapped_tasks


async def insert_one_task(task: TaskIn) -> None:
    query = tasks.insert()
    await db.connect()
    await db.execute(query=query, values=task.to_dict())
    await db.disconnect()


async def insert_many_tasks(task_inputs: List[TaskIn]) -> None:
    query = tasks.insert()
    await db.connect()
    await db.execute_many(query=query, values=[task_inputs[i].to_dict() for i in range(0, len(task_inputs))])
    await db.disconnect()


