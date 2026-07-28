# ARIA

ARIA is a Vietnamese AI companion robot project combining an application
computer with an independent real-time motion and safety controller.

## Current status

| Milestone | Status |
|---|---|
| M0 — Frozen requirements | Complete |
| M1 — Hardware selection | Complete; historical drafts removed from the active tree |
| M2 — Sprint 2 hardware freeze | Synchronized; validation holds remain |
| M3 — Verified CAD library and packing study | In progress; 3 user CAD files imported |
| M4 — Mainboard and bench prototype | Not started |

No document in this repository currently authorizes a full component purchase,
PCB fabrication, or enclosure manufacture.

## Authoritative documents

1. [ARIA-PRD-001](docs/ARIA-PRD-001.md) — frozen product requirements.
2. [ARIA-BOM-001](docs/ARIA-BOM-001.md) — **single source of truth** for
   component IDs, approved selections, quantities, and freeze states.
3. [ARIA-HW-001](docs/ARIA-HW-001.md) — Sprint 2 hardware-freeze decision,
   compatibility review, and release gates.
4. [ARIA-PCB-001](docs/ARIA-PCB-001.md) — two-layer mainboard development rules.
5. [ARIA-MECH-001](docs/ARIA-MECH-001.md) — mechanical and CAD conventions.
6. [ARIA-WIRING-001](docs/ARIA-WIRING-001.md) — wiring and internal interfaces.
7. [ARIA-PURCHASE-001](docs/ARIA-PURCHASE-001.md) — Amazon/AliExpress
   procurement register for frozen parts.
8. [ARIA-CAD-STATUS-001](docs/ARIA-CAD-STATUS-001.md) — CAD file inventory,
   hashes, verification state, and naming map.
9. [ARIA-SPRINT-2](docs/ARIA-SPRINT-2.md) — active Sprint 2 work and exit
   criteria.

10. [ARIA-COMPONENT-SHAPE-001](docs/ARIA-COMPONENT-SHAPE-001.md) — component-form reference and bare-chassis concept.

See [docs/README.md](docs/README.md) for document ownership and change rules.

## Repository structure

```text
ARIA/
├── cad/              # Verified parts, assemblies, PCB exchange, drawings
├── docs/             # Controlled requirements and engineering specifications
├── electronics/      # Native mainboard design and reviewed fabrication output
├── firmware/         # Real-time and safety-controller firmware
├── manufacturing/    # Approved release packages and assembly records
├── .gitignore
├── LICENSE
└── README.md
```

Generated files stay out of source folders unless they are part of an explicitly
reviewed release. Hardware artifacts identify the source commit used to create
them.

## Change control

- Never duplicate an approved model name or quantity outside
  `docs/ARIA-BOM-001.md`; refer to its stable ARIA ID instead.
- Never silently replace a frozen component. Add a new ID and record the
  superseded relationship.
- Never guess geometry. Use manufacturer data, a dimensionally verified model,
  or a measured physical sample.
- Never fabricate a PCB or mechanical part from an unreviewed export.
- New component or CAD data must be checked against the BOM, existing hashes,
  and stable ARIA IDs before it is added. Conflicts are resolved in the
  controlled documents rather than duplicated.
- Merge only after the branch diff, validation holds, and generated release
  package have been reviewed.
