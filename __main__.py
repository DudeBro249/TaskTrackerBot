from discord_slash.client import SlashCommand
from bot import TaskTrackerBot
from constants.environment import DISCORD_TOKEN
from db_manager.db import create_all_tables


def main():
    bot = TaskTrackerBot.new()
    SlashCommand(bot, sync_commands=True)

    extension_names = [
        'exts.channels',
        'exts.copypastas',
        'exts.fun',
        'exts.moderation',
        'exts.tasks',
    ]

    for extension_name in extension_names:
        bot.load_extension(extension_name)
    create_all_tables()
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    main()
