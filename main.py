import logging
import sys
import os
from discord_bot import SyncBot
from config import Config

def main():
    """Main entry point for the bot"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Roblox Deploy Bot...")
    
    try:
        bot = SyncBot()
        if not Config.DISCORD_TOKEN:
            logger.error("DISCORD_TOKEN is missing. Check your .env file.")
            sys.exit(1)
        bot.run(Config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
