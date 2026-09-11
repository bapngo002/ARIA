# ARIA-WIRING-001 — Wiring and safety rules

Purchased component identity and quantity come only from [`docs/ARIA-BOM-001.md`](ARIA-BOM-001.md).

- Battery and motor current must not pass through breadboards or low-current buttons.
- Use short, fused, strain-relieved high-current wiring.
- Route motor phases and switching power away from audio, camera, IMU and control wiring.
- Verify connector polarity, wire gauge, current derating and service disconnects.
- Keep replaceable parts disconnectable.
- Prove motor stop behavior for loss of the main computer, controller reset and sensor faults.
- The real-time controller interface remains a design decision until an exact controller is actually purchased and added to the canonical inventory.

This file intentionally contains no connector BOM, component list or CAD status copy.

## Power sensing and battery protection

Use INA260 for current power-sensing wiring; board identity and quantity are in the canonical BOM. Verify the delivered boards and I²C address configuration before finalizing the harness. Battery protection uses the 3S BMS inside the battery pack; validate the pack protection and charging connections as part of the battery assembly.
