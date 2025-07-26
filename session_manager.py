#!/usr/bin/env python3
"""
Session Management Utilities for SONALI Music Bot
Helps diagnose and fix session-related issues
"""

import asyncio
import os
import sys
import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration"""
    try:
        import config
        return config
    except ImportError as e:
        logger.error(f"Failed to load config: {e}")
        return None

def validate_session_string(session_string):
    """Validate session string format"""
    if not session_string:
        return False, "Empty session string"
    
    if len(session_string) < 50:
        return False, "Session string too short"
    
    # Basic validation - session strings should be base64-like
    try:
        import base64
        # Try to decode as base64 (most session strings are base64 encoded)
        base64.b64decode(session_string + "==")  # Add padding
        return True, "Valid format"
    except Exception:
        # If not base64, check if it's a valid string format
        if all(c.isalnum() or c in "+-/=" for c in session_string):
            return True, "Valid format"
        return False, "Invalid character in session string"

async def test_session_connection(session_string, api_id, api_hash, session_name="test"):
    """Test if a session string can connect"""
    try:
        from pyrogram import Client
        
        client = Client(
            name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            session_string=session_string,
            no_updates=True
        )
        
        logger.info(f"Testing session: {session_name}")
        
        await client.start()
        me = await client.get_me()
        await client.stop()
        
        return True, {
            "id": me.id,
            "username": me.username,
            "first_name": me.first_name,
            "phone_number": me.phone_number
        }
        
    except Exception as e:
        return False, str(e)

def analyze_session_strings():
    """Analyze all session strings in config"""
    config = load_config()
    if not config:
        return
    
    sessions = [
        ("STRING1", getattr(config, "STRING1", None)),
        ("STRING2", getattr(config, "STRING2", None)),
        ("STRING3", getattr(config, "STRING3", None)),
        ("STRING4", getattr(config, "STRING4", None)),
        ("STRING5", getattr(config, "STRING5", None))
    ]
    
    print("🔍 Analyzing Session Strings...")
    print("=" * 50)
    
    valid_sessions = 0
    total_sessions = 0
    
    for name, session_string in sessions:
        if session_string:
            total_sessions += 1
            is_valid, message = validate_session_string(session_string)
            
            if is_valid:
                print(f"✅ {name}: {message}")
                valid_sessions += 1
            else:
                print(f"❌ {name}: {message}")
        else:
            print(f"⚪ {name}: Not configured")
    
    print(f"\n📊 Summary: {valid_sessions}/{total_sessions} sessions appear valid")
    return sessions

async def test_all_sessions():
    """Test connection for all configured sessions"""
    config = load_config()
    if not config:
        return
    
    sessions = [
        ("STRING1", getattr(config, "STRING1", None)),
        ("STRING2", getattr(config, "STRING2", None)),
        ("STRING3", getattr(config, "STRING3", None)),
        ("STRING4", getattr(config, "STRING4", None)),
        ("STRING5", getattr(config, "STRING5", None))
    ]
    
    print("\n🔗 Testing Session Connections...")
    print("=" * 50)
    
    working_sessions = 0
    results = []
    
    for name, session_string in sessions:
        if session_string:
            try:
                success, result = await test_session_connection(
                    session_string, 
                    config.API_ID, 
                    config.API_HASH, 
                    f"test_{name.lower()}"
                )
                
                if success:
                    print(f"✅ {name}: Connected as @{result.get('username', 'N/A')} ({result.get('first_name', 'N/A')})")
                    working_sessions += 1
                    results.append({"session": name, "status": "OK", "user": result})
                else:
                    print(f"❌ {name}: {result}")
                    results.append({"session": name, "status": "FAILED", "error": result})
                    
            except Exception as e:
                print(f"💥 {name}: Unexpected error - {e}")
                results.append({"session": name, "status": "ERROR", "error": str(e)})
        else:
            results.append({"session": name, "status": "NOT_CONFIGURED"})
    
    print(f"\n📊 Connection Test Summary: {working_sessions} sessions working")
    return results

def clean_session_files():
    """Clean up session files"""
    print("\n🧹 Cleaning Session Files...")
    
    # Session directories created by the userbot
    session_dirs = ["session1", "session2", "session3", "session4", "session5"]
    
    # Session files that might be created
    session_files = [
        "RAUSHANAss1.session", "RAUSHANAss2.session", "RAUSHANAss3.session",
        "RAUSHANAss4.session", "RAUSHANAss5.session"
    ]
    
    cleaned = 0
    
    # Clean directories
    for session_dir in session_dirs:
        path = Path(session_dir)
        if path.exists():
            try:
                import shutil
                shutil.rmtree(path)
                print(f"🗑️ Removed directory: {session_dir}")
                cleaned += 1
            except Exception as e:
                print(f"⚠️ Could not remove {session_dir}: {e}")
    
    # Clean session files
    for session_file in session_files:
        path = Path(session_file)
        if path.exists():
            try:
                path.unlink()
                print(f"🗑️ Removed file: {session_file}")
                cleaned += 1
            except Exception as e:
                print(f"⚠️ Could not remove {session_file}: {e}")
    
    if cleaned == 0:
        print("ℹ️ No session files to clean")
    else:
        print(f"✅ Cleaned {cleaned} session files/directories")

def generate_session_report(test_results):
    """Generate a detailed session report"""
    report = {
        "timestamp": str(asyncio.get_event_loop().time()),
        "session_tests": test_results,
        "recommendations": []
    }
    
    working_count = sum(1 for r in test_results if r.get("status") == "OK")
    total_configured = sum(1 for r in test_results if r.get("status") != "NOT_CONFIGURED")
    
    report["summary"] = {
        "working_sessions": working_count,
        "total_configured": total_configured,
        "success_rate": (working_count / total_configured * 100) if total_configured > 0 else 0
    }
    
    # Generate recommendations
    if working_count == 0:
        report["recommendations"].append("❌ No working sessions found! Check your session strings.")
        report["recommendations"].append("🔧 Generate new session strings using @StringFatherBot")
    elif working_count < total_configured:
        report["recommendations"].append("⚠️ Some sessions are not working")
        report["recommendations"].append("🔧 Regenerate failed session strings")
    else:
        report["recommendations"].append("✅ All configured sessions are working!")
    
    # Save report
    with open("session_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Session report saved to: session_report.json")
    return report

def show_session_tips():
    """Show tips for session management"""
    print("\n💡 Session Management Tips:")
    print("=" * 50)
    print("1. 🔑 Generate session strings using @StringFatherBot on Telegram")
    print("2. ⚠️ Never share your session strings publicly")
    print("3. 🔄 If sessions stop working, regenerate them")
    print("4. 📱 Use different phone numbers for different assistants")
    print("5. 🚫 Avoid using your main account as an assistant")
    print("6. 🔒 Enable 2FA on accounts used for sessions")
    print("7. 📋 Keep backup of working session strings")
    print("8. 🧹 Clear session files when troubleshooting")

async def main():
    """Main session management function"""
    print("🎵 SONALI Music Bot - Session Manager")
    print("=" * 50)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. 🔍 Analyze session strings")
        print("2. 🔗 Test session connections")
        print("3. 🧹 Clean session files")
        print("4. 📄 Generate session report")
        print("5. 💡 Show session tips")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                analyze_session_strings()
            elif choice == "2":
                results = await test_all_sessions()
                generate_session_report(results)
            elif choice == "3":
                clean_session_files()
            elif choice == "4":
                results = await test_all_sessions()
                generate_session_report(results)
            elif choice == "5":
                show_session_tips()
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"💥 Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Session manager stopped by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
