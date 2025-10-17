"""
Simplified FastAPI application for the Agricultural Advisory System.
This version works without heavy ML dependencies for demonstration purposes.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime

# Create FastAPI application
app = FastAPI(
    title="Agricultural Advisory System",
    description="AI-powered platform for agricultural advisories, weather data, and crop disease detection",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.post("/api/disease/detect")
async def detect_disease_demo():
    """
    Demo disease detection endpoint.
    Returns mock data for demonstration purposes.
    """
    return {
        "success": True,
        "disease": "Healthy",
        "confidence": 0.95,
        "is_diseased": False,
        "crop_type": "rice",
        "image_quality": "excellent",
        "all_predictions": {
            "Healthy": 0.95,
            "Brown Spot": 0.03,
            "Bacterial Leaf Blight": 0.01,
            "Leaf Smut": 0.005,
            "Rice Blast": 0.005
        },
        "recommendations": [
            "Your crop appears healthy!",
            "Continue regular monitoring",
            "Maintain good agricultural practices",
            "Ensure proper irrigation and nutrition"
        ]
    }


@app.get("/api/disease/supported-crops")
async def get_supported_crops():
    """Get list of supported crop types."""
    return {
        "success": True,
        "crops": ["rice", "wheat", "maize", "tomato", "potato"],
        "disease_classes": {
            "rice": {
                0: "Healthy",
                1: "Brown Spot",
                2: "Bacterial Leaf Blight",
                3: "Leaf Smut",
                4: "Rice Blast"
            },
            "wheat": {
                0: "Healthy",
                1: "Rust",
                2: "Powdery Mildew",
                3: "Septoria",
                4: "Fusarium Head Blight"
            }
        }
    }


@app.get("/api/weather/current")
async def get_current_weather_demo(latitude: float = 17.3850, longitude: float = 78.4867):
    """
    Demo weather endpoint.
    Returns mock weather data for demonstration purposes.
    """
    return {
        "success": True,
        "data_source": "demo",
        "weather": {
            "location": f"{latitude},{longitude}",
            "temperature": 28.5,
            "humidity": 65,
            "pressure": 1013,
            "wind_speed": 12.5,
            "wind_direction": 180,
            "precipitation": 0,
            "cloud_cover": 25,
            "condition": "Clear",
            "description": "clear sky",
            "recorded_at": datetime.now().isoformat()
        }
    }


@app.get("/api/weather/forecast")
async def get_weather_forecast_demo(latitude: float = 17.3850, longitude: float = 78.4867, days: int = 5):
    """
    Demo weather forecast endpoint.
    Returns mock forecast data for demonstration purposes.
    """
    forecast = []
    for i in range(days):
        forecast.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "temperature": {
                "min": 22 + i,
                "max": 32 + i,
                "avg": 27 + i
            },
            "humidity": 60 + (i * 2),
            "precipitation": i * 0.5,
            "condition": ["Clear", "Cloudy", "Rain", "Sunny", "Partly Cloudy"][i % 5]
        })
    
    return {
        "success": True,
        "forecast": forecast,
        "location": f"{latitude},{longitude}",
        "days": days
    }


@app.get("/api/market/prices")
async def get_market_prices_demo():
    """
    Demo market prices endpoint.
    Returns mock market data for demonstration purposes.
    """
    return {
        "success": True,
        "prices": [
            {
                "crop_name": "Rice",
                "variety": "Basmati",
                "current_price": 2800,
                "unit": "quintal",
                "market_name": "APMC Market",
                "district": "Hyderabad",
                "state": "Telangana",
                "price_change": 2.5,
                "trend": "rising"
            },
            {
                "crop_name": "Wheat",
                "variety": "Durum",
                "current_price": 2200,
                "unit": "quintal",
                "market_name": "APMC Market",
                "district": "Hyderabad",
                "state": "Telangana",
                "price_change": -1.2,
                "trend": "falling"
            }
        ]
    }


@app.post("/api/whatsapp/send")
async def send_whatsapp_demo():
    """
    Demo WhatsApp endpoint.
    Returns mock response for demonstration purposes.
    """
    return {
        "success": True,
        "message": "WhatsApp integration demo - would send message in production",
        "delivered": True,
        "message_sid": "demo_sid_12345"
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
                "/api/disease/supported-crops",
                "/api/weather/current",
                "/api/weather/forecast",
                "/api/market/prices",
                "/api/whatsapp/send",
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
            "error": str(exc)
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
