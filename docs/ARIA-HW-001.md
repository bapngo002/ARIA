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
- Use a real-time controller only after its exact purchased model is added to the canonical inventory.
- ESP32 is currently a design candidate, not a purchased component.

## Release rule

No PCB, enclosure or harness is released from unverified CAD or from a planned-but-unpurchased component assumption.
