import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.constants import *

# Load environment variables from env directory
load_dotenv('../env/.env')

class DraXonMechanic(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=discord.Intents.default(),
            help_command=None
        )

    async def setup_hook(self):
        """Setup hook for loading cogs and syncing commands"""
        # Load all cogs
        await self.load_extension('cogs.system')
        print("Loaded system cog")
        
        # Sync commands with Discord
        await self.tree.sync()
        print("Synced command tree")

    async def on_ready(self):
        """Event handler for when the bot is ready"""
        print(f'{self.user} has connected to Discord!')
        print(f'Bot Version: {APP_VERSION}')
        print(f'Build Date: {BUILD_DATE}')
        
        await self.change_presence(activity=discord.Activity(
            type=getattr(discord.ActivityType, BOT_ACTIVITY_TYPE),
            name=BOT_ACTIVITY_NAME
        ))

def main():
    """Main function to run the bot"""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print(MSG_ERROR_TOKEN)
        return
    
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    if debug:
        print("Debug mode enabled")
    
    bot = DraXonMechanic()
    bot.run(token)

if __name__ == "__main__":
    main()
