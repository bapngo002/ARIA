# CAD — YD-ESP32-S3 N16R8

Trạng thái: **đúng họ PCB đã đặt, hình học danh nghĩa; chưa duyệt để chế tạo vỏ**.

## Nhận dạng

- Ảnh đơn hàng xác nhận tùy chọn `ESP32S3 N16R8`.
- [Ảnh pinout](../../evidence/16-esp32-s3-n16r8-pinout.png) cho thấy module `ESP32-S3-WROOM-1-N16R8`, 44 chân, hai cổng USB-C đặt cạnh nhau và RGB ở GPIO48.
- Bố trí này khớp họ `YD-ESP32-S3` của VCC-GND Studio; **không phải PCB Espressif ESP32-S3-DevKitC-1 chính hãng**.

## File giữ lại

- [`16-yd-esp32-s3-n16r8_dimensions.dwg`](16-yd-esp32-s3-n16r8_dimensions.dwg): bản vẽ 2D AutoCAD 2018.
- [`16-yd-esp32-s3-n16r8_dimensions.dxf`](16-yd-esp32-s3-n16r8_dimensions.dxf): nguồn 2D có layer và kích thước.
- [`16-yd-esp32-s3-n16r8_board.step`](16-yd-esp32-s3-n16r8_board.step): mô hình 3D board và bao linh kiện chính, không gồm header rời.
- [`16-yd-esp32-s3-n16r8_preview.png`](16-yd-esp32-s3-n16r8_preview.png): ảnh xem nhanh.

## Kích thước danh nghĩa

- PCB: **63.50 × 27.94 × 1.60 mm** (2.5 × 1.1 inch).
- Hai hàng, mỗi hàng 22 lỗ; pitch **2.54 mm**.
- Khoảng cách tâm hai hàng: **25.40 mm**.
- Lỗ header: **Ø1.00 mm**.
- Module WROOM-1: **18.00 × 25.50 mm**.
- Bao tổng có phần antenna: khoảng **27.94 × 70.00 mm**.
- PCB không có lỗ bắt vít.

Vị trí USB-C, nút nhấn và linh kiện nhỏ được tỷ lệ hóa từ ảnh, chỉ dùng kiểm tra va chạm sơ bộ. Sau khi nhận hàng phải đo lại bằng thước cặp trước khi khóa lỗ mở hoặc khoảng hở nhỏ hơn **±0.30 mm**.

## Kiểm tra file

- DWG đã được chuyển ngược sang DXF và audit thành công: 44 lỗ, 4 polyline, 7 đường kích thước và 6 ghi chú được giữ nguyên.
- SHA-256 DWG: `AC02E1AB0A3A8603DE5E4D959B0803804FB58B2BC3D3EA54220BD1A12CFD2851`
- SHA-256 DXF: `65C7996A3B58E00D73CCCD8FBEDDDFAD488881823C82CADE1EAF6D154DCFAF1D`
- SHA-256 STEP: `3F0E1DCD6B1FAE7410FC7D64DFDACE371CCCE45C28A794D921B2933200553FEF`

Nguồn đối chiếu: [YD-ESP32-S3 N16R8 trên CircuitPython](https://circuitpython.org/board/yd_esp32_s3_n16r8/), [tài liệu nhận dạng/pinout họ YD-ESP32-S3](https://github.com/profharris/YD-ESP32-S3_ESP32-S3-WROOM-1_Dev), và [tài liệu Espressif DevKitC-1 dùng để phân biệt PCB](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html).
