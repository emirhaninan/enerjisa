#!/usr/bin/env python3
"""
Voltage Spike Monitor - Startup Script
Checks dependencies and starts the application
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask_cors', 
        'telegram',
        'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
        else:
            print(f"✅ {package} is installed")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies!")
            print("   Please run: pip install -r requirements.txt")
            return False
    
    return True

def check_telegram_config():
    """Check if Telegram is configured"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or bot_token == 'YOUR_BOT_TOKEN_HERE':
        print("⚠️  Telegram not configured")
        print("   Set TELEGRAM_BOT_TOKEN environment variable")
        return False
    
    if not chat_id or chat_id == 'YOUR_CHAT_ID_HERE':
        print("⚠️  Telegram not configured")
        print("   Set TELEGRAM_CHAT_ID environment variable")
        return False
    
    print("✅ Telegram configured")
    return True

def print_banner():
    """Print application banner"""
    banner = """
    ⚡ Voltage Spike Monitor ⚡
    ============================
    
    A beautiful Apple-style website that monitors voltage spikes
    and sends Telegram notifications when critical levels are detected.
    
    """
    print(banner)

def print_instructions():
    """Print setup instructions"""
    instructions = """
    📱 Telegram Setup (Optional):
    
    1. Create a bot:
       - Open Telegram and search for @BotFather
       - Send /newbot command
       - Follow instructions to create your bot
       - Save the bot token
    
    2. Get your chat ID:
       - Search for @userinfobot in Telegram
       - Send any message to get your chat ID
    
    3. Set environment variables:
       Windows:  set TELEGRAM_BOT_TOKEN=your_token_here
       macOS/Linux: export TELEGRAM_BOT_TOKEN=your_token_here
       
       Windows:  set TELEGRAM_CHAT_ID=your_chat_id_here
       macOS/Linux: export TELEGRAM_CHAT_ID=your_chat_id_here
    
    🌐 Access the application at: http://localhost:5000
    """
    print(instructions)

def main():
    """Main startup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Telegram configuration
    telegram_configured = check_telegram_config()
    
    print("\n" + "="*50)
    print("🚀 Starting Voltage Spike Monitor...")
    print("="*50)
    
    if not telegram_configured:
        print("\n⚠️  Running without Telegram notifications")
        print("   Alerts will be logged to console only")
    
    print("\n🌐 Starting web server...")
    print("📊 Frontend will be available at: http://localhost:5000")
    print("🔧 API endpoints:")
    print("   - GET  /api/status")
    print("   - POST /api/telegram-alert")
    print("   - GET  /api/test-telegram")
    print("   - GET  /api/voltage-data")
    
    if not telegram_configured:
        print_instructions()
    
    print("\n" + "="*50)
    print("Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Voltage Spike Monitor...")
        print("Thanks for using our application! ⚡")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 