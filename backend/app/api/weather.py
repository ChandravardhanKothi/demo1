"""
API endpoints for weather data and forecasts.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import requests
import json
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.weather_data import WeatherData
from app.models.user import User
from app.core.config import settings

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/current")
async def get_current_weather(
    latitude: float,
    longitude: float,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get current weather data for a location.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        location: Location name (optional)
        db: Database session
        
    Returns:
        Current weather data
    """
    try:
        # Check if we have recent data in database (within last hour)
        recent_weather = db.query(WeatherData).filter(
            WeatherData.latitude == latitude,
            WeatherData.longitude == longitude,
            WeatherData.recorded_at >= datetime.utcnow() - timedelta(hours=1)
        ).first()
        
        if recent_weather:
            return {
                "success": True,
                "data_source": "database",
                "weather": {
                    "location": recent_weather.location,
                    "temperature": recent_weather.temperature,
                    "humidity": recent_weather.humidity,
                    "pressure": recent_weather.pressure,
                    "wind_speed": recent_weather.wind_speed,
                    "wind_direction": recent_weather.wind_direction,
                    "precipitation": recent_weather.precipitation,
                    "cloud_cover": recent_weather.cloud_cover,
                    "condition": recent_weather.condition,
                    "description": recent_weather.description,
                    "recorded_at": recent_weather.recorded_at.isoformat()
                }
            }
        
        # Fetch fresh data from OpenWeather API
        weather_data = await _fetch_weather_from_api(latitude, longitude, location)
        
        # Save to database
        weather_record = WeatherData(
            location=location or f"{latitude},{longitude}",
            latitude=latitude,
            longitude=longitude,
            temperature=weather_data["main"]["temp"],
            humidity=weather_data["main"]["humidity"],
            pressure=weather_data["main"]["pressure"],
            wind_speed=weather_data["wind"]["speed"],
            wind_direction=weather_data["wind"].get("deg"),
            precipitation=weather_data.get("rain", {}).get("1h", 0),
            cloud_cover=weather_data["clouds"]["all"],
            condition=weather_data["weather"][0]["main"],
            description=weather_data["weather"][0]["description"],
            forecast_data=json.dumps(weather_data.get("forecast", {}))
        )
        
        db.add(weather_record)
        db.commit()
        
        return {
            "success": True,
            "data_source": "api",
            "weather": {
                "location": weather_record.location,
                "temperature": weather_record.temperature,
                "humidity": weather_record.humidity,
                "pressure": weather_record.pressure,
                "wind_speed": weather_record.wind_speed,
                "wind_direction": weather_record.wind_direction,
                "precipitation": weather_record.precipitation,
                "cloud_cover": weather_record.cloud_cover,
                "condition": weather_record.condition,
                "description": weather_record.description,
                "recorded_at": weather_record.recorded_at.isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch weather data: {str(e)}"
        )


@router.get("/forecast")
async def get_weather_forecast(
    latitude: float,
    longitude: float,
    days: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get weather forecast for a location.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        days: Number of forecast days (max 5)
        db: Database session
        
    Returns:
        Weather forecast data
    """
    try:
        # Fetch forecast from OpenWeather API
        forecast_data = await _fetch_forecast_from_api(latitude, longitude, days)
        
        return {
            "success": True,
            "forecast": forecast_data,
            "location": f"{latitude},{longitude}",
            "days": days
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch forecast: {str(e)}"
        )


@router.get("/advisory")
async def get_weather_advisory(
    latitude: float,
    longitude: float,
    crop_type: str = "rice",
    db: Session = Depends(get_db)
):
    """
    Get weather-based agricultural advisory.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        crop_type: Type of crop
        db: Database session
        
    Returns:
        Weather-based advisory
    """
    try:
        # Get current weather
        weather_response = await get_current_weather(latitude, longitude, db=db)
        weather = weather_response["weather"]
        
        # Generate advisory based on weather conditions
        advisory = _generate_weather_advisory(weather, crop_type)
        
        return {
            "success": True,
            "advisory": advisory,
            "weather_data": weather,
            "crop_type": crop_type
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate advisory: {str(e)}"
        )


async def _fetch_weather_from_api(latitude: float, longitude: float, location: Optional[str] = None):
    """Fetch weather data from OpenWeather API."""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": settings.openweather_api_key,
        "units": "metric"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()


async def _fetch_forecast_from_api(latitude: float, longitude: float, days: int):
    """Fetch weather forecast from OpenWeather API."""
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": settings.openweather_api_key,
        "units": "metric",
        "cnt": days * 8  # 8 forecasts per day (every 3 hours)
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Process forecast data
    forecast = []
    daily_data = {}
    
    for item in data["list"]:
        date = item["dt_txt"].split()[0]
        if date not in daily_data:
            daily_data[date] = {
                "date": date,
                "temperatures": [],
                "humidity": [],
                "precipitation": [],
                "conditions": []
            }
        
        daily_data[date]["temperatures"].append(item["main"]["temp"])
        daily_data[date]["humidity"].append(item["main"]["humidity"])
        daily_data[date]["precipitation"].append(item.get("rain", {}).get("3h", 0))
        daily_data[date]["conditions"].append(item["weather"][0]["description"])
    
    # Calculate daily averages and summaries
    for date, data in daily_data.items():
        forecast.append({
            "date": date,
            "temperature": {
                "min": min(data["temperatures"]),
                "max": max(data["temperatures"]),
                "avg": sum(data["temperatures"]) / len(data["temperatures"])
            },
            "humidity": sum(data["humidity"]) / len(data["humidity"]),
            "precipitation": sum(data["precipitation"]),
            "condition": max(set(data["conditions"]), key=data["conditions"].count)
        })
    
    return forecast[:days]


def _generate_weather_advisory(weather: dict, crop_type: str) -> dict:
    """Generate weather-based agricultural advisory."""
    temperature = weather["temperature"]
    humidity = weather["humidity"]
    precipitation = weather["precipitation"]
    condition = weather["condition"].lower()
    
    advisory = {
        "title": f"Weather Advisory for {crop_type.title()}",
        "priority": "normal",
        "recommendations": [],
        "warnings": [],
        "opportunities": []
    }
    
    # Temperature-based recommendations
    if temperature < 10:
        advisory["recommendations"].append("Cold weather detected. Consider covering young plants.")
        advisory["warnings"].append("Risk of frost damage to tender crops.")
    elif temperature > 35:
        advisory["recommendations"].append("Hot weather detected. Increase irrigation frequency.")
        advisory["warnings"].append("High temperature stress on crops.")
    elif 20 <= temperature <= 30:
        advisory["opportunities"].append("Optimal temperature range for most crops.")
    
    # Humidity-based recommendations
    if humidity > 80:
        advisory["recommendations"].append("High humidity detected. Monitor for fungal diseases.")
        advisory["warnings"].append("Increased risk of fungal infections.")
    elif humidity < 40:
        advisory["recommendations"].append("Low humidity detected. Ensure adequate irrigation.")
    
    # Precipitation-based recommendations
    if precipitation > 10:
        advisory["recommendations"].append("Heavy rainfall detected. Check drainage systems.")
        advisory["warnings"].append("Risk of waterlogging and root diseases.")
    elif precipitation == 0 and humidity < 50:
        advisory["recommendations"].append("Dry conditions detected. Increase irrigation.")
    
    # Weather condition-based recommendations
    if "rain" in condition:
        advisory["recommendations"].append("Rainfall expected. Postpone fertilizer application.")
    elif "clear" in condition:
        advisory["opportunities"].append("Clear weather ideal for field operations.")
    elif "storm" in condition or "thunder" in condition:
        advisory["warnings"].append("Storm conditions expected. Secure equipment and structures.")
    
    # Crop-specific recommendations
    if crop_type.lower() == "rice":
        if humidity > 70 and temperature > 25:
            advisory["warnings"].append("Conditions favorable for rice blast disease.")
            advisory["recommendations"].append("Apply preventive fungicide for rice blast.")
    
    elif crop_type.lower() == "wheat":
        if temperature > 30 and humidity < 50:
            advisory["warnings"].append("Hot and dry conditions may cause wheat stress.")
            advisory["recommendations"].append("Ensure adequate soil moisture for wheat.")
    
    # Set priority based on warnings
    if len(advisory["warnings"]) > 2:
        advisory["priority"] = "high"
    elif len(advisory["warnings"]) > 0:
        advisory["priority"] = "normal"
    else:
        advisory["priority"] = "low"
    
    return advisory
