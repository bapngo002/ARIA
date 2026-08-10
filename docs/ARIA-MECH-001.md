# ARIA-MECH-001 — Mechanical and CAD rules

The only component/CAD inventory is [`purchased-hardware/README.md`](../purchased-hardware/README.md).

## Conventions

- Units: millimetres.
- Prefer manufacturer STEP/DWG; otherwise measure the delivered sample.
- Record source filename and SHA-256.
- Check envelope, holes, connectors, cable bends and optical/acoustic/thermal keep-outs.
- Put matching purchased-part CAD in `purchased-hardware/cad/`.
- Put unique but mismatched or not-purchased CAD in `purchased-hardware/cad-review/`.
- Do not create another CAD status table.

## Release gate

A CAD file is usable for design only after its critical dimensions are checked against manufacturer data or a measured physical sample. None of the current imported files is yet released for manufacture.
