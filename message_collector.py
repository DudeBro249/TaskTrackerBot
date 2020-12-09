from typing import Any, Dict, List
import discord
import os

async def get_user_messages(guild: discord.Guild, member_names: List[str], blacklisted_channel_ids: List[int]=None) -> None:
    bot_prefixes = ['?', '-', '_', '!', '/', 'pls', ">"]
    special_text = ['*', '_']

    members: List[discord.Member] = []
    files: Dict[str, Any] = {}
    
    for member_name in member_names:
        member = discord.utils.get(guild.members, name=member_name)
        members.append(member)

        if not os.path.exists(f'{member.name}-messages.txt'):
            files[member.name] = open(f'{member.name}-messages.txt', mode='x', encoding='utf-8')

        else:
            files[member.name] = open(f'{member.name}-messages.txt', mode='w+', encoding='utf-8')

    for channel in guild.channels:
        if not isinstance(channel, discord.TextChannel):
            continue

        if int(channel.id) in blacklisted_channel_ids:
            continue

        print(f'started going through {channel.name}')

        async for message in channel.history(limit=None):
            assert isinstance(message, discord.Message)
            
            if message.author in members:
                text = str(message.content).strip()
                print(f'{message.author} posted {text}')

                flag = False
                
                for prefix in bot_prefixes: 
                    if text.startswith(prefix):
                        flag = True

                for chars in special_text:
                    text = text.replace(chars, '')

                if message.attachments: flag = True
                
                if text.isspace(): flag = True 
                
                if not flag:
                    
                    try:
                        utf_text = (text + "\n" + r"<|endoftext|>" + "\n")
                        
                        files[message.author.name].write(utf_text)

                    except Exception as e:
                        print(e)
            
        print(f'finished going through {channel.name}')

    for filename in files.keys():
        files[filename].close()


