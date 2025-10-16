#!/bin/bash

# Agricultural Advisory System Setup Script
# This script sets up the development environment for the Agricultural Advisory System

set -e

echo "🌾 Agricultural Advisory System Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        print_status "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        print_status "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if Node.js is installed (for local development)
check_node() {
    print_status "Checking Node.js installation..."
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed. You can still use Docker for development."
        return 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 16 ]; then
        print_warning "Node.js version is less than 16. Please upgrade to Node.js 16 or higher."
        return 1
    fi
    
    print_success "Node.js $(node --version) is installed"
    return 0
}

# Check if Python is installed (for local development)
check_python() {
    print_status "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 is not installed. You can still use Docker for development."
        return 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_success "Python $PYTHON_VERSION is installed"
    return 0
}

# Create environment files
setup_environment() {
    print_status "Setting up environment files..."
    
    # Backend environment file
    if [ ! -f "backend/.env" ]; then
        cp backend/env.example backend/.env
        print_success "Created backend/.env file"
        print_warning "Please edit backend/.env with your API keys and configuration"
    else
        print_status "backend/.env already exists"
    fi
    
    # Frontend environment file
    if [ ! -f "frontend/.env" ]; then
        cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WHATSAPP_ENABLED=true
REACT_APP_MULTI_LANGUAGE=true
EOF
        print_success "Created frontend/.env file"
    else
        print_status "frontend/.env already exists"
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p backend/uploads/voice
    mkdir -p backend/logs
    mkdir -p ml_models
    mkdir -p deployment/ssl
    
    print_success "Created necessary directories"
}

# Setup Docker environment
setup_docker() {
    print_status "Setting up Docker environment..."
    
    # Pull required images
    docker-compose pull
    
    print_success "Docker environment ready"
}

# Setup local development environment
setup_local_backend() {
    if [ -d "backend" ]; then
        print_status "Setting up local backend environment..."
        
        cd backend
        
        # Create virtual environment
        if [ ! -d "venv" ]; then
            python3 -m venv venv
            print_success "Created Python virtual environment"
        fi
        
        # Activate virtual environment and install dependencies
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        
        cd ..
        print_success "Backend dependencies installed"
    fi
}

# Setup local frontend environment
setup_local_frontend() {
    if [ -d "frontend" ]; then
        print_status "Setting up local frontend environment..."
        
        cd frontend
        npm install
        cd ..
        
        print_success "Frontend dependencies installed"
    fi
}

# Create sample ML model
create_sample_model() {
    print_status "Creating sample ML model..."
    
    if [ ! -f "ml_models/crop_disease_model.h5" ]; then
        cat > ml_models/create_sample_model.py << 'EOF'
import tensorflow as tf
import numpy as np

# Create a simple sample model for development
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')  # 5 disease classes
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Save the model
model.save('crop_disease_model.h5')
print("Sample model created successfully!")
EOF
        
        cd ml_models
        python3 create_sample_model.py
        rm create_sample_model.py
        cd ..
        
        print_success "Sample ML model created"
    else
        print_status "ML model already exists"
    fi
}

# Start services
start_services() {
    print_status "Starting services with Docker Compose..."
    
    # Start database and Redis first
    docker-compose up -d db redis
    
    # Wait for database to be ready
    print_status "Waiting for database to be ready..."
    sleep 10
    
    # Start all services
    docker-compose up -d
    
    print_success "All services started successfully!"
}

# Display status
show_status() {
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo ""
    echo "Services Status:"
    docker-compose ps
    echo ""
    echo "🌐 Application URLs:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo "  Database: localhost:5432"
    echo "  Redis: localhost:6379"
    echo ""
    echo "📋 Next Steps:"
    echo "  1. Edit backend/.env with your API keys:"
    echo "     - OPENWEATHER_API_KEY (for weather data)"
    echo "     - TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN (for WhatsApp)"
    echo "  2. Visit http://localhost:3000 to access the application"
    echo "  3. Check the API documentation at http://localhost:8000/docs"
    echo ""
    echo "🔧 Useful Commands:"
    echo "  View logs: docker-compose logs -f"
    echo "  Stop services: docker-compose down"
    echo "  Restart services: docker-compose restart"
    echo "  Update services: docker-compose pull && docker-compose up -d"
    echo ""
    echo "📚 Documentation:"
    echo "  README.md - Project overview"
    echo "  DEVELOPMENT_GUIDE.md - Development guide"
    echo "  SYSTEM_ARCHITECTURE.md - System architecture"
    echo ""
}

# Main setup function
main() {
    echo "Starting setup process..."
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Setup environment
    setup_environment
    create_directories
    setup_docker
    
    # Setup local development (optional)
    if check_node; then
        setup_local_frontend
    fi
    
    if check_python; then
        setup_local_backend
    fi
    
    # Create sample model
    create_sample_model
    
    # Start services
    start_services
    
    # Show status
    show_status
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Agricultural Advisory System Setup Script"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --docker-only  Setup only Docker environment"
        echo "  --local-only   Setup only local development environment"
        echo "  --stop         Stop all services"
        echo "  --restart      Restart all services"
        echo "  --logs         Show service logs"
        echo ""
        exit 0
        ;;
    --docker-only)
        check_docker
        setup_environment
        create_directories
        setup_docker
        create_sample_model
        start_services
        show_status
        ;;
    --local-only)
        check_node
        check_python
        setup_environment
        create_directories
        setup_local_backend
        setup_local_frontend
        create_sample_model
        echo ""
        echo "Local development environment ready!"
        echo "To start the backend: cd backend && source venv/bin/activate && python main.py"
        echo "To start the frontend: cd frontend && npm start"
        ;;
    --stop)
        print_status "Stopping all services..."
        docker-compose down
        print_success "All services stopped"
        ;;
    --restart)
        print_status "Restarting all services..."
        docker-compose restart
        print_success "All services restarted"
        ;;
    --logs)
        docker-compose logs -f
        ;;
    *)
        main
        ;;
esac
