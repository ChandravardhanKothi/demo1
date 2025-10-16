"""
User model for managing farmer profiles and authentication.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    """User model for farmer profiles."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    language = Column(String(10), default="en")  # en, hi, te, ta
    location = Column(String(100))  # Village/District
    latitude = Column(Float)
    longitude = Column(Float)
    crop_types = Column(Text)  # JSON string of preferred crops
    whatsapp_enabled = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    crop_images = relationship("CropImage", back_populates="user")
    advisories = relationship("Advisory", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone_number}, name={self.name})>"
