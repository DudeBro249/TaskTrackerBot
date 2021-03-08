from dotenv import load_dotenv

DEBUG = False
if DEBUG:
    load_dotenv()

from typing import List
from message_collector import download_server

from db_manager import task_db
from db_manager import channel_db
from db_manager import copypasta_db
from utilities.general_utilities import remove_all, sort_dict_by_value
from utilities.bot_utilities import displayTasks, get_and_add_task, get_copypasta_from_user, get_role_by_attribute, manage_voice_channel_roles, task_completion_screen
import os

import discord
from discord.ext import commands

bot_intents = discord.Intents.default()
bot_intents.members = True

bot = commands.Bot(command_prefix='-', intents=bot_intents)

@bot.command()
async def addTask(ctx, *, role: discord.Role=None) -> None:
    await get_and_add_task(ctx, bot, role=role)


@bot.command()
async def getTasks(ctx, *, role: discord.Role=None) -> None:
    mapped_tasks = await task_db.get_guild_tasks(ctx.guild, role=role)
    await displayTasks(ctx, mapped_tasks)


@bot.command()
async def markComplete(ctx, *, role: discord.Role=None) -> None:
    await task_completion_screen(ctx, bot, role=role)


@bot.command()
async def countMessage(ctx, *, message_string: str=None) -> None:
    def check(message: discord.Message) -> bool:
        if ctx.author != message.author:
            return False
        return True

    counts = {}
    if message_string:
        message_string = message_string.strip()
    
    await ctx.send("What channel would you like to count in?")
    channel_id = remove_all((await bot.wait_for('message', check=check)).content, ['<', '>', '#'])
    channel: discord.TextChannel = bot.get_channel(int(channel_id))

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


@bot.command()
async def purgeRole(ctx, *, role: discord.Role=None) -> None:
    for member in ctx.guild.members:
        try:
            if role in member.roles:
                await member.remove_roles(role, reason=f'purgeRole command issued by {ctx.author.name}')
        except Exception as exception:
            pass
    await ctx.send('Done!')


@bot.command()
async def addChannel(ctx, channel: discord.TextChannel) -> None:
    if isinstance(channel, discord.TextChannel):
        await channel_db.insert_one_channel(raw_discord_channel=channel)
        await ctx.send('Done!')
    else:
        await ctx.send('Unable to store channel. Please make sure to mention it with #')


@bot.command()
async def addCopypasta(ctx) -> None:
    copypasta_input = await get_copypasta_from_user(ctx, bot)
    if not copypasta_input:
        return
    await copypasta_db.insert_one_copypasta(copypasta_input)
    await ctx.send('Done!')


@bot.command()
async def copypasta(ctx, *, copypasta_name: str) -> None:
    copypasta_output = await copypasta_db.get_copypasta_by_name_and_guild(copypasta_name, ctx.guild)
    if copypasta_output:
        await ctx.send(f'From {ctx.author.mention}:\n{copypasta_output.content}')
    else:
        await ctx.send('Copypasta not found!')


@bot.command()
async def copypastas(ctx) -> None:
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
        


# @bot.command()
# async def kick(ctx, member:discord.Member, *, reason: str=None) -> None:
#     if reason:
#         await member.kick(reason=reason)
#     else:
#         await ctx.send('Please provide a reason with the command')


# @bot.command()
# async def ban(ctx, member:discord.Member, *, reason: str=None) -> None:
#     if reason:
#         await member.ban(reason=reason)
#     else:
#         await ctx.send('Please provide a reason with the command')



@bot.command()
async def downloadServer(ctx) -> None:
    def check(message: discord.Message) -> bool:
        if ctx.author != message.author:
            return False
        return True
    
    blacklisted_channel_ids = None

    await ctx.send('What is the id of the server you want to scrape data from?')
    guild_id = int((await bot.wait_for('message', check=check)).content)

    await ctx.send('What channel ids would you like to blacklist? NA for none (separate by comma)')
    blacklist_string = str((await bot.wait_for('message', check=check)).content).replace('\n', '').strip()

    if blacklist_string.lower() != 'na':
        blacklisted_channel_ids = [int(item) for item in blacklist_string.split(',')]

    await ctx.send('Starting process...')
    await download_server(bot.get_guild(guild_id), blacklisted_channel_ids=blacklisted_channel_ids)
    await ctx.send(f'{ctx.author.mention} Done collecting data ;)')


@bot.command()
async def pingVC(ctx):
    vc_role: discord.Role = get_role_by_attribute('name', ctx.author.voice.channel.name, ctx.guild.roles)
    await ctx.send(vc_role.mention)


@bot.command()
async def setStatus(ctx, new_status: str) -> None:
    possible_statuses = ['dnd', 'online', 'idle']
    if new_status in possible_statuses:
        await bot.change_presence(status=new_status)
    return


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot_guilds: List[discord.Guild] = bot.guilds
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
                    

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
    await manage_voice_channel_roles(member, before, after)
    if before.channel and after.channel and before.channel == after.channel and after.self_stream:
        designated_channel = await channel_db.get_bot_channel_by_guild(before.channel.guild)
        text_channel: discord.TextChannel = discord.utils.get(before.channel.guild.channels, id=int(designated_channel.channel_id))
        await text_channel.send(f'{member.name} is streaming! Get in here!')

bot.run(str(os.getenv('DISCORD_TOKEN')))

