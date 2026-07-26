# ARIA-PCB-001 — Mainboard Development Specification

| Field | Value |
|---|---|
| Document ID | ARIA-PCB-001 |
| Revision | 0 |
| Status | Sprint 2 placeholder — architecture not released |
| Governing documents | ARIA-PRD-001, ARIA-BOM-001, ARIA-HW-001, ARIA-MECH-001, ARIA-WIRING-001 |

## Objective

Develop a compact, serviceable two-layer ARIA mainboard whose outline and
connector positions are derived from the verified CAD assembly.

## Frozen constraints

- Two copper layers.
- Board outline is not fixed until the mechanical packing study is complete.
- Power, motor, audio, sensor, and high-speed/display/camera paths must not be
  mixed casually.
- The main fuse, TVS, reverse-polarity protection, soft-latch, and power
  monitoring require coordinated review.
- No Gerber release before schematic review, ERC, DRC, and 1:1 mechanical
  interference review.

## Candidate functional scope

The exact scope is intentionally not frozen. The architecture review will decide
whether the board contains:

- protected power entry and distribution;
- `ARIA-PWR-004` soft-latch;
- `ARIA-PWR-005` power monitoring and shunt;
- `ARIA-PWR-006` fuse, `ARIA-PWR-007` TVS, and `ARIA-PWR-008` reverse protection;
- two `ARIA-AUD-003` amplifier circuits or headers for commercial modules;
- connectors for compute, MCU, sensors, motor drivers, speakers, fan, and user
  controls;
- test points and programming/debug headers.

`ARIA-PWR-002`, `ARIA-PWR-003`, `ARIA-MOT-002`, and `ARIA-MCU-001` remain
modules unless an explicit architecture revision says otherwise.

## Required outputs

- reviewed block diagram and power tree;
- exact schematic with manufacturer part numbers;
- power/current/thermal budget;
- connector and pin-allocation table;
- 2D board outline linked to the CAD origin;
- routed two-layer PCB with controlled return paths;
- schematic ERC and PCB DRC reports;
- STEP model of the populated board;
- fabrication drawings, Gerbers, drills, pick-and-place, and PCB BOM;
- bring-up and fault-injection checklist.

## Release gates

- [ ] All applicable holds in ARIA-BOM-001 and ARIA-HW-001 are closed.
- [ ] Exact board outline and mounting holes are approved in CAD.
- [ ] Wire/connector choices are frozen in ARIA-WIRING-001.
- [ ] Inrush, fuse, TVS, MOSFET SOA, and trace-current calculations are reviewed.
- [ ] `ARIA-CPU-001` power-transient requirements are verified by test.
- [ ] Audio grounding and motor-noise isolation strategy is reviewed.
- [ ] User approves the manufacturing preview before files are ordered.
