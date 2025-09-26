"""
Models module for the Geo Processor application.

This module contains the models for the Geo Processor application.
"""

from typing import List
from pydantic import BaseModel, Field, model_validator


class Point(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude in degrees [-90, 90]")
    lng: float = Field(..., ge=-180, le=180, description="Longitude in degrees [-180, 180]")


class PointsRequest(BaseModel):
    points: List[Point] = Field(..., description="Non-empty array of {lat, lng} points")

    @model_validator(mode="after")
    def _non_empty_points(self) -> "PointsRequest":
        if not self.points:
            raise ValueError("`points` must be a non-empty array of coordinate objects.")
        return self


class Bounds(BaseModel):
    north: float
    south: float
    east: float
    west: float


class Centroid(BaseModel):
    lat: float
    lng: float


class PointsResponse(BaseModel):
    centroid: Centroid
    bounds: Bounds
