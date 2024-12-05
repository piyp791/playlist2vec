from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
import traceback

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as ex:
            error_response = {
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "An unexpected error occurred.",
                    "details": repr(ex),
                },
                "status": "FAILURE",
            }
            traceback.print_exc()
            return JSONResponse(error_response, status_code=500)