from typing import List
import discord
import os

async def download_server(guild: discord.Guild, blacklisted_channel_ids: List[int]):
    
    count = 0

    file = None

    if not os.path.exists(f'all-messages.txt'):
        file = open('all-messages.txt', mode='x', encoding='utf-8')

    else:
        file = open('all-messages.txt', mode='w+', encoding='utf-8')
    
    for channel in guild.channels:
        if not isinstance(channel, discord.TextChannel):
            continue
        
        if int(channel.id) in blacklisted_channel_ids:
            continue

        print(f'started going through {channel.name}')

        file.write(r"<|" + channel.name + r"|>" + "\n")

        async for message in channel.history(limit=None):
            assert isinstance(message, discord.Message)

            text = str(message.content).strip()
            file.write(str(message.author) + '::' + str(message.created_at) + "::" + text + r"<|endoftext|>" + "\n")

            print(f'Message #{count}: {message.author} --> {text}')
            count += 1

        print(f'finished going through {channel.name}')

    file.close()

