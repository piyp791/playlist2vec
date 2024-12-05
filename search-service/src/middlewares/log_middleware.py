from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
from src.logfactory import LogFactory

logger = None

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logFactory: LogFactory):
        global logger
        super().__init__(app)
        logger = logFactory.get_logger("LoggingMiddleware")

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("requestid", "unknown")
        logger.info(f"Incoming request: {request.method} {request.url}", 
                    extra={"request_url": request.url,
                           "request_id": request_id})

        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"[RequestID: {request_id}] Error: {repr(e)}", exc_info=True)
            raise

        process_time = (time.time() - start_time) * 1000
        logger.info(f"Response status: {response.status_code}, Time: {process_time:.2f}ms",
                        extra={"request_url": request.url,
                                "request_id": request_id})

        return response
