import aiohttp
import asyncio
import os
import subprocess
from config import Config

class RobloxClient:
    def __init__(self):
        self.cookie = Config.ROBLOX_COOKIE
        self.place_id = Config.PLACE_ID
        self.universe_id = Config.UNIVERSE_ID
        self.temp_dir = Config.TEMP_DIR
        self.place_file_path = Config.PLACE_FILE_PATH
        self.data_files_dir = Config.DATA_FILES_DIR
        self.lune_script_path = Config.LUNE_SCRIPT_PATH
    
    async def download_place_file(self):
        """Download the latest place file from Roblox using Open Cloud API"""
        os.makedirs(self.temp_dir, exist_ok=True)
        
        try:
            cmd = [
                "rokit", "download", 
                "--place-id", str(self.place_id),
                "--output", self.place_file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to download place file: {e.stderr}")
        except FileNotFoundError:
            raise Exception("rokit not found. Please install rokit: cargo install rokit")
    
    async def sync_data_files(self):
        """Use Lune to sync data files into the place file"""
        if not os.path.exists(self.lune_script_path):
            raise Exception(f"Lune script not found at {self.lune_script_path}")
        
        if not os.path.exists(self.data_files_dir):
            raise Exception(f"Data files directory not found at {self.data_files_dir}")
        
        cmd = [
            "lune", "run", self.lune_script_path,
            "--place-file", self.place_file_path,
            "--data-dir", self.data_files_dir
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to sync data files: {e.stderr}")
    
    async def publish_place(self):
        """Publish the updated place file to Roblox using rokit"""
        if not os.path.exists(self.place_file_path):
            raise Exception("Place file not found")
        
        try:
            cmd = [
                "rokit", "publish",
                "--place-id", str(self.place_id),
                "--file", self.place_file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to publish place: {e.stderr}")
        except FileNotFoundError:
            raise Exception("rokit not found. Please install rokit: cargo install rokit")
    
    async def get_place_info(self):
        """Get information about the current place using Roblox API"""
        async with aiohttp.ClientSession() as session:
            url = f"https://games.roblox.com/v1/games?universeIds={self.universe_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('data'):
                        return data['data'][0]
                raise Exception(f"Failed to get place info: {response.status}")
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
