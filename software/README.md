# ARIA software

Source capture Pi nằm trong [pi/](pi/); unit được bảo tồn tại pi/aria-core.service. [capture-manifest.json](capture-manifest.json) lưu SHA-256 và nguồn. Không dùng pip-freeze.txt như môi trường tái dựng đã verified. Model/Whisper mới có danh sách đường dẫn.

Chương trình mới [pi/aria_sensors.py](pi/aria_sensors.py) chỉ đọc 4 VL53L1X, BME280, BNO085 và INA260 trên Pi. Nó không mở serial ESP, không có lệnh motor và không thay `aria-core.service`. Chạy thủ công bằng venv hiện có:

```bash
/home/aria/aria-venv/bin/python /home/aria/aria_sensors.py
```

Mặc định xuất dòng dễ đọc mỗi giây; thêm `--jsonl` để lấy JSON Lines. Chương trình kéo toàn bộ XSHUT xuống rồi gán lại 0x30–0x33 tuần tự, vì địa chỉ VL53L1X không tồn tại qua reset/mất điện. `None` và timeout có trạng thái riêng, không được đổi thành 0 mm. Dừng bằng Ctrl+C để `stop_ranging()`, kéo XSHUT xuống và đóng GPIO/I2C.

Trạng thái, giới hạn runtime, IPC và checklist duy nhất nằm trong [MASTER HANDOFF](../docs/ARIA-MASTER-HANDOFF.md). Không tự deploy snapshot trước khi đối chiếu thiết bị.

## App màn hình tròn và AI hội thoại

Bản thử giao diện mới nhất theo yêu cầu chủ nhân: avatar nữ cách điệu (tóc dài nâu ánh tím, da ấm, mắt nâu, lông mi nhẹ và môi hồng), giữ chuyển động và chọn biểu cảm. Chưa chốt nhân vật cuối cùng; các mô tả robot cyan bên dưới là các bản thiết kế trước, được bảo tồn trong Git.

Khuôn mặt dùng mắt/miệng cyan theo ảnh tham khảo của chủ nhân. Trong **Cài đặt → Biểu cảm khi chờ**, chọn vui vẻ, bình thường, buồn hoặc cau có; lựa chọn được lưu trên trình duyệt này. Khi app nghe/nghĩ/nói/báo lỗi, khuôn mặt đổi theo trạng thái xử lý rồi trở về biểu cảm đã chọn. Đây là biểu diễn trạng thái app, chưa phải AI suy luận cảm xúc.

Mắt có lòng mắt, tròng mắt, con ngươi và điểm sáng; biểu cảm chuyển mềm, mắt nhìn quanh nhẹ và chớp với khoảng nghỉ thay đổi. Hoạt ảnh không theo dõi người bằng camera. Tôn trọng cài đặt giảm chuyển động của hệ điều hành; độ mượt trên panel Pi vẫn cần kiểm tra thực tế.

Khuôn mặt tạo chiều sâu bằng chuyển sắc xanh teal/lam, ánh sáng viền, bóng đổ, mắt trắng có độ bóng, tròng xanh ngọc và má hồng. Miệng có lòng tối và lưỡi hồng được cắt theo hình miệng khi đổi biểu cảm. Đây là SVG tạo cảm giác 3D, không cần tải mô hình 3D.

Mặc định mở **màn hình chờ** chỉ có giờ, khuôn mặt và nhiệt độ phòng. Chạm vào để mở giao diện chính; chạm chữ ARIA để trở về màn hình chờ. Tự trở về sau 30 giây không thao tác, trừ khi đang nghe/nghĩ/nói/dừng hoặc còn nội dung đang nhập. Giao diện chính và hội thoại vẫn được giữ nguyên. Nhiệt độ hiển thị `— °C` khi mất kết nối, số đo cũ hoặc cảm biến chưa có dữ liệu hợp lệ.

[pi/aria_app.py](pi/aria_app.py) chạy độc lập với core capture, Python 3.10+ và thư viện chuẩn. Giao diện web cục bộ nằm trong vùng tròn, dùng Chromium trên chính Pi. Có hội thoại chữ, chọn OpenAI/Gemini, cá tính, ghi nhớ thêm/xóa chủ động, trạng thái nghe/nghĩ/nói, dừng lượt và chế độ cục bộ. Không cài service hay tự mở serial/I2C/motor. Chưa có wake word, camera/vision, tự hành, app điện thoại hoặc tự mở ứng dụng bằng lời nói.

Sau khi người dùng sao chép **cả thư mục** `software/pi` đến `/home/aria/aria-app`, chạy trên Pi:

```bash
python3 /home/aria/aria-app/aria_app.py --data-dir /home/aria/.local/share/aria-assistant
```

Trên desktop Pi mở `http://127.0.0.1:8765`; chọn **Toàn màn hình**, hoặc chạy Chromium với `--kiosk http://127.0.0.1:8765`. App chỉ lắng nghe loopback; dùng đúng `127.0.0.1`, không mở cổng LAN. Ctrl+C ở terminal dừng app. Lần này chỉ chạy thử trên PC, chưa sao chép/cài đặt trên Pi. Không bật lại `aria-core.service`; service cũ có thể tự chạy sau reboot.

**AI:** điền khóa và model được tài khoản cho phép vào bản riêng của [assistant.env.example](pi/assistant.env.example), để ngoài repo, hạn chế quyền đọc. File phải là cú pháp biến shell hợp lệ (đặt nháy quanh giá trị có khoảng trắng). App không tự đọc file; trên Pi có thể nạp trước khi chạy:

```bash
set -a
. /home/aria/.config/aria/assistant.env
set +a
python3 /home/aria/aria-app/aria_app.py --data-dir /home/aria/.local/share/aria-assistant
```

Model không bị hardcode; không tự chọn model khác hoặc tự gọi lại khi lỗi. Khóa nằm ở tiến trình Python, không gửi xuống trình duyệt. Chọn AI trực tuyến sẽ gửi câu hỏi, tối đa 12 tin nhắn ngữ cảnh và tối đa 30 ghi nhớ tới nhà cung cấp đó. Gói ChatGPT/GitHub Copilot không được app sử dụng làm quyền API; khóa/quyền sử dụng API cấu hình riêng. Chưa gọi API trả phí trong kiểm thử. OpenAI dùng Responses `store=false`; điều này không phải cam kết không có lưu giữ từ phía nhà cung cấp. Hội thoại chỉ ở RAM (tối đa 24 tin nhắn), ghi nhớ và cài đặt trong SQLite cục bộ. Xóa ghi nhớ cũng xóa ngữ cảnh hội thoại của app. Không có công cụ chạy shell hoặc hành động phần cứng cho model.

**Giọng nói:** cấu hình đường dẫn thực tế đến `whisper-cli`, model Whisper đa ngôn ngữ, executable Piper, model giọng Việt `.onnx` cùng file `.onnx.json`; không tự tải model hoặc suy ra file có mặt từ capture listing. `ARIA_CAPTURE_DEVICE` là thiết bị ALSA hỗ trợ PCM16 stereo 16kHz; pipeline thu 5 giây bằng `arecord`, trộn mono rồi gọi Whisper `-l vi`. Nút **Chạm để nói** chỉ bật khi các thành phần cấu hình tồn tại. Piper đọc câu trả lời nếu bật trong Cài đặt. `ARIA_PLAYBACK_DEVICE` chọn đầu ra I²S hoặc USB bằng tên card ổn định từ `aplay -L`. Ví dụ tên card trong ảnh gần nhất là `plughw:CARD=sndrpihifiberry,DEV=0`; phải đối chiếu lại trước dùng. Nhận thấy file/executable không chứng minh model, micro hay loa chạy tốt.

Hủy lượt dừng subprocess thu/phát; yêu cầu cloud đang gửi không bảo đảm hủy xử lý/chi phí phía nhà cung cấp. App chờ network timeout/response rồi bỏ câu trả lời bị hủy; không mở thêm lượt chồng trong lúc chờ. Audio tạm được xóa sau mỗi lượt bình thường hoặc lỗi; mất điện có thể để lại thư mục `voice-*` trong data-dir. Không tự ghi âm liên tục. Test thực tế tiếng Việt, độ trễ, phần cứng, touch/keyboard và hiss sau chập còn chờ.

**Số đo trong app:** chỉ chạy một tiến trình sở hữu I2C. Sau khi xác nhận core cũ đã dừng, người dùng có thể chạy chương trình cảm biến riêng:

```bash
/home/aria/aria-venv/bin/python /home/aria/aria-app/aria_sensors.py --snapshot /home/aria/.local/share/aria-assistant/sensors.json
```

Chạy app với thêm `--sensor-snapshot /home/aria/.local/share/aria-assistant/sensors.json`. Sensor writer thay file nguyên tử; app không chạm bus. Bản ghi quá 5 giây, tương lai, thiếu/sai timestamp bị đánh dấu cũ/không có. Cục bộ nhận các câu “Mấy giờ rồi?”, “Trạng thái”, “Nhiệt độ”, “Độ ẩm”. Không suy ra phần trăm pin từ điện áp nhánh INA260. Không dùng dữ liệu này làm vòng an toàn động cơ.

Kiểm thử không cần Pi hoặc API:

```bash
python3 -m unittest discover -s software/pi -p 'test_*.py' -v
```

Tài liệu giao thức đã đối chiếu: [OpenAI Responses/text](https://developers.openai.com/api/docs/guides/text), [Gemini generateContent](https://ai.google.dev/api/generate-content), [Whisper CLI](https://github.com/ggml-org/whisper.cpp/tree/master/examples/cli), [Piper CLI](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md). Mã nguồn adapter đã có; kết nối provider/model và toàn bộ vòng nghe–hiểu–nói trên Pi vẫn NOT VERIFIED.
