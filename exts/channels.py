
import discord
from bot import TaskTrackerBot
from db_manager import channel_db
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext


class Channels(commands.Cog):
    bot: TaskTrackerBot
    def __init__(self, bot: TaskTrackerBot) -> None:
        self.bot = bot
    
    @cog_ext.cog_slash(name='setChannel', description="Sets the server's designated channel to post updates and announcements in")
    async def setChannel(ctx: SlashContext, channel: discord.TextChannel) -> None:
        if isinstance(channel, discord.TextChannel):
            await channel_db.insert_one_channel(raw_discord_channel=channel)
            await ctx.send('Done!')
        else:
            await ctx.send('Unable to store channel. Please make sure to mention it with #')


def setup(bot: TaskTrackerBot):
    bot.add_cog(Channels(bot))

def teardown(bot: TaskTrackerBot):
    bot.remove_cog('Channels')
