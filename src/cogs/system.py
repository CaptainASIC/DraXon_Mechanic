import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from utils.constants import *

class SystemSpecsModal(discord.ui.Modal, title="System Specifications"):
    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    os = discord.ui.TextInput(
        label="Operating System",
        placeholder="e.g., Arch Linux, Windows 11, macOS Sonoma",
        required=True
    )

    cpu = discord.ui.TextInput(
        label="CPU",
        placeholder="e.g., AMD Ryzen 9 5950X, Intel i9-13900K",
        required=True
    )

    gpu = discord.ui.TextInput(
        label="GPU",
        placeholder="e.g., NVIDIA RTX 4090, AMD RX 7900 XTX",
        required=True
    )

    memory = discord.ui.TextInput(
        label="Memory",
        placeholder="e.g., 32GB DDR5-6000",
        required=True
    )

    storage = discord.ui.TextInput(
        label="Storage",
        placeholder="e.g., 2TB NVMe SSD, 8TB HDD",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await self.cog.save_system_info(
            interaction.user.id,
            str(self.os),
            str(self.cpu),
            str(self.gpu),
            str(self.memory),
            str(self.storage)
        )
        
        # After saving system specs, show the peripherals modal
        await interaction.response.send_modal(PeripheralsModal(self.cog, update_only=True))

class PeripheralsModal(discord.ui.Modal, title="Input Devices"):
    def __init__(self, cog, update_only=False):
        super().__init__()
        self.cog = cog
        self.update_only = update_only

    keyboard = discord.ui.TextInput(
        label="Keyboard",
        placeholder="e.g., Keychron Q1 w/ Gateron Browns",
        required=False
    )

    mouse = discord.ui.TextInput(
        label="Mouse",
        placeholder="e.g., Logitech G Pro X Superlight",
        required=False
    )

    other_controllers = discord.ui.TextInput(
        label="Other Controllers",
        placeholder="e.g., Xbox Elite Controller, HOTAS",
        required=False,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        if self.update_only:
            # Update only peripherals
            await self.cog.update_peripherals(
                interaction.user.id,
                str(self.keyboard),
                str(self.mouse),
                str(self.other_controllers)
            )
        
        embed = discord.Embed(
            title=f"{ICON_SUCCESS} System Information Saved",
            description="Your system information has been saved. Use `/system show` to display it.",
            color=COLOR_SUCCESS
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SystemCog(commands.GroupCog, name="system"):
    """Cog for system-related commands"""
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def save_system_info(self, user_id, os, cpu, gpu, memory, storage):
        """Save core system information to database"""
        await self.bot.db.save_system_info(user_id, os, cpu, gpu, memory, storage)

    async def update_peripherals(self, user_id, keyboard, mouse, other_controllers):
        """Update peripherals information in database"""
        await self.bot.db.update_peripherals(user_id, keyboard, mouse, other_controllers)

    @app_commands.command(name="collect", description=CMD_COLLECT_DESC)
    async def collect(self, interaction: discord.Interaction):
        """Open modal to collect system specifications"""
        modal = SystemSpecsModal(self)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="show", description=CMD_SHOW_DESC)
    async def show(self, interaction: discord.Interaction):
        """Display collected system specifications"""
        info = await self.bot.db.get_system_info(interaction.user.id)
        
        if not info:
            embed = discord.Embed(
                title=f"{ICON_ERROR} No System Information Available",
                description=MSG_NO_INFO,
                color=COLOR_ERROR
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title=f"{ICON_SYSTEM} System Specifications",
            description=f"Last Updated: {info['updated_at'].strftime('%Y-%m-%d %H:%M:%S')}",
            color=COLOR_INFO
        )

        # Core system specs
        embed.add_field(name="Operating System", value=info['os'], inline=True)
        embed.add_field(name="CPU", value=info['cpu'], inline=True)
        embed.add_field(name="GPU", value=info['gpu'], inline=True)
        embed.add_field(name="Memory", value=info['memory'], inline=True)
        embed.add_field(name="Storage", value=info['storage'], inline=True)
        
        # Input devices (only show if they exist and have values)
        if 'keyboard' in info and info['keyboard']:
            embed.add_field(name="Keyboard", value=info['keyboard'], inline=True)
        if 'mouse' in info and info['mouse']:
            embed.add_field(name="Mouse", value=info['mouse'], inline=True)
        if 'other_controllers' in info and info['other_controllers']:
            embed.add_field(name="Other Controllers", value=info['other_controllers'], inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function for the system cog"""
    await bot.add_cog(SystemCog(bot))
