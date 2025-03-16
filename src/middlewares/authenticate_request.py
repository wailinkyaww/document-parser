import os

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

API_KEY = os.getenv("API_KEY")


class AuthenticateRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/":
            return await call_next(request)

        authorization = request.headers.get("Authorization")

        if not authorization:
            return JSONResponse(status_code=401, content={"detail": "Please provide a valid API Key."})

        if not authorization.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Please provide a valid API Key."})

        token = authorization.split("Bearer ")[1].strip()

        if token != API_KEY:
            return JSONResponse(status_code=401, content={"detail": "Please provide a valid API Key."})

        return await call_next(request)
