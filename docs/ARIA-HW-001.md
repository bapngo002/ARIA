# ARIA-HW-001 — Sprint 2 Hardware Freeze

| Field | Value |
|---|---|
| Document ID | ARIA-HW-001 |
| Revision | A |
| Date | 2026-07-26 |
| Status | Hardware freeze — review required |
| Project phase | Sprint 2 |
| Governing documents | ARIA-PRD-001, ARIA-BOM-001 |

## 1. Purpose

This document records the Sprint 2 hardware-freeze decision, compatibility
review, and release gates. Component identities, quantities, and freeze states
are maintained only in `ARIA-BOM-001.md`.

The freeze permits CAD, schematic, and bench-validation work. It does **not**
authorize procurement, PCB fabrication, or enclosure manufacturing.

## 2. Freeze result

- `ARIA-CPU-001` and `ARIA-MCU-001` form the two-level compute architecture.
- The voice, display, camera, drive, sensing, power, and cooling selections in
  BOM Revision A are frozen for design.
- The wheel envelope is frozen at Ø60 mm × 18–20 mm; transmission geometry
  remains intentionally open.
- The mainboard is a two-layer design whose outline comes from the approved CAD
  assembly.
- The initial 150 × 150 × 150 mm volume is a packaging target, not a final
  enclosure constraint.
- Exact variants and validation evidence remain mandatory where the BOM marks a
  `VALIDATION-HOLD`.

## 3. Compatibility review

| Path | Review result | Required evidence |
|---|---|---|
| `ARIA-PWR-001` → `ARIA-PWR-002` → protection → `ARIA-MOT-002` | Conditional | Confirm chemistry/current behavior, fuse coordination, wiring, inrush, and motor stall protection. |
| `ARIA-PWR-001` → `ARIA-PWR-003` → 5 V loads | Conditional | Measure peak load, voltage drop, ripple, and temperature. |
| `ARIA-CPU-001` → `ARIA-CAM-001` | Compatible in principle | Confirm CSI cable, connector, and physical keep-out. |
| `ARIA-CPU-001` → `ARIA-DSP-001` | Conditional | Confirm exact revision, host support, cable set, touch path, and current draw. |
| `ARIA-CPU-001` → `ARIA-AUD-001` | Compatible in principle | Verify USB enumeration, Linux audio path, AEC reference strategy, and acoustics. |
| `ARIA-CPU-001` → `ARIA-AUD-003` | Conditional | Verify I²S pin allocation, channel selection, shared clocks, mute/startup behavior, and speaker impedance. |
| `ARIA-MCU-001` → `ARIA-MOT-002` → `ARIA-MOT-001` | Conditional | Verify PWM allocation, current limits, loop rate, calibration, stall behavior, and temperature. |
| `ARIA-MCU-001` → encoders integrated in `ARIA-MOT-001` | Unresolved | Prove separate buses, supported alternate output mode, or another valid topology. |
| `ARIA-MCU-001` → `ARIA-SEN-001` | Unresolved | Prove XSHUT address assignment, bus partitioning, or multiplexing with the exact carriers. |
| `ARIA-MCU-001` → `ARIA-SEN-002`/`003` and `ARIA-PWR-005` | Conditional | Allocate interfaces and test update rate, address conflicts, and bus recovery. |
| `ARIA-CPU-001` ↔ `ARIA-MCU-001` | Compatible in principle | Verify pins, boot states, ground, routing, CRC fault handling, and watchdog stop. |

## 4. CAD readiness gate

A component is CAD-ready only when it has:

1. an identified manufacturer source or measured physical sample;
2. X/Y/Z envelope and mass;
3. mounting holes, connectors, and cable-bend keep-outs;
4. airflow, acoustic, optical, magnetic, or service keep-outs as applicable;
5. a confidence label: manufacturer model, verified community model, or
   measured in-house model;
6. a STEP model and dimensioned drawing checked against the source.

Verified part models live in `cad/parts/`. The robot coordinate system and
assembly rules are defined in `ARIA-MECH-001.md`.

## 5. PCB readiness gate

PCB layout begins only after the exact variants of the MCU, battery, display,
amplifiers, speakers, sensor carriers, connectors, and power-protection devices
in the BOM are resolved.

Before fabrication:

- the power tree and protection coordination are reviewed;
- schematic ERC and PCB DRC pass;
- a populated-board STEP model passes the 1:1 CAD interference check;
- the wiring and connector register is frozen;
- the manufacturing package identifies its source commit;
- the user reviews and approves the release.

## 6. Procurement gate

An order is authorized only after:

- all applicable BOM validation holds are closed;
- exact manufacturer part numbers and supplier variants are recorded;
- the power, thermal, acoustic, and motor bench tests pass;
- the 1:1 CAD packing study is complete;
- the total delivered cost and contingency are reviewed.

Until then, Sprint 2 remains a **design freeze**, not a purchase release.

## 7. Sprint 2 exit criteria

- [ ] Every frozen component has a verified CAD envelope and source record.
- [ ] Unresolved encoder and multi-ToF strategies pass bench tests.
- [ ] The battery, display, MCU, speakers, and sensor carrier variants are exact.
- [ ] The power tree and mainboard functional scope are approved.
- [ ] The master assembly has no hard interference and preserves service access.
- [ ] PCB outline and connector positions are exported from the approved CAD.
- [ ] BOM and manufacturing review show no silent component substitutions.
