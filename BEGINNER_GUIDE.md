# 🌾 Agricultural Advisory System - Complete Beginner Guide

## 📖 Table of Contents
1. [What is this system?](#what-is-this-system)
2. [Prerequisites](#prerequisites)
3. [Installation & Setup](#installation--setup)
4. [Getting API Keys](#getting-api-keys)
5. [Running the System](#running-the-system)
6. [Using the System](#using-the-system)
7. [Troubleshooting](#troubleshooting)
8. [Deployment](#deployment)

---

## 🎯 What is this system?

This is an **AI-Powered Agricultural Advisory System** that helps farmers:

- 🤖 **Detect crop diseases** by uploading photos
- 🌤️ **Get weather updates** and forecasts
- 📊 **Check market prices** for crops
- 💬 **Receive advisories** via WhatsApp and web
- 🗣️ **Listen to voice advisories** in multiple languages (English, Hindi, Telugu, Tamil)

**Think of it as a smart assistant for farmers!**

---

## ✅ Prerequisites

### What you need on your computer:

1. **Operating System**: Windows, macOS, or Linux
2. **Docker Desktop** (most important!)
3. **Git** (to download the code)
4. **Internet connection**

### Step-by-step installation:

#### 1. Install Docker Desktop

**For Windows:**
1. Go to: https://www.docker.com/products/docker-desktop/
2. Click "Download for Windows"
3. Run the installer
4. Restart your computer
5. Open Docker Desktop and wait for it to start

**For macOS:**
1. Go to: https://www.docker.com/products/docker-desktop/
2. Click "Download for Mac"
3. Run the installer
4. Drag Docker to Applications folder
5. Open Docker Desktop and wait for it to start

**For Linux (Ubuntu/Debian):**
```bash
# Open terminal and run these commands one by one:
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
# Log out and log back in for changes to take effect
```

#### 2. Install Git

**For Windows:**
1. Go to: https://git-scm.com/download/win
2. Download and install
3. Use default settings

**For macOS:**
```bash
# Open terminal and run:
brew install git
# If you don't have Homebrew, install it first from https://brew.sh
```

**For Linux:**
```bash
sudo apt install git
```

#### 3. Verify Installation

Open terminal/command prompt and run:
```bash
# Check Docker
docker --version
docker-compose --version

# Check Git
git --version
```

You should see version numbers. If you get "command not found", installation didn't work properly.

---

## 🚀 Installation & Setup

### Step 1: Download the Project

```bash
# Open terminal/command prompt and run:
git clone https://github.com/your-repo/agricultural-advisory-system.git
cd agricultural-advisory-system
```

**If you don't have the git repository, create the project folder:**
```bash
mkdir agricultural-advisory-system
cd agricultural-advisory-system
# Copy all the files we created into this folder
```

### Step 2: Check Project Structure

```bash
# List all files and folders
ls -la

# You should see these folders:
# backend/
# frontend/
# deployment/
# ml_models/
# And these files:
# docker-compose.yml
# setup.sh
# README.md
```

### Step 3: Make Setup Script Executable

```bash
# Make the setup script runnable
chmod +x setup.sh

# For Windows users, if chmod doesn't work, that's okay
```

### Step 4: Run the Setup Script

```bash
# This will set up everything automatically
./setup.sh
```

**What this script does:**
- Creates necessary folders
- Sets up environment files
- Downloads required software
- Starts all services

**Expected output:**
```
🌾 Agricultural Advisory System Setup
======================================
[INFO] Checking Docker installation...
[SUCCESS] Docker and Docker Compose are installed
[INFO] Setting up environment files...
[SUCCESS] Created backend/.env file
[INFO] Creating necessary directories...
[SUCCESS] Created necessary directories
[INFO] Setting up Docker environment...
[SUCCESS] Docker environment ready
[INFO] Creating sample ML model...
[SUCCESS] Sample ML model created
[INFO] Starting services with Docker Compose...
[SUCCESS] All services started successfully!

🎉 Setup Complete!
==================

Services Status:
Name                    Command               State           Ports
agricultural_backend    uvicorn main:app ...  Up      0.0.0.0:8000->8000/tcp
agricultural_db         docker-entrypoint.sh  Up      0.0.0.0:5432->5432/tcp
agricultural_frontend   npm start             Up      0.0.0.0:3000->3000/tcp
agricultural_redis      docker-entrypoint.sh  Up      0.0.0.0:6379->6379/tcp

🌐 Application URLs:
  Frontend: http://localhost:3000
  Backend API: http://localhost:8000
  API Documentation: http://localhost:8000/docs
  Database: localhost:5432
  Redis: localhost:6379
```

---

## 🔑 Getting API Keys

### Why do we need API keys?
- **Weather data**: To show real weather information
- **WhatsApp messaging**: To send messages to farmers
- **Security**: To protect your application

### Option 1: Start Without API Keys (Recommended for beginners)

You can run the system without API keys to see how it works:

```bash
# The system will work with sample data
# No API keys needed for basic functionality
```

### Option 2: Get Real API Keys (For full features)

#### Getting OpenWeather API Key (5 minutes):

1. **Go to website:**
   ```
   https://openweathermap.org/api
   ```

2. **Sign up:**
   - Click "Sign Up"
   - Fill in your details
   - Verify your email

3. **Get API Key:**
   - Login to your account
   - Go to "API Keys" section
   - Copy your API key (looks like: `a1b2c3d4e5f6g7h8i9j0`)

#### Getting Twilio WhatsApp API (10 minutes):

1. **Go to website:**
   ```
   https://www.twilio.com/
   ```

2. **Sign up:**
   - Click "Sign Up"
   - Fill in your details
   - Verify your phone number

3. **Get Credentials:**
   - In your Twilio Console Dashboard, find:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token**: `your-auth-token-here`

4. **Setup WhatsApp Sandbox:**
   - Go to "Messaging" → "Try it out" → "Send a WhatsApp message"
   - Follow instructions to connect your WhatsApp
   - Use sandbox number: `whatsapp:+14155238886`

#### Adding API Keys to the System:

```bash
# Open the environment file
nano backend/.env

# Or use any text editor like Notepad, VS Code, etc.
```

**Edit the file and add your keys:**
```bash
# Replace these lines with your actual keys:

# OpenWeather API (replace with your key)
OPENWEATHER_API_KEY=a1b2c3d4e5f6g7h8i9j0

# Twilio WhatsApp (replace with your credentials)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-actual-twilio-auth-token-here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Security (generate a random string)
SECRET_KEY=my-super-secret-key-12345

# Database (keep as is for local development)
DATABASE_URL=postgresql://postgres:postgres123@db:5432/agricultural_advisory
```

**Save the file and restart services:**
```bash
# Restart to apply new settings
docker-compose restart backend
```

---

## 🏃‍♂️ Running the System

### Starting the System

```bash
# Start all services
docker-compose up -d

# Check if everything is running
docker-compose ps
```

**Expected output:**
```
Name                    Command               State           Ports
agricultural_backend    uvicorn main:app ...  Up      0.0.0.0:8000->8000/tcp
agricultural_db         docker-entrypoint.sh  Up      0.0.0.0:5432->5432/tcp
agricultural_frontend   npm start             Up      0.0.0.0:3000->3000/tcp
agricultural_redis      docker-entrypoint.sh  Up      0.0.0.0:6379->6379/tcp
```

### Accessing the System

**Open your web browser and go to:**
```
http://localhost:3000
```

**You should see the Agricultural Advisory System dashboard!**

### Other Useful URLs:

```
Frontend (Main App):     http://localhost:3000
Backend API:             http://localhost:8000
API Documentation:       http://localhost:8000/docs
Health Check:            http://localhost:8000/health
```

### Stopping the System

```bash
# Stop all services
docker-compose down

# Stop and remove all data (if you want to start fresh)
docker-compose down -v
```

### Viewing Logs

```bash
# See all logs
docker-compose logs

# See logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f backend
```

---

## 🎮 Using the System

### 1. Web Dashboard

**Access:** http://localhost:3000

**Features you can try:**

#### Disease Detection:
1. Click "Disease Detection" in the menu
2. Click "Upload Image" area
3. Select a crop image (JPG/PNG)
4. Choose crop type (rice, wheat, etc.)
5. Click "Analyze Image"
6. See the disease detection results!

#### Weather Information:
1. Click "Weather" in the menu
2. Enter your location coordinates
3. See current weather and forecast

#### Market Prices:
1. Click "Market Prices" in the menu
2. Select your region and crop
3. View price trends

### 2. API Testing

**Access:** http://localhost:8000/docs

**Try these endpoints:**

#### Test Disease Detection:
```bash
# Test in terminal
curl -X POST "http://localhost:8000/api/disease/detect" \
  -F "file=@path/to/your/image.jpg" \
  -F "crop_type=rice"
```

#### Test Weather API:
```bash
# Test weather endpoint
curl "http://localhost:8000/api/weather/current?latitude=17.3850&longitude=78.4867"
```

#### Test Health Check:
```bash
# Check if system is working
curl "http://localhost:8000/health"
```

### 3. WhatsApp Integration (If you have Twilio keys)

**Test WhatsApp messaging:**
```bash
# Send a test message (replace with your user_id)
curl -X POST "http://localhost:8000/api/whatsapp/send" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "Hello! This is a test advisory from the Agricultural Advisory System.",
    "language": "en"
  }'
```

---

## 🔧 Troubleshooting

### Common Problems and Solutions

#### Problem 1: "Docker not found" error

**Solution:**
```bash
# Check if Docker is running
docker --version

# If not installed, install Docker Desktop from:
# https://www.docker.com/products/docker-desktop/
```

#### Problem 2: "Port already in use" error

**Solution:**
```bash
# Stop all services
docker-compose down

# Check what's using the ports
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# Kill processes using those ports (replace PID with actual process ID)
kill -9 PID

# Start services again
docker-compose up -d
```

#### Problem 3: "Cannot connect to database" error

**Solution:**
```bash
# Restart database
docker-compose restart db

# Wait for database to start
sleep 10

# Check database logs
docker-compose logs db

# Restart all services
docker-compose restart
```

#### Problem 4: Frontend not loading

**Solution:**
```bash
# Check frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend

# If still not working, rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

#### Problem 5: API not responding

**Solution:**
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Test API directly
curl http://localhost:8000/health
```

#### Problem 6: ML model not working

**Solution:**
```bash
# Check if model file exists
ls -la ml_models/

# If missing, create sample model
cd ml_models
python3 -c "
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.save('crop_disease_model.h5')
print('Model created successfully!')
"
cd ..
```

### Getting Help

#### Check System Status:
```bash
# Check all services
docker-compose ps

# Check resource usage
docker stats

# Check system logs
docker-compose logs --tail=50
```

#### Reset Everything:
```bash
# Stop and remove everything
docker-compose down -v

# Remove all images (optional)
docker system prune -a

# Start fresh
./setup.sh
```

---

## 🚀 Deployment

### Local Development (What we've been doing)
- ✅ Perfect for learning and testing
- ✅ Runs on your computer
- ✅ Uses sample/mock data
- ✅ No external dependencies

### Production Deployment (For real users)

#### Option 1: Cloud Deployment (Recommended)

**Using AWS/GCP/Azure:**

1. **Create a cloud server:**
   ```bash
   # Example for AWS EC2
   # Launch Ubuntu 20.04 instance
   # Minimum requirements: 2GB RAM, 2 CPU cores
   ```

2. **Connect to your server:**
   ```bash
   # SSH into your server
   ssh -i your-key.pem ubuntu@your-server-ip
   ```

3. **Install Docker on server:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   sudo apt install docker.io docker-compose -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ubuntu
   ```

4. **Upload your project:**
   ```bash
   # On your local computer, upload files
   scp -r agricultural-advisory-system ubuntu@your-server-ip:~/
   ```

5. **Run on server:**
   ```bash
   # SSH into server
   ssh ubuntu@your-server-ip
   
   # Go to project directory
   cd agricultural-advisory-system
   
   # Set up environment
   ./setup.sh
   ```

6. **Configure domain (optional):**
   ```bash
   # Edit nginx configuration
   nano deployment/nginx.conf
   
   # Replace localhost with your domain
   server_name your-domain.com;
   ```

#### Option 2: VPS Deployment

**Using DigitalOcean/Linode/Vultr:**

1. **Create VPS:**
   - Choose Ubuntu 20.04
   - Minimum: 2GB RAM, 2 CPU cores
   - Get server IP address

2. **Follow same steps as cloud deployment above**

#### Option 3: Docker Hosting

**Using services like:**
- **Railway**: https://railway.app/
- **Render**: https://render.com/
- **Heroku**: https://heroku.com/

**Steps:**
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### Production Configuration

#### Environment Variables for Production:
```bash
# Production .env file
DATABASE_URL=postgresql://user:password@prod-db:5432/agricultural_advisory
SECRET_KEY=your-very-secure-production-secret-key
OPENWEATHER_API_KEY=your-production-openweather-key
TWILIO_ACCOUNT_SID=your-production-twilio-sid
TWILIO_AUTH_TOKEN=your-production-twilio-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+your-production-number

# Production settings
LOG_LEVEL=WARNING
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

#### SSL Certificate (for HTTPS):
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Monitoring and Maintenance

#### Health Checks:
```bash
# Check if services are running
docker-compose ps

# Check logs
docker-compose logs -f

# Check system resources
docker stats
```

#### Backup Database:
```bash
# Create backup
docker-compose exec db pg_dump -U postgres agricultural_advisory > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres agricultural_advisory < backup.sql
```

#### Update System:
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 📚 Additional Resources

### Learning Resources:
- **Docker Tutorial**: https://docs.docker.com/get-started/
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **React Tutorial**: https://reactjs.org/tutorial/tutorial.html
- **PostgreSQL Tutorial**: https://www.postgresql.org/docs/current/tutorial.html

### Useful Commands Reference:

#### Docker Commands:
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Rebuild service
docker-compose build backend

# Check status
docker-compose ps
```

#### System Commands:
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check running processes
ps aux

# Check network connections
netstat -tulpn
```

#### Git Commands:
```bash
# Clone repository
git clone <repository-url>

# Check status
git status

# Pull latest changes
git pull

# Commit changes
git add .
git commit -m "Your message"
git push
```

---

## 🎉 Congratulations!

You've successfully set up and deployed an AI-powered Agricultural Advisory System! 

### What you've accomplished:
- ✅ Set up a complete full-stack application
- ✅ Integrated AI/ML for disease detection
- ✅ Connected weather and market data APIs
- ✅ Implemented WhatsApp messaging
- ✅ Created a multi-language voice system
- ✅ Deployed to production (if you followed deployment steps)

### Next Steps:
1. **Test all features** thoroughly
2. **Add real API keys** for production use
3. **Customize** for your specific region/crops
4. **Train better ML models** with local data
5. **Add more features** like IoT sensor integration
6. **Scale up** for more users

### Need Help?
- Check the logs: `docker-compose logs -f`
- Restart services: `docker-compose restart`
- Reset everything: `docker-compose down -v && ./setup.sh`
- Check documentation: `README.md` and `DEVELOPMENT_GUIDE.md`

**Happy Farming! 🌾🚜**
