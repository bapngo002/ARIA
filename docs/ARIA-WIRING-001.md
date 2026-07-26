# ARIA-WIRING-001 — Wiring and Internal Interfaces

| Field | Value |
|---|---|
| Document ID | ARIA-WIRING-001 |
| Revision | A |
| Status | Sprint 2 interface baseline |
| Governing documents | ARIA-PRD-001, ARIA-BOM-001, ARIA-HW-001, ARIA-PCB-001 |

## Frozen control link

`ARIA-CPU-001` and `ARIA-MCU-001` communicate over a 3.3 V hardware PL011 UART at
921600 bit/s:

```text
CPU TX  -> MCU RX
CPU RX  <- MCU TX
GND    -- GND
```

The protocol uses binary frames with header, type, length, sequence, payload,
and CRC16. Heartbeat interval is 100 ms. If no valid control heartbeat is
received for 300 ms, the MCU commands both motors to stop.

## Wiring principles

- Battery and motor current never pass through breadboards or the 12 mm button.
- High-current wiring is short, fused, strain-relieved, and routed away from
  audio, IMU, camera, and sensor wiring.
- Motor phase wires are grouped together and kept away from UART/I²C/USB.
- Logic and power returns use a reviewed grounding topology; “common ground”
  does not permit uncontrolled shared high-current return paths.
- Permanent internal connections may be soldered only when service replacement
  is not reasonably expected. Replaceable assemblies use keyed connectors.
- Direct soldering is preferred where it safely reduces volume, but battery,
  fuse, storage, compute, camera, display, motors, speakers, and other service
  parts retain a documented disconnect or service method.
- Wire gauge, insulation, connector family, pinout, and current derating remain
  open until the measured power budget and CAD routing are complete.

## Interface register

| Interface | Endpoints | State / open work |
|---|---|---|
| UART | `ARIA-CPU-001` ↔ `ARIA-MCU-001` | Speed/protocol frozen; exact pins and boot states open. |
| CSI | `ARIA-CPU-001` ↔ `ARIA-CAM-001` | Exact cable and routing open. |
| DSI/touch | `ARIA-CPU-001` ↔ `ARIA-DSP-001` | Exact revision, cables, and touch path open. |
| USB audio | `ARIA-CPU-001` ↔ `ARIA-AUD-001` | Port allocation and reconnect behavior open. |
| I²S audio | `ARIA-CPU-001` ↔ `ARIA-AUD-003` | Pins, overlays, channel selection, mute, and grounding open. |
| Motor PWM | `ARIA-MCU-001` ↔ `ARIA-MOT-002` | Exact pins, enable/fault behavior, and loop timing open. |
| Encoder | `ARIA-MCU-001` ↔ encoder in `ARIA-MOT-001` | Address/topology unresolved. |
| ToF | `ARIA-MCU-001` ↔ `ARIA-SEN-001` | Carrier, XSHUT/address plan, update schedule unresolved. |
| Sensor bus | `ARIA-MCU-001` ↔ `ARIA-SEN-002`/`003` and `ARIA-PWR-005` | Bus allocation, addresses, recovery, and sample rates open. |
| Shutdown | `ARIA-UI-001`, CPU, and MCU ↔ `ARIA-PWR-004` | State machine, voltage domains, fail-safe states open. |

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
- [ ] Encoder and multi-ToF strategies pass bench tests.
- [ ] Peak and continuous current are measured.
- [ ] Every connector is keyed or clearly protected against reversal.
- [ ] Motor-stop behavior is proven for UART loss, CPU crash, MCU reset, and
      sensor failure.
