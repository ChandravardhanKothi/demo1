# API Keys Setup Guide

## 🔑 Required API Keys

### 1. OpenWeather API Key

**Purpose**: Weather data and forecasts

**Steps to get it**:
1. Go to https://openweathermap.org/api
2. Click "Sign Up" and create a free account
3. After verification, go to "API Keys" in your account
4. Copy your API key (starts with something like `a1b2c3d4e5f6g7h8i9j0`)

**Free Tier Limits**:
- 1,000 API calls per day
- 60 calls per minute
- Current weather, 5-day forecast, and historical data

### 2. Twilio WhatsApp API

**Purpose**: WhatsApp messaging and voice advisories

**Steps to get it**:
1. Go to https://www.twilio.com/
2. Sign up for a free account
3. Verify your phone number
4. In your Twilio Console Dashboard, you'll find:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token**: `your-auth-token-here`

**WhatsApp Sandbox Setup**:
1. In Twilio Console, go to "Messaging" → "Try it out" → "Send a WhatsApp message"
2. Follow instructions to connect your WhatsApp number to the sandbox
3. Use the sandbox number: `whatsapp:+14155238886`

**Pricing**: 
- Free tier: Limited messages
- Production: ~$0.005 per message

## 🔧 Configuration Steps

### Step 1: Create Environment File
```bash
# Copy the example file
cp backend/env.example backend/.env
```

### Step 2: Edit the .env file
```bash
# Open the file in your editor
nano backend/.env  # or use any text editor
```

### Step 3: Add Your API Keys
```bash
# Replace these values with your actual API keys:

# OpenWeather API
OPENWEATHER_API_KEY=your-actual-openweather-api-key-here

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-actual-twilio-auth-token-here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Security (generate a strong secret key)
SECRET_KEY=your-very-secure-random-secret-key-here

# Database (for local development)
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/agricultural_advisory
```

## 🧪 Testing Your API Keys

### Test OpenWeather API
```bash
# Test in your browser or terminal
curl "http://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
```

### Test Twilio Connection
```bash
# Test with curl
curl -X POST https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID.json \
  -u YOUR_ACCOUNT_SID:YOUR_AUTH_TOKEN
```

## 🚨 Security Best Practices

### ✅ Do:
- Keep your API keys in `.env` file (not committed to git)
- Use different keys for development and production
- Regularly rotate your API keys
- Monitor your API usage

### ❌ Don't:
- Share API keys in code or documentation
- Commit `.env` file to version control
- Use production keys in development
- Hardcode keys in your application

## 🔄 Alternative: Development Without API Keys

If you want to test the system without API keys initially:

### Mock Weather Data
The system will work with mock weather data if no API key is provided.

### Mock WhatsApp
The WhatsApp integration will log messages instead of sending them if Twilio keys are not configured.

### Disease Detection
The ML model will work with dummy predictions if no trained model is available.

## 🚀 Quick Start Without API Keys

You can still run the system and see the interface:

```bash
# Start the system
./setup.sh

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

The system will show placeholder data and you can test the UI/UX before adding real API keys.

## 📞 Support

### OpenWeather Issues
- Documentation: https://openweathermap.org/api
- Support: https://openweathermap.org/help

### Twilio Issues
- Documentation: https://www.twilio.com/docs/whatsapp
- Support: https://support.twilio.com/

### Application Issues
- Check logs: `docker-compose logs -f backend`
- Health check: `curl http://localhost:8000/health`
