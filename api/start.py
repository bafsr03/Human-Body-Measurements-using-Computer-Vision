#!/usr/bin/env python3
"""
Startup script for the Human Body Measurements API
"""

import uvicorn
from app.core.config import settings
from app.core.logging import logger

if __name__ == "__main__":
    logger.info("Starting Human Body Measurements API", 
                version=settings.version,
                host=settings.host,
                port=settings.port)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=True
    )

