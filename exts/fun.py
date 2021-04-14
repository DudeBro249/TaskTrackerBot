from discord.ext.commands.core import command
from utilities.bot_utilities import get_role_by_attribute
from message_collector import download_server
from utilities.general_utilities import remove_all, sort_dict_by_value

import discord
from bot import TaskTrackerBot
from discord.ext import commands


class Fun(commands.Cog):
    bot: TaskTrackerBot
    def __init__(self, bot: TaskTrackerBot) -> None:
        self.bot = bot
    
    @commands.command()
    async def countMessage(self, ctx, *, message_string: str=None) -> None:
        def check(message: discord.Message) -> bool:
            if ctx.author != message.author:
                return False
            return True

        counts = {}
        if message_string:
            message_string = message_string.strip()
        
        await ctx.send("What channel would you like to count in?")
        channel_id = remove_all((await self.bot.wait_for('message', check=check)).content, ['<', '>', '#'])
        channel: discord.TextChannel = self.bot.get_channel(int(channel_id))

        async for message in channel.history(limit=None):
            if message_string:
                if message.content.lower() == message_string.lower():
                    if str(message.author.name) in counts.keys():
                        counts[str(message.author.name)] += 1
                    else:
                        counts[str(message.author.name)] = 1
            elif not message_string:
                if str(message.author.name) in counts.keys():
                    counts[str(message.author.name)] += 1
                else:
                    counts[str(message.author.name)] = 1

        counts = sort_dict_by_value(counts)
        message_count_embed = discord.Embed(
            type='rich',
            title='Message Count'
        )
        message_count_embed.description = f'Total: {sum(counts.values())}\n'
        for member_name in counts.keys():
            message_count_embed.description += f'{member_name}: {counts.get(member_name)}\n'
        
        await ctx.send(embed=message_count_embed)
    
    @commands.command()
    async def downloadServer(self, ctx: commands.Context) -> None:
        def check(message: discord.Message) -> bool:
            if ctx.author != message.author:
                return False
            return True
        
        blacklisted_channel_ids = None

        await ctx.send('What is the id of the server you want to scrape data from?')
        guild_id = int((await self.bot.wait_for('message', check=check)).content)

        await ctx.send('What channel ids would you like to blacklist? NA for none (separate by comma)')
        blacklist_string = str((await self.bot.wait_for('message', check=check)).content).replace('\n', '').strip()

        if blacklist_string.lower() != 'na':
            blacklisted_channel_ids = [int(item) for item in blacklist_string.split(',')]

        await ctx.send('Starting process...')
        await download_server(self.bot.get_guild(guild_id), blacklisted_channel_ids=blacklisted_channel_ids)
        await ctx.send(f'{ctx.author.mention} Done collecting data ;)')


    @commands.command()
    async def pingVC(ctx: commands.Context):
        vc_role = get_role_by_attribute('name', ctx.author.voice.channel.name, ctx.guild.roles)
        await ctx.send(vc_role.mention)
    
    @commands.command(pass_context=False)
    async def setStatus(self, new_status: str) -> None:
        possible_statuses = ['dnd', 'online', 'idle']
        if new_status in possible_statuses:
            await self.bot.change_presence(status=new_status)
        return

def setup(bot: TaskTrackerBot):
    bot.add_cog(Fun(bot))

def teardown(bot: TaskTrackerBot):
    bot.remove_cog('Fun')
