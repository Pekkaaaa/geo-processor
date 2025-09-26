"""
Middleware module for the Geo Processor application.

This module contains the API key middleware for the application.
"""


from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path

        if path in settings.public_paths:
            return await call_next(request)

        provided_key = request.headers.get("x-api-key")

        if not provided_key or provided_key != settings.api_key:
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized: invalid or missing x-api-key"},
            )

        return await call_next(request)
