from fastapi import APIRouter
from app.api.v1 import measurements, auth

api_router = APIRouter()

api_router.include_router(measurements.router)
api_router.include_router(auth.router)

