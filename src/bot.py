import discord
import os
from dotenv import load_dotenv
from utils.constants import *
from commands import setup_system_commands

# Load environment variables from env directory
load_dotenv('env/.env')

class DraXonMechanic(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Setup commands
        await setup_system_commands(self)
        await self.tree.sync()

client = DraXonMechanic()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(
        type=getattr(discord.ActivityType, BOT_ACTIVITY_TYPE), 
        name=BOT_ACTIVITY_NAME
    ))

def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print(MSG_ERROR_TOKEN)
        return
    
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    if debug:
        print("Debug mode enabled")
    
    client.run(token)

if __name__ == "__main__":
    main()
