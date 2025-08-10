#!/usr/bin/env python3
"""
Voltage Spike Monitor - Telegram Notification System
Sends alerts to Telegram when voltage spikes are detected
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional

# For Telegram bot functionality
try:
    import telegram
except ImportError:
    print("Please install python-telegram-bot: pip install python-telegram-bot")
    exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VoltageSpikeNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize the Telegram notifier
        
        Args:
            bot_token: Your Telegram bot token from BotFather
            chat_id: Your personal chat ID or group chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=bot_token)
        self.last_alert_time = None
        self.alert_cooldown = 300  # 5 minutes between alerts
        
    async def send_voltage_spike_alert(
        self, 
        voltage: float, 
        area: str = "Unknown Area",
        severity: str = "HIGH",
        additional_info: Optional[dict] = None
    ) -> bool:
        """
        Send a formatted voltage spike alert to Telegram
        
        Args:
            voltage: The detected voltage value
            area: The area where the spike was detected
            severity: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
            additional_info: Additional information to include
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        
        # Check cooldown to prevent spam
        if self.last_alert_time:
            time_since_last = (datetime.now() - self.last_alert_time).total_seconds()
            if time_since_last < self.alert_cooldown:
                logger.info(f"Alert cooldown active. Skipping alert. ({time_since_last:.1f}s remaining)")
                return False
        
        # Determine emoji and color based on severity
        severity_config = {
            "LOW": {"emoji": "⚠️", "color": "🟡"},
            "MEDIUM": {"emoji": "⚡", "color": "🟠"},
            "HIGH": {"emoji": "🚨", "color": "🔴"},
            "CRITICAL": {"emoji": "💥", "color": "🔴"}
        }
        
        config = severity_config.get(severity, severity_config["HIGH"])
        
        # Create the alert message
        message = (
            f"{config['emoji']} *VOLTAGE SPIKE ALERT* {config['emoji']}\n\n"
            f"{config['color']} **Severity:** {severity}\n"
            f"⚡ **Voltage:** {voltage:.1f}V\n"
            f"📍 **Area:** {area}\n"
            f"🕐 **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"🚨 **IMMEDIATE ACTION REQUIRED:**\n"
            f"• Turn off sensitive electronics\n"
            f"• Unplug expensive equipment\n"
            f"• Check circuit breakers\n"
            f"• Monitor for additional spikes\n\n"
            f"⚠️ *This is an automated alert from your voltage monitoring system*"
        )
        
        # Add additional information if provided
        if additional_info:
            message += "\n\n📊 **Additional Data:**\n"
            for key, value in additional_info.items():
                message += f"• {key}: {value}\n"
        
        try:
            # Send the message
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            
            self.last_alert_time = datetime.now()
            logger.info(f"Successfully sent voltage spike alert to chat {self.chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
            return False
    
    async def send_system_status(
        self, 
        status: str = "ONLINE",
        voltage: Optional[float] = None,
        uptime: Optional[str] = None
    ) -> bool:
        """
        Send system status updates
        
        Args:
            status: System status (ONLINE, OFFLINE, MAINTENANCE)
            voltage: Current voltage reading
            uptime: System uptime string
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        
        status_emoji = {
            "ONLINE": "🟢",
            "OFFLINE": "🔴", 
            "MAINTENANCE": "🟡"
        }.get(status, "⚪")
        
        message = (
            f"{status_emoji} *SYSTEM STATUS UPDATE*\n\n"
            f"**Status:** {status}\n"
            f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        
        if voltage:
            message += f"**Current Voltage:** {voltage:.1f}V\n"
        
        if uptime:
            message += f"**Uptime:** {uptime}\n"
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logger.info(f"Successfully sent system status update")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send system status: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Test the Telegram bot connection
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            me = await self.bot.get_me()
            logger.info(f"Bot connection successful: @{me.username}")
            return True
        except Exception as e:
            logger.error(f"Bot connection failed: {e}")
            return False

# Example usage and setup
async def main():
    """
    Example usage of the VoltageSpikeNotifier
    """
    
    # Configuration - Replace with your actual values
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
    CHAT_ID = "YOUR_CHAT_ID_HERE"      # Get from @userinfobot
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️  Please configure your bot token and chat ID first!")
        print("\nSetup Instructions:")
        print("1. Message @BotFather on Telegram to create a bot")
        print("2. Get your bot token and replace BOT_TOKEN above")
        print("3. Message @userinfobot to get your chat ID")
        print("4. Replace CHAT_ID above with your chat ID")
        print("5. Install required package: pip install python-telegram-bot")
        return
    
    # Initialize the notifier
    notifier = VoltageSpikeNotifier(BOT_TOKEN, CHAT_ID)
    
    # Test connection
    if await notifier.test_connection():
        print("✅ Bot connection successful!")
        
        # Send a test alert
        print("📤 Sending test voltage spike alert...")
        success = await notifier.send_voltage_spike_alert(
            voltage=295.5,
            area="Istanbul, Kadıköy District",
            severity="HIGH",
            additional_info={
                "Grid Load": "85%",
                "Temperature": "24°C",
                "Humidity": "65%"
            }
        )
        
        if success:
            print("✅ Test alert sent successfully!")
        else:
            print("❌ Failed to send test alert")
    else:
        print("❌ Bot connection failed!")

# Flask/Web API integration example
class WebhookHandler:
    """
    Example webhook handler for receiving voltage data from the frontend
    """
    
    def __init__(self, notifier: VoltageSpikeNotifier):
        self.notifier = notifier
    
    async def handle_voltage_data(self, data: dict):
        """
        Handle incoming voltage data from webhook
        
        Args:
            data: Dictionary containing voltage data
        """
        voltage = data.get('voltage', 0)
        area = data.get('area', 'Unknown Area')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Determine severity based on voltage
        if voltage >= 300:
            severity = "CRITICAL"
        elif voltage >= 280:
            severity = "HIGH"
        elif voltage >= 260:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        
        # Send alert if voltage is concerning
        if voltage > 234:
            await self.notifier.send_voltage_spike_alert(
                voltage=voltage,
                area=area,
                severity=severity,
                additional_info={
                    "Timestamp": timestamp,
                    "Threshold": "234V"
                }
            )

if __name__ == "__main__":
    # Run the example
    asyncio.run(main()) 