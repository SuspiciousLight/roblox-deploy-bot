import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = int(os.getenv('GUILD_ID', 0))
    
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_REPO = os.getenv('GITHUB_REPO') 
    GITHUB_BRANCH = os.getenv('GITHUB_BRANCH', 'main')
    
    ROBLOX_API_KEY = os.getenv('ROBLOX_API_KEY')
    PLACE_ID = int(os.getenv('PLACE_ID', 0))
    UNIVERSE_ID = int(os.getenv('UNIVERSE_ID', 0))
    
    TEMP_DIR = os.getenv('TEMP_DIR', './temp')
    PLACE_FILE_PATH = os.path.join(TEMP_DIR, 'place.rbxl')
    DATA_FILES_DIR = os.path.join(TEMP_DIR, 'data_files')
    
    LUNE_SCRIPT_PATH = os.getenv('LUNE_SCRIPT_PATH', './lune_sync.luau')
    
    ALLOWED_ROLES = os.getenv('ALLOWED_ROLES', '').split(',')  
    ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',')  
