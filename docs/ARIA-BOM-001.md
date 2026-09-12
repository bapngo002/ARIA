# ARIA-BOM-001 — BOM và trạng thái phần cứng canonical

> **Đây là nguồn chuẩn duy nhất cho BOM, trạng thái phần cứng hiện hành, linh kiện đã mua, số lượng và CAD tương ứng.**
> Không sao chép bảng này sang file khác. ESP32-S3 N16R8 đã được bổ sung ở dòng 16.

Cập nhật: 2026-09-13

**Cập nhật hiện hành 2026-09-13, thay thế trạng thái nhận hàng/sự cố cũ bên dưới:** người dùng xác nhận đã có ESP thay thế cùng loại YD N16R8; không suy ra thêm số lượng mua hoặc giá. Encoder AS5600 bên trái hỏng, bên phải còn nối và đang chờ kiểm tra sau đổi chân; chưa xác nhận đã thay encoder trái. INA260 ×1 đã có và nối Pi; ảnh terminal xác nhận mã nhận dạng tại địa chỉ 0x40. Chi tiết số đo và giới hạn kiểm chứng nằm trong master. Các ghi chú “chưa nhận hàng” INA260 và “chưa xác nhận nhận board thay thế” trong snapshot dưới đây là lịch sử đã superseded.

Tiến độ, kết quả test và migration gaps nằm trong [MASTER HANDOFF](ARIA-MASTER-HANDOFF.md); không suy ra tiến độ dự án từ bảng mua hàng này.
Phạm vi bảng đã mua có hồ sơ trước migration (không phải toàn bộ phần cứng live): **15 hạng mục / 28 đơn vị ở snapshot lịch sử** (trước điều chỉnh INA260 xuống 1; không phải tổng đã nhận hiện tại); không cộng lại phần bảo vệ tích hợp trong cụm pin. Bánh xe hiện hành được ghi riêng bên dưới do chưa có số lượng mua được xác nhận.
Tổng chi phí đã ghi nhận: **khoảng ¥90,576** (gồm phí/thuế đơn truyền động; không dùng để suy ra giá từng dòng)

## Danh sách đã mua

| # | Nhóm | Linh kiện / model đã mua | SL | CAD hiện có | Kết luận |
|---:|---|---|---:|---|---|
| 1 | Compute | Raspberry Pi 5 4GB | 1 | [Pi 5 + Official Cooler](../purchased-hardware/cad-review/01-raspberry-pi-5-with-official-cooler_UNVERIFIED-MISMATCH.dwg) | **Sai một phần:** cooler trong file là loại chính hãng, cooler mua là Smraza; chưa kiểm kích thước. |
| 2 | Power sensing | Board INA260 đo dòng điện / điện áp / công suất qua I²C; DigiKey **1528-2955-ND**; board code **4226** | 1 | — | **Đã có, đã nối Pi** theo xác nhận 2026-09-13; mã nhận dạng INA260 đọc được tại **0x40**. Chưa xác minh routing IN+/IN−, độ chính xác hoặc full-load bench. Thiếu CAD/revision. |
| 3 | Thermal | Smraza Active Cooler cho Raspberry Pi 5, 5V PWM 4-pin | 1 | — | Thiếu. |
| 4 | Power | Pololu D24V90F5, 5V/9A | 1 | — | Thiếu. |
| 5 | Vision | Raspberry Pi Camera Module 3 Wide NoIR | 1 | [DWG](../purchased-hardware/cad/05-raspberry-pi-camera-module-3-wide-noir.dwg) | Đúng tên model; chưa kiểm scale, lỗ bắt, lens keep-out và kích thước. |
| 7 | Audio input | reSpeaker / XMOS XVF3800 4-Mic Array | 1 | — | Thiếu; cần xác minh revision/USB variant. |
| 8 | Audio output | Loa thay thế JBL GO2 | 1 | — | Thiếu; cần đo outline, lỗ bắt, trở kháng và đầu nối. |
| 9 | Charging | Module IP2368, 3S USB-C PD, hai chiều 100W theo listing | 1 | — | Thiếu; cần xác minh board/revision. |
| 10 | Amplifier | Module MAX98357A I²S Class-D | 2 | — | **2 board mới, cả 2 đều OK** theo xác nhận của người dùng; thiếu CAD, cần xác minh layout board cụ thể. |
| 11 | Display | Waveshare Round DSI 4-inch, cảm ứng điện dung | 1 | — | Thiếu; chưa xác minh revision và bộ cáp. |
| 12 | Battery cells | Cell 18650, listing ghi “35E / 3.7V / 3000mAh” | 10 | — | Thiếu; tên 35E và dung lượng 3000mAh mâu thuẫn, phải kiểm mã in/capacity khi nhận. |
| 13 | IMU | Adafruit BNO085 9-DOF breakout | 1 | — | Thiếu. |
| 14 | Drive | DFRobot FIT1035 2208 BLDC, tích hợp encoder từ AS5600 | 2 | — | Thiếu; không cần encoder rời. |
| 15 | Motor driver | DFRobot DRI0058 SimpleFOCMini | 2 | — | Thiếu. |
| 16 | Real-time control | YD-ESP32-S3 / ESP32-S3-WROOM-1-N16R8, 44 chân, dual USB-C ([đơn hàng](../purchased-hardware/evidence/16-esp32-s3-n16r8-order.png), [pinout](../purchased-hardware/evidence/16-esp32-s3-n16r8-pinout.png)) | 1 | [Bộ CAD 2D/3D](../purchased-hardware/cad-review/16-yd-esp32-s3-n16r8/README.md) | Đã đặt ngày 2026-08-07, ¥1,496; họ PCB canonical theo ảnh. **Board cũ cháy; người dùng xác nhận đã có board thay thế cùng loại YD N16R8 ngày 2026-09-13. Chưa có hồ sơ giá/số lượng mua mới; không cộng thêm số lượng mua.** Báo cáo test trước sự cố là lịch sử. Chưa đối chiếu exact revision của board test; CAD còn phải đo bo thực tế. |

## Cấu hình hiện hành do người dùng xác nhận

Cấu hình được chốt ngày 2026-09-11 và bổ sung từ migration snapshot ngày 2026-09-12 theo xác nhận của người dùng. Các ID trong bảng đã mua được giữ ổn định để không làm sai tham chiếu CAD; ID 6 được bỏ khỏi bảng linh kiện rời, xem phần nội bộ pin bên dưới. Tổng chi phí vẫn là số đã ghi nhận, không suy ra chi phí mới từ thay đổi cách đếm.

### Bổ sung cấu hình live từ migration 2026-09-12

Nguồn: xác nhận trực tiếp của người dùng trong yêu cầu migration; xem evidence/mức test ở master handoff. Không cộng các mục sau vào tổng 15 hạng mục / 28 đơn vị hoặc tổng chi phí cũ khi chưa có hồ sơ mua đối chiếu.

- microSD **128GB** đang dùng trên Pi; chưa có exact SKU/hồ sơ mua ở repo. Thay spec 64GB trong lịch sử.
- **BME280** là sensor môi trường hiện hành; chưa có exact board/revision, số lượng mua và CAD được đối chiếu. SHT45 lịch sử không phải cấu hình live.
- **VL53L1X ×4** theo snapshot người dùng; chưa có carrier/revision, hồ sơ mua và CAD. Không tiếp tục dùng số lượng 6 từ BOM cũ như inventory hiện tại.
- **AS5600 ×2**: bảng dòng 14 ghi tích hợp trong hai FIT1035; không cộng thêm encoder rời.
- Màn hình AliExpress đã chạy theo snapshot; tên Waveshare ở dòng 11 là định danh đang lưu, exact revision/bộ cáp và vùng tròn cần đối chiếu, không tự thay model.

Số lượng INA260 hiện hành: **1 board**, theo điều chỉnh trực tiếp của người dùng ngày 2026-09-12; thay cho số lượng 2 trước đó. Board đã có, nối vào Pi và được nhận dạng tại 0x40 theo bằng chứng người dùng ngày 2026-09-13; routing IN+/IN−, ALERT và accuracy/full-load chưa xác nhận. Tổng chi phí lịch sử không được tự giảm khi chưa có hồ sơ đơn hàng cập nhật.

### Bánh xe

- Loại lốp: **gravel tire**.
- Đường kính ngoài **Ø60 mm**, bề rộng lốp **22 mm**.
- Ảnh được người dùng mô tả ghi **center/hub dimension 12 mm**; chưa xác định đó là đường kính lỗ trục hay kích thước khác của hub.
- Khối lượng ghi trên ảnh: **108.8 g/set**; chưa xác nhận số bánh trong một set, không diễn giải thành khối lượng mỗi bánh.
- Số lượng mua, mã sản phẩm và CAD chưa được xác nhận trong lần cập nhật này. Dùng thông số hiện hành để lập kế hoạch cơ khí; đo bánh/hub thực tế trước khi chốt lắp ghép.

### Nội bộ cụm pin, bảo vệ và sạc

- **BMS 3S đã tích hợp bên trong cụm pin**, không phải linh kiện standalone trong BOM hoặc hardware summary.
- Chỉ đề cập BMS trong nội bộ pin, bảo vệ, sạc hoặc ghi chú lịch sử. Kiểm tra chức năng bảo vệ của cụm pin khi thử nguồn/sạc.
- Kiến trúc **3S**; kế hoạch **18650 3S3P / 9 cell**, candidate **Samsung INR18650-35E** theo migration snapshot, chỉ **planned/not confirmed inventory**. Không có xác nhận pack đã lắp đúng cấu hình này.
- Thông tin 10 cell đã ghi nhận trong bảng không tự xác định cấu hình lắp pack, số cell dự phòng hoặc xác nhận Samsung 35E chính hãng; mâu thuẫn listing vẫn mở.

### Lịch sử thay đổi / superseded

- INA226 đã được thay thế hoàn toàn bởi INA260 ×1 tại dòng 2; không dùng INA226 trong thiết kế, wiring hoặc firmware hiện hành.
- Trạng thái MAX98357A cũ “1 tốt, 1 hỏng” đã bị thay thế bởi 2 board mới, cả 2 đều OK.
- Bánh xe Ø40 × 20 mm đã obsolete; thông số hiện hành nằm ở mục Bánh xe.
- Dòng BMS rời ID 6 trước đây ghi 3S Li-ion, 20A + NTC. Đây là dữ liệu lịch sử, không xác nhận rating/model của BMS bên trong cụm pin hiện tại.
- BOM được đưa về `docs/ARIA-BOM-001.md`; `purchased-hardware/README.md` chỉ dẫn tới nguồn chuẩn này.

## Kết quả đối chiếu CAD

Các đường dẫn trong cột File repo bên dưới tính từ `purchased-hardware/`.

- **1 file đúng tên model nhưng chưa xác minh kích thước:** Camera Module 3 Wide NoIR.
- **1 file sai một phần:** Raspberry Pi 5 ghép với **Official Active Cooler**, không khớp cooler **Smraza** đã mua.
- **1 bộ CAD đúng họ PCB YD-ESP32-S3 N16R8:** ảnh pinout xác nhận 44 chân, dual USB-C và RGB GPIO48. DWG DevKitC-1 cũ sai PCB đã bị thay bằng DWG/DXF 2D và STEP 3D kích thước danh nghĩa; vẫn nằm trong `cad-review/` cho đến khi đo bo thực tế.
- **12 hạng mục trong bảng đã mua hoàn toàn chưa có CAD trong repo.** Bánh xe hiện hành cũng chưa có CAD; chưa tính vào bảng đã mua vì chưa xác nhận số lượng.
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
3. Không tạo BOM, purchase register hoặc CAD-status thứ hai. Các tài liệu kỹ thuật dẫn tới BOM này; cấu hình người dùng đã chốt nhưng chưa đủ dữ liệu mua được ghi ở phần cấu hình hiện hành, không tự thêm số lượng vào bảng đã mua.
4. Không gọi CAD là “verified” nếu chưa kiểm units, kích thước tổng, lỗ bắt, đầu nối và keep-out.
5. Không đưa linh kiện dự kiến mua vào bảng. ESP32-S3 ở dòng 16 đã xác định đúng họ YD-N16R8 nhưng vẫn phải đo PCB/revision thực tế khi nhận.
