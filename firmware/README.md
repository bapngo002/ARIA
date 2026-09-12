# ARIA firmware

Mới 2026-09-13: [ARIA_ENCODER_CHECK_R1](esp32/ARIA_ENCODER_CHECK_R1/README.md) v0.1.0, chỉ kiểm tra encoder phải SDA4/SCL5 trên ESP thay thế. Không chạy motor; giữ nguồn driver ngắt. Encoder trái hỏng để tách khỏi mạch. Đây là bản riêng, không sửa capture dưới đây.

Đã nhập nguyên bản [ARIA_DRIVE_ONLY.ino](esp32/ARIA_DRIVE_ONLY/ARIA_DRIVE_ONLY.ino), banner Drive V0.3. Đây là source capture, chưa xác minh flash hoặc last-known-good. Không sửa pin/tuning hoặc tự flash trong đợt hợp nhất.

[MASTER HANDOFF](../docs/ARIA-MASTER-HANDOFF.md) là nguồn duy nhất cho pinmap, motor PARTIALLY VERIFIED, các nhánh watchdog còn mở và checklist build/bench. Hash nằm trong [capture manifest](../software/capture-manifest.json).
