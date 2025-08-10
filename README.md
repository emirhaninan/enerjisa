# ⚡ Voltage Spike Monitor

A beautiful, Apple-style minimalistic website with flashy animations that monitors voltage spikes and sends Telegram notifications when critical levels are detected.

![Voltage Monitor Demo](https://img.shields.io/badge/Status-Demo%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey)
![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-blue)

## 🌟 Features

### Frontend (Apple-Style Design)
- **Minimalistic Interface**: Clean, modern design inspired by Apple's aesthetic
- **Real-time Monitoring**: Live voltage graph with smooth animations
- **Flashy Animations**: GSAP-powered animations for voltage spikes
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Dark Theme**: Professional dark interface with glassmorphism effects
- **Interactive Elements**: Hover effects and smooth transitions

### Backend (Python/Flask)
- **Real-time Data Processing**: Handles voltage data and spike detection
- **Telegram Integration**: Sends instant notifications to your phone
- **RESTful API**: Clean API endpoints for data exchange
- **Error Handling**: Robust error handling and logging
- **Configurable Alerts**: Customizable voltage thresholds and cooldowns

### Telegram Notifications
- **Instant Alerts**: Get notified immediately when voltage spikes occur
- **Rich Formatting**: Beautifully formatted messages with emojis and details
- **Severity Levels**: Different alert levels based on voltage magnitude
- **Cooldown System**: Prevents spam notifications
- **Test Functionality**: Easy testing of notification system

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd voltage-spike-monitor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Telegram Bot

#### Step 1: Create a Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Save the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Step 2: Get Your Chat ID
1. Search for `@userinfobot` in Telegram
2. Send any message to get your chat ID
3. Save the chat ID (looks like: `123456789`)

#### Step 3: Set Environment Variables

**Windows:**
```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
```

**macOS/Linux:**
```bash
export TELEGRAM_BOT_TOKEN=your_bot_token_here
export TELEGRAM_CHAT_ID=your_chat_id_here
```

### 4. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 📱 Telegram Setup Guide

### Creating Your Bot

1. **Start BotFather**: Open Telegram and search for `@BotFather`
2. **Create New Bot**: Send `/newbot`
3. **Choose Name**: Enter a name for your bot (e.g., "Voltage Monitor")
4. **Choose Username**: Enter a unique username ending with 'bot' (e.g., "voltage_monitor_bot")
5. **Get Token**: BotFather will give you a token - save it!

### Getting Your Chat ID

1. **Find UserInfoBot**: Search for `@userinfobot` in Telegram
2. **Send Message**: Send any message to the bot
3. **Get ID**: The bot will reply with your chat ID

### Testing Your Setup

Once configured, you can test the Telegram integration:

```bash
curl http://localhost:5000/api/test-telegram
```

## 🎨 Customization

### Frontend Customization

#### Colors and Styling
Edit `style.css` to customize:
- Color scheme
- Animation timing
- Layout dimensions
- Typography

#### Animation Effects
Modify `app.js` to adjust:
- Spike detection frequency
- Animation intensity
- Chart behavior
- Alert thresholds

### Backend Customization

#### Voltage Thresholds
Edit `telegram_notifier.py` to change:
```python
# Voltage severity levels
if voltage >= 300:
    severity = "CRITICAL"
elif voltage >= 280:
    severity = "HIGH"
elif voltage >= 260:
    severity = "MEDIUM"
else:
    severity = "LOW"
```

#### Alert Cooldown
Adjust the cooldown period in `telegram_notifier.py`:
```python
self.alert_cooldown = 300  # 5 minutes between alerts
```

## 🔧 API Endpoints

### Frontend Routes
- `GET /` - Main application interface
- `GET /static/*` - Static files (CSS, JS, images)

### Backend API
- `GET /api/status` - System status and configuration
- `POST /api/telegram-alert` - Send voltage spike alert
- `GET /api/test-telegram` - Test Telegram integration
- `GET /api/voltage-data` - Get simulated voltage data

### Example API Usage

#### Send Alert
```bash
curl -X POST http://localhost:5000/api/telegram-alert \
  -H "Content-Type: application/json" \
  -d '{
    "voltage": 295.5,
    "area": "Istanbul, Kadıköy",
    "timestamp": "2024-01-15T14:30:00Z"
  }'
```

#### Check Status
```bash
curl http://localhost:5000/api/status
```

## 🎯 Features in Detail

### Real-time Monitoring
- **Live Updates**: Voltage data updates every 200ms
- **Smooth Animations**: Chart.js with GSAP for fluid animations
- **Spike Detection**: Automatic detection of voltage spikes
- **Visual Feedback**: Color changes and animations during spikes

### Alert System
- **Instant Notifications**: Telegram messages sent immediately
- **Rich Content**: Formatted messages with severity levels
- **Actionable Information**: Clear instructions for users
- **Spam Prevention**: Cooldown system prevents notification spam

### User Interface
- **Apple-Style Design**: Clean, minimalistic interface
- **Glassmorphism Effects**: Modern blur and transparency effects
- **Responsive Layout**: Works on all screen sizes
- **Interactive Elements**: Hover effects and smooth transitions

## 🛠️ Development

### Project Structure
```
voltage-spike-monitor/
├── index.html          # Main HTML file
├── style.css           # Apple-style CSS with animations
├── app.js              # Frontend JavaScript with Chart.js and GSAP
├── app.py              # Flask backend server
├── telegram_notifier.py # Telegram notification system
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js for real-time data visualization
- **Animations**: GSAP (GreenSock) for smooth animations
- **Backend**: Python Flask for API and server
- **Notifications**: Telegram Bot API
- **Styling**: Custom CSS with Apple-inspired design

### Browser Support
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🔒 Security Considerations

- **Environment Variables**: Store sensitive data (bot tokens) in environment variables
- **Input Validation**: All API inputs are validated
- **Error Handling**: Comprehensive error handling prevents crashes
- **Rate Limiting**: Built-in cooldown prevents spam

## 🚨 Troubleshooting

### Common Issues

#### Telegram Notifications Not Working
1. Check bot token and chat ID are correct
2. Ensure bot is not blocked
3. Verify internet connection
4. Check console logs for errors

#### Frontend Not Loading
1. Ensure Flask server is running
2. Check browser console for JavaScript errors
3. Verify all static files are accessible

#### Chart Not Displaying
1. Check Chart.js CDN is accessible
2. Verify canvas element exists
3. Check JavaScript console for errors

### Debug Mode
Run with debug enabled:
```bash
export FLASK_ENV=development
python app.py
```

## 📈 Future Enhancements

- **Database Integration**: Store historical voltage data
- **Multiple Areas**: Monitor multiple locations simultaneously
- **Advanced Analytics**: Trend analysis and predictions
- **Mobile App**: Native mobile application
- **Email Notifications**: Additional notification methods
- **WebSocket Support**: Real-time bidirectional communication
- **Machine Learning**: Predictive voltage spike detection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Chart.js** for beautiful data visualization
- **GSAP** for smooth animations
- **Telegram Bot API** for instant notifications
- **Apple Design Guidelines** for UI inspiration

---

**⚡ Stay safe and monitor your voltage! ⚡** 