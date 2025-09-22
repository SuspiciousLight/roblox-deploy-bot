# Roblox Deploy Bot

A Discord bot that automates syncing GitHub changes to your Roblox game. This bot allows your balancing developer to use a simple `/sync` command to push their changes directly to Roblox without needing to ping programmers.

## Features

- 🤖 Discord slash command (`/sync')
- 🔄 Automatic GitHub repository syncing (with support for the branch parameter)
- 🎮 Download/publish Roblox place via rokit
- 📊 Sync data files via Lune
- 🔐 Role-based permissions (optional)
- 📝 Step-by-step messaging and logging

## Prerequisites

- Python 3.8+
- Rust (Cargo) — to install Lune/rokit
- Discord Bot Token
- GitHub Personal Access Token
- Roblox cookie (`.ROBLOSECURITY`) and publishing rights
- Roblox Place ID и Universe ID

## Installation

1. **Clone or download this repository**

2. **Run the setup script:**

   ```bash
   python setup.py
   ```

3. **Configure your environment:**

   - Copy `env_example.txt` to `.env`
   - Fill in all the required values in `.env`

4. **Set up Discord Bot:**

   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to "Bot" section and create a bot
   - Copy the bot token to your `.env` file
   - Message Content Intent not required (slash commands work without it)

5. **Set up GitHub:**

   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `repo` permissions
   - Copy the token to your `.env` file

6. **Install CLI tools:**
   - Install rokit: `cargo install rokit`
   - Install Lune: `cargo install lune`
   - Restart the terminal and make sure that both utilities are in the PATH

## Configuration

Edit the `.env` file with your configuration:

```env
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
GUILD_ID=your_guild_id_here

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=owner/repository_name
GITHUB_BRANCH=main

# Roblox Configuration
ROBLOX_COOKIE=your_roblox_cookie_here
PLACE_ID=your_place_id_here
UNIVERSE_ID=your_universe_id_here

# File Paths
TEMP_DIR=./temp
LUNE_SCRIPT_PATH=./lune_sync.luau

# Permissions (comma-separated IDs)
ALLOWED_ROLES=role_id_1,role_id_2
ALLOWED_USERS=user_id_1,user_id_2
```

## Usage

1. **Start the bot:**

   ```bash
   python main.py
   ```

2. **Use Discord commands:**
   - `/sync` — synchronize changes from the default branch (`GITHUB_BRANCH')
   - `/sync branch:<name>` — synchronize the specified branch

## Restart & Testing

Restarting the bot:

```
Ctrl + C   # stop the running process
python main.py
```

Тест в Discord:

- Make sure that the bot is invited from the scope `applications.commands`
- If the `GUILD_ID` is correct, the commands are registered for the server immediately; if not— a global sync (sometimes 1-2 minutes)
- Enter `/sync` or `/sync branch:<thread>` and follow the steps in the bot's responses

## Commands

### `/sync`

Syncs the latest changes from your GitHub repository to Roblox:

1. Fetches latest commit from GitHub
2. Downloads the repository
3. Extracts data files
4. Downloads current place file from Roblox using rokit
5. Syncs data files using Lune
6. Publishes the updated place to Roblox using rokit

## File Structure

```
roblox-deploy-bot/
├── main.py                 # Main entry point
├── discord_bot.py          # Discord bot implementation
├── github_client.py        # GitHub API client
├── roblox_client.py        # Roblox operations client (using rokit)
├── config.py              # Configuration management
├── lune_sync.luau         # Lune script for data syncing
├── setup.py               # Setup script
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables example
└── README.md              # This file
```

## Permissions

By default, if `ALLOWED_USERS` and `ALLOWED_ROLES` are empty, `/sync` is available to everyone.
To restrict access, set allowlist in `.env`:

```
ALLOWED_USERS=discord_user_id_1,discord_user_id_2
ALLOWED_ROLES=discord_role_id_1
```

## Troubleshooting

### Common Issues

1. **"You don't have permission to use this command"**

   - Check that your user ID or role ID is in the `.env` file
   - Make sure the bot has the correct permissions in your Discord server

2. **"Failed to download place file"**

   - Make sure that `rokit` is installed in the PATH as well
   - Check the Place ID
   - The account by `ROBLOX_COOKIE` has access to the place

3. **"Failed to sync data files"**

   - Make sure Lune is installed and in your PATH
   - Check that the Lune script path is correct
   - Verify your data files are in the correct format

4. **"Failed to publish place"**
   - Make sure that `rokit` is installed in the PATH as well
   - Check the publishing rights of the account (cookie)
   - Check the Place ID and Universe ID

### Logs

Check the `bot.log` file for detailed error messages and debugging information.

## Dependencies

- **rokit**: Roblox place download/upload
- **Lune**: Data file synchronization
- **discord.py**: For Discord bot functionality
- **aiohttp**: For async HTTP requests

## Contributing

Feel free to submit issues and enhancement requests!
