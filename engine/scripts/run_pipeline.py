import argparse
import json
import sys
from roomscan_engine.pipeline import RoomScanPipeline

def main():
    parser = argparse.ArgumentParser(description="Run RoomScan AI 3D Reconstruction Pipeline")
    parser.add_argument("--input", required=True, help="Path to input room scan video or image directory")
    parser.add_argument("--config", default="configs/default.yaml", help="Path to YAML configuration file")
    parser.add_argument("--room-id", default="room_001", help="Identifier for the target room")
    args = parser.parse_args()

    pipeline = RoomScanPipeline(config_path=args.config)
    result = pipeline.process_video(video_path=args.input, room_id=args.room_id)
    
    print("\n--- [RoomScan Result Summary] ---")
    print(json.dumps(result.model_dump(), indent=2))

if __name__ == "__main__":
    main()
