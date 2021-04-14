from typing import List
from .general_utilities import remove_all
import discord

def get_role_from_mention(role_mention: str, roles: List[discord.Role]) -> discord.Role:
    role_id = remove_all(role_mention, ['<', '>', '!', '@', '&'])
    return get_role_by_attribute('id', role_id, roles)

def get_role_by_attribute(attribute_name, role_attribute, roles: List[discord.Role]) -> discord.Role:
    for role in roles:
        if str(getattr(role, attribute_name)) == role_attribute:
            return role
    return None


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
