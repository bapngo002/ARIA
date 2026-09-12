# ARIA-WIRING-001 — Wiring and safety rules

Purchased component identity and quantity come only from [`docs/ARIA-BOM-001.md`](ARIA-BOM-001.md).

- Battery and motor current must not pass through breadboards or low-current buttons.
- Use short, fused, strain-relieved high-current wiring.
- Route motor phases and switching power away from audio, camera, IMU and control wiring.
- Verify connector polarity, wire gauge, current derating and service disconnects.
- Keep replaceable parts disconnectable.
- Prove motor stop behavior for loss of the main computer, controller reset and sensor faults.
- The canonical controller family is recorded in the BOM. Pi↔ESP32 protocol and integrated wiring still need validation; controller selection is no longer waiting for an inventory entry.
- Preserve the historical bench pinmap and unresolved pin holds in the [master handoff](ARIA-MASTER-HANDOFF.md#pinmap-bench-được-bảo-tồn--chưa-là-pinmap-tích-hợp-đã-release). The former ESP ToF mapping is historical. For a replacement N16R8 board, follow the proposed PCB revision below: do not allocate memory pins GPIO35/36/37.

This file intentionally contains no connector BOM, component list or CAD status copy.

## Power sensing and battery protection

Use INA260 for current power-sensing wiring; board identity and quantity are in the canonical BOM. Verify the delivered boards and I²C address configuration before finalizing the harness. Battery protection uses the 3S BMS inside the battery pack; validate the pack protection and charging connections as part of the battery assembly.

## Previous captured signal mapping — 2026-09-12 (preserved evidence, not replacement-PCB wiring)

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

## Replacement carrier PCB — proposed signal allocation R1

Status: DESIGN PROPOSAL / NOT RELEASED FOR SOLDERING OR FABRICATION. User reported ESP burned and requested pin optimization for a new PCB, confirming replacement is the same board type, YD-ESP32-S3 N16R8. Assume a carrier connecting existing modules; integration of bare power/driver ICs and PCB dimensions are not specified. Historical firmware/capture is preserved and has NOT been edited to this map. Do not run captured firmware on the new map.

### Why change the encoder pins

Espressif WROOM-1 datasheet v1.8 Table 1-1 identifies N16R8 as Octal PSRAM; Table 3-1 note b explicitly reserves IO35/36/37 for that memory. New encoder allocation must avoid those pins regardless of historical PASS labels. GPIO4/5/8/9 are general-purpose module I/O and appear on the stored YD family pinout. This establishes a design constraint, not the cause of the burned board or proof of the old board identity/build.

### ESP32 signal allocation (GPIO labels, not header pad numbers)

| Net | ESP GPIO proposed | Previous GPIO | Endpoint |
|---|---:|---:|---|
| ESP_MOTOR_L_IN1 | 15 | 15 | Left DRI0058 IN1 |
| ESP_MOTOR_L_IN2 | 16 | 16 | Left DRI0058 IN2 |
| ESP_MOTOR_L_IN3 | 17 | 17 | Left DRI0058 IN3 |
| ESP_MOTOR_L_EN | 18 | 18 | Left DRI0058 EN |
| ESP_MOTOR_R_IN1 | 11 | 11 | Right DRI0058 IN1 |
| ESP_MOTOR_R_IN2 | 12 | 12 | Right DRI0058 IN2 |
| ESP_MOTOR_R_IN3 | 13 | 13 | Right DRI0058 IN3 |
| ESP_MOTOR_R_EN | 14 | 14 | Right DRI0058 EN |
| ESP_ENC_L_SDA | 8 | 38 | Left FIT1035 encoder SDA, I2C controller 0 |
| ESP_ENC_L_SCL | 9 | 35 | Left FIT1035 encoder SCL, I2C controller 0 |
| ESP_ENC_R_SDA | 4 | 36 | Right FIT1035 encoder SDA, I2C controller 1 |
| ESP_ENC_R_SCL | 5 | 37 | Right FIT1035 encoder SCL, I2C controller 1 |

Keep separate encoder buses; do not short their SDA/SCL nets together. Both keep their own 3.3V pull-up network, accounting for resistors already on the encoder boards. Values and bus speed need cable-capacitance/rise-time checks; no blanket pull-up installation in parallel. Manufacturer specifies FIT1035 encoder operation at 3.3V; do not confuse motor 12V with encoder supply.

Reserve ESP19/20 for native USB; preserve 0/3/45/46 boot strapping; do not allocate flash/PSRAM signals (including 35–37); leave RGB48, UART0 43/44 and JTAG39–42 out of peripheral allocation. GPIO6/7/10/21/38/47 remain unassigned by this draft; do not treat them as final assignments for optional switches/faults without a circuit. ESP CHIP_EN/RST is not the same signal as either MOTOR_EN.

### Pi 40-pin header — retained signals

Physical numbers below apply to the Pi header viewed from its component side with pin 1 identified; they do not describe the mirrored solder side of a carrier. Pi GPIO and ESP GPIO are separate electrical nets even when their numeric suffixes match.

| Net/function | Pi BCM GPIO | Pi physical header pin | Endpoint |
|---|---:|---:|---|
| PI_I2C_SDA | 2 | 3 | Shared BME280/BNO085/ToF SDA |
| PI_I2C_SCL | 3 | 5 | Shared BME280/BNO085/ToF SCL |
| PI_TOF1_XSHUT | 22 | 15 | S1 XSHUT |
| PI_TOF2_XSHUT | 23 | 16 | S2 XSHUT |
| PI_TOF3_XSHUT | 24 | 18 | S3 XSHUT |
| PI_TOF4_XSHUT | 25 | 22 | S4 XSHUT |
| PI_I2S_BCLK | 18 | 12 | Both MAX98357A BCLK |
| PI_I2S_LRCLK | 19 | 35 | Both MAX98357A LRC |
| PI_I2S_DOUT | 21 | 40 | Both MAX98357A DIN |

Supply pin identification only: Pi 3.3V is physical 1/17; 5V is 2/4; GND is 6/9/14/20/25/30/34/39. This is NOT approval to feed Pi from the carrier header. Keep Pi/ESP 3.3V regulator outputs separate; shared GND does not mean parallel power outputs. Do not connect 5V to any signal GPIO. Pi GPIO0/1 (physical27/28) remain reserved for HAT identification; unused pins remain NC in this carrier draft. Allocate no INA260 signal/address yet, as expressly requested until the board arrives.

Camera retains CAM/DISP0; display retains CAM/DISP1 and reported DSI overlay; microphone remains USB; ESP link remains native USB. Use original FFC/USB connectors and cables for these links, not hand-routed substitute CSI/DSI or USB data traces. Fan uses existing Pi fan connector, not a newly assigned GPIO. MAX98357A left/right channel and shutdown straps remain to verify; shared I2S wiring alone does not select stereo. Speaker outputs are differential: do not join speaker negative outputs to logic ground or each other.

### Power and PCB organization

- For isolated replacement-controller bring-up, use one USB power source for ESP at a time with all suspect encoder/driver harnesses disconnected. For the carrier proposal, ESP supply comes through the Pi native-USB link; do not also connect carrier 5V or 3.3V as an ESP supply input. Verify actual YD power routing before a different dual-source scheme. USB and signal grounds are common, not galvanically isolated; provide intentional ground returns so motor current does not use USB/encoder/Pi wiring.
- Separate protected motor-power branches from regulated 5V electronics and 3.3V logic. Do not join Pi and ESP regulator outputs or driver auxiliary 3.3V outputs. DRI0058 auxiliary 3.3V is rated only 10mA by the manufacturer: never power ESP from it. Trace widths, connector current ratings, fuse values and power-entry topology require actual loads/board specifications; not assigned by pin selection.
- Place ESP on replaceable sockets if mechanical space permits, leave USB/BOOT/RESET accessible, respect antenna keep-out. Put each driver connection and encoder connector in distinct labeled groups, keep motor phase/high-current paths away from encoder/I2C/audio. Use continuous intentional reference/return routing; do not casually split ground planes under signals.
- Label nets with ESP_/PI_ prefixes, rail voltage, connector pin1 and component-side orientation. Give left/right encoders separate keyed connectors and check their actual GH1.25 cable order; do not infer it from wire color. Driver revision controls physical IN1/IN2/IN3/EN order. No physical YD pad numbering, connector footprint, or mirrored solder layout is released until replacement board and connector orientation are checked.
- Provide EN default-low circuitry near both drivers, test points for rails/GND/SDA/SCL/EN, and provision for an independent motor-disable path. Pulldown values and hard-stop circuit still need schematic review; a GPIO-only stop is not a completed hardware E-stop. Driver outputs must remain disabled with ESP absent/reset/unpowered and through power sequencing.
- Current source calls driver.init and initFOC during startup; it can energize motors before normal control is ready. A passive EN pulldown alone does not defeat an actively driven HIGH. Firmware gating, encoder-failure behavior, command timeout and disable/reset tests remain required before connecting motor power.

### Incident recovery and release checklist

- [x] User specifies same YD N16R8 replacement family.
- [x] Propose conflict-free per-controller signal allocation and retain captured baseline.
- [ ] Identify failed component and incident supply path; inspect isolated harnesses for shorts/reversal before reuse. Encoder condition is UNKNOWN, not presumed damaged or passed.
- [ ] Confirm replacement markings/revision, connector orientation, PCB type/dimensions and module footprints.
- [ ] Check each isolated encoder with correctly limited 3.3V supply and independent communication; replacement MCU is not a sacrificial tester. Preserve results individually.
- [ ] Verify regulator outputs, power sequencing, I2C pull-ups/logic voltages and inactive EN behavior; no motor power during initial tests.
- [ ] Draw/review electrical schematic including power/disable paths, ERC, layout/DRC and 1:1 fit check before production PCB release. For perfboard, review the actual point-to-point solder plan and unpowered continuity instead.
- [ ] Prepare separately versioned firmware pin changes and fault handling; preserve captured/LKG sources; validate build and non-motion tests first.
- [ ] Only then isolated motor/stop tests; log hardware, firmware/build, supply and result. INA260 remains deferred pending delivery.

### Sources and review

- [Espressif WROOM-1/1U datasheet, Tables 1-1 and 3-1; boot configuration](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf).
- [Raspberry Pi official header documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-and-the-40-pin-header).
- [DFRobot FIT1035 specification: encoder supply and connector](https://wiki.dfrobot.com/fit1035/).
- [DFRobot DRI0058 specification: EN and auxiliary supply](https://wiki.dfrobot.com/dri0058).
- [Analog Devices MAX98357A/MAX98357B datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf) — speaker/channel circuitry must match actual module.

Copilot Pro CLI supplied a bounded review (1.76 AI credits, no file changes). Its claimed numeric GPIO collision between Pi and ESP and claimed contradiction between common ground and USB power were rejected: different MCUs have distinct GPIOs, and intentional common ground is compatible with USB. Pull-up, power-sequencing, EN/boot and missing-footprint concerns were retained for primary review. No assistant review is hardware verification.
