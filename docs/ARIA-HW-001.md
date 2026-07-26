# ARIA-HW-001 — Sprint 2 Hardware Freeze

| Field | Value |
|---|---|
| Document ID | ARIA-HW-001 |
| Revision | A |
| Date | 2026-07-26 |
| Status | Hardware freeze — review required |
| Project phase | Sprint 2 |
| Governing requirement | ARIA-PRD-001 |

## 1. Purpose and authority

This document is the authoritative component register for ARIA V1 entering
mechanical layout and PCB development. It supersedes component selections in
`ARIA-BOM-001.md` and `ARIA-ARCH-001.md`; those documents remain as Sprint 1
design history.

“Frozen” means the function or named product cannot be changed silently. It
does **not** mean every item is ready to order. Items with missing dimensions,
manufacturer part numbers, electrical data, or compatibility evidence remain
on validation hold.

## 2. Freeze states

| State | Meaning |
|---|---|
| `FROZEN-SKU` | Named commercial product is locked. Exact revision/listing must still be recorded before ordering. |
| `FROZEN-SPEC` | Required specification is locked; exact purchasable SKU is still required. |
| `DESIGN-ITEM` | ARIA-specific part or circuit to be designed and reviewed. |
| `VALIDATION-HOLD` | Do not order or manufacture until the stated evidence is recorded. |

## 3. Stable component ID rules

- IDs never get reused, even when a component is retired.
- A replacement receives a new ID and the old record is marked superseded.
- Quantity is an assembly attribute; it does not change the component ID.
- CAD filenames start with the stable ID, for example
  `ARIA-CPU-001_Raspberry-Pi-5.step`.
- PCB references such as `U1` and `J3` are not component IDs.

Prefixes used in Revision A: `CPU`, `MCU`, `THM`, `CAM`, `DSP`, `AUD`, `MOT`,
`WHL`, `SEN`, `PWR`, and `UI`.

## 4. Frozen BOM

### 4.1 Compute, display, camera, and thermal

| ARIA ID | Approved component | Qty | Main interface / supply | Freeze state | CAD and procurement note |
|---|---|---:|---|---|---|
| ARIA-CPU-001 | Raspberry Pi 5, 4 GB | 1 | 5 V; CSI/DSI/USB/GPIO | FROZEN-SKU | Record board revision and official mechanical model. |
| ARIA-MCU-001 | ESP32-S3 DevKit | 1 | 3.3 V logic; UART/I²C/PWM | FROZEN-SPEC, VALIDATION-HOLD | Exact board, flash/PSRAM option, dimensions, and pinout are not selected. |
| ARIA-THM-001 | Official Raspberry Pi Active Cooler for Pi 5 | 1 | Pi 5 fan header | FROZEN-SKU | Use official keep-out and airflow envelope. |
| ARIA-CAM-001 | Raspberry Pi Camera Module 3 Wide NoIR | 1 | CSI | FROZEN-SKU | Cable length, connector orientation, and lens keep-out must be captured. |
| ARIA-DSP-001 | Waveshare 4-inch DSI LCD (C), 720 × 720, touch | 1 | DSI; touch interface per exact revision | FROZEN-SKU, VALIDATION-HOLD | Confirm exact Waveshare revision, cable set, mounting holes, power demand, and CAD dimensions. |

### 4.2 Voice and audio output

| ARIA ID | Approved component | Qty | Main interface / supply | Freeze state | CAD and procurement note |
|---|---|---:|---|---|---|
| ARIA-AUD-001 | reSpeaker XVF3800 USB 4-Mic Array | 1 | USB audio | FROZEN-SKU | Confirm exact product revision and microphone acoustic keep-out. |
| ARIA-AUD-002 | HP Pavilion 15/17 FX390R laptop speaker set, left + right | 1 set | Passive speakers | FROZEN-SKU, VALIDATION-HOLD | Preserve the exact approved listing/photo. Measure the purchased set; impedance, connector, outline, and mounting points are not yet verified. |
| ARIA-AUD-003 | MAX98357A I²S Class-D amplifier module | 2 | Shared I²S; one channel per module; 5 V | FROZEN-SPEC, VALIDATION-HOLD | Select exact module, verify L/R channel selection and speaker load before schematic release. |

### 4.3 Drive system

| ARIA ID | Approved component | Qty | Main interface / supply | Freeze state | CAD and procurement note |
|---|---|---:|---|---|---|
| ARIA-MOT-001 | DFRobot FIT1035 — 2208 BLDC motor with integrated AS5600 encoder | 2 | Three-phase motor; encoder interface | FROZEN-SKU, VALIDATION-HOLD | Exact shaft/hub geometry and encoder connector must be captured from manufacturer data or samples. |
| ARIA-MOT-002 | DFRobot SimpleFOCmini DRI0058 | 2 | PWM control; 3-phase output | FROZEN-SKU, VALIDATION-HOLD | Bench-test current limit and thermal margin with ARIA-MOT-001 before vehicle use. |
| ARIA-WHL-001 | Custom wheel, Ø60 mm × 18–20 mm | 2 | Custom mechanical interface | FROZEN-SPEC, DESIGN-ITEM | Wheel diameter and width are locked. Gear type, ratio, teeth, hub, bearings, and axle remain intentionally open for owner CAD design. |

### 4.4 Navigation and environment sensing

| ARIA ID | Approved component | Qty | Main interface / supply | Freeze state | CAD and procurement note |
|---|---|---:|---|---|---|
| ARIA-SEN-001 | VL53L1X ToF carrier module | 6 | I²C plus shutdown/address control | FROZEN-SPEC, VALIDATION-HOLD | Planned allocation: four horizontal obstacle sensors and two downward cliff sensors. Exact carrier SKU and multi-device address strategy are open. |
| ARIA-SEN-002 | BNO085 IMU breakout | 1 | I²C/SPI per final design | FROZEN-SPEC, VALIDATION-HOLD | Select exact breakout and verify mounting axes, magnetic environment, dimensions, and interface reliability. |
| ARIA-SEN-003 | SHT45 temperature and humidity breakout | 1 | I²C | FROZEN-SPEC, VALIDATION-HOLD | Exact breakout is open. It needs an isolated ventilation path away from Pi, regulators, motors, speakers, and exhaust air. |

### 4.5 Power, protection, and user control

| ARIA ID | Approved component | Qty | Main interface / supply | Freeze state | CAD and procurement note |
|---|---|---:|---|---|---|
| ARIA-PWR-001 | LiPo pouch pack, 3S, 8,000–8,500 mAh | 1 | 12.6 V maximum pack voltage | FROZEN-SPEC, VALIDATION-HOLD | Exact pack, C rating, connector, balance lead, mass, dimensions, and safety certification are open. The 9-hour target is not yet validated. |
| ARIA-PWR-002 | Enerkey EK-BM3r4S30A-NTC BMS | 1 | 3S battery path | FROZEN-SKU, VALIDATION-HOLD | Verify authentic datasheet, 3S configuration, LiPo chemistry support, balance behavior, NTC, continuous current, and dimensions. |
| ARIA-PWR-003 | Pololu D24V90F5 5 V regulator | 1 | 3S input to regulated 5 V | FROZEN-SKU, VALIDATION-HOLD | Complete worst-case load and thermal test with Pi, display, audio, USB, and peripherals. |
| ARIA-PWR-004 | ARIA high-side MOSFET soft-latch power circuit | 1 | Battery path; power button; ESP32 hold/shutdown | DESIGN-ITEM, VALIDATION-HOLD | Target circuit area ≤20 × 15 mm. Exact topology and devices require schematic, fault analysis, and bench validation. |
| ARIA-PWR-005 | INA226 current and voltage monitor | 1 | I²C; high-side shunt | FROZEN-SPEC, VALIDATION-HOLD | Exact IC/breakout, shunt value, Kelvin routing, voltage range, and calibration are open. |
| ARIA-PWR-006 | Littelfuse Nano² 456 Series, 15 A fuse | 1 | Main battery protection | FROZEN-SPEC, VALIDATION-HOLD | Select exact manufacturer part number and confirm time-current curve against wiring and inrush. |
| ARIA-PWR-007 | SMBJ15A TVS diode | 1 | Main input transient clamp | FROZEN-SPEC, VALIDATION-HOLD | Select exact manufacturer and polarity variant; verify standoff/clamp voltage and energy coordination with fuse/BMS. |
| ARIA-PWR-008 | P-channel MOSFET reverse-polarity protection | 1 circuit | Main battery path | DESIGN-ITEM, VALIDATION-HOLD | Exact MOSFET and topology are open; verify gate stress, SOA, dissipation, and interaction with soft latch. |
| ARIA-UI-001 | 12 mm waterproof metal momentary pushbutton with LED ring | 1 | Low-current control signal and LED | FROZEN-SPEC, VALIDATION-HOLD | Exact contact arrangement, LED voltage/color, depth, connector, and mounting drawing are open. It must not switch traction current directly. |

## 5. Frozen system interfaces

These decisions are part of the hardware freeze but are not purchased
components:

| Interface ID | Decision |
|---|---|
| ARIA-IF-001 | Raspberry Pi 5 ↔ ESP32-S3: 3.3 V PL011 UART at 921600 bit/s. |
| ARIA-IF-002 | Binary frames use header, type, length, sequence, payload, and CRC16. |
| ARIA-IF-003 | Heartbeat every 100 ms; ESP32 stops both motors after a 300 ms communication timeout. |
| ARIA-IF-004 | Camera data remains on the Pi CSI path; it is never transported over the control UART. |
| ARIA-IF-005 | ARIA main PCB is a two-layer design whose final outline is derived from the CAD assembly. |

## 6. Compatibility review

| Path | Review result | Required evidence |
|---|---|---|
| 3S LiPo → BMS → protection → motor drivers | Conditional | Confirm BMS chemistry/current behavior, fuse coordination, wiring, inrush, and motor stall protection. |
| 3S LiPo → Pololu 5 V → Pi/display/audio/USB | Conditional | Measured peak load, voltage-drop, ripple, and thermal test. |
| Pi 5 → Camera Module 3 Wide NoIR | Compatible in principle | Correct CSI cable/connector and physical keep-out. |
| Pi 5 → Waveshare DSI display | Conditional | Exact display revision, Pi 5 support, cables, touch path, and current draw. |
| Pi 5 → reSpeaker XVF3800 | Compatible in principle | USB enumeration, Linux audio path, AEC reference strategy, and acoustic test. |
| Pi 5 → two MAX98357A modules | Conditional | I²S overlay/pin allocation, channel selection, clock sharing, mute/startup behavior, and speaker impedance. |
| ESP32-S3 → two SimpleFOCmini → two FIT1035 motors | Conditional | Exact PWM pin allocation, current limit, loop rate, startup calibration, stall behavior, and thermal test. |
| ESP32-S3 → two integrated AS5600 encoders | Unresolved | Two devices may share an address. Choose and prove separate buses, alternate output mode, or another supported topology. |
| ESP32-S3 → six VL53L1X modules | Unresolved | Choose exact carriers and prove XSHUT-based address assignment, multiplexing, or bus partitioning. |
| ESP32-S3 → BNO085/SHT45/INA226 | Conditional | Allocate buses/addresses, select exact breakouts, and test update rates and bus recovery. |
| Pi 5 ↔ ESP32-S3 UART | Compatible in principle | Final pins, boot-state behavior, common ground, cable routing, CRC fault injection, and watchdog test. |

## 7. Required items not yet frozen

The following are required by the product intent or by safe assembly, but no
approved purchasable part exists yet. They must not be silently substituted:

- Boot storage for Raspberry Pi 5.
- LiPo balance charger, charge connector, and service disconnect method.
- mmWave presence sensor required by the PRD.
- Physical bumper/contact sensors required by the PRD.
- NoIR illumination and ambient-light strategy for night operation.
- Hardware microphone/camera privacy switches and their visible indicators.
- Exact cables, connectors, wire gauges, strain relief, and service loops.
- Caster/support wheel, axles, bearings, fasteners, and transmission geometry.
- Mainboard connectors, mounting hardware, and test points.

## 8. CAD release requirements

No part is marked CAD-ready until its record includes:

1. source URL or measured sample identity;
2. X/Y/Z envelope and mass;
3. mounting holes, connector positions, and cable bend keep-outs;
4. airflow, acoustic, optical, magnetic, or service keep-outs as applicable;
5. source confidence: manufacturer model, verified community model, or
   measured in-house model;
6. a STEP model and a dimensioned drawing checked against the source.

The CAD library lives in `cad/parts/`. Assembly coordinates, PCB origin, and
robot origin will be defined in `ARIA-MECH-001.md`.

## 9. PCB and procurement gates

PCB layout may begin only after the exact ESP32 board, battery pack, display
revision, audio amplifier modules, speaker set, sensor carriers, and power
protection devices are resolved.

Ordering is authorized only after:

- every `VALIDATION-HOLD` affecting the order is closed;
- the main power budget and protection coordination are reviewed;
- a 1:1 CAD interference check is complete;
- schematic ERC and PCB DRC pass;
- the user reviews the resulting BOM and manufacturing package.

Until then, this is a **design freeze**, not a purchase release.
