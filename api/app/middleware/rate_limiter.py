from fastapi import Request, HTTPException
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings

# Determine storage backend. Default to in-memory to avoid requiring Redis in dev.
_storage_uri = os.getenv("RATE_LIMIT_STORAGE_URI")
if not _storage_uri:
    if settings.redis_host and settings.redis_host.lower() not in {"memory", "none", ""}:
        _storage_uri = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"
    else:
        _storage_uri = "memory://"

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=_storage_uri,
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

