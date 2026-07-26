# ARIA-CAD-STATUS-001 — CAD Library Status

| Field | Value |
|---|---|
| Document ID | ARIA-CAD-STATUS-001 |
| Revision | A |
| Date | 2026-07-27 |
| Status | Active Sprint 2 inventory |
| Governing documents | ARIA-BOM-001, ARIA-MECH-001 |

## Imported CAD

| ARIA ID | Repository file | SHA-256 | State |
|---|---|---|---|
| ARIA-CPU-001 | `cad/parts/ARIA-CPU-001/ARIA-CPU-001_Raspberry-Pi-5_Active-Cooler.dwg` | `54B941F2210CF043CEC7F9E826D32738850710780BBC9B49B460F33F7F667A4F` | Imported; dimensional verification pending |
| ARIA-MCU-001 | `cad/parts/ARIA-MCU-001/ARIA-MCU-001_ESP32-S3-DevKitC-1.dwg` | `3CDCF4305BB62F79AA52780F26449277D7CE0F3542CB31A376870152A3DFDFDB` | Imported; variant and dimensional verification pending |
| ARIA-CAM-001 | `cad/parts/ARIA-CAM-001/ARIA-CAM-001_Camera-Module-3-Wide-NoIR.dwg` | `D3B28B76AD57CCA2DB5FC2A12D78417A592557A5F56D5D4C3DAAEA016415A2BE` | Imported; lens keep-out and dimensional verification pending |

All three files have an `AC1032` DWG header. Import proves file identity and
preserves the user-created CAD; it does not yet prove scale, units, mounting
geometry, or suitability for manufacture.

## Canonical naming resolution

The camera source file used `ARIA-SEN-001`. That ID is already canonical for
the six VL53L1X modules in `ARIA-BOM-001`. The camera is therefore stored as
`ARIA-CAM-001`. The original filename and hash remain recorded beside the file.

## Review procedure for every new CAD file

1. Match the part against the exact BOM ID and quantity.
2. Calculate SHA-256 and compare it with every existing CAD entry.
3. Preserve the original file; do not overwrite it with edits.
4. Check format, units, overall envelope, holes, connectors, and keep-outs.
5. Compare critical dimensions with manufacturer drawings or a measured part.
6. Create a revisioned derivative only after the imported master is recorded.
7. Update this file and the part-level README in the same commit.

## CAD backlog

The next models are the frozen display, microphone array, speakers, motors,
motor drivers, wheels, sensors, battery, BMS, regulator, power monitor, button,
and mainboard design items in `ARIA-BOM-001`.
