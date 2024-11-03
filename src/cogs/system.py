import discord
from discord import app_commands
from discord.ext import commands
import platform
import psutil
import datetime
import distro
from utils.constants import *

class SystemCog(commands.GroupCog, name="system"):
    """Cog for system-related commands"""
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.system_info = {}

    def get_os_info(self):
        """Get detailed OS information"""
        if platform.system() == "Linux":
            return f"{distro.name(pretty=True)}"
        elif platform.system() == "Windows":
            return platform.win32_ver()[0]
        elif platform.system() == "Darwin":
            return f"macOS {platform.mac_ver()[0]}"
        else:
            return platform.system()

    def get_processor_info(self):
        """Get detailed processor information"""
        if platform.system() == "Linux":
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if line.startswith('model name'):
                            return line.split(':')[1].strip()
            except:
                pass
        return platform.processor() or "Unknown"

    @app_commands.command(name="collect", description=CMD_COLLECT_DESC)
    async def collect(self, interaction: discord.Interaction):
        """Collect system specifications"""
        self.system_info = {
            "OS": self.get_os_info(),
            "Architecture": platform.machine(),
            "Processor": self.get_processor_info(),
            "Total RAM": f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB",
            "Collection Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        embed = discord.Embed(
            title=f"{ICON_SUCCESS} System Information Collected",
            description=MSG_COLLECTED,
            color=COLOR_SUCCESS
        )
        
        # Make the response ephemeral (only visible to the command user)
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
