# ARIA software

Source capture Pi nằm trong [pi/](pi/); unit được bảo tồn tại pi/aria-core.service. [capture-manifest.json](capture-manifest.json) lưu SHA-256 và nguồn. Không dùng pip-freeze.txt như môi trường tái dựng đã verified. Model/Whisper mới có danh sách đường dẫn.

Chương trình mới [pi/aria_sensors.py](pi/aria_sensors.py) chỉ đọc 4 VL53L1X, BME280, BNO085 và INA260 trên Pi. Nó không mở serial ESP, không có lệnh motor và không thay `aria-core.service`. Chạy thủ công bằng venv hiện có:

```bash
/home/aria/aria-venv/bin/python /home/aria/aria_sensors.py
```

Mặc định xuất dòng dễ đọc mỗi giây; thêm `--jsonl` để lấy JSON Lines. Chương trình kéo toàn bộ XSHUT xuống rồi gán lại 0x30–0x33 tuần tự, vì địa chỉ VL53L1X không tồn tại qua reset/mất điện. `None` và timeout có trạng thái riêng, không được đổi thành 0 mm. Dừng bằng Ctrl+C để `stop_ranging()`, kéo XSHUT xuống và đóng GPIO/I2C.

Trạng thái, giới hạn runtime, IPC và checklist duy nhất nằm trong [MASTER HANDOFF](../docs/ARIA-MASTER-HANDOFF.md). Không tự deploy snapshot trước khi đối chiếu thiết bị.
