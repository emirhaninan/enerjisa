#!/usr/bin/env python3
"""
Flask Backend for Voltage Spike Monitor
Serves the frontend and handles Telegram notifications
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import csv
from datetime import datetime, timedelta
import random
from telegram_notifier import VoltageSpikeNotifier

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Initialize Telegram notifier
telegram_notifier = None

# Global variable to store CSV data
csv_data = []
current_data_index = 0

def load_csv_data():
    """Load data from dc_current_log.csv"""
    global csv_data
    csv_data = []
    try:
        with open('dc_current_log.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert current to voltage (assuming 220V base with current variations)
                current = float(row['Current (A)'])
                # Simple conversion: voltage = 220 + (current * 100) for demonstration
                # In real scenario, this would be actual voltage measurements
                voltage = 220 + (current * 100)
                csv_data.append({
                    'timestamp': row['Timestamp'],
                    'current': current,
                    'voltage': voltage
                })
        print(f"Loaded {len(csv_data)} data points from CSV")
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        # Fallback to simulated data
        csv_data = []

def get_next_data_point():
    """Get the next data point from CSV, cycling through the data"""
    global current_data_index
    if not csv_data:
        return None
    
    data_point = csv_data[current_data_index]
    current_data_index = (current_data_index + 1) % len(csv_data)
    return data_point

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_file(filename)

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'telegram_configured': telegram_notifier is not None,
        'data_source': 'CSV' if csv_data else 'Simulated'
    })

@app.route('/api/telegram-alert', methods=['POST'])
def telegram_alert():
    try:
        data = request.get_json()
        voltage = data.get('voltage', 0)
        area = data.get('area', 'Unknown Area')
        severity = data.get('severity', 'MEDIUM')
        
        # Send Telegram notification (simulated for now)
        success = True
        print(f"🚨 VOLTAGE SPIKE ALERT (Telegram not configured):")
        print(f"   Voltage: {voltage}V")
        print(f"   Area: {area}")
        print(f"   Severity: {severity}")
        print(f"   Time: {datetime.now().isoformat()}")
        
        return jsonify({
            'success': success,
            'message': 'Alert sent successfully' if success else 'Alert sent in demo mode'
        })
    except Exception as e:
        print(f"Error handling telegram alert: {e}")
        return jsonify({
            'success': False,
            'message': 'Error sending alert'
        }), 500

@app.route('/api/voltage-data')
def get_voltage_data():
    """Get real-time voltage data from CSV"""
    try:
        data_point = get_next_data_point()
        if data_point:
            return jsonify({
                'timestamp': data_point['timestamp'],
                'voltage': data_point['voltage'],
                'current': data_point['current'],
                'success': True
            })
        else:
            # Fallback to simulated data
            voltage = 220 + random.uniform(-10, 10)
            return jsonify({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'voltage': voltage,
                'current': random.uniform(0, 0.5),
                'success': True
            })
    except Exception as e:
        print(f"Error getting voltage data: {e}")
        return jsonify({
            'success': False,
            'message': 'Error retrieving data'
        }), 500

@app.route('/api/csv-data')
def get_csv_data():
    """Get all CSV data for chart initialization"""
    try:
        # Return last 100 data points for chart
        recent_data = csv_data[-100:] if len(csv_data) > 100 else csv_data
        return jsonify({
            'data': recent_data,
            'success': True
        })
    except Exception as e:
        print(f"Error getting CSV data: {e}")
        return jsonify({
            'success': False,
            'message': 'Error retrieving CSV data'
        }), 500

if __name__ == '__main__':
    # Load CSV data on startup
    load_csv_data()
    print("Starting Flask server...")
    print(f"Loaded {len(csv_data)} data points from CSV")
    app.run(debug=True, host='0.0.0.0', port=5000) 