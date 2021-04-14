from typing import List
import discord
from models.task import TaskIn, TaskOut, TaskTable


async def delete_one_task(task: TaskOut) -> None:
    task_to_delete = TaskTable(
        task_id=task.task_id
    )
    await task_to_delete.delete()

async def get_guild_tasks(guild: discord.Guild, role: discord.Role=None) -> List[TaskOut]:
    """Gets a list of tasks by both the guild and role id"""
    role_id: str = ''
    if role != None:
        role_id = str(role.id)
    
    action = TaskTable.objects.filter(guild_id=str(guild.id))
    if role_id:
        action = action.filter(role_id=role_id)
    action = action.all()
    retrieved_tasks = await action
    return [
        TaskOut(**dict(task)) for task in retrieved_tasks
    ]

async def insert_one_task(task_input: TaskIn) -> TaskOut:
    inserted_task = await TaskTable.objects.create(**task_input.dict())
    return TaskOut(
        task_id=inserted_task.id,
        title=inserted_task.title,
        content=inserted_task.content,
        deadline=inserted_task.deadline,
        date_assigned=inserted_task.date_assigned,
        guild_id=inserted_task.guild_id,
        role_id=inserted_task.role_id
    )
