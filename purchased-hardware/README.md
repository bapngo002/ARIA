# ARIA — Linh kiện đã mua và CAD

> **Đây là nguồn duy nhất trong repo cho linh kiện ĐÃ MUA, số lượng và CAD tương ứng.**
> Không sao chép bảng này sang file khác. ESP32-S3 N16R8 đã được bổ sung ở dòng 16.

Cập nhật: 2026-08-10
Phạm vi: **16 hạng mục / 28 đơn vị vật lý**
Tổng chi phí đã ghi nhận: **khoảng ¥90,576** (gồm phí/thuế đơn truyền động; không dùng để suy ra giá từng dòng)

## Danh sách đã mua

| # | Nhóm | Linh kiện / model đã mua | SL | CAD hiện có | Kết luận |
|---:|---|---|---:|---|---|
| 1 | Compute | Raspberry Pi 5 4GB | 1 | [Pi 5 + Official Cooler](cad-review/01-raspberry-pi-5-with-official-cooler_UNVERIFIED-MISMATCH.dwg) | **Sai một phần:** cooler trong file là loại chính hãng, cooler mua là Smraza; chưa kiểm kích thước. |
| 2 | Power sensing | Module INA226, I²C, 0–36V | 1 | — | Thiếu; cần xác minh board/shunt cụ thể. |
| 3 | Thermal | Smraza Active Cooler cho Raspberry Pi 5, 5V PWM 4-pin | 1 | — | Thiếu. |
| 4 | Power | Pololu D24V90F5, 5V/9A | 1 | — | Thiếu. |
| 5 | Vision | Raspberry Pi Camera Module 3 Wide NoIR | 1 | [DWG](cad/05-raspberry-pi-camera-module-3-wide-noir.dwg) | Đúng tên model; chưa kiểm scale, lỗ bắt, lens keep-out và kích thước. |
| 6 | Battery protection | BMS 3S Li-ion, 20A + NTC | 1 | — | Thiếu; hãng/model chính xác chưa được ghi nhận. |
| 7 | Audio input | reSpeaker / XMOS XVF3800 4-Mic Array | 1 | — | Thiếu; cần xác minh revision/USB variant. |
| 8 | Audio output | Loa thay thế JBL GO2 | 1 | — | Thiếu; cần đo outline, lỗ bắt, trở kháng và đầu nối. |
| 9 | Charging | Module IP2368, 3S USB-C PD, hai chiều 100W theo listing | 1 | — | Thiếu; cần xác minh board/revision. |
| 10 | Amplifier | Module MAX98357A I²S Class-D | 2 | — | Thiếu; cần xác minh layout board cụ thể. |
| 11 | Display | Waveshare Round DSI 4-inch, cảm ứng điện dung | 1 | — | Thiếu; chưa xác minh revision và bộ cáp. |
| 12 | Battery cells | Cell 18650, listing ghi “35E / 3.7V / 3000mAh” | 10 | — | Thiếu; tên 35E và dung lượng 3000mAh mâu thuẫn, phải kiểm mã in/capacity khi nhận. |
| 13 | IMU | Adafruit BNO085 9-DOF breakout | 1 | — | Thiếu. |
| 14 | Drive | DFRobot FIT1035 2208 BLDC, tích hợp encoder từ AS5600 | 2 | — | Thiếu; không cần encoder rời. |
| 15 | Motor driver | DFRobot DRI0058 SimpleFOCMini | 2 | — | Thiếu. |
| 16 | Real-time control | YD-ESP32-S3 / ESP32-S3-WROOM-1-N16R8, 44 chân, dual USB-C ([đơn hàng](evidence/16-esp32-s3-n16r8-order.png), [pinout](evidence/16-esp32-s3-n16r8-pinout.png)) | 1 | [Bộ CAD 2D/3D](cad-review/16-yd-esp32-s3-n16r8/README.md) | Đã đặt ngày 2026-08-07, ¥1,496, đang chờ giao; đã xác định đúng họ PCB, kích thước CAD còn phải đo lại trên bo thực tế. |

## Kết quả đối chiếu CAD

- **1 file đúng tên model nhưng chưa xác minh kích thước:** Camera Module 3 Wide NoIR.
- **1 file sai một phần:** Raspberry Pi 5 ghép với **Official Active Cooler**, không khớp cooler **Smraza** đã mua.
- **1 bộ CAD đúng họ PCB YD-ESP32-S3 N16R8:** ảnh pinout xác nhận 44 chân, dual USB-C và RGB GPIO48. DWG DevKitC-1 cũ sai PCB đã bị thay bằng DWG/DXF 2D và STEP 3D kích thước danh nghĩa; vẫn nằm trong `cad-review/` cho đến khi đo bo thực tế.
- **13 hạng mục hoàn toàn chưa có CAD trong repo.**
- **Không phát hiện CAD trùng SHA-256** trong các file đang giữ.
- **Chưa có CAD nào được xác minh đủ để chế tạo.**

### Dấu vết CAD đang giữ

| Phân loại | File repo | File gốc đã ghi nhận | SHA-256 | Quyết định |
|---|---|---|---|---|
| Ứng viên đúng model | `cad/05-raspberry-pi-camera-module-3-wide-noir.dwg` | `ARIA-SEN-001_Camera-Module-3-Wide-NoIR_colored.dwg` | `D3B28B76AD57CCA2DB5FC2A12D78417A592557A5F56D5D4C3DAAEA016415A2BE` | Giữ; cần đo/đối chiếu datasheet. |
| Sai một phần | `cad-review/01-raspberry-pi-5-with-official-cooler_UNVERIFIED-MISMATCH.dwg` | `ARIA-CPU-001_colored-final.dwg` | `54B941F2210CF043CEC7F9E826D32738850710780BBC9B49B460F33F7F667A4F` | Giữ; không coi là CAD của cooler đã mua. |
| Đúng họ PCB, kích thước danh nghĩa | `cad-review/16-yd-esp32-s3-n16r8/` | Bộ YD-ESP32-S3 N16R8 đã tạo trên máy | DWG `AC02E1…D2851`; DXF `65C799…AF1D`; STEP `3F0E1D…53FEF` | Thay file DevKitC-1 sai loại; giữ ở review cho đến khi đo bo nhận được. |

## Quy tắc duy trì

1. Chỉ thêm một dòng khi có bằng chứng đã đặt/mua.
2. Model, số lượng và trạng thái CAD chỉ sửa trong file này.
3. Không tạo BOM, purchase register hoặc CAD-status thứ hai.
4. Không gọi CAD là “verified” nếu chưa kiểm units, kích thước tổng, lỗ bắt, đầu nối và keep-out.
5. Không đưa linh kiện dự kiến mua vào bảng. ESP32-S3 ở dòng 16 đã xác định đúng họ YD-N16R8 nhưng vẫn phải đo PCB/revision thực tế khi nhận.
