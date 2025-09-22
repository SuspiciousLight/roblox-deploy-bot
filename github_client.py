import aiohttp
import asyncio
import os
import zipfile
from config import Config

class GitHubClient:
    def __init__(self):
        self.token = Config.GITHUB_TOKEN
        self.repo = Config.GITHUB_REPO
        self.branch = Config.GITHUB_BRANCH
        self.base_url = f"https://api.github.com/repos/{self.repo}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def get_latest_commit(self, branch: str = None):
        """Get the latest commit from the specified branch.

        If branch is not provided, uses the default branch from config.
        """
        async with aiohttp.ClientSession() as session:
            branch_to_use = branch or self.branch
            url = f"{self.base_url}/commits/{branch_to_use}"
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to get latest commit: {response.status}")
    
    async def download_repository(self, output_path, branch: str = None):
        """Download the repository as a ZIP file for the given branch.

        If branch is not provided, uses the default branch from config.
        """
        async with aiohttp.ClientSession() as session:
            branch_to_use = branch or self.branch
            url = f"{self.base_url}/zipball/{branch_to_use}"
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    output_dir = os.path.dirname(output_path)
                    if output_dir:
                        os.makedirs(output_dir, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                    return True
                else:
                    raise Exception(f"Failed to download repository: {response.status}")
    
    async def extract_data_files(self, zip_path, extract_to):
        """Extract data files from the downloaded repository"""
        os.makedirs(extract_to, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            members = zip_ref.namelist()
            root_dir = members[0] if members else ""
            
            data_patterns = ['*.json', '*.lua', '*.luau', '*.txt', '*.csv']
            
            for member in members:
                if any(member.endswith(pattern.replace('*', '')) for pattern in data_patterns):
                    relative_path = member[len(root_dir):] if member.startswith(root_dir) else member
                    if relative_path: 
                        zip_ref.extract(member, extract_to)
                        old_path = os.path.join(extract_to, member)
                        new_path = os.path.join(extract_to, relative_path)
                        if old_path != new_path:
                            os.makedirs(os.path.dirname(new_path), exist_ok=True)
                            os.rename(old_path, new_path)
                            try:
                                os.rmdir(os.path.dirname(old_path))
                            except OSError:
                                pass 
    
    async def get_file_contents(self, file_path):
        """Get the contents of a specific file from the repository"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/contents/{file_path}"
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    import base64
                    return base64.b64decode(data['content']).decode('utf-8')
                else:
                    raise Exception(f"Failed to get file contents: {response.status}")
