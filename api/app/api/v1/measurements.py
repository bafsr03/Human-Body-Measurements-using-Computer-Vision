from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
import base64
from app.schemas.measurement import MeasurementRequest, MeasurementResponse, ErrorResponse
from app.services.measurement_service import measurement_service
from app.middleware.auth import get_current_user
from app.middleware.rate_limiter import rate_limit
from app.core.logging import logger
from typing import Dict, Any

router = APIRouter(prefix="/measurements", tags=["measurements"])

@router.post(
    "/analyze",
    response_model=MeasurementResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
@rate_limit(requests=5, window=60)  # 5 requests per minute
async def analyze_body_measurements(
    request: Request,
    height: float = Form(..., gt=0, le=300, description="Height in centimeters"),
    image: UploadFile = File(..., description="Image file"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Analyze body measurements from an uploaded image.
    
    - **height**: Height in centimeters (required)
    - **image**: Image file (JPEG, PNG, etc.)
    
    Returns detailed body measurements including waist, chest, arm length, etc.
    """
    try:
        # Validate image file
        if not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read and encode image
        image_data = await image.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        logger.info("Processing measurement request", 
                   username=current_user["username"],
                   height=height,
                   image_size=len(image_data))
        
        # Get measurements
        result = await measurement_service.get_measurements(height, image_base64)
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Measurement processing failed")
            )
        
        logger.info("Measurement request completed successfully",
                   username=current_user["username"],
                   processing_time=result.get("processing_time"))
        
        return MeasurementResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error in measurement analysis", 
                    error=str(e),
                    username=current_user["username"])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post(
    "/analyze-base64",
    response_model=MeasurementResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
@rate_limit(requests=10, window=60)  # 10 requests per minute
async def analyze_body_measurements_base64(
    request: Request,
    payload: MeasurementRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Analyze body measurements from a base64 encoded image.
    
    - **height**: Height in centimeters (required)
    - **image_data**: Base64 encoded image data (required)
    
    Returns detailed body measurements including waist, chest, arm length, etc.
    """
    try:
        logger.info("Processing base64 measurement request", 
                   username=current_user["username"],
                   height=payload.height)
        
        # Get measurements
        result = await measurement_service.get_measurements(payload.height, payload.image_data)
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Measurement processing failed")
            )
        
        logger.info("Base64 measurement request completed successfully",
                   username=current_user["username"],
                   processing_time=result.get("processing_time"))
        
        return MeasurementResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error in base64 measurement analysis", 
                    error=str(e),
                    username=current_user["username"])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for the measurement service"""
    try:
        # Check if model is loaded
        model_loaded = await measurement_service.load_model()
        
        return {
            "status": "healthy" if model_loaded else "unhealthy",
            "model_loaded": model_loaded,
            "service": "measurement"
        }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e),
                "service": "measurement"
            }
        )

