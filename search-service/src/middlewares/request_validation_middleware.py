from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class RequestValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        requestid = request.headers.get("requestid", None)
        endpoint = request.headers.get("endpoint", None)
        
        if not requestid or not endpoint:
            return JSONResponse({
                "error": { "code": "HTTP_ERROR", "message": f"Missing headers. Headers details {request.headers}",},
                "status": "FAILURE",
            }, status_code=400)
        
        return await call_next(request)