"""
Main module for the Geo Processor application.

This module creates the FastAPI application and includes the middleware and routers.
"""

from fastapi import FastAPI

from .config import settings
from .middleware import APIKeyMiddleware
from .router import router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="Compute centroid and bounding box for a list of coordinates.",
        version="1.0.0",
        debug=settings.debug,
    )

    app.add_middleware(APIKeyMiddleware)

    app.include_router(router)

    return app


app = create_app()
