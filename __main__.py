from constants.environment import DISCORD_TOKEN
from bot import TaskTrackerBot
from dotenv import load_dotenv

DEBUG = True
if DEBUG:
    load_dotenv()

def main():
    bot = TaskTrackerBot.new()
    extension_names = [
        'exts.channels',
        'exts.copypastas',
        'exts.fun',
        'exts.moderation',
        'exts.tasks',
    ]

    for extension_name in extension_names:
        bot.load_extension(extension_name)
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    main()