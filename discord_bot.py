import discord
from discord.ext import commands
import asyncio
import os
import logging
from typing import Optional
from config import Config
from github_client import GitHubClient
from roblox_client import RobloxClient
from discord import app_commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SyncBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = False
        intents.guilds = True
        
        super().__init__(command_prefix='!', intents=intents)
        
        self.github_client = GitHubClient()
        self.roblox_client = RobloxClient()
    
    async def setup_hook(self):
        """Called when the bot is starting up"""
        try:
            guild_obj = discord.Object(id=Config.GUILD_ID) if (Config.GUILD_ID and Config.GUILD_ID > 0) else None
            for cmd in list(self.tree.get_commands()):
                if cmd.name == 'sync':
                    try:
                        self.tree.remove_command(cmd.name, guild=guild_obj)
                    except Exception:
                        pass
            self.tree.add_command(app_commands.Command(
                name='sync',
                description='Sync latest changes from GitHub to Roblox',
                callback=sync_command_handler
            ), guild=guild_obj)

            if guild_obj:
                await self.tree.sync(guild=guild_obj)
                guild_cmds = await self.tree.fetch_commands(guild=guild_obj)
                logger.info(f"Slash commands synced to guild {Config.GUILD_ID}: {[c.name for c in guild_cmds]}")
            else:
                await self.tree.sync()
                global_cmds = await self.tree.fetch_commands()
                logger.info(f"Slash commands synced globally: {[c.name for c in global_cmds]}")
        except Exception as e:
            logger.error(f"Slash command registration/sync failed: {e}")
        logger.info("Bot setup complete")
    
    def has_permission(self, user: discord.Member) -> bool:
        """Check if user has permission to use sync command.

        If no allowlists are configured, allow everyone to use the command.
        """
        allowed_users = [u for u in Config.ALLOWED_USERS if u]
        allowed_roles = [r for r in Config.ALLOWED_ROLES if r]

        if not allowed_users and not allowed_roles:
            return True

        if str(user.id) in allowed_users:
            return True

        user_roles = [str(role.id) for role in user.roles]
        if any(role_id in allowed_roles for role_id in user_roles):
            return True

        return False
    
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        logger.error(f"Command error: {error}")
        await ctx.send(f"An error occurred: {str(error)}")

bot = SyncBot()

async def sync_command_handler(interaction: discord.Interaction, branch: Optional[str] = None):
    """Handle the /sync command"""
    if not bot.has_permission(interaction.user):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    try:
        await interaction.followup.send(f"🔄 Fetching latest changes from GitHub... (branch: {branch or bot.github_client.branch})")
        commit_info = await bot.github_client.get_latest_commit(branch)
        commit_sha = commit_info['sha'][:7]
        commit_message = commit_info['commit']['message']
        
        await interaction.followup.send("📥 Downloading repository...")
        zip_path = os.path.join(Config.TEMP_DIR, 'repo.zip')
        await bot.github_client.download_repository(zip_path, branch)
        
        await interaction.followup.send("📂 Extracting data files...")
        await bot.github_client.extract_data_files(zip_path, Config.DATA_FILES_DIR)
        
        await interaction.followup.send("🎮 Downloading current place file...")
        await bot.roblox_client.download_place_file()
        
        await interaction.followup.send("🔄 Syncing data files with Lune...")
        await bot.roblox_client.sync_data_files()
        
        await interaction.followup.send("🚀 Publishing to Roblox...")
        await bot.roblox_client.publish_place()
        
        embed = discord.Embed(
            title="✅ Sync Completed Successfully!",
            color=0x00ff00,
            description=f"**Commit:** `{commit_sha}`\n**Message:** {commit_message}"
        )
        embed.add_field(name="Steps Completed", value="• Fetched latest changes\n• Downloaded repository\n• Extracted data files\n• Downloaded place file\n• Synced with Lune\n• Published to Roblox", inline=False)
        
        await interaction.followup.send(embed=embed)
        
        bot.roblox_client.cleanup_temp_files()
        
    except Exception as e:
        logger.error(f"Sync error: {e}")
        embed = discord.Embed(
            title="❌ Sync Failed",
            color=0xff0000,
            description=f"An error occurred during sync: {str(e)}"
        )
        await interaction.followup.send(embed=embed)
        
        bot.roblox_client.cleanup_temp_files()

if __name__ == "__main__":
    if not Config.DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables")
        exit(1)
    
    if not Config.GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN not found in environment variables")
        exit(1)
    
    if not Config.ROBLOX_COOKIE:
        logger.error("ROBLOX_COOKIE not found in environment variables")
        exit(1)
    
    os.makedirs(Config.TEMP_DIR, exist_ok=True)
    
    bot.run(Config.DISCORD_TOKEN)
