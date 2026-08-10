# ARIA-PCB-001 — Mainboard development rules

Purchased module identity and quantity come only from [`purchased-hardware/README.md`](../purchased-hardware/README.md).

- Do not choose footprints from product photos or from planned components.
- Confirm the delivered revision, pinout, connector orientation and mechanical drawing first.
- Review power entry, protection, current paths, grounding, audio noise and motor noise.
- Complete schematic review, ERC, PCB DRC and a 1:1 mechanical check before fabrication.
- Generated Gerbers must identify their source commit and explicit approval.

This file intentionally contains no second BOM.
