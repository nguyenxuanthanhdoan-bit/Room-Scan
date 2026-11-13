#!/usr/bin/env python3
"""
Feasibility Verification Script - RoomScan AI
Demonstrates in ~45 lines of Python:
1. Back-projection from 2D RGB-D to 3D Point Cloud.
2. Open3D RANSAC Plane Segmentation to automatically extract the floor and highlight it in RED.
"""

import os
import numpy as np
from PIL import Image
import open3d as o3d

def main():
    base_dir = "/Users/test/Documents/SCIC/RoomScan/data/sample_room/42445173/42445173_frames"
    frame_name = "42445173_8098.954"

    rgb_path = os.path.join(base_dir, "lowres_wide", f"{frame_name}.png")
    depth_path = os.path.join(base_dir, "lowres_depth", f"{frame_name}.png")
    intrinsic_path = os.path.join(base_dir, "lowres_wide_intrinsics", f"{frame_name}.pincam")
    output_ply = "/Users/test/Documents/SCIC/RoomScan/data/sample_room/feasibility_test.ply"

    print("=== [RoomScan AI] Feasibility Proof ===")
    print(f"Loading Frame: {frame_name}")

    # 1. Read Intrinsics (width, height, fx, fy, cx, cy)
    with open(intrinsic_path) as f:
        w, h, fx, fy, cx, cy = map(float, f.read().split())

    # 2. Read RGB and Depth images
    rgb_img = Image.open(rgb_path).convert("RGB")
    depth_img = Image.open(depth_path)

    rgb = np.array(rgb_img, dtype=np.float32) / 255.0  # normalize to [0, 1]
    depth = np.array(depth_img, dtype=np.float32) / 1000.0  # mm to meters

    # 3. Mathematical Back-projection (2D Pixels -> 3D Points in meters)
    H, W = depth.shape
    u, v = np.meshgrid(np.arange(W), np.arange(H))
    
    valid = (depth > 0.1) & (depth < 6.0)  # filter valid range (0.1m - 6.0m)
    z = depth[valid]
    x = (u[valid] - cx) * z / fx
    y = -(v[valid] - cy) * z / fy  # flip y for standard 3D upright orientation

    points = np.stack([x, y, z], axis=-1)
    colors = rgb[valid]

    print(f"Generated {len(points):,} 3D points from a single 2D camera frame.")

    # 4. Create Open3D PointCloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # 5. RANSAC Plane Segmentation: Find the dominant flat plane (Floor)
    print("Running RANSAC plane segmentation (finding floor/surface)...")
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.03, ransac_n=3, num_iterations=1000)
    a, b, c, d = plane_model
    print(f"Plane Equation found: {a:.3f}x + {b:.3f}y + {c:.3f}z + {d:.3f} = 0")
    print(f"Detected {len(inliers):,} points belonging to the plane.")

    # Color the detected plane RED to visually prove the algorithm found it
    colors_mod = np.asarray(pcd.colors).copy()
    colors_mod[inliers] = [1.0, 0.1, 0.1]  # Bright Red
    pcd.colors = o3d.utility.Vector3dVector(colors_mod)

    # 6. Save the resulting 3D model
    o3d.io.write_point_cloud(output_ply, pcd)
    print(f"Saved feasibility 3D model to: {output_ply}")
    print("========================================")

if __name__ == "__main__":
    main()
