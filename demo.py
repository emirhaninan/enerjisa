#!/usr/bin/env python3
"""
Voltage Spike Monitor - Demo Script
Simulates voltage spikes for testing the system
"""

import time
import random
import requests
import json
from datetime import datetime

def simulate_voltage_spike():
    """Simulate a voltage spike and send it to the API"""
    
    # Simulate different types of voltage events
    events = [
        {"voltage": 295.5, "area": "Istanbul, Kadıköy", "severity": "HIGH"},
        {"voltage": 310.2, "area": "Istanbul, Beşiktaş", "severity": "CRITICAL"},
        {"voltage": 285.8, "area": "Istanbul, Şişli", "severity": "HIGH"},
        {"voltage": 275.3, "area": "Istanbul, Üsküdar", "severity": "MEDIUM"},
        {"voltage": 320.1, "area": "Istanbul, Fatih", "severity": "CRITICAL"}
    ]
    
    event = random.choice(events)
    
    data = {
        "voltage": event["voltage"],
        "area": event["area"],
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/telegram-alert',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Spike simulated: {event['voltage']}V in {event['area']}")
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   Message: {result.get('message', 'No message')}")
        else:
            print(f"❌ Failed to send spike: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask app is running!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def check_server_status():
    """Check if the server is running"""
    try:
        response = requests.get('http://localhost:5000/api/status')
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Server is running")
            print(f"   Status: {status.get('status', 'unknown')}")
            print(f"   Telegram configured: {status.get('telegram_configured', False)}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("   Please start the server first: python start.py")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

def main():
    """Main demo function"""
    print("⚡ Voltage Spike Monitor - Demo Mode")
    print("=" * 40)
    
    # Check if server is running
    if not check_server_status():
        return
    
    print("\n🎯 Demo Options:")
    print("1. Simulate random voltage spikes")
    print("2. Simulate a specific spike")
    print("3. Continuous monitoring simulation")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                print("\n🎲 Simulating random voltage spike...")
                simulate_voltage_spike()
                
            elif choice == "2":
                print("\n📊 Enter voltage spike details:")
                try:
                    voltage = float(input("Voltage (V): "))
                    area = input("Area (default: Istanbul, Kadıköy): ").strip()
                    if not area:
                        area = "Istanbul, Kadıköy"
                    
                    data = {
                        "voltage": voltage,
                        "area": area,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    response = requests.post(
                        'http://localhost:5000/api/telegram-alert',
                        json=data,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"✅ Custom spike sent: {voltage}V in {area}")
                        print(f"   Status: {result.get('status', 'unknown')}")
                    else:
                        print(f"❌ Failed to send spike: {response.status_code}")
                        
                except ValueError:
                    print("❌ Invalid voltage value!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            elif choice == "3":
                print("\n🔄 Starting continuous simulation...")
                print("   Press Ctrl+C to stop")
                
                try:
                    while True:
                        # Random delay between 5-15 seconds
                        delay = random.uniform(5, 15)
                        time.sleep(delay)
                        
                        # 30% chance of spike
                        if random.random() < 0.3:
                            simulate_voltage_spike()
                        else:
                            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Normal voltage levels")
                            
                except KeyboardInterrupt:
                    print("\n⏹️  Continuous simulation stopped")
                    
            elif choice == "4":
                print("👋 Thanks for using the demo!")
                break
                
            else:
                print("❌ Invalid option. Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 