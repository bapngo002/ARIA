# ARIA CAD execution inventory

This is an **operational CAD instance/readiness map**, not a purchase BOM. Purchased identity, quantity and purchase/CAD status remain canonical only in [`purchased-hardware/README.md`](../../purchased-hardware/README.md). “Instances” below means geometry instances needed in the final mechanical assembly.

## State rules

- `CAD_EXACT`: verified release geometry. None exists in the current repo snapshot.
- `ASSEMBLY_LOCKED`: rigid assembly role; internal relative geometry must not change. Missing authoritative assembly can still block release.
- `ENVELOPE_ONLY`: use only stated outside envelope/datums.
- `PENDING`: a critical input or verification is missing.
- `DESIGN_NEW`: geometry is created by this CAD project from locked constraints.

| ID | Mechanical item | Instances | Primary state | Repo/input evidence | Locked use | Release blocker |
|---|---|---:|---|---|---|---|
| `main_compute_display` | Pi 5 + round display + Smraza cooler + existing spacers/mounting | 1 | `ASSEMBLY_LOCKED` | Authoritative integrated assembly is not in repo; current Pi DWG in `cad-review/` contains the wrong official cooler | Transform as one rigid body only | **YES:** import, scan, hash and map assembly |
| `camera` | Camera Module 3 Wide NoIR | 1 | `PENDING` | Same-model DWG exists at `purchased-hardware/cad/05-...dwg`, but repo says unverified | Center above display; lens FRONT; connector DOWN; lens only exposed | **YES:** verify scale, holes, lens/FOV, connector datum |
| `ir_left` | Left IR module | 1 | `PENDING` | No model/file in current repo | Large + small eye both open; mirror-symmetric exterior | **YES:** exact model, optical datums, mounts |
| `ir_right` | Right IR module, same physical board as left | 1 | `PENDING` | No model/file in current repo | PCB may rotate 180° about view axis; preserve mirrored eye pattern | **YES:** same as left plus verified rotated clearance |
| `microphone_array` | reSpeaker/XMOS XVF3800 array | 1 | `PENDING` | Canonical inventory says exact revision/USB variant and CAD missing | Completely isolated top acoustic chamber | **YES:** revision, CAD/measurements, ports, mounts |
| `microphone_roof` | Separate mic roof/cap/carrier supports | 1 set | `DESIGN_NEW` | Created in final CAD | Curved cap; acoustic gap about 2–3 mm; tool-accessible supports | Depends on verified mic geometry |
| `tof_front_left` | VL53L1X | 1 | `PENDING` | No model/file in current repo | Connector UP; beam-to-floor R200 ±10; hole spacing 20 mm | **YES:** exact CAD/object; verify board 25×10 |
| `tof_front_right` | VL53L1X | 1 | `PENDING` | No model/file in current repo | Same; initial yaw intent near ±15°, geometry decides reduction | **YES** |
| `tof_side_left` | VL53L1X | 1 | `PENDING` | No model/file in current repo | Side position optimized; connector UP; R200 ±10 | **YES** |
| `tof_side_right` | VL53L1X | 1 | `PENDING` | No model/file in current repo | Mirror exterior; connector UP; R200 ±10 | **YES** |
| `motor_left` | FIT1035 2208 BLDC | 1 | `PENDING` | Purchased but no CAD in repo | Stator inside; only rotor output exposed | **YES:** exact CAD and measured critical dimensions |
| `motor_right` | FIT1035 2208 BLDC | 1 | `PENDING` | Purchased but no CAD in repo | Mirror placement, same rules | **YES** |
| `encoder_left` | Integrated AS5600 encoder PCB geometry | 1 | `PENDING` | No separate/exact CAD in repo | Outer PCB face to stator fixed face = 5 mm; coaxial | **YES:** PCB geometry/object mapping |
| `encoder_right` | Integrated AS5600 encoder PCB geometry | 1 | `PENDING` | No separate/exact CAD in repo | Same | **YES** |
| `wheel_left` | Wheel outside envelope | 1 | `ENVELOPE_ONLY` | User-approved envelope | Ø61 × 24; axis exactly motor axis; internal hub excluded | Axle height/running clearance pending |
| `wheel_right` | Wheel outside envelope | 1 | `ENVELOPE_ONLY` | User-approved envelope | Same | Axle height/running clearance pending |
| `battery_block` | Assembled cells + integrated BMS | 1 | `ENVELOPE_ONLY` | User-approved final block | 60 × 74 × 65; orthogonal orientation only; removable lower cradle | Pack cable exit, clearance/padding and mass pending |
| `aux_electronics_block` | Trimmed perfboard + small electronics incl. D24V90F5 | 1 | `PENDING` | 90×150 mm is raw stock only; YD board nominal CAD remains in `cad-review/` | Temporary visualization only; no shell/mount release | **YES:** populate, trim, measure final envelope/mounts/connectors |
| `speaker_left` | Square speaker | 1 | `ENVELOPE_ONLY` | Purchased; no exact CAD | Ø40 acoustic aperture; 25 mm frame-to-magnet depth; provisional structural region | **YES:** outline, holes, gasket, rear clearance |
| `speaker_right` | Square speaker | 1 | `ENVELOPE_ONLY` | Purchased; no exact CAD | Same | **YES** |
| `passive_radiator` | Oval passive radiator | 1 | `PENDING` | Product-image estimate only (~78×42 outer) | Shared sealed volume with both speakers | **YES:** measured outline, mount/gasket, acoustic data |
| `speaker_enclosure` | Rear sealed speaker/PR enclosure | 1 | `DESIGN_NEW` | Created in final CAD | Removable; no airflow/electronics leakage; amps outside | Depends on exact speakers/PR and tuning target |
| `ip2368` | Rear charging board | 1 | `PENDING` | Purchased; no CAD or verified measurements | Below blower; USB-C rear; hot face in dedicated airflow | **YES:** board, mounts, connector, heights/hotspot |
| `blower_3010` | 5 V centrifugal blower | 1 | `ENVELOPE_ONLY` | Approved 30×30×10 envelope; exact revision/mount absent | Exhaust in charging-only duct | **YES:** mount, inlet/outlet and actual revision |
| `cooling_duct` | IP2368/blower duct and rear/upper exhaust | 1 | `DESIGN_NEW` | Created in final CAD | Separate from mic/speaker; short unrestricted path | Depends on exact IP2368/blower |
| `air_intake` | Lower/body slanted parallel intake slots | 1 pattern | `DESIGN_NEW` | Approved sketch intent | Fish-gill pattern; open area ≥ verified blower useful inlet | Airflow area/recirculation calculation pending |
| `power_button` | HUSA metal tri-colour momentary switch | 1 | `ENVELOPE_ONLY` | Only 12 mm mounting variant is locked | Ø12 mounting aperture; rear service zone | **YES:** body/bezel/depth/terminal dimensions |
| `upper_shell` | Upper body shell | 1 | `DESIGN_NEW` | Created in final CAD | Carries front/top geometry; serviceable | Depends on complete layout and print rules |
| `lower_shell` | Lower load-bearing shell/chassis | 1 | `DESIGN_NEW` | Created in final CAD | Motors, Battery Block, AUX and lower sensors supported here | Depends on complete layout and print rules |
| `shell_joint` | M2.5 bosses, pilot holes and locating lip | 1 set | `DESIGN_NEW` | Created in final CAD | Lip locates only; screws clamp; all tools accessible | **YES:** print process/material/tolerances/fasteners |

## Items intentionally absorbed into blocks

- BMS is internal to `battery_block`; no separate layout object.
- YD-ESP32-S3, two SimpleFOCMini boards, BNO085, two MAX98357A, INA226 and D24V90F5 are internal to `aux_electronics_block`; they do not receive separate shell mounts in this pass.
- Pi, display, Smraza cooler and existing spacer stack remain internal children of `main_compute_display`; they are not independently repositioned.

## Current readiness summary

- `CAD_EXACT`: 0.
- `ASSEMBLY_LOCKED`: 1 role, but its authoritative file/map is pending.
- `ENVELOPE_ONLY`: Battery Block, two wheels, two partial speaker envelopes, blower envelope and 12 mm button aperture.
- `PENDING`: all unverified/missing component geometry listed above.
- `DESIGN_NEW`: mic roof/carrier, speaker enclosure, cooling duct, intake slots, upper shell, lower shell and shell joint.

This means layout exploration may begin only after the integrated assembly is supplied, but manufacturing geometry/export remains blocked until all critical pending data is resolved.
