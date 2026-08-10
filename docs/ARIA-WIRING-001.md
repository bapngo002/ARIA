# ARIA-WIRING-001 — Wiring and safety rules

Purchased component identity and quantity come only from [`purchased-hardware/README.md`](../purchased-hardware/README.md).

- Battery and motor current must not pass through breadboards or low-current buttons.
- Use short, fused, strain-relieved high-current wiring.
- Route motor phases and switching power away from audio, camera, IMU and control wiring.
- Verify connector polarity, wire gauge, current derating and service disconnects.
- Keep replaceable parts disconnectable.
- Prove motor stop behavior for loss of the main computer, controller reset and sensor faults.
- The real-time controller interface remains a design decision until an exact controller is actually purchased and added to the canonical inventory.

This file intentionally contains no connector BOM, component list or CAD status copy.
