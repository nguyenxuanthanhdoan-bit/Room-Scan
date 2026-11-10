from typing import Protocol, List
import numpy as np
from roomscan_engine.core.types import Frame, RoomLayoutResult

class DepthEstimator(Protocol):
    """Interface for depth estimation backends (Depth Anything, ARKit LiDAR, etc.)."""
    def estimate(self, image: np.ndarray) -> np.ndarray:
        """Returns 2D depth map (float32, metric distance in meters)."""
        ...

class PlaneDetector(Protocol):
    """Interface for plane segmentation and boundary extraction."""
    def extract_planes(self, point_cloud: np.ndarray) -> List[dict]:
        """Identifies floor, ceiling, and bounded vertical wall candidate planes."""
        ...

class WallSnapper(Protocol):
    """Interface for geometric orthogonal regularization (Manhattan World)."""
    def snap_and_close_polygon(self, raw_lines: List[dict]) -> List[tuple]:
        """Snaps walls to 90 degrees and closes boundary polygon."""
        ...

class MeshExporter(Protocol):
    """Interface for CAD / SketchUp file exporters."""
    def export(self, layout: RoomLayoutResult, output_dir: str) -> dict:
        """Exports 3D solid model (.obj, .dxf) and returns file paths."""
        ...
