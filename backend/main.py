"""
Main FastAPI application for the Agricultural Advisory System.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api import disease, weather

# Create uploads directory
os.makedirs(settings.upload_dir, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("Starting Agricultural Advisory System...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
    
    yield
    
    # Shutdown
    print("Shutting down Agricultural Advisory System...")


# Create FastAPI application
app = FastAPI(
    title="Agricultural Advisory System",
    description="AI-powered platform for agricultural advisories, weather data, and crop disease detection",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Include API routers
app.include_router(disease.router)
app.include_router(weather.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Agricultural Advisory System API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "disease_detection": "/api/disease",
            "weather": "/api/weather",
            "documentation": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Endpoint not found",
            "available_endpoints": [
                "/api/disease/detect",
                "/api/disease/history",
                "/api/weather/current",
                "/api/weather/forecast",
                "/docs"
            ]
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc) if settings.log_level == "DEBUG" else "An error occurred"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
