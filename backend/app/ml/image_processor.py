"""
Image processing utilities for crop disease detection.
"""
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional
import io


class ImageProcessor:
    """Handles image preprocessing for ML model input."""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        """
        Initialize image processor.
        
        Args:
            target_size: Target size for image resizing (width, height)
        """
        self.target_size = target_size
    
    def process_image(self, image_data: bytes) -> np.ndarray:
        """
        Process uploaded image for ML model input.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Preprocessed image array ready for ML model
        """
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(self.target_size)
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Normalize pixel values to [0, 1]
        image_array = image_array.astype(np.float32) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    
    def validate_image(self, image_data: bytes) -> Tuple[bool, str]:
        """
        Validate uploaded image.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check file size (10MB limit)
            if len(image_data) > 10 * 1024 * 1024:
                return False, "Image file too large. Maximum size is 10MB."
            
            # Try to open image
            image = Image.open(io.BytesIO(image_data))
            
            # Check image format
            if image.format not in ['JPEG', 'PNG', 'JPG']:
                return False, "Unsupported image format. Please use JPEG or PNG."
            
            # Check image dimensions
            width, height = image.size
            if width < 100 or height < 100:
                return False, "Image too small. Minimum size is 100x100 pixels."
            
            if width > 4000 or height > 4000:
                return False, "Image too large. Maximum size is 4000x4000 pixels."
            
            return True, ""
            
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    def get_image_quality(self, image_data: bytes) -> str:
        """
        Assess image quality for disease detection.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Quality assessment: 'excellent', 'good', 'poor'
        """
        try:
            # Convert to OpenCV format
            image = Image.open(io.BytesIO(image_data))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale for quality assessment
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Calculate Laplacian variance (sharpness measure)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calculate brightness
            brightness = np.mean(gray)
            
            # Calculate contrast
            contrast = np.std(gray)
            
            # Quality assessment based on multiple factors
            if laplacian_var > 100 and 50 < brightness < 200 and contrast > 30:
                return "excellent"
            elif laplacian_var > 50 and 30 < brightness < 220 and contrast > 20:
                return "good"
            else:
                return "poor"
                
        except Exception:
            return "poor"
    
    def extract_image_metadata(self, image_data: bytes) -> dict:
        """
        Extract metadata from image.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dictionary containing image metadata
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            
            metadata = {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "file_size": len(image_data),
                "quality": self.get_image_quality(image_data)
            }
            
            # Extract EXIF data if available
            if hasattr(image, '_getexif') and image._getexif():
                exif = image._getexif()
                if exif:
                    metadata["exif"] = {str(k): v for k, v in exif.items()}
            
            return metadata
            
        except Exception as e:
            return {"error": str(e)}
