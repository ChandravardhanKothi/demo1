"""
API endpoints for crop disease detection.
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.core.database import get_db
from app.models.crop_image import CropImage
from app.models.user import User
from app.ml.disease_detector import CropDiseaseDetector
from app.ml.image_processor import ImageProcessor
from app.core.config import settings

router = APIRouter(prefix="/api/disease", tags=["disease"])

# Initialize ML components
disease_detector = CropDiseaseDetector()
image_processor = ImageProcessor()


@router.post("/detect")
async def detect_disease(
    file: UploadFile = File(...),
    crop_type: str = "rice",
    user_id: int = 1,  # In production, get from JWT token
    db: Session = Depends(get_db)
):
    """
    Detect disease in uploaded crop image.
    
    Args:
        file: Uploaded image file
        crop_type: Type of crop (rice, wheat, maize, tomato, potato)
        user_id: User ID (from authentication)
        db: Database session
        
    Returns:
        Disease detection results
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read file data
        image_data = await file.read()
        
        # Validate image
        is_valid, error_msg = image_processor.validate_image(image_data)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Detect disease
        detection_result = disease_detector.detect_disease(image_data, crop_type)
        
        if not detection_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=detection_result["error"]
            )
        
        # Save image record to database
        crop_image = CropImage(
            user_id=user_id,
            filename=file.filename,
            file_path=f"uploads/{file.filename}",  # In production, use proper file storage
            file_size=len(image_data),
            predicted_disease=detection_result["disease"],
            confidence_score=detection_result["confidence"],
            is_diseased=detection_result["is_diseased"],
            crop_type=crop_type,
            image_quality=detection_result["image_quality"],
            processed=True
        )
        
        db.add(crop_image)
        db.commit()
        db.refresh(crop_image)
        
        # Get disease information
        disease_info = disease_detector.get_disease_info(crop_type, detection_result["disease"])
        
        return {
            "success": True,
            "image_id": crop_image.id,
            "disease": detection_result["disease"],
            "confidence": detection_result["confidence"],
            "is_diseased": detection_result["is_diseased"],
            "crop_type": crop_type,
            "image_quality": detection_result["image_quality"],
            "all_predictions": detection_result["all_predictions"],
            "disease_info": disease_info,
            "recommendations": _get_treatment_recommendations(
                detection_result["disease"], 
                detection_result["is_diseased"]
            )
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/history")
async def get_detection_history(
    user_id: int = 1,  # In production, get from JWT token
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get disease detection history for a user.
    
    Args:
        user_id: User ID
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of detection history records
    """
    try:
        crop_images = db.query(CropImage).filter(
            CropImage.user_id == user_id
        ).order_by(CropImage.created_at.desc()).limit(limit).all()
        
        history = []
        for image in crop_images:
            history.append({
                "id": image.id,
                "filename": image.filename,
                "crop_type": image.crop_type,
                "disease": image.predicted_disease,
                "confidence": image.confidence_score,
                "is_diseased": image.is_diseased,
                "image_quality": image.image_quality,
                "created_at": image.created_at.isoformat()
            })
        
        return {
            "success": True,
            "history": history,
            "total": len(history)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/supported-crops")
async def get_supported_crops():
    """
    Get list of supported crop types for disease detection.
    
    Returns:
        List of supported crop types
    """
    return {
        "success": True,
        "crops": disease_detector.get_supported_crops(),
        "disease_classes": disease_detector.DISEASE_CLASSES
    }


@router.get("/disease-info/{crop_type}/{disease_name}")
async def get_disease_information(crop_type: str, disease_name: str):
    """
    Get detailed information about a specific disease.
    
    Args:
        crop_type: Type of crop
        disease_name: Name of the disease
        
    Returns:
        Disease information
    """
    disease_info = disease_detector.get_disease_info(crop_type, disease_name)
    
    return {
        "success": True,
        "crop_type": crop_type,
        "disease_name": disease_name,
        "information": disease_info
    }


def _get_treatment_recommendations(disease: str, is_diseased: bool) -> List[str]:
    """Generate treatment recommendations based on detection results."""
    if not is_diseased or disease == "Healthy":
        return [
            "Your crop appears healthy!",
            "Continue regular monitoring",
            "Maintain good agricultural practices",
            "Ensure proper irrigation and nutrition"
        ]
    
    recommendations = [
        f"Disease detected: {disease}",
        "Immediate action required",
        "Consult with local agricultural extension officer",
        "Consider appropriate fungicide/bactericide application"
    ]
    
    # Add specific recommendations based on disease type
    if "blight" in disease.lower():
        recommendations.append("Improve air circulation and reduce humidity")
        recommendations.append("Remove and destroy infected plant parts")
    elif "rust" in disease.lower():
        recommendations.append("Apply sulfur-based fungicides")
        recommendations.append("Use resistant varieties for future planting")
    elif "spot" in disease.lower():
        recommendations.append("Improve drainage and avoid overhead irrigation")
        recommendations.append("Apply copper-based fungicides")
    
    return recommendations
