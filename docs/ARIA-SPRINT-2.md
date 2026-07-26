# ARIA Sprint 2 — Hardware Synchronization and CAD Baseline

| Field | Value |
|---|---|
| Revision | A |
| Date | 2026-07-27 |
| Status | In progress |

## Completed in this synchronization

- Re-reviewed the active repository from `main`.
- Kept `ARIA-BOM-001.md` as the only authority for component IDs and quantities.
- Reconciled the frozen conversation decisions with the controlled baseline.
- Added a purchase register for Amazon and AliExpress.
- Imported and hashed three user-provided DWG files.
- Resolved the camera/ToF `ARIA-SEN-001` naming collision without duplicating a
  component.
- Preserved the two-layer mainboard decision and CAD-derived board outline.

## Active work

- Verify the three imported CAD models against manufacturer dimensions.
- Collect or build the remaining frozen component models.
- Resolve validation holds that affect electrical safety and PCB footprints.
- Build the 1:1 packaging assembly.
- Derive the compact robot envelope and mainboard outline from that assembly.

## Exit criteria

- [ ] Every frozen purchasable component has an exact listing or manufacturer
      part number.
- [ ] Every frozen component has a verified CAD envelope and keep-outs.
- [ ] No duplicate ARIA IDs, duplicate CAD hashes, or conflicting quantities
      remain.
- [ ] Power protection, motor control, encoder, and six-ToF topologies pass
      review and bench validation.
- [ ] Mainboard schematic, ERC, PCB DRC, and 1:1 interference review pass.
- [ ] Purchase and fabrication releases are explicitly approved.
