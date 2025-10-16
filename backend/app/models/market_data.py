"""
Market data model for storing crop prices and market trends.
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.core.database import Base


class MarketData(Base):
    """Market data model for storing crop prices and trends."""
    
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Crop information
    crop_name = Column(String(100), nullable=False)
    crop_variety = Column(String(100))
    
    # Location and market
    market_name = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    
    # Price information
    current_price = Column(Float, nullable=False)  # per quintal/kg
    price_unit = Column(String(20), default="quintal")  # quintal, kg, tonne
    previous_price = Column(Float)
    price_change = Column(Float)  # percentage change
    
    # Market conditions
    demand = Column(String(20))  # high, medium, low
    supply = Column(String(20))  # high, medium, low
    market_trend = Column(String(20))  # rising, falling, stable
    
    # Additional data (JSON string)
    additional_data = Column(Text)
    
    # Data source and timing
    data_source = Column(String(50), default="market_api")
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<MarketData(crop={self.crop_name}, price={self.current_price}, market={self.market_name})>"
