from models.copypasta import CopypastaIn
from typing import List, Union
from .general_utilities import remove_all
from datetime import date
import os
import sys

sys.path.append('../')
from db_manager import task_db
from models.task import TaskIn, TaskOut

import discord

def get_role_from_mention(role_mention: str, roles: List[discord.Role]) -> discord.Role:
    role_id = remove_all(role_mention, ['<', '>', '!', '@', '&'])
    return get_role_by_attribute('id', role_id, roles)

def get_role_by_attribute(attribute_name, role_attribute, roles: List[discord.Role]) -> discord.Role:
    for role in roles:
        if str(getattr(role, attribute_name)) == role_attribute:
            return role
    return None

def create_task_embed(task: Union[TaskIn, TaskOut]) -> discord.Embed:
    task_embed = discord.Embed(
        type="rich",
        title=task.title
    )
    task_embed.color = discord.Colour(0x3fce8)
    task_embed.description = ''
    if hasattr(task, 'task_id'):
        task_embed.description += f'Task Id: {task.task_id}\n'
    task_embed.description += f'Task content: {task.content}\n'
    task_embed.description += f'Deadline: {task.deadline}\n'
    task_embed.description += f'Date assigned: {task.date_assigned}'
    if task.role_id != '':
        task_embed.description += f'\nGroup: {"<@&%s>" % int(task.role_id)}'

    return task_embed

async def displayTasks(ctx, mapped_tasks: List[TaskOut]) -> bool:
    if len(mapped_tasks) == 0:
        await ctx.send('No tasks. Woohoo!')
        return True
        
    for task in mapped_tasks:
        task_embed = create_task_embed(task)
        await ctx.send(embed=task_embed)
    return False


async def get_task_from_user(ctx, bot) -> TaskIn:
    def check(message: discord.Message) -> bool:
        if ctx.author != message.author:
            return False
        return True
    
    def deadline_check(message: discord.Message) -> bool:
        if '/' not in message.content:
            return False

        date_information = message.content.split('/')
        if len(date_information) != 3:
            return False
        return True
    
    await ctx.send('Enter the task title')
    title_message: discord.Message = await bot.wait_for('message', check=check)
    title: str = str(title_message.content)

    await ctx.send('Enter the content of the task')
    content_message: discord.Message = await bot.wait_for('message', check=check)
    task_content: str = str(content_message.content)

    await ctx.send('What is the deadline? Please provide in the format DD/MM/YY')
    deadline_message: discord.Message = await bot.wait_for('message', check=deadline_check)
    deadline: str = str(deadline_message.content)

    return TaskIn(
        title=str(title),
        content=str(task_content),
        deadline=str(deadline),
        date_assigned=date.today().strftime('%d/%m/%Y'),
        guild_id=str(ctx.guild.id),
        role_id=''
    )


async def get_copypasta_from_user(ctx, bot) -> Union[CopypastaIn, None]:
    def check(message: discord.Message) -> bool:
        if ctx.author != message.author:
            return False
        return True
    await ctx.send('What is the name of the copypasta?')
    copypasta_name = str((await bot.wait_for('message', check=check)).content)
    if len(copypasta_name) > 60:
        await ctx.send('The copypasta cannot be more than 60 characters')
        return

    await ctx.send('What is the copypasta content?(Paste in chat)')
    copypasta_content = str((await bot.wait_for('message', check=check)).content)

    return CopypastaIn(
        name=str(copypasta_name),
        content=str(copypasta_content),
        guild_id=str(ctx.guild.id)
    )


async def manage_voice_channel_roles(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
    if before.channel == None and after.channel != None:
        guild: discord.Guild = after.channel.guild
        role = get_role_by_attribute('name', after.channel.name, roles=guild.roles)
        if role == None:
            role = await guild.create_role(name=after.channel.name)
        
        await member.add_roles(role)
    elif before.channel != None and after.channel == None:
        guild: discord.Guild = before.channel.guild
        role = get_role_by_attribute('name', before.channel.name, roles=guild.roles)
        await member.remove_roles(role)

    elif before.channel != None and after.channel != None and before.channel != after.channel:
        guild: discord.Guild = before.channel.guild
        before_role = get_role_by_attribute('name', before.channel.name, roles=guild.roles)
        after_role = get_role_by_attribute('name', after.channel.name, roles=guild.roles)
        if before_role == None:
            before_role = await guild.create_role(name=before.channel.name)
        if after_role == None:
            after_role = await guild.create_role(name=after.channel.name)
        await member.remove_roles(before_role)
        await member.add_roles(after_role)


async def post_to_secret_server(ctx, input_task: TaskIn) -> None:
    secret_guild_id = str(os.getenv('SECRET_GUILD_ID'))

    if secret_guild_id == str(ctx.guild.id):
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                if channel.name == str(input_task.title).lower():
                    await channel.send(f'{ctx.author.mention}')
                    await channel.send(embed=create_task_embed(input_task))


async def get_and_add_task(ctx, bot, role: discord.Role=None) -> None:
    input_task = await get_task_from_user(ctx, bot)
    await post_to_secret_server(ctx, input_task=input_task)

    if role != None:
        input_task.role_id = str(role.id)

    await task_db.insert_one_task(input_task)
    await ctx.send('Added task to database!')

async def input_role_from_user(ctx, bot, error_message: str) -> discord.Role:

    def check(message: discord.Message) -> bool:
        if message.author != ctx.author:
            return False
        return True

    await ctx.send('What is the name of the role?')
    role_name = (await bot.wait_for('message', check=check)).content
    role = get_role_by_attribute('name', role_name, ctx.guild.roles)
    if role == None:
        await ctx.send(error_message)
    return role 


async def task_completion_screen(ctx, bot, role=None) -> None:
    def check(message: discord.Message) -> bool:
        if message.author != ctx.author:
            return False
        try:
            serial_number = int(message.content)
        except:
            return False
        
        return True
    
    mapped_tasks = await task_db.get_guild_tasks(ctx.guild, role=role)
    await displayTasks(ctx, mapped_tasks)
    if len(mapped_tasks) == 0:
        return

    await ctx.send('Please enter the id of the task you would like to mark as complete')
    serial_number_message: discord.Message = await bot.wait_for('message', check=check)
    serial_number: int = int(serial_number_message.content)

    for task in mapped_tasks:
        if str(task.task_id) == str(serial_number):
            task_embed = create_task_embed(task)
            await ctx.send(embed=task_embed)
            await ctx.send('Removing this task...')
            await task_db.delete_one_task(task)
            await ctx.send('Done!')
            return






