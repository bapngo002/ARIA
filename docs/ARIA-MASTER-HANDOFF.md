# ARIA — MASTER HANDOFF

**Status: CURRENT/CANONICAL · Migration + local live-source consolidation: 2026-09-12**

## ACTIVE CHECKPOINT — ESP damaged; replacement PCB planning

User reports ESP burned, encoder condition unknown, and intends replacement. User explicitly requests optimizing ESP/all pin allocation for new PCB and confirms same YD-ESP32-S3 N16R8 board type. This is authorization to propose a replacement map, not confirmation of the cause of failure, encoder health, or a new test pass. Earlier PASS reports remain historical evidence and do not describe the post-incident hardware.

Current work: STEP-003 with incident recovery. Proposed carrier signal allocation R1 is in docs/ARIA-WIRING-001.md; it is not released for soldering/fabrication. Keep motor GPIO15/16/17/18 and11/12/13/14; propose left encoder SDA8/SCL9 and right SDA4/SCL5. Pi mapping retained; INA260 ×1 pending delivery with wiring/address TBD. Actual replacement revision, connector orientation, PCB type/dimensions and power/disable circuit remain open.

NEW VERIFIED DOCUMENT CONSTRAINT: Espressif WROOM-1 datasheet v1.8 Table3-1 note b says GPIO35/36/37 are unavailable for external use on Octal-PSRAM modules; Table1-1 identifies N16R8 as that variant. This supersedes the earlier uncertainty about using these pins in a new N16R8 PCB. It does NOT prove why the old board burned. Source capture retains original mapping untouched for provenance; do not flash/run it as the new-map firmware.

Owner-reported: old ESP damaged; replacement same family selected, purchase/receipt not confirmed. NOT VERIFIED: both encoders and other attached hardware after incident, root cause and power path. Before further motion, isolate and inspect the old harness, verify supply/polarity and each encoder independently, confirm replacement board, and review power/EN/boot behavior. Source initFOC can energize motors during boot; zero target is not driver disable. No motor, flash or power test was run in this planning session.

## NEW CHATGPT ACCOUNT BOOTSTRAP

1. Đọc file này trước khi tiếp tục Project ARIA. Sau hợp nhất theo yêu cầu người dùng, **checkout ARIA đã hợp nhất là source of truth làm việc duy nhất**, gồm master này cho quyết định và source đã nhập cho phần mềm capture. GitHub `bapngo002/ARIA/main` là baseline quyết định đã đối chiếu; các thay đổi hoàn tất được đồng bộ GitHub theo ủy quyền thường xuyên của người dùng; kiểm tra remote HEAD khi báo kết quả. Không dùng export/kho ổ D như trạng thái song song.
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
- Power sensing hiện hành là **INA260 ×1**, DigiKey **1528-2955-ND**, board code **4226** (E1/E2); chưa có bằng chứng bench INA260 pass.

### Pinmap bench được bảo tồn — chưa là pinmap tích hợp đã release

Nguồn mapping lịch sử E2; đợt E4 đã nhập sketch để đối chiếu, xem phần hợp nhất bên dưới. Không đổi chân khi nhập lại code mà chưa ghi quyết định và test lại.

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
- **Pi audio/display/voice stack:** module có test; E4 đã nhập Core/AV/service và danh sách môi trường, còn thiếu display/voice source, cấu hình và môi trường venv đầy đủ. Không xác nhận voice/AI/display integration hoàn tất.
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

## Nơi lưu dữ liệu — quyết định người dùng 2026-09-12

- **Repo làm việc duy nhất: D:\UserData\ARIA\repo.** Từ nay mọi source, dữ liệu tải, model, CAD, work và outputs của ARIA phải lưu trên D, không tạo dữ liệu dự án mới trên C.
- Capture gốc đã chuyển nguyên byte sang D:\UserData\ARIA\capture-original; lịch sử tác vụ ở D:\UserData\ARIA\history. Đây là evidence/history, không phải current-state song song. Kho phần cứng hiện có D:\UserData\ARIA_DONG_BO được truy cập qua D:\UserData\ARIA\hardware-library.
- Work/output của tác vụ hiện tại ở D:\UserData\ARIA\current-task. Các junction thư mục cũ chỉ chuyển tiếp đến D; không phải bản sao dữ liệu trên C. Các file lẻ của tác vụ CAD 2026-07-30/ti dùng đường dẫn D trực tiếp vì không tạo được file symlink.
- Đã đối chiếu SHA-256 trước khi bỏ các bản trên C. Không xóa CAD/backup khác nội dung, model, nguồn thử nghiệm hoặc lịch sử Git. Kết quả lọc cache và nhật ký chuyển lưu tại D:\UserData\ARIA\storage-audit; không tạo master/handoff thứ hai.
- Pi: dùng đúng **ssh aria@aria.local**. Việc chuyển ổ không thay đổi phần mềm trên Pi/ESP32 và không đóng runtime/flash verification gaps.

## Software/artifacts và MIGRATION GAPS

**E4 — Local consolidation 2026-09-12.** Đã đọc nội dung 9 file export và 9 tài liệu repo và .gitattributes (19 file); đối chiếu thêm 9 bản tương ứng ở ổ D bằng SHA-256. Không gọi đây là đã đọc mọi CAD/binary trong kho PC.

Đường dẫn thực là `C:\Users\bapca\ARIA_EXPORT` và `D:\UserData\ARIA_DONG_BO`; các đường dẫn có thêm dấu phân cách trong yêu cầu cũ không tồn tại. Kho ổ D không có Git hoặc master. Checkout được xác nhận remote đúng và HEAD = origin/main sau fetch tại baseline `cc1889114ac9530542528190bf230321d30f8eda`:
`D:\UserData\ARIA\repo`. Vị trí trước khi chuyển ổ: `C:\Users\bapca\Documents\Codex\2026-09-12\referenced-chatgpt-conversation-this-is-an\work\ARIA` (nay đi qua junction tới D).

9/9 bản export giống byte với kho ổ D; cả 9 chưa có trong baseline Git, đã nhập nguyên byte vào đúng cây hiện tại. Không overwrite source cũ; không sửa tuning, pinmap hoặc PRD. Baseline Git giữ nguyên tài liệu trước hợp nhất; export và kho D giữ nguyên. Chưa tìm được bản last-known-good riêng có log pass: không gắn nhãn LKG cho sketch chỉ vì comment “đã PASS”.

| File repo đã nhập | Phạm vi bằng chứng |
|---|---|
| software/pi/aria_core.py | Core V0.6 theo banner/source |
| software/pi/aria_av.py | AriaAV kiểm thiết bị, capture/record/play |
| software/pi/ariactl | Client UNIX socket |
| software/pi/aria-core.service | Unit capture, Description V0.4 nhưng chạy aria_core.py |
| software/pi/python-version.txt | Python 3.13.5; chưa chứng minh interpreter của service |
| software/pi/pip-freeze.txt | Danh sách package capture; chưa xác định môi trường gốc |
| software/pi/models-list.txt | Hai đường dẫn aria.onnx và aria_v2.onnx; không có model binary |
| software/pi/whisper-files.txt | Danh sách whisper.cpp, ggml-base/tiny, whisper-cli và libwhisper.so.1.9.3; không có binary/source tree tương ứng |
| firmware/esp32/ARIA_DRIVE_ONLY/ARIA_DRIVE_ONLY.ino | Drive V0.3 source; chưa xác nhận firmware flash |

[Manifest SHA-256](../software/capture-manifest.json) lưu nguồn, kích thước, hash từng file. Hai target dự kiến cũ firmware/ARIA_DRIVE_ONLY và software/systemd được thay bằng đường dẫn nhập ở bảng; không tạo bản code/unit thứ hai.

### Code capture thực hiện gì — VERIFIED ở mức đọc source

- Pi mở /dev/ttyACM0, 115200 baud; gửi H mỗi 0.1 s, nhận serial bằng readline và in log. Lệnh F/B/L/R/S/+/- qua bàn phím hoặc /tmp/aria-core.sock. ariactl còn hỗ trợ CAM/MIC/STATUS.
- Pi init BNO085 trước BME280/ToF rồi mới kết nối ESP và tạo threads. BNO085 tại 0x4A đọc acceleration/gyro/quaternion; BME280 tại 0x76 đọc nhiệt/ẩm/áp suất. Đây là địa chỉ trong code, chưa phải đo bus thực tế.
- 4 VL53L1X: gpiozero XSHUT trên Pi 22/23/24/25; khởi tạo từ 0x29 rồi gán 0x30–0x33, distance_mode=2, timing_budget=100, đổi cm thành mm. Log trạng thái khoảng mỗi giây; chưa có obstacle/cliff stop.
- AV nhận diện camera imx708_wide_noir, ReSpeaker XVF3800, MAX98357A qua danh sách thiết bị. CAM gọi rpicam-still; MIC ghi 3 s, hw:1,0, S16_LE/16 kHz/2 kênh. Hàm play dùng pw-play nhưng core chưa cung cấp lệnh playback. Check audio không chứng minh cả hai amp/stereo đã phát.
- ESP dùng SimpleFOC velocity cho hai motor 7 pole-pairs và hai AS5600 split I2C 400 kHz; pin motor/encoder khớp lịch sử E2. Nguồn cấu hình 12 V, motor/driver limit 3 V, align 1.5 V; PID 0.15/1/0, ramp 500, LPF 0.02; speed mặc định 8, +/-2 trong 2–20. Đây là cấu hình source, không phải tuning đã tái kiểm chứng. Rẽ dùng hệ số 0.45 một bên; không có odometry/encoder telemetry gửi về Pi.
- Không có triển khai INA260, display/UI, wake-word, STT, AI/dialogue, autonomy trong các source capture này. File model/package có mặt trong listing không có nghĩa core đã gọi chúng.

### Mâu thuẫn và giới hạn được hợp nhất

1. ToF ở code là Pi GPIO22/23/24/25; E2 là ESP GPIO41/42/47/48 lịch sử. Bảo tồn cả hai với nhãn nguồn; không tự đổi chân hoặc tuyên bố wiring đã chuyển. GPIO48 hold chỉ liên quan nhánh wiring lịch sử; encoder N16R8 hold vẫn mở. BNO085 được code chuyển sang Pi; phù hợp Pi high-level/ESP realtime nhưng khác cách đọc rằng mọi sensor đã chạy trên ESP.
2. Service Description V0.4 không khớp Core banner V0.6; ExecStart là /home/aria/aria-venv/bin/python /home/aria/aria_core.py. Giữ nguyên unit capture để bảo toàn evidence; chưa dùng label V0.4 làm phiên bản runtime.
3. pip-freeze không liệt kê các Adafruit imports của core hoặc onnxruntime trong khi whisper listing có onnxruntime dưới aria-venv. Môi trường capture không đủ tái dựng venv; chưa kết luận thiết bị thiếu dependencies.
4. Comment PID “đã PASS” không đóng regression nóng/no-spin trong master. Motor vẫn PARTIALLY VERIFIED.
5. Watchdog source timeout 500 ms chỉ hoạt động sau H đầu tiên; khi failsafeActive=true, lệnh drive mới vẫn đặt target và checkHeartbeat không forceStop lần nữa. Trước H đầu tiên cũng nhận lệnh drive. forceStop chỉ đặt target=0, không disable driver. VERIFIED bằng đọc nhánh code; stop vật lý và các tình huống lỗi NOT VERIFIED. Không sửa firmware trong đợt kiểm kê.
6. Pi trả “DRIVE ... SENT” dù send_esp thất bại; STATUS chủ yếu là trạng thái init/handle, không phải health/ack mới. ESP không sẵn sàng thì connect_esp chặn startup socket/status; sensor lỗi không liên động dừng motor. Không gọi đây là integrated safety pass.

### VERIFIED / PARTIALLY VERIFIED / NOT VERIFIED sau hợp nhất

- **VERIFIED (file/static):** nội dung 9 file, 9/9 hash khớp kho D và bản nhập, config/protocol/nhánh code mô tả ở trên. Không phải bench execution.
- **VERIFIED (owner-reported E2):** các module trong bảng VERIFIED/PASSED; giữ giới hạn và thiếu log như trước.
- **PARTIALLY VERIFIED:** motor/encoder, ToF, pinmap tích hợp và audio/voice/display integration theo master. Capture source hoàn thành một phần bước 2, không đóng bước 1 hoặc bước 2.
- **NOT VERIFIED:** process/unit thực sự đang chạy, hash file trên Pi hiện tại, firmware trong flash, LKG độc lập, build/library settings, fresh-clone reproduction, watchdog/stop/reset thực tế, INA260 và system acceptance.
- Đã thử SSH chỉ đọc tới aria@aria.local với BatchMode/known-host verification; bị “Permission denied (publickey,password)” trước khi chạy lệnh. Không đổi SSH/thiết bị, không flash, không bench test. Vì vậy chỉ xác định chính xác được **source capture Core V0.6 + Drive V0.3**, chưa thể khẳng định đó là runtime hiện tại.

### Checklist capture

- [x] Nhập 9 file capture nguyên byte và manifest; đối chiếu 9 bản kho D.
- [ ] Pi: lấy systemctl cat/show/status (unit + overrides + PID/ExecStart), journal và SHA-256 source hiện tại để gắn capture với runtime; xác nhận quyền/owner socket và executable ariactl.
- [ ] Pi: lấy /home/aria/aria-venv/bin/python --version và -m pip freeze, OS build, boot/config.txt, I2C/GPIO wiring, ALSA/PipeWire/camera/display config, launch commands; không đưa credential/token hoặc dữ liệu riêng tư vào repo.
- [ ] Pi: lấy model binaries hoặc nguồn tải/license + hash, wake-word/voice/display source, whisper.cpp commit/build flags và checksum binary/model.
- [ ] Lấy sketch đang flash và last-known-good motor/encoder sketches từ Pi/PC/old chats; lưu hash, ngày và kết quả riêng từng phiên bản, không nhầm code regression với code pass.
- [ ] Lấy test sketches/logs IMU, BME280, ToF, INA260, ESP32, camera và audio; ghi board revision, wiring, nguồn thử, phạm vi test và pass/fail. INA260 chưa có pass evidence.
- [ ] Khôi phục ảnh approved exterior reference, số đo battery/speaker và CAD từ PC/chat; phân biệt hình tham khảo với bản đã duyệt.
- [ ] Bổ sung bằng chứng microSD/BME280/4 ToF và exact display/controller revision vào phần cấu hình của BOM; chưa tự cộng chi phí hoặc sửa tổng purchase register.
- [ ] Review các nhánh CAD chưa merge nếu còn cần: `origin/cad-final-api`, `origin/agent/chassis-visual-reference`, `origin/agent/component-reference-validation`, `origin/agent/add-waveshare-10670-ir-cad`. Chúng có artifact/reference ngoài `main`, không mặc nhiên approved/current; không merge hàng loạt trong migration.

### Kết quả rà repo

- Baseline trước E4 (historical): `firmware/` chỉ có README; không có `software/`, runnable Pi/ESP32 source, service, model hoặc bench logs. Lịch sử tên file trên các refs đã fetch chỉ thấy Python tooling CAD, không thấy các live files nêu trên. Không có code thật để chuẩn hóa trong đợt này.
- Sau E4: firmware/software đã có source capture; README dẫn vào source và master duy nhất.
- `electronics/` và `manufacturing/` trên `main` chỉ có README; chưa có schematic/mainboard/gerber release. CAD được giữ trong `purchased-hardware/`; trạng thái duyệt vẫn do BOM quản lý.
- Root/docs index đã đổi để dẫn vào master; wiring/HW/MECH đã đồng bộ phạm vi hiện hành. `purchased-hardware/README.md` tiếp tục dẫn về BOM và không chứa inventory thứ hai.
- PRD giữ nguyên byte-for-byte; các ghi chú tiến độ stale của nó được phân loại historical ở đây. PCB/manufacturing rules vẫn là release gates, không phải tuyên bố đã hoàn thành.

## OPEN ISSUES

1. Motor nóng/no-spin sau merge; thiếu bản tái lập và bench evidence mới.
2. Pinmap chưa freeze tích hợp: GPIO48 RGB/XSHUT, khả dụng GPIO encoder với N16R8, bus/address sensor và Pi link chưa xác minh.
3. Pi↔ESP32 protocol, watchdog, lost-link/reset/sensor-fault stop chưa được chứng minh end-to-end; không dùng số timeout lịch sử như kết quả đã test.
4. INA260 current sensing, tải regulator, battery protection/charging, thermal và power-fault behavior thiếu validation. Listing ratings không phải số đo.
5. Đã nhập source/service capture E4; còn thiếu runtime identity, model binaries, venv/build/config và logs để tái tạo từ fresh clone.
6. Final mechanics: fan khi sạc, caster/ball caster, measured packaging, wheel hub, missing approved reference và CAD release.
7. PRD acceptance còn mở: locomotion/autonomy, tránh vật cản/chống rơi, presence/bumper, privacy hardware và voice/AI/display integration; module pass không chứng minh các chức năng này đã hoàn tất.

## Phối hợp Codex / Copilot — quyết định người dùng 2026-09-12

Codex giữ vai trò viết code chính và duyệt tích hợp. Tận dụng GitHub Copilot Pro cho công việc hỗ trợ có phạm vi rõ: bản nháp nhỏ, test cần thiết, giải thích và review; tránh thực hiện trùng cả tác vụ ở hai bên. Quy tắc thực hiện tại AGENTS.md và .github/copilot-instructions.md, không thay thế NEXT STEP ORDER.

Copilot CLI 1.0.83 đã cài từ GitHub release chính thức trên D, kiểm SHA-256 và chạy thành công một lượt review pinmap bằng thông tin đã cung cấp: 0 file thay đổi, 0.86 AI credit theo CLI. Đây chỉ là kiểm chứng kênh hỗ trợ, không phải xác minh wiring/hardware hoặc toàn bộ tính năng Copilot. State/logs đặt dưới D:/UserData/ARIA/tools/copilot/state. Không bật chi phí vượt gói hoặc API trả phí riêng. Hạn mức hai dịch vụ độc lập; theo dõi trong phiên làm việc và lưu checkpoint sớm, không cam kết sử dụng vô hạn.

## KST / STEP-001–106 — đối chiếu tiếp tục tiến trình

Theo yêu cầu người dùng tiếp tục dựa trên kế hoạch KST, đã đọc ngày 2026-09-12: kế hoạch Word FINAL, roadmap 106 bước, báo cáo STEP-001 v0.4 và báo cáo kiểm tra lại KST ngày 07/09. Dùng mã STEP làm chỉ mục công việc tham chiếu; trạng thái hiện hành và NEXT STEP ORDER vẫn ở master này. Không tạo master/roadmap thứ hai, không reset các module đã có về chưa bắt đầu và không đánh dấu DONE chỉ vì có source.

Nguồn được giữ nguyên trên D (tài liệu lịch sử, không phải nguồn quyết định song song):
- D:/UserData/Downloads/ARIA_MASTER_TRANSFER_V2/ARIA_KST_REVERSE_MASTER_PLAN_FINAL.docx — SHA-256 e2c88b681d80b077b112b3279cdab4a081fd903f9a112a6d63777e136df845dc.
- D:/UserData/Downloads/ARIA_MASTER_TRANSFER_V2/ARIA-ROADMAP-106-STEPS.md — SHA-256 24abfa370bf2d51ffdf71e23f779efc0ef9be5bda2dbc1d7485a677f48b98dcb.
- D:/UserData/ARIA/history/2026-09-07/xe/outputs/ARIA-STEP-001-DOI-CHIEU.md — SHA-256 ec2b6a4841074a07b96c75db2cbbc88f388b4b53deca37c1d55f152f0251dfb2.
- D:/UserData/ARIA/history/2026-09-07/xe/outputs/ARIA-KST-KIEM-TRA-FILE-GOC-VA-AP-DUNG.md — báo cáo static review; chưa tái thực hiện reverse/bench trong lần đối chiếu này.

### Điều chỉnh khi áp dụng tài liệu KST

1. STEP-001/002 dùng docs/ARIA-BOM-001.md là inventory duy nhất. Nhận định cũ “BOM không tồn tại” và baseline e3a6a83 đã hết hiệu lực; không chuyển inventory trở lại purchased-hardware/README.md.
2. STEP-015/024 dùng INA260 ×1, không INA226. BME280 và 4 VL53L1X theo cấu hình hiện hành; không đưa lại sensor/model lịch sử vào thiết kế.
3. STEP-006 không yêu cầu bỏ cây software/pi và firmware/esp32 đang có hoặc viết lại code từ đầu. Chỉ tái cấu trúc khi có nhu cầu triển khai cụ thể và bảo tồn capture/LKG.
4. STEP-014/016 không mặc định chuyển IMU/ToF về ESP32: source capture đang đọc chúng trên Pi. Wiring/ownership cuối phải được xác minh; ESP32 vẫn có trách nhiệm dừng độc lập khi mất link.
5. KST cung cấp tham khảo về dashboard, state machine, công cụ AI, lệnh có thời hạn, settings và recovery. Không dùng firmware KST làm firmware ARIA; không copy GPIO, driver L298N/servo, ngưỡng hoặc timeout mặc định sang ARIA. Có chuỗi safety/tool trong binary không chứng minh runtime hoặc safe stop trên ARIA.
6. Báo cáo kiểm tra lại giới hạn các tuyên bố “reverse hoàn tất”, “hard max đã được bảo đảm” và “OTA luôn rollback”: giữ ở mức bằng chứng static đã báo cáo, không nâng thành bench VERIFIED. Source custom và cloud backend không được khôi phục từ gói này.
7. KST xếp autonomy cuối còn NEXT STEP ORDER hiện hành tách locomotion/autonomy trước voice. Không tự đổi thứ tự đã chốt: phần caller/person approach của STEP-104 vẫn phụ thuộc vision và obstacle safety; không gọi mọi autonomy hoàn tất trước khi các phụ thuộc tương ứng đạt.

### Trạng thái đối chiếu theo STEP

| STEP | Trạng thái tiếp tục | Phần còn thiếu để đóng |
|---|---|---|
| 001 | PARTIALLY VERIFIED — đối chiếu hồ sơ đã có, không làm lại từ đầu | Đóng delta vật lý còn thiếu hoặc ghi rõ deferred; báo cáo v0.4 tự ghi chưa DONE |
| 002 | PARTIALLY VERIFIED — BOM hiện hành đã hợp nhất các quyết định mới | Hoàn thiện evidence/revision còn thiếu và đồng bộ GitHub khi được yêu cầu |
| 003 | PARTIALLY VERIFIED — người dùng xác nhận họ board; pinout mới khớp capture | Còn revision/build/memory, rails và dây thật; không hỏi lại model hoặc tự đổi encoder GPIO35/36/37 |
| 004 | PARTIALLY VERIFIED — đã xác nhận cấu hình chính, tài liệu pinout xác định sensors trên Pi | INA260 ×1 pending delivery; các revision/cấu hình ngoại vi còn thiếu giữ PROVISIONAL |
| 005 | PARTIALLY VERIFIED — baseline và capture đã commit | Protocol/safety decisions chưa đủ để đóng bước |
| 006–010 | PARTIALLY VERIFIED — có cây source, serial 115200 và heartbeat | Handshake/version, structured log, fault/link tests; không coi liên kết đã ổn định |
| 011–017 | PARTIALLY VERIFIED — motor/encoder và sensor source đã có một phần | SAFE_MODE, INA260, snapshot/self-test và bằng chứng từng driver |
| 018–027 | NOT VERIFIED về gate an toàn | Còn lỗi watchdog đã ghi ở E4; chưa có fault-injection/stop evidence |
| 028–034 | PARTIALLY VERIFIED — có F/B/L/R/S và ariactl | Bounded motion, ACK/status/safety API và test dừng; CLI hiện tại chưa đạt gate |
| 035–053 | NOT VERIFIED | Chưa có state machine/event bus/MCP implementation trong capture |
| 054–060 | PARTIALLY VERIFIED — có thu âm/module audio | Wake/VAD/STT/TTS/barge-in và hội thoại end-to-end |
| 061–067 | NOT VERIFIED | AI router/tool-call loop chưa có trong capture |
| 068–072 | PARTIALLY VERIFIED — camera/chụp ảnh đã có | Công cụ vision, phân tích ảnh và lifecycle/privacy chưa đủ |
| 073–077 | PARTIALLY VERIFIED — display đã được báo cáo chạy | Chưa có source UI/biểu cảm trong capture |
| 078–099 | NOT VERIFIED trên ARIA | Dashboard KST chỉ là tham khảo; settings/OTA/memory chưa được chứng minh triển khai |
| 100–106 | NOT VERIFIED | Odometry/autonomy/soak và fault tests chưa có evidence |

**Điểm tiếp tục:** hoàn thiện phần còn mở của STEP-001–004, tương ứng bước 1 của NEXT STEP ORDER. Việc cụ thể ngay sau đối chiếu là xác nhận board/build/wiring hiện tại; thu cấu hình Pi chỉ đọc để hỗ trợ đối chiếu. Lần kiểm tra mạng ngày 2026-09-12 gần nhất không phân giải được aria.local, khác lần E4 đã tới xác thực nhưng bị từ chối; chưa chạy được lệnh trên Pi. Không suy ra Pi tắt hoặc firmware thay đổi từ lỗi mạng này.

## Xác nhận phần cứng và kiểm kê wiring — 2026-09-12

Người dùng xác nhận “đúng chuẩn rồi” đối với bảng vừa trình bày: Pi 5 4GB/microSD 128GB, YD-ESP32-S3 N16R8 44 chân dual USB-C, FIT1035 ×2, DRI0058 ×2, AS5600 ×2 đi cùng motor, INA260 ×2 Adafruit 4226 (số lượng ở xác nhận cũ, đã thay bằng ×1 theo điều chỉnh sau đó), VL53L1X ×4, BNO085 và BME280. Đây là VERIFIED ở mức owner-reported cho cấu hình/model đã liệt kê; không xác nhận revision, dây đang đấu, pin availability hay kết quả bench mới. Không cần hỏi lại model trong bảng nếu không có mâu thuẫn mới.

Kiểm kê wiring: docs/ARIA-WIRING-001.md hiện có quy tắc và cập nhật INA260/BMS tích hợp, chưa có sơ đồ pin-to-pin hợp nhất theo capture. electronics/schematics chỉ có README. Tìm được bản lịch sử D:/UserData/ARIA/history/2026-08-01/referenced-chatgpt-conversation-this-is-an/outputs/docs/ARIA-WIRING-002.md và PDF/KiCad tương ứng; Rev A ghi DESIGN BASELINE - DO NOT BUILD, dùng Pi 8GB, DevKitC-1, INA226, 6 ToF/SHT45 và BMS Enerkey, nên không dùng như sơ đồ hiện hành. D:/UserData/ARIA_DONG_BO/01_ARIA_MECH_FROM_ZERO_R1/CH500_WIRING_SERVICE_R1.json là routing cơ khí, tự ghi electrical release blocked; giả định pack/DALY trong đó không thay thế cấu hình pin hiện hành. Các bản này được bảo tồn lịch sử, chưa nhập lại vào repo.

Kết luận: tài liệu quy tắc đã cập nhật một phần, sơ đồ đấu dây toàn hệ thống chưa cập nhật/được xác minh theo cấu hình hiện tại. Bước tiếp tục vẫn là đối chiếu wiring thật với capture rồi cập nhật chính ARIA-WIRING-001; không lấy sự xác nhận model làm xác nhận dây.

## Cập nhật INA260 — xác nhận trực tiếp 2026-09-12

**Số lượng chốt mới nhất: INA260 ×1.** Người dùng điều chỉnh từ 2 xuống 1; cấu hình hai board đã superseded. Chưa nhận hàng, chưa chốt wiring/address và chưa bench.

Người dùng chốt INA260, nhưng linh kiện chưa về nên chưa cập nhật chân đấu nối. Cấu hình mục tiêu là INA260 ×1 theo điều chỉnh số lượng mới nhất của người dùng; trạng thái nhận hàng: chưa nhận; lắp/bench: chưa thực hiện; chân SDA/SCL, nguồn, ALERT nếu dùng và địa chỉ I²C: NOT VERIFIED/TBD. Không sao chép địa chỉ 0x44 của INA226 sang INA260. Xác nhận này làm rõ câu “đúng chuẩn rồi” trước đó là xác nhận lựa chọn model, không phải đã nhận/lắp INA260. Không yêu cầu test INA260 trước khi hàng về; giữ hạng mục này pending delivery, có thể đối chiếu phần wiring khác độc lập.

File người dùng cung cấp D:/UserData/Downloads/PROJECT_ARIA_LATEST_PINOUT_HANDOFF_2026-09-12.md đã đọc và đối chiếu: motor/encoder/tuning, USB Serial 115200, ToF Pi GPIO22–25/0x30–0x33, BNO085 0x4A và BME280 0x76 khớp capture. File báo audio GPIO18/19/21, camera CAM/DISP0, display CAM/DISP1 và overlay; đây là evidence tài liệu mới, chưa kiểm cấu hình runtime. File ghi INA226 còn đang dùng và planned INA260; xác nhận mới không chứng minh INA226 hiện còn lắp. Không phục hồi INA226 làm cấu hình mục tiêu. Các nhãn bounded motion/failsafe PASS trong file chưa đóng lỗi static của sketch capture: chưa thấy command-duration timeout độc lập heartbeat. Không nâng runtime/flash/bench thành VERIFIED hoặc đổi pin chỉ từ nhãn PASS/LOCKED trong tài liệu.

## Checkpoint STEP sau bổ sung pinout và INA260 ×1

Đã cập nhật docs/ARIA-WIRING-001.md bằng bảng tín hiệu từ capture + pinout mới, ghi riêng phần chỉ có trong tài liệu (I2S, camera/display connector, overlay). Đây là VERIFIED ở mức đối chiếu hồ sơ/source, chưa phải wiring release vật lý. Bản kiểm kê trước đó nói wiring chưa có bảng là trạng thái trước cập nhật này.

Điểm công việc hiện tại là STEP-003 (board/build/wiring evidence), trong Phase 0 chưa đóng gate; không có cơ sở tuyên bố đã hoàn thành tuần tự tới STEP-034. STEP-001 đã đối chiếu và nhận xác nhận nhóm phần cứng chính; phần inventory mở về pack, phụ kiện, revision và evidence vẫn giữ trong BOM/master, không bắt người dùng xác nhận lại toàn bộ. STEP-002 đã cập nhật local nhưng chưa xuất bản GitHub, nên chưa DONE theo định nghĩa gốc. STEP-005 còn protocol/safety decisions; STEP-006 đã có cây source tương đương, không tạo lại skeleton cho đủ tên thư mục.

Tiến độ triển khai vượt Phase 0 ở nhiều nhánh: STEP-008/009 có USB serial/heartbeat nhưng thiếu handshake/version và fault evidence; STEP-013/014/016 có encoder/BNO085/ToF source và báo cáo PASS; STEP-029/030/034 có stop/velocity/CLI một phần; STEP-054/068 có thu âm/chụp ảnh. Không dùng các phần này để đánh dấu cả phase DONE. STEP-019/031/032 còn thiếu command-duration timeout trong source hiện có; STEP-020 có heartbeat stop nhưng còn nhánh lỗi static đã ghi. STEP-015/024 (đổi INA226 thành INA260) là DEFERRED — pending delivery, không yêu cầu bench khi chưa nhận hàng. Voice/AI/UI/OTA/autonomy vẫn theo giới hạn capture đã ghi, danh sách chức năng trong pinout không phải source triển khai.

Không có bench/flash/runtime test mới trong lần đối chiếu STEP này. Giữ báo cáo PASS của pinout như evidence tài liệu, giữ regression/safety gaps chưa giải quyết riêng để không xóa lịch sử hoặc nâng mức kiểm chứng không có cơ sở.

## Quy tắc đồng bộ GitHub thường xuyên — 2026-09-12

Người dùng yêu cầu luôn đồng bộ GitHub và tận dụng GitHub Copilot Pro. Từ mốc này, sau mỗi phần việc hoàn tất: kiểm tra thay đổi phù hợp, commit local, fetch/đối chiếu remote, push origin/main và xác minh SHA remote; không cần hỏi lại cho các lần đồng bộ thuộc phạm vi ARIA đã giao. Không force-push hoặc ghi đè công việc khác. Nếu không đồng bộ được, báo rõ và giữ bản local. Các ghi chú “chưa push” phía trên là lịch sử checkpoint, không phải trạng thái remote cố định. Đợt đồng bộ này bao gồm toàn bộ các commit hợp nhất/cập nhật local đang chờ.

Tiếp tục dùng Copilot Pro cho các việc hỗ trợ có lợi ích cụ thể (review, bản nháp nhỏ, test cần thiết), với prompt/output gọn và kiểm tra lại trước tích hợp. Không gọi thêm chỉ để lặp lại một chỉnh sửa đơn giản. Codex vẫn viết chính và chịu trách nhiệm tích hợp. Không phát sinh mua credit, overage hoặc API trả phí riêng; hạn mức Copilot và Codex độc lập. Quyền đồng bộ GitHub không phải quyền tự flash hoặc vận hành motor.

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

**Bước tiếp theo duy nhất:** tiếp tục STEP-003 theo ACTIVE CHECKPOINT sau sự cố cháy ESP: xác minh board thay thế/cách cấp nguồn và các đầu nối để hoàn thiện sơ đồ carrier R1; encoder GPIO35/36/37 không được dùng trên N16R8 mới. Kiểm tra encoder và dây cũ trước tái sử dụng; chưa cấp motor hoặc flash firmware cũ lên wiring mới. INA260 chờ hàng, wiring/address giữ TBD.

Mỗi lần hoàn thành một bước: cập nhật trạng thái + evidence tại master này, lưu artifact thật vào repo, rồi commit local; tự đồng bộ GitHub theo ủy quyền thường xuyên bên dưới và xác minh remote HEAD. Snapshot này khôi phục tri thức hiện có; khả năng dựng lại phần mềm hoàn chỉnh còn phụ thuộc MIGRATION GAPS.
