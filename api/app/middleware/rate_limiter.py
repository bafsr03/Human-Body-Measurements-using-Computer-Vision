from fastapi import Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.redis_client import redis_client
import time

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
    enabled=True
)

# Custom rate limit handler
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    response = HTTPException(
        status_code=429,
        detail=f"Rate limit exceeded: {exc.detail}"
    )
    response.headers = exc.headers
    return response

# Apply rate limiting decorator
def rate_limit(requests: int = None, window: int = None):
    """Apply rate limiting to an endpoint"""
    requests = requests or settings.rate_limit_requests
    window = window or settings.rate_limit_window
    
    return limiter.limit(f"{requests}/{window}seconds")

