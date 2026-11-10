#!/usr/bin/env python3
"""
Sample Scene Downloader for RoomScan AI
Downloads a verified real-world indoor room sequence from Apple ARKitScenes dataset:
- RGB frames (normal camera simulation)
- LiDAR depth maps (hardware ground truth)
- Camera intrinsics & 6DoF trajectory/poses
- Ground truth 3D mesh (.ply)
"""

import os
import sys
import subprocess
import zipfile
import shutil

VIDEO_ID = "42445173"
BASE_URL = "https://docs-assets.developer.apple.com/ml-research/datasets/arkitscenes/v1"
ZIP_URL = f"{BASE_URL}/threedod/Training/{VIDEO_ID}.zip"
MESH_URL = f"{BASE_URL}/raw/Training/{VIDEO_ID}/{VIDEO_ID}_3dod_mesh.ply"

TARGET_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_room")
)

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, check=True)
    return result

def download_file(url, output_path):
    print(f"--> Downloading: {url}")
    print(f"    Destination: {output_path}")
    curl_cmd = f'curl -L --progress-bar "{url}" -o "{output_path}"'
    run_cmd(curl_cmd)

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    zip_path = os.path.join(TARGET_DIR, f"{VIDEO_ID}.zip")
    mesh_path = os.path.join(TARGET_DIR, "ground_truth_mesh.ply")

    print("==================================================")
    print("   RoomScan AI - Sample Room Dataset Downloader   ")
    print("   Source: Apple ARKitScenes Indoor Dataset       ")
    print(f"   Target Directory: {TARGET_DIR}")
    print("==================================================")

    # 1. Download Room Data Zip (RGB, LiDAR, Poses, Intrinsics)
    if not os.path.exists(zip_path) and not os.path.exists(os.path.join(TARGET_DIR, VIDEO_ID)):
        download_file(ZIP_URL, zip_path)
    else:
        print("[Info] Room archive already downloaded.")

    # 2. Extract Archive
    extracted_folder = os.path.join(TARGET_DIR, VIDEO_ID)
    if not os.path.exists(extracted_folder):
        print(f"--> Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TARGET_DIR)
        print("--> Extraction complete.")
        # Remove zip to save disk space
        if os.path.exists(zip_path):
            os.remove(zip_path)

    # 3. Download Ground Truth 3D Mesh
    if not os.path.exists(mesh_path):
        download_file(MESH_URL, mesh_path)
    else:
        print("[Info] Ground truth 3D mesh already exists.")

    print("\n==================================================")
    print("✅ Download & Setup Finished Successfully!")
    print(f"📁 Files available at: {TARGET_DIR}")
    print("==================================================")

if __name__ == "__main__":
    main()
