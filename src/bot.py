import discord
from discord import app_commands
import platform
import psutil
import datetime
import os
from dotenv import load_dotenv
from utils.constants import *

# Load environment variables from env directory
load_dotenv('env/.env')

class DraXonMechanic(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.system_info = {}

    async def setup_hook(self):
        await self.tree.sync()

client = DraXonMechanic()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(
        type=getattr(discord.ActivityType, BOT_ACTIVITY_TYPE), 
        name=BOT_ACTIVITY_NAME
    ))

@client.tree.command(name="system-collect", description=CMD_COLLECT_DESC)
async def system_collect(interaction: discord.Interaction):
    # Collect system information
    client.system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
        "Memory Total": f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB",
        "Memory Available": f"{round(psutil.virtual_memory().available / (1024.0 ** 3), 2)} GB",
        "Disk Usage": f"{round(psutil.disk_usage('/').used / (1024.0 ** 3), 2)} GB / {round(psutil.disk_usage('/').total / (1024.0 ** 3), 2)} GB",
        "Collection Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    embed = discord.Embed(
        title=f"{ICON_SUCCESS} System Information Collected",
        description=MSG_COLLECTED,
        color=COLOR_SUCCESS
    )
    
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="system-show", description=CMD_SHOW_DESC)
async def system_show(interaction: discord.Interaction):
    if not client.system_info:
        embed = discord.Embed(
            title=f"{ICON_ERROR} No System Information Available",
            description=MSG_NO_INFO,
            color=COLOR_ERROR
        )
        await interaction.response.send_message(embed=embed)
        return

    embed = discord.Embed(
        title=f"{ICON_SYSTEM} System Specifications",
        description=f"Collected at: {client.system_info['Collection Time']}",
        color=COLOR_INFO
    )

    for key, value in client.system_info.items():
        if key != "Collection Time":
            embed.add_field(name=key, value=value, inline=True)

    await interaction.response.send_message(embed=embed)

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
