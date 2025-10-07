from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from enum import Enum

class MeasurementType(str, Enum):
    HEIGHT = "height"
    WAIST = "waist"
    BELLY = "belly"
    CHEST = "chest"
    WRIST = "wrist"
    NECK = "neck"
    ARM_LENGTH = "arm_length"
    THIGH = "thigh"
    SHOULDER_WIDTH = "shoulder_width"
    HIPS = "hips"
    ANKLE = "ankle"

class MeasurementRequest(BaseModel):
    height: float = Field(..., gt=0, le=300, description="Height in centimeters")
    image_data: str = Field(..., description="Base64 encoded image data")
    
    @validator('height')
    def validate_height(cls, v):
        if v <= 0 or v > 300:
            raise ValueError('Height must be between 0 and 300 cm')
        return v

class MeasurementResponse(BaseModel):
    success: bool = Field(..., description="Whether the measurement was successful")
    measurements: Dict[str, float] = Field(..., description="Body measurements in centimeters")
    processing_time: float = Field(..., description="Processing time in seconds")
    model_version: str = Field(..., description="Model version used")
    timestamp: str = Field(..., description="Processing timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "measurements": {
                    "height": 72.0,
                    "waist": 35.61,
                    "belly": 34.14,
                    "chest": 40.16,
                    "wrist": 6.75,
                    "neck": 14.45,
                    "arm_length": 22.27,
                    "thigh": 22.34,
                    "shoulder_width": 19.74,
                    "hips": 40.63,
                    "ankle": 8.52
                },
                "processing_time": 12.34,
                "model_version": "1.0.0",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }

class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Whether the request was successful")
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: str = Field(..., description="Error timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Invalid image format",
                "error_code": "INVALID_IMAGE",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }

