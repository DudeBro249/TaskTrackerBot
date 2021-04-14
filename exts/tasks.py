from datetime import date
from typing import List, Union

import discord
from bot import TaskTrackerBot
from constants.environment import SECRET_GUILD_ID
from db_manager import task_db
from discord.ext import commands
from models.task import TaskIn, TaskOut


class Tasks(commands.Cog):
    bot: TaskTrackerBot
    def __init__(self, bot: TaskTrackerBot) -> None:
        self.bot = bot
    
    async def get_task_from_user(self, ctx) -> TaskIn:
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
        title_message: discord.Message = await self.bot.wait_for('message', check=check)
        title: str = str(title_message.content)

        await ctx.send('Enter the content of the task')
        content_message: discord.Message = await self.bot.wait_for('message', check=check)
        task_content: str = str(content_message.content)

        await ctx.send('What is the deadline? Please provide in the format DD/MM/YY')
        deadline_message: discord.Message = await self.bot.wait_for('message', check=deadline_check)
        deadline: str = str(deadline_message.content)

        return TaskIn(
            title = str(title),
            content = str(task_content),
            deadline = str(deadline),
            date_assigned = date.today().strftime('%d/%m/%Y'),
            guild_id = str(ctx.guild.id),
            role_id = ''
        )
    
    def create_task_embed(self, task: Union[TaskIn, TaskOut]) -> discord.Embed:
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
    
    async def displayTasks(self, ctx: commands.Context, tasks: List[TaskOut]) -> bool:
        if len(tasks) == 0:
            await ctx.send('No tasks. Woohoo!')
            return True
            
        for task in tasks:
            task_embed = self.create_task_embed(task)
            await ctx.send(embed=task_embed)
        return False
    
    async def post_to_secret_server(self, ctx: commands.Context, input_task: TaskIn) -> None:
        if SECRET_GUILD_ID == str(ctx.guild.id):
            for channel in ctx.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    if channel.name == str(input_task.title).lower():
                        await channel.send(f'{ctx.author.mention}')
                        await channel.send(embed=self.create_task_embed(input_task))
    
    async def get_and_add_task(self, ctx: commands.Context, role: discord.Role=None) -> None:
        input_task = await self.get_task_from_user(ctx)
        await self.post_to_secret_server(ctx, input_task=input_task)

        if role != None:
            input_task.role_id = str(role.id)

        await task_db.insert_one_task(input_task)
        await ctx.send('Added task to database!')
    
    @commands.command()
    async def addTask(self, ctx: commands.Context, *, role: discord.Role=None) -> None:
        await self.get_and_add_task(ctx, role=role)

    @commands.command()
    async def getTasks(self, ctx: commands.Context, *, role: discord.Role=None) -> None:
        mapped_tasks = await task_db.get_guild_tasks(ctx.guild, role=role)
        await self.displayTasks(
            ctx=ctx,
            tasks=mapped_tasks
        )
    @commands.command()
    async def markComplete(self, ctx, *, role: discord.Role=None) -> None:
        def check(message: discord.Message) -> bool:
            if message.author != ctx.author:
                return False
            try:
                int(message.content)
            except:
                return False
            
            return True
        
        tasks = await task_db.get_guild_tasks(ctx.guild, role=role)
        await self.displayTasks(ctx, tasks)
        if len(tasks) == 0:
            return

        await ctx.send('Please enter the id of the task you would like to mark as complete')
        serial_number_message: discord.Message = await self.bot.wait_for('message', check=check)
        serial_number: int = int(serial_number_message.content)

        for task in tasks:
            if str(task.task_id) == str(serial_number):
                task_embed = self.create_task_embed(task)
                await ctx.send(embed=task_embed)
                await ctx.send('Removing this task...')
                await task_db.delete_one_task(task)
                await ctx.send('Done!')
                return

def setup(bot: TaskTrackerBot):
    bot.add_cog(Tasks(bot))

def teardown(bot: TaskTrackerBot):
    bot.remove_cog('Tasks')
