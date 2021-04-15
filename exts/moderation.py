import discord
from bot import TaskTrackerBot
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext

class Moderation(commands.Cog):
    bot: TaskTrackerBot
    def __init__(self, bot: TaskTrackerBot) -> None:
        self.bot = bot
    
    @cog_ext.cog_slash(name='purgeRole', description='Removes this role from every member in the server')
    async def purge_role(ctx: SlashContext, *, role: discord.Role=None) -> None:
        for member in ctx.guild.members:
            try:
                if role in member.roles:
                    await member.remove_roles(role, reason=f'purgeRole command issued by {ctx.author.name}')
            except Exception:
                pass
        await ctx.send('Done!')
    
    # @commands.command()
    # async def kick(ctx: commands.Context, member:discord.Member, *, reason: str=None) -> None:
    #     if reason:
    #         await member.kick(reason=reason)
    #     else:
    #         await ctx.send('Please provide a reason with the command')


    # @commands.command()
    # async def ban(ctx: commands.Context, member:discord.Member, *, reason: str=None) -> None:
    #     if reason:
    #         await member.ban(reason=reason)
    #     else:
    #         await ctx.send('Please provide a reason with the command')

def setup(bot: TaskTrackerBot):
    bot.add_cog(Moderation(bot))

def teardown(bot: TaskTrackerBot):
    bot.remove_cog('Moderation')
