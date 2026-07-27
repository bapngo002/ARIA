# ARIA-MOT-001 — DFRobot FIT1035

## Component

- DFRobot FIT1035 2208 three-phase BLDC motor.
- Integrated AS5600 magnetic encoder assembly.
- Quantity in ARIA V1: 2.

## CAD files

| File | Purpose | Status |
|---|---|---|
| `ARIA-MOT-001-colored.dwg` | AutoCAD 3D assembly with material-based colors | Verified |
| `ARIA-MOT-001-colored_validation.json` | Geometry, placement, color, and file-integrity record | Verified |

## Coordinate system and alignment

- Units: millimetres.
- Origin: motor shaft axis at the rear motor mounting face.
- +Y points toward the rotor/front face.
- Encoder rotation: -90° about X.
- Encoder translation: Y = -5.320085202569 mm.
- Shaft-to-sensor air gap: 0.50 mm.
- Lateral axis offset: 0 mm.
- Interference volume: 0 mm³.

## Geometry validation

- Motor solids: 18.
- Encoder solids: 55.
- Total colored solids: 73.
- AutoCAD ModelSpace: one block reference at insertion point `[0, 0, 0]`.
- AutoCAD `AUDIT`: 0 errors found, 0 fixed.
- DWG format: AC1032.

## Color groups

The DWG uses separate ARIA layers and true colors for aluminum, steel shaft,
copper windings, motor phase leads, encoder PCB, IC, SMD parts, silkscreen,
connector housings, and contacts.

## Verification state

The source geometry is the official DFRobot STEP package. Alignment and file
integrity are verified for packaging work. Critical mounting dimensions still
require comparison with the manufacturer drawing or a measured production part
before manufacturing release.
