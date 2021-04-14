from typing import List
from utilities.bot_utilities import get_role_by_attribute, manage_voice_channel_roles
import discord
from db_manager import channel_db

from discord.ext import commands

class TaskTrackerBot(commands.Bot):

    async def on_ready(self):
        bot_guilds: List[discord.Guild] = self.guilds
        for guild in bot_guilds:
            for channel in guild.channels:
                if isinstance(channel, discord.VoiceChannel):
                    if len(channel.members) > 0:
                        role = get_role_by_attribute('name', channel.name, roles=guild.roles)
                        if role == None:
                            role = await guild.create_role(name=channel.name)
                    
                        for member in channel.members:
                            assert isinstance(member, discord.Member)
                            if role not in member.roles:
                                await member.add_roles(role)
        print(f'Logged in as {self.user}')

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        await manage_voice_channel_roles(member, before, after)
        if before.channel and after.channel and before.channel == after.channel and after.self_stream:
            designated_channel = await channel_db.get_bot_channel_by_guild(before.channel.guild)
            text_channel: discord.TextChannel = discord.utils.get(before.channel.guild.channels, id=int(designated_channel.channel_id))
            await text_channel.send(f'{member.name} is streaming! Get in here!')
    
    @classmethod
    def new(cls) -> 'TaskTrackerBot':
        bot_intents = discord.Intents.default()
        bot_intents.members = True
        return cls(
            command_prefix='-',
            intents=bot_intents
        )
