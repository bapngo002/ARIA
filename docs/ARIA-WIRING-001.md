# ARIA-WIRING-001 — Wiring and safety rules

Purchased component identity and quantity come only from [`docs/ARIA-BOM-001.md`](ARIA-BOM-001.md).

- Battery and motor current must not pass through breadboards or low-current buttons.
- Use short, fused, strain-relieved high-current wiring.
- Route motor phases and switching power away from audio, camera, IMU and control wiring.
- Verify connector polarity, wire gauge, current derating and service disconnects.
- Keep replaceable parts disconnectable.
- Prove motor stop behavior for loss of the main computer, controller reset and sensor faults.
- The canonical controller family is recorded in the BOM. Pi↔ESP32 protocol and integrated wiring still need validation; controller selection is no longer waiting for an inventory entry.
- Preserve the historical bench pinmap and unresolved pin holds in the [master handoff](ARIA-MASTER-HANDOFF.md#pinmap-bench-được-bảo-tồn--chưa-là-pinmap-tích-hợp-đã-release). Check GPIO48 RGB/XSHUT interaction and encoder-pin availability for the exact N16R8 build before freezing integrated wiring.

This file intentionally contains no connector BOM, component list or CAD status copy.

## Power sensing and battery protection

Use INA260 for current power-sensing wiring; board identity and quantity are in the canonical BOM. Verify the delivered boards and I²C address configuration before finalizing the harness. Battery protection uses the 3S BMS inside the battery pack; validate the pack protection and charging connections as part of the battery assembly.

## Signal mapping reconciled with capture — 2026-09-12

Sources: imported Pi Core V0.6 / ESP Drive V0.3 and user-supplied D:/UserData/Downloads/PROJECT_ARIA_LATEST_PINOUT_HANDOFF_2026-09-12.md. GPIO numbers below are BCM numbers on Pi and GPIO numbers on ESP32, not physical header positions. This is a documented signal baseline, not a complete released power/connector schematic or a new physical continuity test. Preserve wiring; do not remap from historical KST/ESP sensor tables.

| Connection | Mapping | Evidence |
|---|---|---|
| ESP32 → left driver | GPIO15/16/17 → IN1/IN2/IN3; GPIO18 → EN | Capture and supplied pinout agree |
| ESP32 → right driver | GPIO11/12/13 → IN1/IN2/IN3; GPIO14 → EN | Capture and supplied pinout agree |
| Left AS5600 | ESP SDA38 / SCL35; controller 0 | Capture and supplied pinout agree; exact memory/build compatibility still unverified |
| Right AS5600 | ESP SDA36 / SCL37; controller 1 | Capture and supplied pinout agree; exact memory/build compatibility still unverified |
| Pi ↔ ESP32 | USB Serial /dev/ttyACM0, 115200 baud | Capture and supplied pinout agree; no GPIO UART required by this source |
| Pi sensor I2C | SDA GPIO2 / SCL GPIO3 | Supplied pinout; code uses board.I2C(); physical harness not inspected |
| ToF S1–S4 XSHUT | Pi GPIO22/23/24/25 respectively | Capture and supplied pinout agree |
| ToF S1–S4 addresses | 0x30/0x31/0x32/0x33 after initialization | Capture and supplied pinout agree; assigned addresses, not power-on defaults |
| BME280 / BNO085 | Pi I2C, 0x76 / 0x4A | Capture and supplied pinout agree |
| MAX98357A I2S | Pi GPIO18 BCLK / GPIO19 LRC / GPIO21 DOUT | Supplied pinout only; overlays, channel selection and physical wiring still need capture |
| Camera | Pi CAM/DISP0 | Supplied pinout; code checks imx708_wide_noir |
| Microphone | Pi USB; ALSA hw:1,0 at reported test | Capture and supplied pinout agree; card numbering is not a permanent device identity |
| Display | Pi CAM/DISP1 / DSI-2; rotation 180 degrees | Supplied pinout only; runtime boot/display configuration not captured |

Reported display overlay: dtoverlay=vc4-kms-dsi-waveshare-panel-v2,4_0_inch_c. Keep as reported configuration pending runtime capture, not a command to apply automatically.

The supplied pinout explains that ESP GPIO41/42/47/48 ToF mapping belongs to the former sensor-on-ESP architecture. It is not the current documented ToF mapping; GPIO48/RGB is not a current ToF collision under the Pi mapping. Exact board/build provenance for encoder GPIO35/36/37 remains separate.

INA260 is pending delivery. All its wiring and address assignments remain TBD; do not reuse INA226 address 0x44 or treat INA260 as installed. Power input, ground routing, connector polarity, protection, motor phase order, encoder supply and amplifier channel/SD straps are not fully specified by this signal table and must not be invented.
