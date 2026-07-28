# ARIA-MECH-001 — Mechanical and CAD Specification

| Field | Value |
|---|---|
| Document ID | ARIA-MECH-001 |
| Revision | A |
| Status | Sprint 2 active CAD baseline |
| Governing documents | ARIA-PRD-001, ARIA-BOM-001, ARIA-HW-001 |

## Objective

Create a verified 1:1 digital assembly, optimize the final robot envelope, and
derive the mainboard outline and enclosure from real component geometry. The
earlier 150 × 150 × 150 mm envelope is a starting volume, not the final size.

## CAD conventions

- Units: millimetres.
- Exchange format: STEP; native authoring format may also be stored.
- Robot origin: centre of the drive axle projected onto the floor plane.
- Axes: +X forward, +Y left, +Z upward.
- Each part model uses its stable ARIA component ID.
- Manufacturer CAD is preferred. Community models require dimensional checks.
  Parts without reliable CAD are measured from the purchased sample.
- Keep-outs are separate visible bodies, not undocumented extra clearance.
- Imported masters are immutable. Corrections are stored as revisioned
  derivatives with the source hash retained.
- `ARIA-CAD-STATUS-001.md` is checked before every import to prevent duplicate
  hashes or component-ID collisions.

## Frozen geometry

- Two `ARIA-WHL-001` wheels.
- Two `ARIA-MOT-001` motors.
- Gear geometry and transmission ratio are deliberately not frozen; the owner
  will design them after the real motor/wheel mounting geometry is known.
- `ARIA-CPU-001` uses `ARIA-THM-001` and needs a direct intake/exhaust route.
- Camera, display, microphone array, ToF sensors, speakers, and environmental
  sensor need functional openings and keep-outs.

## Packaging priorities

1. Keep battery and heavy drive components low.
2. Preserve wheel loads on dedicated axle/bearing structures, not motor
   bearings unless the final transmission design proves otherwise.
3. Keep motor phases and switching power away from microphone, audio, IMU, and
   sensor wiring.
4. Keep `ARIA-SEN-003` outside internal heat and exhaust flow.
5. Keep microphone ports away from fan turbulence and mechanically isolate them.
6. Provide service access to battery, fuse, storage, connectors, and debug ports.
7. Reserve cable bend radius before shrinking the enclosure.

## Bare-chassis visual direction

The current concept is recorded in `assets/concepts/ARIA-CHASSIS-CONCEPT-001.png`. It is a visual packaging study, not approved geometry.

- Use a serviceable two-deck skeleton before designing the enclosure.
- Mount circular `ARIA-DSP-001` on a rigid front bridge using the verified Ø126 mm envelope and 85 × 65 mm M4 mounting pattern.
- Keep battery, traction hardware, and wheel loads on the lowest deck.
- Keep compute/control electronics above with direct airflow.
- Isolate microphone and speaker brackets from fan and motor vibration.
- Retain a low impact rail, sensor bridge, cliff-sensor brackets, and underside battery service access.
- Styling must not override serviceability or sensor fields of view.

## Required outputs

- verified part library in `cad/parts/`;
- master assembly in `cad/assemblies/`;
- PCB outline/origin exchange files in `cad/pcb/`;
- dimensioned drawings in `cad/drawings/`;
- interference and serviceability report;
- centre-of-mass estimate and tip-risk review;
- airflow and acoustic path review;
- sensor field-of-view and cliff-sensor ground-clearance review;
- final envelope and manufacturing tolerances.

## Release gates

- [ ] Every frozen component has a checked envelope and keep-outs.
- [ ] Exact battery, display, MCU, speakers, and sensor carriers are known.
- [ ] Wheel/transmission design is approved.
- [ ] No hard interference exists in the master assembly.
- [ ] Battery and fuse can be isolated for service.
- [ ] PCB outline is exported from the approved assembly, not guessed separately.
