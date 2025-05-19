from fastapi import Request
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Log request info
    logger.info(f"Request started: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Log response info
    process_time = time.time() - start_time
    logger.info(f"Request completed: {request.method} {request.url.path} - Took {process_time:.4f}s")
    
    return response