#!/usr/bin/env python3
"""
Enhanced startup script for SONALI Music Bot
Includes network diagnostics and connection retry logic
"""

import asyncio
import sys
import time
import subprocess
import socket
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('startup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_network_connectivity():
    """Check basic network connectivity"""
    try:
        # Check internet connectivity
        socket.create_connection(("8.8.8.8", 53), timeout=10)
        logger.info("✅ Internet connectivity: OK")
        return True
    except (socket.error, socket.timeout):
        logger.error("❌ Internet connectivity: FAILED")
        return False

def check_telegram_api():
    """Check Telegram API connectivity"""
    try:
        socket.create_connection(("api.telegram.org", 443), timeout=10)
        logger.info("✅ Telegram API connectivity: OK")
        return True
    except (socket.error, socket.timeout):
        logger.error("❌ Telegram API connectivity: FAILED")
        return False

def check_environment():
    """Check required environment variables and files"""
    required_files = [
        "config.py",
        "SONALI/__init__.py",
        "SONALI/core/userbot.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"❌ Missing required files: {missing_files}")
        return False
    
    logger.info("✅ Required files: OK")
    return True

def clear_session_files():
    """Clear potentially corrupted session files"""
    session_dirs = ["session1", "session2", "session3", "session4", "session5"]
    cleared = 0
    
    for session_dir in session_dirs:
        path = Path(session_dir)
        if path.exists():
            try:
                import shutil
                shutil.rmtree(path)
                cleared += 1
                logger.info(f"🧹 Cleared session directory: {session_dir}")
            except Exception as e:
                logger.warning(f"⚠️ Could not clear {session_dir}: {e}")
    
    if cleared > 0:
        logger.info(f"🧹 Cleared {cleared} session directories")

async def start_bot_with_retry(max_retries=3):
    """Start the bot with retry logic"""
    for attempt in range(1, max_retries + 1):
        logger.info(f"🚀 Starting bot (attempt {attempt}/{max_retries})...")
        
        try:
            # Import and start the bot
            from SONALI import app, userbot
            
            logger.info("📱 Starting main bot...")
            await app.start()
            logger.info("✅ Main bot started successfully")
            
            logger.info("👥 Starting assistants...")
            await userbot.start()
            logger.info("✅ Assistants started successfully")
            
            logger.info("🎵 Bot is now running!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Attempt {attempt} failed: {e}")
            
            if attempt < max_retries:
                wait_time = attempt * 10  # Exponential backoff
                logger.info(f"⏳ Waiting {wait_time}s before retry...")
                await asyncio.sleep(wait_time)
                
                # Clear sessions on retry
                if attempt > 1:
                    logger.info("🧹 Clearing session files for retry...")
                    clear_session_files()
            else:
                logger.error("💥 All startup attempts failed!")
                return False
    
    return False

async def main():
    """Main startup function"""
    logger.info("=" * 50)
    logger.info("🎵 SONALI Music Bot Startup")
    logger.info("=" * 50)
    
    # Pre-flight checks
    logger.info("🔍 Running pre-flight checks...")
    
    checks = [
        ("Network connectivity", check_network_connectivity),
        ("Telegram API", check_telegram_api),
        ("Environment", check_environment)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
    
    if not all_passed:
        logger.error("💥 Pre-flight checks failed! Please fix the issues above.")
        sys.exit(1)
    
    logger.info("✅ All pre-flight checks passed!")
    
    # Start the bot
    success = await start_bot_with_retry()
    
    if success:
        logger.info("🎉 Bot started successfully!")
        # Keep the bot running
        await asyncio.Event().wait()
    else:
        logger.error("💥 Failed to start bot after all retries")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)
