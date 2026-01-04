import uuid
from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import setup_logging

# Context variable to store request ID across async calls
request_id_var: ContextVar[str] = ContextVar("request_id", default=None)

logger = setup_logging()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that:
    1. Extracts or generates a request ID for each request
    2. Stores it in context for access anywhere in the request lifecycle
    3. Adds it to response headers
    4. Binds it to logger for structured logging
    """
    
    async def dispatch(self, request: Request, call_next):
        # Extract from header or generate new UUID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Store in context var
        request_id_var.set(request_id)
        
        # Bind to logger for this request context
        logger_ctx = logger.bind(request_id=request_id, path=request.url.path, method=request.method)
        logger_ctx.info("Request started")
        
        # Process request
        response: Response = await call_next(request)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        logger_ctx.info("Request completed", status_code=response.status_code)
        
        return response


def get_request_id() -> str:
    """Get the current request ID from context"""
    return request_id_var.get()
