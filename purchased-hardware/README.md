# ARIA — Linh kiện đã mua và CAD

> **Đây là nguồn duy nhất trong repo cho linh kiện ĐÃ MUA, số lượng và CAD tương ứng.**
> Không sao chép bảng này sang file khác. ESP32 chưa mua nên không nằm trong bảng.

Cập nhật: 2026-08-10
Phạm vi: **15 hạng mục / 27 đơn vị vật lý**
Tổng chi phí đã ghi nhận: **khoảng ¥89,080** (gồm phí/thuế đơn truyền động; không dùng để suy ra giá từng dòng)

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

## Kết quả đối chiếu CAD

- **1 file đúng tên model nhưng chưa xác minh kích thước:** Camera Module 3 Wide NoIR.
- **1 file sai một phần:** Raspberry Pi 5 ghép với **Official Active Cooler**, không khớp cooler **Smraza** đã mua.
- **1 file không thuộc đồ đã mua:** [ESP32-S3-DevKitC-1](cad-review/not-purchased/esp32-s3-devkitc-1_UNMATCHED.dwg). ESP32 chưa mua nên bị loại khỏi inventory. File vẫn được giữ vì là dữ liệu độc nhất chưa có bản thay thế.
- **13 hạng mục hoàn toàn chưa có CAD trong repo.**
- **Không phát hiện CAD trùng SHA-256** trong ba file đã nhập.
- **Chưa có CAD nào được xác minh đủ để chế tạo.**

### Dấu vết ba file CAD đã nhập

| Phân loại | File repo | File gốc đã ghi nhận | SHA-256 | Quyết định |
|---|---|---|---|---|
| Ứng viên đúng model | `cad/05-raspberry-pi-camera-module-3-wide-noir.dwg` | `ARIA-SEN-001_Camera-Module-3-Wide-NoIR_colored.dwg` | `D3B28B76AD57CCA2DB5FC2A12D78417A592557A5F56D5D4C3DAAEA016415A2BE` | Giữ; cần đo/đối chiếu datasheet. |
| Sai một phần | `cad-review/01-raspberry-pi-5-with-official-cooler_UNVERIFIED-MISMATCH.dwg` | `ARIA-CPU-001_colored-final.dwg` | `54B941F2210CF043CEC7F9E826D32738850710780BBC9B49B460F33F7F667A4F` | Giữ; không coi là CAD của cooler đã mua. |
| Không thuộc đồ đã mua | `cad-review/not-purchased/esp32-s3-devkitc-1_UNMATCHED.dwg` | `Drawing4.dwg esp32 s3.dwg` | `3CDCF4305BB62F79AA52780F26449277D7CE0F3542CB31A376870152A3DFDFDB` | Giữ vì độc nhất; loại khỏi inventory. |

## Quy tắc duy trì

1. Chỉ thêm một dòng khi có bằng chứng đã đặt/mua.
2. Model, số lượng và trạng thái CAD chỉ sửa trong file này.
3. Không tạo BOM, purchase register hoặc CAD-status thứ hai.
4. Không gọi CAD là “verified” nếu chưa kiểm units, kích thước tổng, lỗ bắt, đầu nối và keep-out.
5. Không đưa linh kiện dự kiến mua vào bảng. **ESP32 hiện chưa mua.**
