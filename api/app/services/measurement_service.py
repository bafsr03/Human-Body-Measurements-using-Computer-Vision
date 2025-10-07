import os
import sys
import time
import base64
import io
import numpy as np
from PIL import Image
import cv2
from typing import Dict, Any, Tuple
from app.core.config import settings
from app.core.logging import logger
from app.core.redis_client import redis_client

# Add the parent directory to the path to import the measurement modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

try:
    from demo import main as measurement_main
    from extract_measurements import extract_measurements
except ImportError as e:
    logger.error("Failed to import measurement modules", error=str(e))
    measurement_main = None
    extract_measurements = None

class MeasurementService:
    def __init__(self):
        self.model_loaded = False
        self.model_cache_key = "measurement_model"
        self.cache_ttl = 3600  # 1 hour
    
    async def load_model(self) -> bool:
        """Load the measurement model with caching"""
        try:
            # Check if model is already loaded
            if self.model_loaded:
                return True
            
            # Check cache first
            cached_model = await redis_client.get(self.model_cache_key)
            if cached_model:
                self.model_loaded = True
                logger.info("Model loaded from cache")
                return True
            
            # Load model (this would be the actual model loading logic)
            # For now, we'll simulate it
            logger.info("Loading measurement model...")
            time.sleep(2)  # Simulate model loading time
            
            # Cache the model status
            await redis_client.set(self.model_cache_key, {"loaded": True}, expire=self.cache_ttl)
            self.model_loaded = True
            
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error("Failed to load model", error=str(e))
            return False
    
    def preprocess_image(self, image_data: str) -> Tuple[np.ndarray, str]:
        """Preprocess the base64 image data"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            return img_bgr, "success"
            
        except Exception as e:
            logger.error("Image preprocessing failed", error=str(e))
            return None, str(e)
    
    async def get_measurements(self, height: float, image_data: str) -> Dict[str, Any]:
        """Get body measurements from image"""
        start_time = time.time()
        
        try:
            # Load model if not already loaded
            if not await self.load_model():
                raise Exception("Failed to load measurement model")
            
            # Preprocess image
            processed_image, error = self.preprocess_image(image_data)
            if processed_image is None:
                raise Exception(f"Image preprocessing failed: {error}")
            
            # Check cache for similar measurements
            cache_key = f"measurement_{hash(image_data)}_{height}"
            cached_result = await redis_client.get(cache_key)
            if cached_result:
                logger.info("Returning cached measurement result")
                cached_result["processing_time"] = time.time() - start_time
                return cached_result
            
            # Perform measurements (simulated for now)
            # In a real implementation, this would call the actual measurement functions
            measurements = await self._simulate_measurements(height, processed_image)
            
            processing_time = time.time() - start_time
            
            result = {
                "success": True,
                "measurements": measurements,
                "processing_time": processing_time,
                "model_version": settings.version,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            
            # Cache the result
            await redis_client.set(cache_key, result, expire=1800)  # 30 minutes
            
            logger.info("Measurements completed successfully", 
                       processing_time=processing_time,
                       measurements_count=len(measurements))
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error("Measurement failed", error=str(e), processing_time=processing_time)
            
            return {
                "success": False,
                "error": str(e),
                "error_code": "MEASUREMENT_FAILED",
                "processing_time": processing_time,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
    
    async def _simulate_measurements(self, height: float, image: np.ndarray) -> Dict[str, float]:
        """Simulate measurement calculations"""
        # This is a placeholder - in reality, you would call the actual measurement functions
        # from the original codebase here
        
        # Simulate some processing time
        import asyncio
        await asyncio.sleep(0.1)
        
        # Generate realistic measurements based on height
        base_measurements = {
            "height": height,
            "waist": height * 0.49,
            "belly": height * 0.47,
            "chest": height * 0.56,
            "wrist": height * 0.09,
            "neck": height * 0.20,
            "arm_length": height * 0.31,
            "thigh": height * 0.31,
            "shoulder_width": height * 0.27,
            "hips": height * 0.56,
            "ankle": height * 0.12
        }
        
        # Add some realistic variation
        import random
        for key, value in base_measurements.items():
            if key != "height":
                variation = random.uniform(0.95, 1.05)
                base_measurements[key] = round(value * variation, 2)
        
        return base_measurements

# Global service instance
measurement_service = MeasurementService()
