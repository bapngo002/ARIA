# ARIA-BOM-001 — ARIA V1 Master Bill of Materials

| Field | Value |
|---|---|
| Document ID | ARIA-BOM-001 |
| Revision | B |
| Date | 2026-07-27 |
| Status | Conversation synchronized; hardware frozen with validation holds |
| Governing requirement | ARIA-PRD-001 |

## 1. Authority

This file is the **single source of truth** for ARIA V1 component identities,
quantities, freeze states, and open procurement data.

- Other documents refer to parts by ARIA ID and do not duplicate approved model
  names or quantities.
- A changed or replacement component receives a new ARIA ID. IDs are never
  reused.
- A component is purchasable only when its exact SKU, source, electrical data,
  mechanical data, and applicable validation evidence are complete.
- Prices and supplier links will be added only against exact purchasable
  variants. An approximate marketplace listing is not an approved source.
- `ARIA-HW-001.md` records the Sprint 2 freeze decision and compatibility gates;
  it does not supersede this BOM.
- Historical conversation IDs are not copied when they conflict with an
  existing canonical ID. The canonical mapping in this file wins.

## 2. Freeze states

| State | Meaning |
|---|---|
| `FROZEN-SKU` | The named commercial product is locked. Exact revision or listing may still require validation. |
| `FROZEN-SPEC` | The required specification is locked; an exact purchasable SKU is still required. |
| `OPEN-REQUIRED` | The function is required, but neither its specification nor an exact SKU is frozen. |
| `DESIGN-ITEM` | ARIA-specific mechanical part or circuit must be designed and reviewed. |
| `VALIDATION-HOLD` | Do not order or manufacture until the stated evidence is recorded. |

## 3. Compute, display, camera, and thermal

| ARIA ID | Approved component | Qty | Interface / supply | State | Open procurement and CAD data |
|---|---|---:|---|---|---|
| ARIA-CPU-001 | Raspberry Pi 5, 4 GB | 1 | 5 V; CSI/DSI/USB/GPIO | FROZEN-SKU | Record board revision and official mechanical model. |
| ARIA-MCU-001 | Espressif ESP32-S3-DevKitC-1, N16R8 target variant | 1 | 3.3 V logic; UART/I²C/PWM | FROZEN-SKU, VALIDATION-HOLD | Confirm the purchased board carries the ESP32-S3-WROOM N16R8 variant and matches the imported CAD and pinout. |
| ARIA-THM-001 | Official Raspberry Pi Active Cooler for Pi 5 | 1 | Pi 5 fan header | FROZEN-SKU | Capture official keep-out and airflow envelope. |
| ARIA-CAM-001 | Raspberry Pi Camera Module 3 Wide NoIR | 1 | CSI | FROZEN-SKU | Record cable length, connector orientation, lens keep-out, and mounting geometry. |
| ARIA-DSP-001 | Waveshare 4-inch DSI LCD (C), **round**, 720 × 720, 10-point touch, SKU 24603 | 1 | DSI; I²C touch; 5 V | FROZEN-SKU, VALIDATION-HOLD | Ø126.00 × 17.00 mm; active area Ø101.52 mm; 4 × M4 on 85.00 × 65.00 mm pattern. Confirm cables, rear keep-outs, power demand, and CAD geometry. |
| ARIA-STO-001 | High Endurance microSD, 64 GB, A2 | 1 | Raspberry Pi microSD | FROZEN-SPEC, VALIDATION-HOLD | Select exact manufacturer SKU and endurance rating. |

## 4. Voice and audio output

| ARIA ID | Approved component | Qty | Interface / supply | State | Open procurement and CAD data |
|---|---|---:|---|---|---|
| ARIA-AUD-001 | reSpeaker XVF3800 USB 4-Mic Array | 1 | USB audio | FROZEN-SKU | Confirm exact product revision and acoustic keep-out. |
| ARIA-AUD-002 | HP Pavilion 15/17 FX390R laptop speaker set, left + right | 1 set | Passive speakers | FROZEN-SKU, VALIDATION-HOLD | Preserve the approved listing/photo. Measure impedance, connector, outline, acoustic ports, and mounting points from the purchased set. |
| ARIA-AUD-003 | MAX98357A I²S Class-D amplifier module | 2 | Shared I²S; one channel per module; 5 V | FROZEN-SPEC, VALIDATION-HOLD | Select exact module and verify channel selection, startup mute, and speaker load. |

## 5. Drive system

| ARIA ID | Approved component | Qty | Interface / supply | State | Open procurement and CAD data |
|---|---|---:|---|---|---|
| ARIA-MOT-001 | DFRobot FIT1035 — 2208 BLDC motor with integrated AS5600 encoder | 2 | Three-phase motor; integrated encoder | FROZEN-SKU, VALIDATION-HOLD | Capture exact shaft/hub geometry, connector, and manufacturer mechanical data. |
| ARIA-MOT-002 | DFRobot SimpleFOCmini DRI0058 | 2 | PWM control; three-phase output | FROZEN-SKU, VALIDATION-HOLD | Bench-test current limit and thermal margin with ARIA-MOT-001. |
| ARIA-WHL-001 | Custom wheel, Ø60 mm × 18–20 mm | 2 | Custom mechanical interface | FROZEN-SPEC, DESIGN-ITEM | Diameter and width are locked. Gear type, ratio, teeth, hub, bearings, and axle remain intentionally open for CAD design. |
| ARIA-MEC-001 | Caster or support wheel assembly | 1 | Mechanical | OPEN-REQUIRED, VALIDATION-HOLD | Select after ground clearance and centre-of-mass layout are known. |

## 6. Navigation and environment sensing

| ARIA ID | Approved component | Qty | Interface / supply | State | Open procurement and CAD data |
|---|---|---:|---|---|---|
| ARIA-SEN-001 | VL53L1X ToF carrier module | 6 | I²C plus XSHUT/address control | FROZEN-SPEC, VALIDATION-HOLD | Four horizontal obstacle sensors and two downward cliff sensors. Select exact carrier and prove the multi-device strategy. |
| ARIA-SEN-002 | BNO085 IMU breakout | 1 | I²C or SPI per final design | FROZEN-SPEC, VALIDATION-HOLD | Select exact breakout; verify axes, magnetic environment, dimensions, and interface reliability. |
| ARIA-SEN-003 | SHT45 temperature and humidity breakout | 1 | I²C | FROZEN-SPEC, VALIDATION-HOLD | Select exact breakout and provide an isolated ventilation path away from internal heat and exhaust. |
| ARIA-SEN-004 | Physical bumper/contact sensor assembly | 1 set | ESP32 digital inputs | OPEN-REQUIRED, VALIDATION-HOLD | Select switch count, geometry, and fail-safe wiring after chassis layout. |
| ARIA-SEN-005 | mmWave presence sensor | 1 | Interface open | OPEN-REQUIRED, VALIDATION-HOLD | Required by the PRD; select an exact module after field-of-view and software-support review. |
| ARIA-SEN-006 | NoIR illumination and ambient-light system | 1 set | Supply/control open | OPEN-REQUIRED, VALIDATION-HOLD | Required for night operation; select after camera placement and thermal review. |

## 7. Power, protection, charging, and control

| ARIA ID | Approved component | Qty | Interface / supply | State | Open procurement and CAD data |
|---|---|---:|---|---|---|
| ARIA-PWR-001 | LiPo pouch pack, 3S, 8,000–8,500 mAh | 1 | 12.6 V maximum | FROZEN-SPEC, VALIDATION-HOLD | Select exact pack, C rating, connector, balance lead, mass, dimensions, and safety documentation. Runtime remains unvalidated. |
| ARIA-PWR-002 | Enerkey EK-BM3r4S30A-NTC BMS | 1 | 3S battery path | FROZEN-SKU, VALIDATION-HOLD | Verify authentic datasheet, LiPo support, balance behavior, NTC, current rating, and dimensions. |
| ARIA-PWR-003 | Pololu D24V90F5 5 V regulator | 1 | 3S input to regulated 5 V | FROZEN-SKU, VALIDATION-HOLD | Complete peak-load, voltage-drop, ripple, and thermal tests. |
| ARIA-PWR-004 | ARIA high-side MOSFET soft-latch circuit using AO3401A as the low-current latch/control device | 1 | Battery path; button; ESP32 hold/shutdown | DESIGN-ITEM, VALIDATION-HOLD | Target circuit area ≤20 × 15 mm. AO3401A is not approved as the main 15 A pass device; complete topology, fault analysis, and bench validation. |
| ARIA-PWR-005 | INA226 current and voltage monitor | 1 | I²C; high-side shunt | FROZEN-SPEC, VALIDATION-HOLD | Select exact IC or module, shunt value, Kelvin routing, range, and calibration. |
| ARIA-PWR-006 | Littelfuse Nano² 456 Series, 15 A fuse | 1 | Main battery protection | FROZEN-SPEC, VALIDATION-HOLD | Select exact manufacturer part number and verify the time-current curve against wiring and inrush. |
| ARIA-PWR-007 | SMBJ15A TVS diode | 1 | Main input transient clamp | FROZEN-SPEC, VALIDATION-HOLD | Select exact manufacturer and polarity variant; verify standoff/clamp voltage and fuse/BMS coordination. |
| ARIA-PWR-008 | Reverse-polarity circuit using Infineon IPT015N10N5 as the frozen candidate power MOSFET | 1 | Main battery path | FROZEN-SKU, DESIGN-ITEM, VALIDATION-HOLD | This is an N-channel device, so the earlier P-channel shorthand is superseded. Verify exact suffix/package, gate drive, SOA, dissipation, and interaction with the soft latch before footprint release. |
| ARIA-PWR-009 | LiPo 3S balance charger and charge lead | 1 set | 3S LiPo charging | OPEN-REQUIRED, VALIDATION-HOLD | Select a safe, documented charger and connector before battery procurement. |
| ARIA-PWR-010 | Battery service disconnect | 1 | Main battery path | OPEN-REQUIRED, VALIDATION-HOLD | Select a compact keyed connector after current and CAD review. |
| ARIA-UI-001 | 12 mm waterproof metal momentary pushbutton with LED ring | 1 | Low-current signal and LED | FROZEN-SPEC, VALIDATION-HOLD | Select contact arrangement, LED voltage/color, body depth, connector, and mounting drawing. It must not carry traction current. |
| ARIA-UI-002 | Hardware microphone privacy switch and indicator | 1 set | Hardware power/control cut | OPEN-REQUIRED, VALIDATION-HOLD | Required by the PRD; exact topology and parts are open. |
| ARIA-UI-003 | Hardware camera privacy switch and indicator | 1 set | Hardware power/control cut | OPEN-REQUIRED, VALIDATION-HOLD | Required by the PRD; exact topology and parts are open. |

## 8. Interconnect and assembly items

These entries are required for a complete purchasable BOM. Exact quantities are
derived from the approved CAD assembly and wiring table.

| ARIA ID | Approved component | Qty | State | Open data |
|---|---|---:|---|---|
| ARIA-CBL-001 | Internal cable and harness set | 1 set | DESIGN-ITEM, VALIDATION-HOLD | Define wire gauges, lengths, colors, labels, strain relief, and service loops. |
| ARIA-CON-001 | Keyed connector set | 1 set | OPEN-REQUIRED, VALIDATION-HOLD | Select families, pin counts, current derating, and keying rules. |
| ARIA-MEC-002 | Fastener and standoff set | 1 set | OPEN-REQUIRED, VALIDATION-HOLD | Derive sizes and quantities from the approved assembly. |
| ARIA-BRD-001 | ARIA two-layer mainboard | 1 | DESIGN-ITEM, VALIDATION-HOLD | Outline comes from the CAD assembly. Release only after schematic/PCB review and manufacturing checks. |

## 9. Frozen non-purchasable interfaces

| Interface ID | Decision |
|---|---|
| ARIA-IF-001 | Raspberry Pi 5 ↔ ESP32-S3: 3.3 V PL011 UART at 921600 bit/s. |
| ARIA-IF-002 | Binary frames contain header, type, length, sequence, payload, and CRC16. |
| ARIA-IF-003 | Heartbeat every 100 ms; ESP32 stops both motors after a 300 ms valid-frame timeout. |
| ARIA-IF-004 | Camera data stays on the Pi CSI path and is never transported over the control UART. |
| ARIA-IF-005 | The ARIA main PCB uses two copper layers; its final outline is derived from the approved CAD assembly. |

## 10. Procurement fields

Before any order, add the following evidence to the relevant BOM row or linked
component record:

1. exact manufacturer and part number;
2. supplier URL and captured listing revision;
3. delivered unit price and quote date;
4. electrical ratings and interface evidence;
5. X/Y/Z envelope, mass, mounting points, connectors, and keep-outs;
6. manufacturer datasheet and STEP model, or measurements from an identified
   physical sample;
7. closed validation holds and approving review.

The BOM currently authorizes **design work only**. It does not authorize a full
purchase or manufacturing release.

## 11. Synchronization notes

- Canonical camera ID: `ARIA-CAM-001`. A user CAD filename containing
  `ARIA-SEN-001` was normalized because `ARIA-SEN-001` already identifies the
  six VL53L1X modules.
- `AO3401A` is recorded inside `ARIA-PWR-004`; it is not duplicated as another
  standalone ARIA assembly.
- `IPT015N10N5` is recorded inside `ARIA-PWR-008`. Its electrical use remains on
  validation hold despite the model decision being frozen.
- `ARIA-THM-001` is the Official Raspberry Pi Active Cooler and is represented
  with `ARIA-CPU-001` in the imported CPU CAD assembly.
