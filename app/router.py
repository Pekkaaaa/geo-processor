"""
Router module for the Geo Processor application.

This module contains the router for the Geo Processor application.
"""

from fastapi import APIRouter

from .models import Bounds, Centroid, PointsRequest, PointsResponse

router = APIRouter(tags=["Geo Processor"], prefix="/api")


@router.get("/health", tags=["health"])
async def health() -> dict[str, bool]:
    return {"success": True}


@router.post(
    "/process",
    response_model=PointsResponse,
    summary="Process coordinates",
    tags=["geo"],
    responses={
        400: {
            "description": "Bad Request: validation error",
            "content": {
                "application/json": {
                    "example": {"error": "`points` must be a non-empty array of coordinate objects."}
                }
            },
        },
        401: {
            "description": "Unauthorized: missing or invalid API key",
            "content": {
                "application/json": {
                    "example": {"error": "Unauthorized: invalid or missing x-api-key"}
                }
            },
        },
    },
)
async def process_points(payload: PointsRequest) -> PointsResponse:
    pts = payload.points
    north = max(p.lat for p in pts)
    south = min(p.lat for p in pts)
    east = max(p.lng for p in pts)
    west = min(p.lng for p in pts)
    centroid_lat = sum(p.lat for p in pts) / len(pts)
    centroid_lng = sum(p.lng for p in pts) / len(pts)

    return PointsResponse(
        centroid=Centroid(lat=centroid_lat, lng=centroid_lng),
        bounds=Bounds(north=north, south=south, east=east, west=west),
    )
