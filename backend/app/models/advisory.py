"""
Advisory model for storing generated agricultural advisories.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Advisory(Base):
    """Advisory model for storing agricultural recommendations."""
    
    __tablename__ = "advisories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Advisory content
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    advisory_type = Column(String(50))  # weather, disease, market, general
    
    # Language and localization
    language = Column(String(10), default="en")
    voice_file_path = Column(String(500))
    
    # Advisory context
    weather_data = Column(Text)  # JSON string
    market_data = Column(Text)   # JSON string
    disease_data = Column(Text)  # JSON string
    
    # Delivery status
    whatsapp_sent = Column(Boolean, default=False)
    whatsapp_sent_at = Column(DateTime(timezone=True))
    web_viewed = Column(Boolean, default=False)
    web_viewed_at = Column(DateTime(timezone=True))
    
    # Metadata
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    expires_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="advisories")
    
    def __repr__(self):
        return f"<Advisory(id={self.id}, type={self.advisory_type}, title={self.title})>"
