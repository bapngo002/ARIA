# ARIA-HW-001 — Hardware validation gates

Component identity, quantity, purchase status and CAD status live only in [`docs/ARIA-BOM-001.md`](ARIA-BOM-001.md). This document must not repeat that inventory.

Current progress and reported module passes are in the [master handoff](ARIA-MASTER-HANDOFF.md). The gates below are requirements, not a claim that bench work has not started or has passed.

## Before bench power

- Confirm delivered markings and exact board revisions against the canonical inventory.
- Verify battery chemistry, polarity, cell condition, behavior of the 3S BMS integrated inside the battery pack, fuse strategy and wire ratings.
- Verify every regulator output unloaded before connecting compute, display, audio or sensors.
- Treat marketplace power/current claims as unverified until measured.

## Before mechanical use

- CAD must be checked for units, overall envelope, mounting holes, connectors and functional keep-outs.
- A filename match is not dimensional verification.
- Files in `purchased-hardware/cad-review/` are explicitly not manufacturing references.

## Before motion tests

- Confirm the motor/driver pair, encoder feedback, current limit, thermal behavior and stop behavior on the bench.
- Controller family identity comes from BOM item 16. GPIO/Wi-Fi/Bluetooth tests are owner-reported in the master handoff; exact tested PCB/revision still needs evidence.
- The family pinout, including RGB on GPIO48, may be used for planning. Do not release power wiring, tight enclosure geometry or production pin assignments until the delivered PCB/revision is inspected and measured against the nominal CAD.

## Release rule

No PCB, enclosure or harness is released from unverified CAD or from a planned-but-unpurchased component assumption.
