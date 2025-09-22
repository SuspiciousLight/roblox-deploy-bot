import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_rokit():
    """Install rokit for Roblox operations"""
    print("Installing rokit...")
    try:
        subprocess.check_call(["cargo", "install", "rokit"])
        print("✅ rokit installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install rokit. Please install it manually:")
        print("   cargo install rokit")
    except FileNotFoundError:
        print("❌ Cargo not found. Please install Rust first:")
        print("   https://rustup.rs/")

def install_lune():
    """Install Lune for data syncing"""
    print("Installing Lune...")
    try:
        result = subprocess.run(["lune", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Lune is already installed")
            return
        
        subprocess.check_call(["cargo", "install", "lune"])
        print("✅ Lune installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Lune. Please install it manually:")
        print("   cargo install lune")
    except FileNotFoundError:
        print("❌ Cargo not found. Please install Rust first:")
        print("   https://rustup.rs/")

def create_env_file():
    """Create .env file from example"""
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            with open('env_example.txt', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ Created .env file from example")
            print("⚠️  Please edit .env with your actual configuration values")
        else:
            print("❌ env_example.txt not found")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Roblox Deploy Bot...")
    
    # Install Python requirements
    install_requirements()
    
    # Install external tools
    install_rokit()
    install_lune()
    
    # Create environment file
    create_env_file()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Set up your Discord bot and get the token")
    print("3. Get your GitHub token and repository info")
    print("4. Get your Roblox cookie and place/universe IDs")
    print("5. Run: python main.py")

if __name__ == "__main__":
    main()
