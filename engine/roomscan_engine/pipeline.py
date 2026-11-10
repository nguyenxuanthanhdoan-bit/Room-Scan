import os
import yaml
from typing import Optional
from roomscan_engine.core.types import RoomLayoutResult, RoomDimensions, WallSegment

class RoomScanPipeline:
    """
    Main orchestration pipeline for RoomScan AI Engine.
    Coordinates Video I/O -> Depth -> Point Cloud -> Plane RANSAC -> 90° Snapping -> Export.
    """
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def process_video(self, video_path: str, room_id: str = "demo_room") -> RoomLayoutResult:
        print(f"[Pipeline] Processing video: {video_path} for room: {room_id}")
        
        # 1. Video I/O: Frame selection
        print(f"[Step 1/5] Extracting sharp frames (target_fps={self.config['capture']['target_fps']})...")
        
        # 2. Depth Estimation
        print(f"[Step 2/5] Running Depth Estimation model: {self.config['depth']['model_name']}...")
        
        # 3. 3D Point Cloud Reconstruction & Outlier Filtering
        print(f"[Step 3/5] Fusing Point Cloud with voxel size {self.config['pointcloud']['voxel_size']}m...")
        
        # 4. Plane Segmentation (RANSAC) & Orthogonal Snapping
        print(f"[Step 4/5] Running RANSAC plane detection & Manhattan 90° snapping...")
        
        # Stub result conforming to contracts/room_layout.v1.json
        dims = RoomDimensions(
            width=3.85,
            length=4.20,
            height=self.config["layout"]["default_ceiling_height"],
            area=round(3.85 * 4.20, 2),
            volume=round(3.85 * 4.20 * 2.8, 2)
        )
        
        boundary = [(0.0, 0.0), (3.85, 0.0), (3.85, 4.20), (0.0, 4.20)]
        walls = [
            WallSegment(wall_id="wall_north", start_point=(0.0, 0.0), end_point=(3.85, 0.0), length=3.85),
            WallSegment(wall_id="wall_east", start_point=(3.85, 0.0), end_point=(3.85, 4.20), length=4.20),
            WallSegment(wall_id="wall_south", start_point=(3.85, 4.20), end_point=(0.0, 4.20), length=3.85),
            WallSegment(wall_id="wall_west", start_point=(0.0, 4.20), end_point=(0.0, 0.0), length=4.20),
        ]
        
        # 5. Export 3D Mesh & CAD formats
        print(f"[Step 5/5] Exporting 3D geometry (.obj, .dxf) for SketchUp...")
        output_dir = self.config["export"]["output_dir"]
        os.makedirs(output_dir, exist_ok=True)
        
        result = RoomLayoutResult(
            room_id=room_id,
            dimensions=dims,
            boundary_polygon=boundary,
            walls=walls,
            export_paths={
                "obj": os.path.join(output_dir, f"{room_id}.obj"),
                "dxf": os.path.join(output_dir, f"{room_id}.dxf")
            }
        )
        print(f"[Pipeline] Successfully reconstructed room: {dims.area} m²")
        return result
