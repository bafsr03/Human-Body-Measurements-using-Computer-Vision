import redis
from typing import Optional, Any
import json
from app.core.config import settings
from app.core.logging import logger

class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            decode_responses=True
        )
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("Redis get error", key=key, error=str(e))
            return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set value in Redis with optional expiration"""
        try:
            serialized_value = json.dumps(value)
            result = self.redis_client.set(key, serialized_value, ex=expire)
            return result
        except Exception as e:
            logger.error("Redis set error", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        try:
            result = self.redis_client.delete(key)
            return bool(result)
        except Exception as e:
            logger.error("Redis delete error", key=key, error=str(e))
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis"""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error("Redis exists error", key=key, error=str(e))
            return False

redis_client = RedisClient()

