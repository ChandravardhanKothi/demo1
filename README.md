# AI-Powered Agricultural Advisory System

A comprehensive platform that helps farmers make data-driven decisions through real-time weather updates, market price information, crop disease detection, and hyperlocal advisories.

## 🌟 Features

- **Weather Dashboard**: Real-time weather data based on location
- **Market Trends**: Current crop prices for selected regions
- **Disease Detection**: AI-powered crop disease classification from images
- **Multi-language Support**: Hindi, Telugu, Tamil, English
- **Voice Advisories**: Text-to-speech conversion for accessibility
- **WhatsApp Integration**: Direct messaging and voice advisories
- **Responsive Web Dashboard**: Modern UI for desktop and mobile

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI/ML         │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (TensorFlow)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   WhatsApp      │    │   Database      │    │   External      │
│   Integration   │    │   (PostgreSQL)  │    │   APIs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis (optional, for caching)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd agricultural-advisory-system
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Database Setup**
```bash
# Create database
createdb agricultural_advisory

# Run migrations
cd backend
python -m alembic upgrade head
```

5. **Environment Variables**
```bash
# Copy example env file
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

6. **Run the Application**
```bash
# Backend (Terminal 1)
cd backend
python main.py

# Frontend (Terminal 2)
cd frontend
npm start
```

## 📁 Project Structure

```
agricultural-advisory-system/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── ml/             # ML models and processing
│   │   └── utils/          # Utility functions
│   ├── alembic/            # Database migrations
│   ├── tests/              # Backend tests
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Frontend utilities
│   └── package.json
├── ml_models/              # Trained ML models
├── docs/                   # Documentation
└── deployment/             # Deployment configurations
```

## 🔧 API Endpoints

### Weather
- `GET /api/weather/current` - Current weather data
- `GET /api/weather/forecast` - Weather forecast

### Market
- `GET /api/market/prices` - Current crop prices
- `GET /api/market/trends` - Price trends

### Disease Detection
- `POST /api/disease/detect` - Upload image for disease detection
- `GET /api/disease/history` - Disease detection history

### Advisory
- `POST /api/advisory/generate` - Generate advisory
- `GET /api/advisory/history` - Advisory history
- `POST /api/advisory/voice` - Generate voice advisory

### WhatsApp
- `POST /api/whatsapp/send` - Send WhatsApp message
- `POST /api/whatsapp/voice` - Send voice message

## 🌐 Supported Languages

- English
- Hindi (हिंदी)
- Telugu (తెలుగు)
- Tamil (தமிழ்)

## 📱 WhatsApp Integration

The system supports sending advisories via WhatsApp including:
- Text messages in multiple languages
- Voice messages (TTS)
- Image attachments
- Interactive buttons for quick responses

## 🔒 Security

- JWT-based authentication
- Input validation and sanitization
- Rate limiting
- CORS configuration
- Environment variable protection

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Manual Deployment
See `deployment/` directory for detailed deployment guides.

## 📊 Monitoring

- Application logs
- Performance metrics
- Error tracking
- User analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please contact the development team.
