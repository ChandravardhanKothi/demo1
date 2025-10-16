# Agricultural Advisory System - Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           AGRICULTURAL ADVISORY SYSTEM                          │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FARMER        │    │   FARMER        │    │   FARMER        │    │   FARMER        │
│   (Web App)     │    │   (WhatsApp)    │    │   (Mobile)      │    │   (Voice)       │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │                      │
          │                      │                      │                      │
          ▼                      ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              NGINX REVERSE PROXY                               │
│                              (Load Balancer)                                   │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React)                                  │
│  • Dashboard          • Disease Detection    • Weather Forecast               │
│  • Market Prices      • Advisory History     • Voice Messages                 │
│  • User Profile       • Image Upload         • Multi-language Support         │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND (FastAPI)                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Disease   │  │   Weather   │  │   Market    │  │  Advisory   │            │
│  │ Detection   │  │   Service   │  │   Service   │  │   Service   │            │
│  │   API       │  │    API      │  │    API      │  │    API      │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AI/ML MODULE                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Image     │  │   Disease   │  │   Advisory  │  │   Quality   │            │
│  │ Processor   │  │  Detector   │  │  Generator  │  │  Assessor   │            │
│  │ (OpenCV)    │  │(TensorFlow) │  │    (AI)     │  │  (OpenCV)   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            COMMUNICATION LAYER                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  WhatsApp   │  │   Text-to-  │  │   Email     │  │    SMS      │            │
│  │ Integration │  │   Speech    │  │  Service    │  │  Service    │            │
│  │  (Twilio)   │  │   (gTTS)    │  │ (Future)    │  │ (Future)    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ PostgreSQL  │  │    Redis    │  │ File Storage│  │   Backup    │            │
│  │ (Primary)   │  │  (Cache)    │  │  (Images)   │  │  Storage    │            │
│  │ Database    │  │   & Queue   │  │   & Voice   │  │   (S3)      │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            EXTERNAL SERVICES                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ OpenWeather │  │   Market    │  │   Twilio    │  │   Google    │            │
│  │     API     │  │    APIs     │  │   WhatsApp  │  │     TTS     │            │
│  │  (Weather)  │  │ (Prices)    │  │    API      │  │    API      │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

### 1. Disease Detection Flow
```
User Uploads Image → Frontend → Backend → Image Processor → ML Model → 
Disease Detection → Database → Advisory Generation → User Notification
```

### 2. Weather Advisory Flow
```
User Request → Frontend → Backend → OpenWeather API → Weather Data → 
Database → Advisory Generation → TTS → WhatsApp → User
```

### 3. Market Price Flow
```
Scheduled Task → Market API → Price Data → Database → 
Price Analysis → Advisory Generation → User Notification
```

### 4. WhatsApp Integration Flow
```
User Message → Twilio Webhook → Backend → Message Processing → 
Response Generation → TTS (if needed) → Twilio → User
```

## Component Interactions

### Frontend Components
- **Dashboard**: Overview of all system data
- **Disease Detection**: Image upload and analysis results
- **Weather**: Current weather and forecasts
- **Market**: Price trends and analysis
- **Advisories**: Historical and current recommendations
- **Profile**: User settings and preferences

### Backend Services
- **Disease Detection Service**: Handles image processing and ML inference
- **Weather Service**: Fetches and processes weather data
- **Market Service**: Retrieves and analyzes market prices
- **Advisory Service**: Generates recommendations based on multiple data sources
- **WhatsApp Service**: Handles messaging and voice communications
- **TTS Service**: Converts text to speech in multiple languages

### Database Schema
- **Users**: Farmer profiles and preferences
- **Crop Images**: Uploaded images and detection results
- **Weather Data**: Historical and current weather information
- **Market Data**: Price history and trends
- **Advisories**: Generated recommendations and delivery status

## Security Architecture

### Authentication & Authorization
- JWT tokens for API authentication
- Role-based access control
- Session management
- Password hashing with bcrypt

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection
- File upload security

### Communication Security
- HTTPS/TLS encryption
- API rate limiting
- CORS configuration
- Webhook signature verification

## Scalability Considerations

### Horizontal Scaling
- Load balancer for multiple backend instances
- Database read replicas
- Redis clustering
- CDN for static assets

### Performance Optimization
- Database indexing and query optimization
- Redis caching for frequently accessed data
- Async processing for heavy operations
- Image compression and optimization

### Monitoring & Logging
- Application performance monitoring
- Error tracking and alerting
- Database performance metrics
- User analytics and usage patterns

## Deployment Architecture

### Development Environment
- Docker Compose for local development
- Hot reload for frontend and backend
- Local database and Redis instances
- Mock external services

### Production Environment
- Kubernetes or Docker Swarm orchestration
- Managed database services (RDS/Cloud SQL)
- Managed Redis services (ElastiCache/Cloud Memorystore)
- Load balancers and CDN
- SSL certificates and security groups

### CI/CD Pipeline
- Automated testing on pull requests
- Code quality checks and linting
- Security vulnerability scanning
- Automated deployment to staging/production
- Database migration management
