# ARIA — MASTER HANDOFF

**Status: CURRENT/CANONICAL · Migration snapshot: 2026-09-12**

## NEW CHATGPT ACCOUNT BOOTSTRAP

1. Đọc file này trước khi tiếp tục Project ARIA. Sau migration snapshot, **GitHub `bapngo002/ARIA`, branch `main`, là source of truth**.
2. Ưu tiên CURRENT/CANONICAL. Không hồi sinh thông tin HISTORICAL/OBSOLETE từ chat cũ, commit cũ hoặc branch chưa merge.
3. [ARIA-BOM-001](ARIA-BOM-001.md) là nguồn duy nhất cho inventory, model, số lượng, trạng thái mua và CAD. File này quản lý tiến độ, mức kiểm chứng, pinmap, kiến trúc, migration gaps và thứ tự công việc; không suy diễn tiến độ từ BOM.
4. [PRD frozen](ARIA-PRD-001.md) giữ nguyên yêu cầu sản phẩm. Các ghi chú tiến độ trong PRD, đặc biệt mục 10 “M4 — Bench Prototype: chưa bắt đầu”, là historical và không mô tả hiện trạng. Không sửa PRD để đồng bộ tiến độ.
5. VERIFIED/PASSED bên dưới có ghi nguồn. “Người dùng xác nhận” không tương đương log bench được lưu trong repo; không gọi toàn hệ thống là đã chạy ổn định chỉ vì module đã pass riêng.
6. Tiếp tục theo NEXT STEP ORDER. Không bịa code, thông số tuning, địa chỉ I²C, protocol hoặc kết quả test còn thiếu. Khi lấy được code/log thật, commit chúng và cập nhật chính file này; không tạo handoff thứ hai.

## Evidence và phạm vi snapshot

- **E1 — Repo:** toàn bộ cây `main` tại `b0bb686`, BOM hiện hành, ảnh nhận dạng controller và các README/CAD; rà lịch sử `main` và tên file trong lịch sử các remote branches đã fetch. Đây là baseline trước migration, không phải commit kết quả.
- **E2 — Xác nhận người dùng:** yêu cầu MIGRATION SNAPSHOT ngày 2026-09-12 cung cấp trạng thái live/bench, pinmap, phần mềm và cơ khí được ghi dưới đây. Đây là nguồn trực tiếp cho các thông tin chưa có trong repo.
- **E3 — Chat tham chiếu:** [Hủy liên kết thanh toán](https://chatgpt.com/c/6aa3dca7-6bd8-83e8-b3ed-3ec092203901), các lượt gần nhất được đọc khi migration; xác nhận yêu cầu đồng bộ ngược ChatGPT → GitHub và các thay thế phần cứng. Không yêu cầu tài khoản mới truy cập được chat này để hiểu snapshot. Không coi phát biểu “đã kiểm tra/đã cập nhật” của trợ lý cũ là bằng chứng thực thi.
- Không truy cập Pi, không đọc flash ESP32, không chạy bench trong đợt này. Không có log mới hơn trong repo chứng minh motor đã hết nóng/no-spin. Ngày test cũ, phiên bản firmware và điều kiện test chưa được khôi phục.

## CURRENT/CANONICAL

### Trạng thái dự án và kiến trúc

ARIA đã qua nhiều thử nghiệm module thực tế; không còn là dự án chỉ chọn BOM/chờ bắt đầu prototype. Integration, drive reliability, power/safety và CAD cuối vẫn chưa hoàn tất.

- **Pi 5 = high-level brain:** OS, AI/voice, camera, UI, ứng dụng và điều phối hành vi.
- **ESP32-S3 = realtime/safety controller:** motor, encoder, sensor, watchdog và dừng an toàn. Đây là phân công kiến trúc; chưa có bằng chứng toàn bộ chức năng đã triển khai.
- Pi↔ESP32 communication cần ổn định lại. Test từng module độc lập trước khi merge; giữ bản bench pass có thể tái lập.
- Exact controller canonical theo E1: **YD-ESP32-S3 / ESP32-S3-WROOM-1-N16R8**, 44 chân, dual USB-C. E2 xác nhận ESP32 dev/controller đã test GPIO/Wi-Fi/Bluetooth; chưa có ảnh/log gắn lần test với revision/serial cụ thể của YD board. Không suy ra PCB đã đo chỉ từ tên board hoặc test GPIO.

### Pi, giao diện và cảm biến

- Raspberry Pi 5 4GB đã mua và chạy; **Raspberry Pi OS 64-bit**, SSH host **`aria.local`**, microSD **128GB** (E2). Chưa xác minh lại kết nối SSH hoặc OS build trong lần migration.
- Camera Pi test OK. Màn hình mua AliExpress đã chạy; **UI phải nằm trong vùng tròn**. BOM lưu tên màn hình hiện có; chưa có bằng chứng mới để tự đổi model/revision hoặc suy ra kích thước vùng hiển thị thực.
- Microphone board/array thu tiếng rõ. MAX98357A hiện là **2 board mới, cả 2 OK**. IMU và BME280 đã test OK (E2).
- ToF hiện có **4 × VL53L1X** theo E2; mapping XSHUT được bảo tồn dưới đây. Chat báo đã test ToF nhưng không có kết quả từng S1–S4 hoặc test đồng thời/reboot để kết luận cả cụm pass.
- Power sensing hiện hành là **INA260 ×2**, DigiKey **1528-2955-ND**, board code **4226** (E1/E2); chưa có bằng chứng bench INA260 pass.

### Pinmap bench được bảo tồn — chưa là pinmap tích hợp đã release

Nguồn E2; không có sketch tương ứng trong repo để đối chiếu. Không đổi chân khi nhập lại code mà chưa ghi quyết định và test lại.

| Chức năng | Mapping đã dùng/đã biết | Giới hạn kiểm chứng |
|---|---|---|
| Left motor driver | IN1 GPIO15, IN2 GPIO16, IN3 GPIO17, EN GPIO18 | Bench history; current motor PARTIALLY VERIFIED |
| Right motor driver | IN1 GPIO11, IN2 GPIO12, IN3 GPIO13, EN GPIO14 | Bench history; current motor PARTIALLY VERIFIED |
| Left AS5600 I²C | SCL GPIO35, SDA GPIO38 | Split bus từng dùng; chưa đối chiếu build/revision hiện tại |
| Right AS5600 I²C | SCL GPIO37, SDA GPIO36 | Split bus từng dùng; chưa đối chiếu build/revision hiện tại |
| ToF XSHUT | GPIO41=S1, GPIO42=S2, GPIO47=S3, GPIO48=S4 | Chưa có per-sensor/all-four validation log |

**Pinmap hold:** [pinout controller](../purchased-hardware/evidence/16-esp32-s3-n16r8-pinout.png) và [README CAD](../purchased-hardware/cad-review/16-yd-esp32-s3-n16r8/README.md) ghi onboard RGB ở GPIO48; phải kiểm tra tương tác với S4 XSHUT trước khi freeze. Kiểm tra khả dụng GPIO35/36/37 trên module N16R8 và cấu hình memory thực tế trước khi tái dùng split encoder buses; chưa kết luận mapping lịch sử phù hợp với board hiện tại. SDA/SCL của ToF/INA260/IMU/BME280, địa chỉ sensor và chân Pi↔ESP32 chưa được xác nhận trong snapshot. Không tự điền giá trị mặc định thành canonical.

### Motor current status

Drive sử dụng **2 × BLDC FIT1035**, **2 × SimpleFOC Mini** và **2 × AS5600 magnetic encoder**. BOM ghi encoder tích hợp trong FIT1035; không đếm thêm hai encoder rời. Encoder test đã chạy (E2).

**Current: PARTIALLY VERIFIED.** Hai motor từng chạy được ở bench, nhưng code merge sau đó từng gây nóng/no-spin. Chưa có bằng chứng mới hơn để nâng trạng thái lên stable/pass. Thiếu exact last-known-good sketch, build settings, thư viện, tuning, nguồn thử, dòng/nhiệt, encoder direction/alignment và stop/fault results. Không coi “từng chạy cả hai bên” là xác nhận firmware live hiện tại an toàn để vận hành.

### Power và battery internals/protection/charging

- Pololu D24V90F5 **5V/9A** đã chốt/có; đây là cấu hình phần cứng, không phải kết quả full-load/thermal test (E1/E2).
- Kiến trúc pin **3S**. **BMS 3S tích hợp trong cụm pin**; không liệt kê standalone trong inventory/hardware summary. Rating và chức năng bảo vệ thực tế vẫn cần xác minh tại cụm pin.
- Kế hoạch **18650 3S3P, 9 cell**, candidate **Samsung INR18650-35E** được giữ ở mức **planned, không phải confirmed inventory/pack build** (E2). E1 ghi 10 cell theo listing “35E / 3.7V / 3000mAh”, còn mâu thuẫn định danh/dung lượng. Không gọi 10 cell đó là Samsung chính hãng, không suy ra pack đã lắp 9 cell và còn 1 dự phòng.
- Charger/IP2368 và các bộ phận nguồn xem BOM; không suy ra sạc khi robot hoạt động, balancing, cutoff hoặc runtime đã pass.

### Cơ khí hiện hành

- Bỏ hướng **vỏ cầu cố định 200 mm**. Dùng **approved reference form** làm exterior guide; kích thước ngoài do packaging linh kiện thật và clearances quyết định (E2). File/ảnh reference đã duyệt chưa xác định được trong `main`; cần khôi phục đúng bản, không tự tạo hình thay thế rồi gọi là approved.
- Bánh canonical: **gravel tire Ø60 mm × 22 mm**; ảnh được mô tả ghi **hub/center 12 mm** và **108.8 g/set**. Chưa xác nhận 12 mm là lỗ trục hoặc số bánh/set; chi tiết inventory/CAD chỉ ở BOM.
- Packaging direction theo E2, không tìm thấy quyết định mới hơn trên `main`: **battery ở giữa; motors hai bên/về phía sau; speaker module sau battery**. Battery width **54 mm ±10**, length **65 mm ±2**; chừa không gian loa phía sau **50 mm**. Đây là envelope/layout tham chiếu, chưa phải kích thước pack đo kiểm hoặc CAD release; chiều cao và clearance dây còn thiếu.
- Còn mở: vị trí fan khi sạc, chọn caster/ball caster cuối, final CAD packaging, airflow, service access và lắp ghép bánh/hub. Chưa CAD nào được release chế tạo theo BOM.

## VERIFIED/PASSED

**Nguồn xác nhận là E2 (owner-reported), trừ khi ghi khác; chưa có log test lưu trong repo.** Giữ giới hạn của từng lần test, không chuyển thành system acceptance.

| Hạng mục | Phần đã được xác nhận | Chưa được suy ra |
|---|---|---|
| Pi | Đã chạy Raspberry Pi OS 64-bit | Image tái lập, uptime/integration |
| Camera | Test OK | Pipeline perception/autonomy |
| Display | Đã hiển thị/chạy | UI tròn hoàn chỉnh, calibration touch |
| Microphone | Thu tiếng rõ | Wake word/STT/DOA end-to-end |
| MAX98357A | Hai board mới đều OK | Integrated stereo/noise/power validation |
| ESP32 | GPIO/Wi-Fi/Bluetooth đã test | Safety firmware, exact test board revision |
| IMU | Test OK | Axis/calibration trong chassis |
| BME280 | Test OK | Độ chính xác sau packaging/nhiệt |
| AS5600 | Encoder test đã chạy | Closed-loop motor ổn định sau merge |

E1 xác nhận repo có ảnh nhận dạng YD board và CAD danh nghĩa; điều này chỉ chứng minh nguồn tài liệu hiện có, không chứng minh hardware/CAD đã pass đo kiểm.

## PARTIALLY VERIFIED

- **Motor + encoder integration:** lịch sử chạy hai bên; regression nóng/no-spin chưa đóng, xem current motor status.
- **ToF:** đã có báo cáo test và mapping 4 XSHUT; thiếu kết quả riêng S1–S4, address assignment, chạy đồng thời và power-cycle recovery. Không đánh dấu toàn bộ 4 sensor pass.
- **Pi audio/display/voice stack:** module có test nhưng live sources, services và môi trường chưa được capture. Không xác nhận voice/AI/display integration hoàn tất.
- **Controller pinmap:** pinmap lịch sử chưa chứng minh cùng exact board/revision/build hiện tại; còn GPIO48 và memory-pin hold.

## HISTORICAL/OBSOLETE

| Dữ liệu cũ | Cách xử lý hiện tại |
|---|---|
| INA226 | OBSOLETE; dùng INA260 theo BOM |
| MAX98357A “1 tốt, 1 hỏng” | OBSOLETE; 2 board mới đều OK |
| Bánh Ø40×20; các width 18–20 mm ở BOM lịch sử | OBSOLETE; Ø60×22 mm |
| Vỏ cầu cố định 200 mm; envelope ban đầu dùng làm kích thước cuối | OBSOLETE; reference form + actual packaging |
| microSD 64GB, SHT45, 6 ToF trong BOM cũ | Không phải cấu hình hiện tại; 128GB, BME280, 4 VL53L1X theo E2. Nhu cầu chống rơi của PRD vẫn phải đáp ứng, không suy ra 4 ToF đã đủ |
| DevKitC-1 CAD, official Pi cooler như linh kiện đã mua | Không dùng thay YD PCB/Smraza đã ghi trong BOM |
| LiPo pouch 8,000–8,500mAh, speaker laptop, thông số protocol 921600/100ms/300ms trong `4c34439` | Historical design; không tự phục hồi như cấu hình live. Dùng BOM hiện hành và validate protocol mới |
| “Bench chưa bắt đầu” trong PRD §10; “controller chưa mua” trong wiring cũ | Tiến độ stale, không dùng để lập kế hoạch hiện tại |
| “Đang chờ giao” controller ở snapshot mua hàng cũ | Không dùng làm trạng thái tiến độ hiện tại; E2 đã báo test ESP32, exact revision/test provenance vẫn cần bổ sung |
| Motor đã quay cả hai bên | Giữ như lịch sử pass giới hạn; sau đó có nóng/no-spin nên current vẫn PARTIALLY VERIFIED |

Không khôi phục các purchase registers/handoff/architecture documents đã bị hợp nhất chỉ để làm đủ tên file. Git history là nơi truy vết, không phải current-state song song.

## Software/artifacts và MIGRATION GAPS

**Known from live system/chat history, not yet committed** là trạng thái của các đường dẫn E2 dưới đây. Chưa kiểm tra chúng còn tồn tại hoặc đang chạy trên Pi. Target repo là vị trí dự kiến để capture, chưa phải file đã được tạo.

| Live path/artifact được nhắc | Target repo dự kiến | Việc cần capture |
|---|---|---|
| `/home/aria/aria_core.py` | `software/pi/aria_core.py` | Nội dung thật, dependencies, IPC/drive behavior |
| `/home/aria/aria_av.py` | `software/pi/aria_av.py` | Audio/video/UI config và launch arguments |
| `/home/aria/ariactl` | `software/pi/ariactl` | Script thật, quyền executable, cách gọi |
| `/home/aria/ARIA_DRIVE_ONLY/ARIA_DRIVE_ONLY.ino` | `firmware/ARIA_DRIVE_ONLY/ARIA_DRIVE_ONLY.ino` | Sketch thật và bản đang flash, board/core/library versions |
| `/tmp/aria-core.sock` | Không commit socket runtime | Ghi IPC schema, ownership/permissions và lifecycle từ source thật |
| `aria-core.service` | `software/systemd/aria-core.service` | Unit thực tế + overrides; vị trí unit hiện tại chưa biết |
| `/home/aria/aria_models/aria.onnx` | Manifest model trong `software/` | File/source, version, checksum, license và cách lấy; không bịa model |
| `whisper.cpp` + `ggml-base.bin` | Manifest/dependency setup trong `software/` | Checkout/build flags, model path/version/checksum; đường dẫn đầy đủ chưa biết |

### Checklist capture

- [ ] Copy live Pi files và cấu hình OS/audio/camera/display/service thực tế; lưu launch commands, dependencies và phiên bản. Loại credential/token và dữ liệu cá nhân khỏi nội dung commit.
- [ ] Lấy sketch đang flash và last-known-good motor/encoder sketches từ Pi/PC/old chats; lưu hash, ngày và kết quả riêng từng phiên bản, không nhầm code regression với code pass.
- [ ] Lấy test sketches/logs IMU, BME280, ToF, INA260, ESP32, camera và audio; ghi board revision, wiring, nguồn thử, phạm vi test và pass/fail. INA260 chưa có pass evidence.
- [ ] Khôi phục ảnh approved exterior reference, số đo battery/speaker và CAD từ PC/chat; phân biệt hình tham khảo với bản đã duyệt.
- [ ] Bổ sung bằng chứng microSD/BME280/4 ToF và exact display/controller revision vào phần cấu hình của BOM; chưa tự cộng chi phí hoặc sửa tổng purchase register.
- [ ] Review các nhánh CAD chưa merge nếu còn cần: `origin/cad-final-api`, `origin/agent/chassis-visual-reference`, `origin/agent/component-reference-validation`, `origin/agent/add-waveshare-10670-ir-cad`. Chúng có artifact/reference ngoài `main`, không mặc nhiên approved/current; không merge hàng loạt trong migration.

### Kết quả rà repo

- Trước snapshot: `firmware/` chỉ có README; không có `software/`, runnable Pi/ESP32 source, service, model hoặc bench logs. Lịch sử tên file trên các refs đã fetch chỉ thấy Python tooling CAD, không thấy các live files nêu trên. Không có code thật để chuẩn hóa trong đợt này.
- [Firmware README](../firmware/README.md) và [software README](../software/README.md) là entrypoints/checklist pointers, không phải implementation.
- `electronics/` và `manufacturing/` trên `main` chỉ có README; chưa có schematic/mainboard/gerber release. CAD được giữ trong `purchased-hardware/`; trạng thái duyệt vẫn do BOM quản lý.
- Root/docs index đã đổi để dẫn vào master; wiring/HW/MECH đã đồng bộ phạm vi hiện hành. `purchased-hardware/README.md` tiếp tục dẫn về BOM và không chứa inventory thứ hai.
- PRD giữ nguyên byte-for-byte; các ghi chú tiến độ stale của nó được phân loại historical ở đây. PCB/manufacturing rules vẫn là release gates, không phải tuyên bố đã hoàn thành.

## OPEN ISSUES

1. Motor nóng/no-spin sau merge; thiếu bản tái lập và bench evidence mới.
2. Pinmap chưa freeze tích hợp: GPIO48 RGB/XSHUT, khả dụng GPIO encoder với N16R8, bus/address sensor và Pi link chưa xác minh.
3. Pi↔ESP32 protocol, watchdog, lost-link/reset/sensor-fault stop chưa được chứng minh end-to-end; không dùng số timeout lịch sử như kết quả đã test.
4. INA260 current sensing, tải regulator, battery protection/charging, thermal và power-fault behavior thiếu validation. Listing ratings không phải số đo.
5. Live code, service, model/dependencies và logs còn ngoài repo; chưa tái tạo được hệ thống từ fresh clone.
6. Final mechanics: fan khi sạc, caster/ball caster, measured packaging, wheel hub, missing approved reference và CAD release.
7. PRD acceptance còn mở: locomotion/autonomy, tránh vật cản/chống rơi, presence/bumper, privacy hardware và voice/AI/display integration; module pass không chứng minh các chức năng này đã hoàn tất.

## NEXT STEPS — NEXT STEP ORDER

| Thứ tự | Công việc | Điều kiện hoàn thành |
|---|---|---|
| 1 | **Freeze pinmap/current BOM** | Đối chiếu board/build thực tế, giải quyết pin holds; chốt bus/address/power wiring và cập nhật BOM duy nhất. Bảo tồn mapping lịch sử đến khi có quyết định thay thế |
| 2 | **Capture live code từ Pi/ESP32** | Commit nguồn thật, services/config/dependencies; xác định bản đang flash và last-known-good; đóng checklist capture tương ứng |
| 3 | **Re-run bench motor+encoder+ToF+INA260** | Test riêng rồi phối hợp; lưu source commit, wiring/build, log từng kênh, nhiệt/dòng, reset và stop results; chỉ nâng status khi có evidence |
| 4 | **Ổn định Pi↔ESP32 protocol** | Chốt transport/framing/commands/telemetry, versioning, heartbeat/timeout và fault handling; test mất link/reset |
| 5 | **Power/safety** | Validate power tree, protection/charging, load/thermal, stop/fault behavior trước vận hành robot; các kiểm tra an toàn bench tối thiểu vẫn phải làm trước bước 3 |
| 6 | **Locomotion/autonomy** | Drive ổn định, feedback/odometry, obstacle/cliff/bumper behavior và safe stopping có test |
| 7 | **Voice/AI/display integration** | Merge module đã pass, UI nằm trong vùng tròn, test wake/STT/response/audio/video và không làm hỏng drive/safety |
| 8 | **Mechanical finalization** | Chốt caster/fan/layout từ phần cứng đo thật, clearance/airflow/serviceability và CAD kiểm duyệt trước chế tạo |

Mỗi lần hoàn thành một bước: cập nhật trạng thái + evidence tại master này, lưu artifact thật vào repo, rồi commit lên `main`. Snapshot này khôi phục tri thức hiện có; khả năng dựng lại phần mềm hoàn chỉnh còn phụ thuộc MIGRATION GAPS.
