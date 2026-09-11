# ARIA-MECH-001 — Mechanical and CAD rules

The only component/CAD inventory is [`docs/ARIA-BOM-001.md`](ARIA-BOM-001.md).

## Conventions

- Units: millimetres.
- Prefer manufacturer STEP/DWG; otherwise measure the delivered sample.
- Record source filename and SHA-256.
- Check envelope, holes, connectors, cable bends and optical/acoustic/thermal keep-outs.
- Put matching purchased-part CAD in `purchased-hardware/cad/`.
- Put unique but mismatched or not-purchased CAD in `purchased-hardware/cad-review/`.
- Do not create another CAD status table.

## Current wheel reference

Use the [canonical wheel specification](ARIA-BOM-001.md#bánh-xe) for clearance and fit planning. Confirm the meaning of the reported center/hub dimension and the contents of a set before designing the axle interface or assigning per-wheel mass.

## Release gate

A CAD file is usable for design only after its critical dimensions are checked against manufacturer data or a measured physical sample. None of the current imported files is yet released for manufacture.
