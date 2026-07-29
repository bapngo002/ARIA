# ARIA controlled documents

This directory contains the active engineering baseline.

| Document | Owns |
|---|---|
| `ARIA-PRD-001.md` | Frozen product behavior, scope, and acceptance criteria |
| `ARIA-BOM-001.md` | Component identities, quantities, freeze states, and procurement evidence |
| `ARIA-HW-001.md` | Sprint 2 freeze decision, compatibility review, and release gates |
| `ARIA-PCB-001.md` | Mainboard design and fabrication rules |
| `ARIA-MECH-001.md` | CAD coordinates, packaging rules, and mechanical release gates |
| `ARIA-WIRING-001.md` | Electrical interfaces, harness rules, and fail-safe behavior |
| `ARIA-PURCHASE-001.md` | Marketplace search terms, quantities, and order-readiness checks |
| `ARIA-COMPONENT-REFERENCE-001.md` | Official product-image references, verified dimensions, mounting data, and validation holds |
| `ARIA-CAD-STATUS-001.md` | CAD inventory, source filenames, hashes, and geometry validation |
| `ARIA-SPRINT-2.md` | Current Sprint 2 status, work queue, and exit criteria |

## Rules

- Component names and quantities are edited only in `ARIA-BOM-001.md`.
- Other documents refer to stable ARIA IDs.
- Product requirement changes require a new PRD revision.
- Historical Sprint 1 drafts are available through Git history and are not kept
  in the active document tree because they conflict with the Sprint 2 baseline.
- Datasheets and supplier files are added only when their source and exact
  component revision are known.
- New data is reviewed from the BOM outward: ID, quantity, model, electrical
  fit, CAD identity, then duplicate/hash check.
