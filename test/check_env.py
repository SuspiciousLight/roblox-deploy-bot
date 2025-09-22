import json, os
from config import Config

def mask(s):
    if not s:
        return None
    return s[:4] + '...' + s[-4:] if len(s) > 8 else s

report = {
  'DISCORD_TOKEN': mask(Config.DISCORD_TOKEN),
  'GUILD_ID': Config.GUILD_ID,
  'GITHUB_TOKEN': mask(Config.GITHUB_TOKEN),
  'GITHUB_REPO': Config.GITHUB_REPO,
  'GITHUB_BRANCH': Config.GITHUB_BRANCH,
  'ROBLOX_COOKIE': mask(Config.ROBLOX_COOKIE),
  'PLACE_ID': Config.PLACE_ID,
  'UNIVERSE_ID': Config.UNIVERSE_ID,
  'LUNE_SCRIPT_PATH': Config.LUNE_SCRIPT_PATH,
  'TEMP_DIR': Config.TEMP_DIR,
  'ALLOWED_USERS': [u for u in Config.ALLOWED_USERS if u],
  'ALLOWED_ROLES': [r for r in Config.ALLOWED_ROLES if r],
  'exists': {
    'LUNE_SCRIPT_PATH_exists': os.path.exists(Config.LUNE_SCRIPT_PATH),
    'TEMP_DIR_exists': os.path.exists(Config.TEMP_DIR),
  },
  'validations': {
    'discord_token_present': bool(Config.DISCORD_TOKEN),
    'guild_id_positive': isinstance(Config.GUILD_ID, int) and Config.GUILD_ID > 0,
    'github_token_present': bool(Config.GITHUB_TOKEN),
    'github_repo_format_ok': isinstance(Config.GITHUB_REPO, str) and '/' in (Config.GITHUB_REPO or ''),
    'github_branch_present': bool(Config.GITHUB_BRANCH),
    'roblox_cookie_present': bool(Config.ROBLOX_COOKIE),
    'place_id_positive': isinstance(Config.PLACE_ID, int) and Config.PLACE_ID > 0,
    'universe_id_positive': isinstance(Config.UNIVERSE_ID, int) and Config.UNIVERSE_ID > 0,
    'lune_script_exists': os.path.exists(Config.LUNE_SCRIPT_PATH),
  }
}
print(json.dumps(report, ensure_ascii=False, indent=2))
