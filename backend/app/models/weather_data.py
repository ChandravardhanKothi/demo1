"""
Weather data model for storing current and historical weather information.
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.core.database import Base


class WeatherData(Base):
    """Weather data model for storing weather information."""
    
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Location
    location = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Weather data
    temperature = Column(Float)  # in Celsius
    humidity = Column(Float)     # percentage
    pressure = Column(Float)     # hPa
    wind_speed = Column(Float)   # m/s
    wind_direction = Column(Float)  # degrees
    precipitation = Column(Float)   # mm
    cloud_cover = Column(Float)     # percentage
    
    # Weather conditions
    condition = Column(String(50))  # clear, cloudy, rain, etc.
    description = Column(String(100))
    
    # Forecast data (JSON string for multiple days)
    forecast_data = Column(Text)
    
    # Data source and timing
    data_source = Column(String(50), default="openweather")
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<WeatherData(location={self.location}, temp={self.temperature}°C, condition={self.condition})>"
