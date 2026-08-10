# ARIA-HW-001 — Hardware validation gates

Component identity, quantity, purchase status and CAD status live only in [`purchased-hardware/README.md`](../purchased-hardware/README.md). This document must not repeat that inventory.

## Before bench power

- Confirm delivered markings and exact board revisions against the canonical inventory.
- Verify battery chemistry, polarity, cell condition, BMS behavior, fuse strategy and wire ratings.
- Verify every regulator output unloaded before connecting compute, display, audio or sensors.
- Treat marketplace power/current claims as unverified until measured.

## Before mechanical use

- CAD must be checked for units, overall envelope, mounting holes, connectors and functional keep-outs.
- A filename match is not dimensional verification.
- Files in `purchased-hardware/cad-review/` are explicitly not manufacturing references.

## Before motion tests

- Confirm the motor/driver pair, encoder feedback, current limit, thermal behavior and stop behavior on the bench.
- The ordered controller is identified from the order and pinout evidence as a 44-pin, dual-USB-C YD-ESP32-S3 with an ESP32-S3-WROOM-1-N16R8 module; it is inventory item 16.
- The family pinout, including RGB on GPIO48, may be used for planning. Do not release power wiring, tight enclosure geometry or production pin assignments until the delivered PCB/revision is inspected and measured against the nominal CAD.

## Release rule

No PCB, enclosure or harness is released from unverified CAD or from a planned-but-unpurchased component assumption.
