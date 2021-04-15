import asyncio
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from utilities.bot_utilities import get_role_by_attribute
from message_collector import download_server
from utilities.general_utilities import remove_all, sort_dict_by_value
from discord_slash import cog_ext

import discord
from bot import TaskTrackerBot
from discord.ext import commands


class Fun(commands.Cog):
    bot: TaskTrackerBot
    def __init__(self, bot: TaskTrackerBot) -> None:
        self.bot = bot
    
    @cog_ext.cog_slash(name='countMessage', description='Counts all the messages in a certain channel')
    async def count_messages(self, ctx: SlashContext, *, message_string: str=None) -> None:
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
    
    # @cog_ext.cog_slash(name='downloadServer', description='Run to find out...')
    # async def downloadServer(self, ctx: SlashContext) -> None:
    #     await ctx.send('lol you ***THOUGHT***')
    #     return
    #     # def check(message: discord.Message) -> bool:
    #     #     if ctx.author != message.author:
    #     #         return False
    #     #     return True
        
    #     # blacklisted_channel_ids = None

    #     # await ctx.send('What is the id of the server you want to scrape data from?')
    #     # guild_id = int((await self.bot.wait_for('message', check=check)).content)

    #     # await ctx.send('What channel ids would you like to blacklist? NA for none (separate by comma)')
    #     # blacklist_string = str((await self.bot.wait_for('message', check=check)).content).replace('\n', '').strip()

    #     # if blacklist_string.lower() != 'na':
    #     #     blacklisted_channel_ids = [int(item) for item in blacklist_string.split(',')]

    #     # await ctx.send('Starting process...')
    #     # await download_server(self.bot.get_guild(guild_id), blacklisted_channel_ids=blacklisted_channel_ids)
    #     # await ctx.send(f'{ctx.author.mention} Done collecting data ;)')


    @cog_ext.cog_slash(name='pingVC', description='Pings the role of the voice channel you are in')
    async def ping_vc(self, ctx: SlashContext):
        if not ctx.author.voice.channel:
            await ctx.send('You are not in a voice channel right now :(')
            return
        vc_role = get_role_by_attribute('name', ctx.author.voice.channel.name, ctx.guild.roles)
        await ctx.send(vc_role.mention)
    
    @cog_ext.cog_slash(name='setStatus', description='Sets the status of the bot')
    async def setStatus(self, ctx: SlashContext, new_status: str) -> None:
        possible_statuses = ['dnd', 'online', 'idle']
        if new_status in possible_statuses:
            await self.bot.change_presence(status=new_status)
        completed_message = await ctx.send('Done')
        await asyncio.sleep(2)
        await completed_message.delete()

def setup(bot: TaskTrackerBot):
    bot.add_cog(Fun(bot))

def teardown(bot: TaskTrackerBot):
    bot.remove_cog('Fun')
