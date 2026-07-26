# ARIA-WIRING-001 — Wiring and Internal Interfaces

| Field | Value |
|---|---|
| Document ID | ARIA-WIRING-001 |
| Revision | 0 |
| Status | Sprint 2 placeholder |
| Governing documents | ARIA-PRD-001, ARIA-HW-001, ARIA-PCB-001 |

## Frozen control link

Raspberry Pi 5 and ESP32-S3 communicate over a 3.3 V hardware PL011 UART at
921600 bit/s:

```text
Pi TX  -> ESP32 RX
Pi RX  <- ESP32 TX
GND    -- GND
```

The protocol uses binary frames with header, type, length, sequence, payload,
and CRC16. Heartbeat interval is 100 ms. If no valid control heartbeat is
received for 300 ms, the ESP32 commands both motors to stop.

## Wiring principles

- Battery and motor current never pass through breadboards or the 12 mm button.
- High-current wiring is short, fused, strain-relieved, and routed away from
  audio, IMU, camera, and sensor wiring.
- Motor phase wires are grouped together and kept away from UART/I²C/USB.
- Logic and power returns use a reviewed grounding topology; “common ground”
  does not permit uncontrolled shared high-current return paths.
- Permanent internal connections may be soldered only when service replacement
  is not reasonably expected. Replaceable assemblies use keyed connectors.
- Wire gauge, insulation, connector family, pinout, and current derating remain
  open until the measured power budget and CAD routing are complete.

## Interface register

| Interface | Endpoints | State / open work |
|---|---|---|
| UART | Pi 5 ↔ ESP32-S3 | Speed/protocol frozen; exact pins and boot states open. |
| CSI | Pi 5 ↔ Camera Module 3 | Exact cable and routing open. |
| DSI/touch | Pi 5 ↔ Waveshare display | Exact revision, cables, and touch path open. |
| USB audio | Pi 5 ↔ reSpeaker XVF3800 | Port allocation and reconnect behavior open. |
| I²S audio | Pi 5 ↔ 2 × MAX98357A | Pins, overlays, channel selection, mute, and grounding open. |
| Motor PWM | ESP32-S3 ↔ 2 × SimpleFOCmini | Exact pins, enable/fault behavior, and loop timing open. |
| Encoder | ESP32-S3 ↔ 2 × integrated AS5600 | Address/topology unresolved. |
| ToF | ESP32-S3 ↔ 6 × VL53L1X | Carrier, XSHUT/address plan, update schedule unresolved. |
| Sensor bus | ESP32-S3 ↔ BNO085/SHT45/INA226 | Bus allocation, addresses, recovery, and sample rates open. |
| Shutdown | Button/Pi/ESP32 ↔ soft latch | State machine, voltage domains, fail-safe states open. |

## Required outputs

- final block diagram and power tree;
- connector family and keying rules;
- complete pin-allocation table;
- wire gauge/current/length table;
- harness drawing with stable cable IDs;
- grounding and shielding diagram;
- UART packet specification and fault behavior;
- assembly inspection and continuity-test checklist.

## Release gates

- [ ] Exact module variants and connector orientations are known.
- [ ] AS5600 and VL53L1X multi-device strategies pass bench tests.
- [ ] Peak and continuous current are measured.
- [ ] Every connector is keyed or clearly protected against reversal.
- [ ] Motor-stop behavior is proven for UART loss, Pi crash, ESP32 reset, and
      sensor failure.
