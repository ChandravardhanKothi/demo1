# Agricultural Advisory System - Development Guide

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.9+ (for local development)
- PostgreSQL 12+ (for local development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd agricultural-advisory-system
```

### 2. Environment Configuration
```bash
# Copy environment files
cp backend/env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit configuration files with your API keys
# - OpenWeather API key for weather data
# - Twilio credentials for WhatsApp integration
```

### 3. Docker Development (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI/ML         │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (TensorFlow)  │
│   Port: 3000    │    │   Port: 8000    │    │   Models        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   WhatsApp      │    │   Database      │    │   External      │
│   Integration   │    │   (PostgreSQL)  │    │   APIs          │
│   (Twilio)      │    │   Port: 5432    │    │   (Weather)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

1. **User Uploads Image** → Frontend → Backend → ML Model → Disease Detection
2. **Weather Request** → Backend → OpenWeather API → Database → Frontend
3. **Advisory Generation** → Backend → TTS Service → WhatsApp API → User
4. **Market Data** → External API → Backend → Database → Frontend

## 📁 Project Structure

```
agricultural-advisory-system/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API Routes
│   │   │   ├── disease.py     # Disease detection endpoints
│   │   │   ├── weather.py     # Weather data endpoints
│   │   │   └── whatsapp.py    # WhatsApp integration
│   │   ├── core/              # Core configurations
│   │   │   ├── config.py      # Settings and environment
│   │   │   └── database.py    # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic services
│   │   │   └── tts_service.py # Text-to-speech service
│   │   └── ml/                # Machine Learning
│   │       ├── disease_detector.py
│   │       └── image_processor.py
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Backend tests
│   ├── main.py                # FastAPI application
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── utils/             # Utility functions
│   ├── public/                # Static assets
│   └── package.json           # Node.js dependencies
├── ml_models/                 # Trained ML models
├── deployment/                # Deployment configs
│   ├── nginx.conf             # Nginx configuration
│   └── init.sql               # Database initialization
├── docker-compose.yml         # Docker services
└── README.md                  # Project documentation
```

## 🔧 API Endpoints

### Disease Detection
- `POST /api/disease/detect` - Upload image for disease detection
- `GET /api/disease/history` - Get detection history
- `GET /api/disease/supported-crops` - Get supported crops
- `GET /api/disease/disease-info/{crop_type}/{disease_name}` - Get disease info

### Weather
- `GET /api/weather/current` - Get current weather
- `GET /api/weather/forecast` - Get weather forecast
- `GET /api/weather/advisory` - Get weather-based advisory

### WhatsApp
- `POST /api/whatsapp/send` - Send WhatsApp message
- `POST /api/whatsapp/voice` - Send voice message
- `POST /api/whatsapp/webhook` - Handle incoming messages
- `POST /api/whatsapp/broadcast` - Broadcast to multiple users

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Tests
```bash
# Test API endpoints
curl -X POST http://localhost:8000/api/disease/detect \
  -F "file=@test_image.jpg" \
  -F "crop_type=rice"

# Test WhatsApp webhook
curl -X POST http://localhost:8000/api/whatsapp/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=weather&From=whatsapp:+1234567890"
```

## 🔐 Security Considerations

### API Security
- JWT authentication for protected endpoints
- Rate limiting on API endpoints
- Input validation and sanitization
- CORS configuration
- SQL injection prevention

### File Upload Security
- File type validation
- File size limits (10MB)
- Virus scanning (recommended)
- Secure file storage

### WhatsApp Security
- Webhook signature verification
- Phone number validation
- Message content filtering
- Rate limiting per user

## 📊 Monitoring and Logging

### Application Logs
```bash
# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# View database logs
docker-compose logs -f db
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Database health
docker-compose exec db pg_isready -U postgres

# Redis health
docker-compose exec redis redis-cli ping
```

### Performance Monitoring
- Database query performance
- API response times
- ML model inference time
- File upload/download speeds

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
```bash
# Set production environment variables
export DATABASE_URL=postgresql://user:pass@prod-db:5432/agricultural_advisory
export SECRET_KEY=your-production-secret-key
export OPENWEATHER_API_KEY=your-api-key
export TWILIO_ACCOUNT_SID=your-twilio-sid
export TWILIO_AUTH_TOKEN=your-twilio-token
```

2. **SSL Configuration**
```bash
# Generate SSL certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Update nginx.conf with SSL configuration
```

3. **Database Migration**
```bash
# Run migrations
docker-compose exec backend alembic upgrade head
```

4. **Deploy with Docker**
```bash
# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Cloud Deployment (AWS/GCP/Azure)

1. **Container Registry**
```bash
# Build and push images
docker build -t your-registry/agricultural-backend ./backend
docker build -t your-registry/agricultural-frontend ./frontend
docker push your-registry/agricultural-backend
docker push your-registry/agricultural-frontend
```

2. **Managed Services**
- PostgreSQL: AWS RDS / GCP Cloud SQL / Azure Database
- Redis: AWS ElastiCache / GCP Memorystore / Azure Cache
- Load Balancer: AWS ALB / GCP Load Balancer / Azure Load Balancer

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/
```

## 📈 Performance Optimization

### Backend Optimization
- Database query optimization
- Redis caching for frequently accessed data
- Async/await for I/O operations
- Connection pooling
- Background task processing with Celery

### Frontend Optimization
- Code splitting and lazy loading
- Image optimization and compression
- Service worker for offline support
- CDN for static assets
- Bundle size optimization

### ML Model Optimization
- Model quantization for faster inference
- Batch processing for multiple images
- GPU acceleration (if available)
- Model caching and preloading
- Edge deployment for low latency

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Issues**
```bash
# Check database status
docker-compose exec db pg_isready -U postgres

# Reset database
docker-compose down -v
docker-compose up -d db
```

2. **ML Model Loading Issues**
```bash
# Check model file exists
ls -la ml_models/

# Verify model format
python -c "import tensorflow as tf; tf.keras.models.load_model('ml_models/crop_disease_model.h5')"
```

3. **WhatsApp Integration Issues**
```bash
# Test Twilio credentials
curl -u $TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN \
  https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID.json
```

4. **File Upload Issues**
```bash
# Check upload directory permissions
ls -la backend/uploads/
chmod 755 backend/uploads/
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
docker-compose up backend
```

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [TensorFlow Documentation](https://www.tensorflow.org/guide)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)

### Tutorials
- [Building REST APIs with FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [React Hooks and State Management](https://reactjs.org/docs/hooks-intro.html)
- [Image Classification with TensorFlow](https://www.tensorflow.org/tutorials/images/classification)

### Community
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
- [React GitHub](https://github.com/facebook/react)
- [TensorFlow GitHub](https://github.com/tensorflow/tensorflow)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- Backend: Black formatter, flake8 linter
- Frontend: ESLint, Prettier
- Commit messages: Conventional Commits format

### Testing Requirements
- Unit tests for new functions
- Integration tests for new endpoints
- Frontend tests for new components
- Documentation updates for new features
