from typing import Union

import discord
from bot import TaskTrackerBot
from db_manager import copypasta_db
from discord.ext import commands
from models.copypasta import CopypastaIn


class CopyPastas(commands.Cog):
    bot: TaskTrackerBot
    def __init__(self, bot: TaskTrackerBot) -> None:
        self.bot = bot
    
    async def get_copypasta_from_user(self, ctx: commands.Context) -> Union[CopypastaIn, None]:
        def check(message: discord.Message) -> bool:
            if ctx.author != message.author:
                return False
            return True
        await ctx.send('What is the name of the copypasta?')
        copypasta_name = str((await self.bot.wait_for('message', check=check)).content)
        if len(copypasta_name) > 60:
            await ctx.send('The copypasta cannot be more than 60 characters')
            return

        await ctx.send('What is the copypasta content?(Paste in chat)')
        copypasta_content = str((await self.bot.wait_for('message', check=check)).content)

        return CopypastaIn(
            name=str(copypasta_name),
            content=str(copypasta_content),
            guild_id=str(ctx.guild.id)
        )
    
    @commands.command(name='addCopypasta')
    async def add_copypasta(self, ctx: commands.Context) -> None:
        copypasta_input = await self.get_copypasta_from_user(ctx)
        if not copypasta_input:
            return
        await copypasta_db.insert_one_copypasta(copypasta_input)
        await ctx.send('Done!')
    
    @commands.command()
    async def copypasta(ctx: commands.Context, *, copypasta_name: str) -> None:
        copypasta_output = await copypasta_db.get_copypasta_by_name_and_guild(copypasta_name, ctx.guild)
        if copypasta_output:
            await ctx.send(f'From {ctx.author.mention}:\n{copypasta_output.content}')
        else:
            await ctx.send('Copypasta not found!')
    
    @commands.command()
    async def copypastas(ctx: commands.Context) -> None:
        copypasta_outputs = await copypasta_db.get_copypastas_by_guild(ctx.guild)
        copypastas_embed = discord.Embed(
            type='rich',
            title='Copypastas for this server',
            description=f'Total: {len(copypasta_outputs)}\n'
        )
        if copypasta_outputs != []:
            for i in range(0, len(copypasta_outputs)):
                copypastas_embed.description += f'{i + 1}. {copypasta_outputs[i].name}\n'
            await ctx.send(embed=copypastas_embed)
        else:
            await ctx.send('No copypastas in database! Use -addCopypasta to add one')

def setup(bot: TaskTrackerBot):
    bot.add_cog(CopyPastas(bot))

def teardown(bot: TaskTrackerBot):
    bot.remove_cog('CopyPastas')
