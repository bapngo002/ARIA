# ARIA firmware — capture pending

Chưa có firmware/sketch thật trong thư mục này. [MASTER HANDOFF](../docs/ARIA-MASTER-HANDOFF.md) là nguồn duy nhất cho pinmap bench, trạng thái motor PARTIALLY VERIFIED và checklist capture nguồn Pi/ESP32.

Controller family canonical và power-sensing identity xem [BOM](../docs/ARIA-BOM-001.md). GPIO48 có onboard RGB và nằm trong mapping ToF XSHUT lịch sử; pin holds phải được kiểm tra trước khi freeze integration.

Capture sketch đang flash và last-known-good độc lập, board/core/library versions, build settings, wiring và bench logs trước khi merge. Không tạo code thay thế rồi gọi là live source. Target paths được ghi trong master; generated build output không commit.
