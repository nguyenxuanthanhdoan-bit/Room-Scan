from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import numpy as np
from pydantic import BaseModel, Field

class CameraIntrinsics(BaseModel):
    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int

class Frame(BaseModel):
    frame_id: int
    timestamp: float
    image_path: Optional[str] = None
    intrinsics: CameraIntrinsics
    pose_matrix: Optional[List[List[float]]] = None  # 4x4 camera-to-world pose if available

class WallSegment(BaseModel):
    wall_id: str
    start_point: Tuple[float, float]
    end_point: Tuple[float, float]
    length: float

class RoomDimensions(BaseModel):
    width: float
    length: float
    height: float
    area: float
    volume: float

class RoomLayoutResult(BaseModel):
    version: str = "1.0"
    room_id: str
    dimensions: RoomDimensions
    boundary_polygon: List[Tuple[float, float]]
    walls: List[WallSegment]
    export_paths: dict = Field(default_factory=dict)
