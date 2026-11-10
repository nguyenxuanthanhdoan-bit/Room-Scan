# 🏗️ RoomScan AI

> **Nền tảng Số hoá Không gian & Hỗ trợ Chốt Hợp đồng Nội thất (Sales Enablement & Pre-sales 3D Staging)**  
> Biến căn phòng thực tế thành mô hình 3D trong 2 phút, trực quan hoá thành phẩm từ kho dữ liệu riêng của xưởng để khách hàng xem trước và chốt cọc ngay tại hiện trường.

---

## 🎯 Định Vị & Mục Tiêu Cốt Lõi

RoomScan AI **sinh ra không phải để thay thế hoàn toàn thước đo laser hay quy trình đo tay truyền thống** ở khâu sản xuất lắp ráp (vốn đòi hỏi dung sai khắt khe từng milimet). 

Mục tiêu số 1 của RoomScan AI là **giải quyết bài toán Chốt hợp đồng & Tiết kiệm thời gian ở khâu Khảo sát ban đầu (Pre-sales)**:

1. **Quét phòng 2 phút bằng điện thoại:** Dựng nhanh bản sao số (Metric Digital Twin) với kích thước và mặt bằng 2D/3D sơ bộ của căn phòng.
2. **Kho Cơ sở Dữ liệu Riêng cho Từng Xưởng (Custom Workshop Catalog):** 
   - Mỗi xưởng mộc / công ty kiến trúc sở hữu một kho dữ liệu sản phẩm riêng biệt (thư viện module nội thất, mẫu tủ áo, tủ bếp, bàn ghế, mã ván An Cường/Ba Thanh, và chính sách đơn giá thi công của chính họ).
   - Đảm bảo **100% đồ đạc hiển thị là đồ thật xưởng tự sản xuất được**, không dùng AI vẽ ảo.
3. **Trực quan hoá thành phẩm tại hiện trường để chốt cọc:** 
   - Khách hàng không cần đọc bản vẽ 2D khô khan. KTS kéo-thả đồ từ catalog của xưởng vào căn phòng thực tế của khách hàng $\rightarrow$ Khách nhìn thấy trước ngôi nhà tương lai của mình.
   - Xuất ngay bảng báo giá sơ bộ khớp với đơn giá xưởng để khách an tâm xuống tiền đặt cọc thiết kế/thi công.
4. **Cầu nối dẫn vào SketchUp:** Xuất file 3D vỏ phòng sạch sẽ (`.obj`, `.dxf`, `.skp`) để KTS mở máy tính lên chau chuốt chi tiết mà không phải tốn 1-2 tiếng dựng lại xác nhà thô.

---

## 🏛️ Kiến Trúc Hệ Thống (Monorepo)

```text
RoomScan/
├── contracts/          # Bản hợp đồng dữ liệu chuẩn hóa (JSON Schemas) dùng chung cho cả team
├── engine/             # Lõi AI & Xử lý Hình học 3D (Depth Anything V2, Open3D RANSAC, 90° Snapping)
├── benchmarks/         # Bộ kiểm nghiệm thực tế đo sai số với thước laser (Ground Truth)
├── backend/            # FastAPI, Quản lý kho dữ liệu xưởng (Catalog DB), Hàng đợi GPU Worker
├── mobile/             # Flutter App: Quay video hướng dẫn, 3D Viewer & Kéo-thả nội thất tại hiện trường
├── web/                # React + Three.js: Dashboard quản lý dự án & Kho vật liệu xưởng trên Desktop
└── docs/               # Tài liệu kỹ thuật, kiến trúc và thuyết minh SCIC
```

---

## 🚀 Điểm Nhấn Công Nghệ (Engine)

- **Monocular Metric Depth:** Ứng dụng mô hình Vision Transformer (Depth Anything V2) để suy luận độ sâu không gian từ camera điện thoại thông thường (không bắt buộc LiDAR).
- **RANSAC Plane Extraction:** Thuật toán phân cụm điểm không gian với Open3D để bóc tách mặt sàn, trần và các diện tường chính, loại bỏ nhiễu đồ đạc bừa bộn.
- **Manhattan World Alignment:** Nắn phẳng các bức tường về góc vuông $90^\circ$ và tính toán giao tuyến khép kín đa giác phòng.
- **Parametric CAD Exporter:** Tạo khối 3D solid chuẩn kích thước xuất thẳng sang SketchUp / AutoCAD.
