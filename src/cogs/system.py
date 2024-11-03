import discord
from discord import app_commands
from discord.ext import commands
import platform
import psutil
import datetime
from utils.constants import *

class SystemCog(commands.GroupCog, name="system"):
    """Cog for system-related commands"""
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.system_info = {}

    @app_commands.command(name="collect", description=CMD_COLLECT_DESC)
    async def collect(self, interaction: discord.Interaction):
        """Collect system specifications"""
        self.system_info = {
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

    @app_commands.command(name="show", description=CMD_SHOW_DESC)
    async def show(self, interaction: discord.Interaction):
        """Display collected system specifications"""
        if not self.system_info:
            embed = discord.Embed(
                title=f"{ICON_ERROR} No System Information Available",
                description=MSG_NO_INFO,
                color=COLOR_ERROR
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title=f"{ICON_SYSTEM} System Specifications",
            description=f"Collected at: {self.system_info['Collection Time']}",
            color=COLOR_INFO
        )

        for key, value in self.system_info.items():
            if key != "Collection Time":
                embed.add_field(name=key, value=value, inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function for the system cog"""
    await bot.add_cog(SystemCog(bot))
