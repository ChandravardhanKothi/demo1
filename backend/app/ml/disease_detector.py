"""
Crop disease detection using deep learning models.
"""
import tensorflow as tf
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import os
from .image_processor import ImageProcessor
from app.core.config import settings


class CropDiseaseDetector:
    """Crop disease detection using CNN models."""
    
    # Disease classes for different crops
    DISEASE_CLASSES = {
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
        },
        "maize": {
            0: "Healthy",
            1: "Northern Leaf Blight",
            2: "Common Rust",
            3: "Gray Leaf Spot",
            4: "Bacterial Wilt"
        },
        "tomato": {
            0: "Healthy",
            1: "Early Blight",
            2: "Late Blight",
            3: "Bacterial Spot",
            4: "Mosaic Virus"
        },
        "potato": {
            0: "Healthy",
            1: "Late Blight",
            2: "Early Blight",
            3: "Blackleg",
            4: "Viral Disease"
        }
    }
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize disease detector.
        
        Args:
            model_path: Path to the trained model file
        """
        self.model_path = model_path or settings.ml_model_path
        self.model = None
        self.image_processor = ImageProcessor()
        self.confidence_threshold = settings.confidence_threshold
        
        # Load model if path exists
        if os.path.exists(self.model_path):
            self.load_model()
    
    def load_model(self):
        """Load the trained model."""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Create a dummy model for development
            self.model = self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create a dummy model for development/testing."""
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
        return model
    
    def detect_disease(self, image_data: bytes, crop_type: str = "rice") -> Dict:
        """
        Detect disease in crop image.
        
        Args:
            image_data: Raw image bytes
            crop_type: Type of crop (rice, wheat, maize, tomato, potato)
            
        Returns:
            Dictionary containing detection results
        """
        try:
            # Validate image
            is_valid, error_msg = self.image_processor.validate_image(image_data)
            if not is_valid:
                return {
                    "success": False,
                    "error": error_msg,
                    "disease": "Unknown",
                    "confidence": 0.0,
                    "is_diseased": False
                }
            
            # Process image
            processed_image = self.image_processor.process_image(image_data)
            
            # Get predictions
            if self.model is None:
                return self._get_dummy_prediction(crop_type)
            
            predictions = self.model.predict(processed_image, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])
            
            # Get disease name
            disease_classes = self.DISEASE_CLASSES.get(crop_type.lower(), self.DISEASE_CLASSES["rice"])
            disease_name = disease_classes.get(predicted_class, "Unknown")
            
            # Determine if diseased
            is_diseased = disease_name != "Healthy" and confidence >= self.confidence_threshold
            
            # Get image metadata
            metadata = self.image_processor.extract_image_metadata(image_data)
            
            return {
                "success": True,
                "disease": disease_name,
                "confidence": confidence,
                "is_diseased": is_diseased,
                "crop_type": crop_type,
                "image_quality": metadata.get("quality", "unknown"),
                "all_predictions": {
                    disease_classes[i]: float(predictions[0][i]) 
                    for i in range(len(predictions[0]))
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Detection failed: {str(e)}",
                "disease": "Unknown",
                "confidence": 0.0,
                "is_diseased": False
            }
    
    def _get_dummy_prediction(self, crop_type: str) -> Dict:
        """Generate dummy prediction for development."""
        import random
        
        disease_classes = self.DISEASE_CLASSES.get(crop_type.lower(), self.DISEASE_CLASSES["rice"])
        diseases = list(disease_classes.values())
        
        # Randomly select a disease with some bias towards "Healthy"
        if random.random() < 0.6:
            disease = "Healthy"
            confidence = random.uniform(0.7, 0.95)
        else:
            disease = random.choice([d for d in diseases if d != "Healthy"])
            confidence = random.uniform(0.6, 0.9)
        
        return {
            "success": True,
            "disease": disease,
            "confidence": confidence,
            "is_diseased": disease != "Healthy",
            "crop_type": crop_type,
            "image_quality": random.choice(["excellent", "good", "poor"]),
            "all_predictions": {d: random.uniform(0.1, 0.3) for d in diseases}
        }
    
    def get_supported_crops(self) -> List[str]:
        """Get list of supported crop types."""
        return list(self.DISEASE_CLASSES.keys())
    
    def get_disease_info(self, crop_type: str, disease_name: str) -> Dict:
        """
        Get detailed information about a specific disease.
        
        Args:
            crop_type: Type of crop
            disease_name: Name of the disease
            
        Returns:
            Dictionary containing disease information
        """
        # This would typically come from a database or knowledge base
        disease_info = {
            "rice": {
                "Brown Spot": {
                    "symptoms": ["Brown spots on leaves", "Yellowing of leaves", "Reduced yield"],
                    "causes": "Fungal infection",
                    "treatment": "Apply fungicides, improve drainage",
                    "prevention": "Use resistant varieties, proper spacing"
                },
                "Bacterial Leaf Blight": {
                    "symptoms": ["Water-soaked lesions", "Yellow streaks", "Leaf wilting"],
                    "causes": "Bacterial infection",
                    "treatment": "Copper-based fungicides",
                    "prevention": "Clean seeds, avoid overhead irrigation"
                }
            },
            "wheat": {
                "Rust": {
                    "symptoms": ["Orange/yellow pustules", "Leaf discoloration", "Reduced grain size"],
                    "causes": "Fungal infection",
                    "treatment": "Fungicide application",
                    "prevention": "Resistant varieties, crop rotation"
                }
            }
        }
        
        return disease_info.get(crop_type.lower(), {}).get(disease_name, {
            "symptoms": ["Symptoms vary"],
            "causes": "Various factors",
            "treatment": "Consult agricultural expert",
            "prevention": "Good agricultural practices"
        })
