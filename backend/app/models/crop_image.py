"""
Crop image model for storing uploaded images and disease detection results.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Float,
    ForeignKey,
    Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class CropImage(Base):
    """Crop image model for disease detection."""

    __tablename__ = "crop_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)

    # Disease detection results
    predicted_disease = Column(String(100))
    confidence_score = Column(Float)
    is_diseased = Column(Boolean, default=False)

    # Image metadata
    crop_type = Column(String(50))  # rice, wheat, maize, etc.
    image_quality = Column(String(20))  # good, poor, excellent

    # Processing status
    processed = Column(Boolean, default=False)
    processing_error = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="crop_images")

    def __repr__(self):
        return f"<CropImage(id={self.id}, disease={self.predicted_disease}, confidence={self.confidence_score})>"
