# 🏗️ RoomScan AI

> **Field Survey to SketchUp in 2 Minutes.**  
> Smartphone-based 3D spatial digitizer, rapid pre-sales staging, and CAD-ready layout generator tailored for interior designers and renovation contractors.

---

## 📌 Overview & Core Value
RoomScan AI eliminates the manual, error-prone workflow of measuring interior spaces with measuring tape and re-drafting empty room shells in CAD/SketchUp.

1. **At the Site (2-Minute Scan):** Scan the room via smartphone camera. The AI-driven geometric pipeline reconstructs a metric digital twin and snaps walls to 90° orthogonal boundaries.
2. **Pre-sales Staging & Closing:** Drag-and-drop modular interior elements to verify walkways and generate preliminary estimates on-site to secure client deposits.
3. **Office Handoff (SketchUp Integration):** Direct export of watertight, clean 3D solid geometry (`.obj`, `.dxf`, `.skp`) into SketchUp without redrawing from scratch.

---

## 🏛️ System Architecture

```text
RoomScan/
├── contracts/          # Versioned data schemas (JSON Schemas) shared across components
├── engine/             # Core AI & 3D Computational Geometry Pipeline (Python, Open3D, Depth)
├── benchmarks/         # Real-world ground truth benchmark suite (Laser measure validation)
├── backend/            # FastAPI orchestration service, database, worker queue
├── mobile/             # Flutter mobile application (Camera capture & 3D AR staging)
├── web/                # React + Three.js web dashboard for office desktop workflow
└── docs/               # System architecture and technical decisions
```

---

## 🚀 Technical Highlights (Engine)
- **Monocular Metric Depth:** Vision Transformer-based depth estimation (Depth Anything V2).
- **RANSAC Plane Extraction:** Open3D-powered spatial clustering separating floor, ceiling, and bounded vertical walls from furniture clutter.
- **Manhattan World Alignment:** Orthogonal plane snapping to enforce clean 90° room contours and closed polygon intersection.
- **Parametric Solid Extrusion:** Height-bounded solid mesh generation ready for SketchUp / CAD imports.

---

## 🛠️ Quickstart (Engine Development)

```bash
cd engine
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Run the pipeline on a test video / image sequence
python scripts/run_pipeline.py --input sample_data/room_video.mp4 --config configs/default.yaml
```

---

## 👥 Team & Responsibilities
- **Core AI & 3D Geometry Engine:** Monocular depth, point cloud filtering, RANSAC plane extraction, orthogonal alignment, and CAD export.
- **Backend & Cloud Infrastructure:** FastAPI, async task queues, storage integration, and GPU deployment.
- **Mobile Client:** Flutter app, camera capture guidance, and real-time interactive 3D viewer.
