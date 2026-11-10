from fastapi import FastAPI, BackgroundTasks, UploadFile, File
import uuid

app = FastAPI(
    title="RoomScan AI Orchestration API",
    version="1.0.0",
    description="Backend API Gateway coordinating mobile uploads, 3D reconstruction jobs, and project management"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "roomscan-backend"}

@app.post("/api/v1/scans/upload")
async def upload_scan_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    scan_id = str(uuid.uuid4())
    # In production: store file to S3/MinIO and queue worker job
    return {
        "scan_id": scan_id,
        "filename": file.filename,
        "status": "QUEUED",
        "message": "Scan uploaded successfully. 3D geometry engine job dispatched."
    }

@app.get("/api/v1/scans/{scan_id}/result")
def get_scan_result(scan_id: str):
    # Returns result conforming to contracts/room_layout.v1.json
    return {
        "scan_id": scan_id,
        "status": "COMPLETED",
        "room_layout_url": f"/storage/results/{scan_id}.json",
        "sketchup_export_url": f"/storage/exports/{scan_id}.obj"
    }
