# ARIA CAD execution inventory

This is an **operational CAD instance/readiness map**, not a purchase BOM. Purchased identity, quantity and purchase/CAD status remain canonical only in [`purchased-hardware/README.md`](../../purchased-hardware/README.md). “Instances” below means geometry instances needed in the final mechanical assembly.

## State and gate rules

- `CAD_EXACT`: verified release geometry.
- `ASSEMBLY_LOCKED`: use the real integrated assembly as one rigid body; repo mapping may follow later.
- `ENVELOPE_ONLY`: use locked/conservative outside volume and functional datums.
- `PENDING`: data remains open, but blocking is determined separately.
- `DESIGN_NEW`: create geometry from constraints.
- `NON_BLOCKING`: layout may continue with the listed assembly/envelope/placeholder strategy.
- `TRUE_BLOCKER`: blocks only the dependent final manufacturing interface/export, never the entire layout workspace.

| ID | Mechanical item | Instances | Primary state | Layout authority / placeholder | Layout gate | TRUE BLOCKER before dependent final manufacture |
|---|---|---:|---|---|---|---|
| `main_compute_display` | Pi 5 + round display + Smraza cooler + existing spacers/mounting | 1 | `ASSEMBLY_LOCKED` | Import/use the existing real assembly as one rigid body; if repo Name map is absent, preserve the whole selected App::Part/group | `NON_BLOCKING` | Capture final assembly envelope, mount interfaces and connector/cooler keep-outs |
| `camera` | Camera Module 3 Wide NoIR | 1 | `PENDING` | Same-model DWG + locked center/FRONT/connector-DOWN orientation; reserve conservative optical head space | `NON_BLOCKING` | Verify final mounting and lens/FOV optical keep-out |
| `ir_left` | Left IR module | 1 | `PENDING` | Conservative head envelope with two independent optical keep-outs (large + small) | `NON_BLOCKING` | Verify one exact board's two eye datums, mount and connector interface |
| `ir_right` | Same physical IR board on right | 1 | `PENDING` | Derive from left placeholder; allow 180° view-axis rotation; mirror exterior openings | `NON_BLOCKING` | No independent blocker; inherits verified left-board definition |
| `microphone_array` | reSpeaker/XMOS XVF3800 array | 1 | `PENDING` | Reserve isolated top chamber and editable carrier under separate roof with 2–3 mm acoustic gap | `NON_BLOCKING` | Verify mic envelope, acoustic ports and mounting interface |
| `microphone_roof` | Separate roof/cap/supports | 1 set | `DESIGN_NEW` | Parametric roof around mic chamber; supports remain editable | `NON_BLOCKING` | No independent blocker; final interface depends on verified mic definition |
| `tof_front_left` | VL53L1X | 1 | `ENVELOPE_ONLY` | 25 × 10 reference envelope, 20 mm hole spacing, connector UP, solved R200 ±10 beam | `NON_BLOCKING` | Verify one module's final outline, holes and optical datum |
| `tof_front_right` | VL53L1X | 1 | `ENVELOPE_ONLY` | Derive/mirror verified placeholder rules; initial yaw intent near ±15° | `NON_BLOCKING` | No independent blocker; inherits shared module definition |
| `tof_side_left` | VL53L1X | 1 | `ENVELOPE_ONLY` | Same placeholder; calculate side position/pitch from beam and drive clearance | `NON_BLOCKING` | No independent blocker; inherits shared module definition |
| `tof_side_right` | VL53L1X | 1 | `ENVELOPE_ONLY` | Mirror external aperture and solve placement independently if internal clearance differs | `NON_BLOCKING` | No independent blocker; inherits shared module definition |
| `motor_left` | FIT1035 2208 BLDC + encoder interface | 1 | `PENDING` | Use existing assembly/model if available or conservative drive envelope preserving rotor axis and 5 mm encoder spacing | `NON_BLOCKING` | Verify one motor/encoder stator mount, rotor axis and encoder envelope |
| `motor_right` | Mirrored drive assembly | 1 | `PENDING` | Derive/mirror left drive placeholder | `NON_BLOCKING` | No independent blocker; inherits shared drive definition |
| `encoder_left` | Integrated AS5600 encoder PCB geometry | 1 | `ENVELOPE_ONLY` | Conservative PCB keep-out at locked 5 mm relation, coaxial with motor | `NON_BLOCKING` | Included in shared motor/encoder blocker |
| `encoder_right` | Integrated AS5600 encoder PCB geometry | 1 | `ENVELOPE_ONLY` | Mirror left placeholder | `NON_BLOCKING` | No independent blocker |
| `wheel_left` | Wheel outside envelope | 1 | `ENVELOPE_ONLY` | Ø61 × 24 with exact motor-axis relation and swept volume | `NON_BLOCKING` | None; axle height/running clearance are calculated design outputs |
| `wheel_right` | Wheel outside envelope | 1 | `ENVELOPE_ONLY` | Same | `NON_BLOCKING` | None |
| `battery_block` | Assembled cells + integrated BMS | 1 | `ENVELOPE_ONLY` | Locked 60 × 74 × 65 block; orthogonal rotations; open cradle/adjustable retainer | `NON_BLOCKING` | None; leave open service/cable access and tune clearance during fit test |
| `aux_electronics_block` | Trimmed perfboard + small electronics incl. D24V90F5 | 1 | `PENDING` | Clearly oversized editable block, slightly larger than ESP board; never reserve raw 90 × 150 stock | `NON_BLOCKING` | Measure populated/trimmed final envelope, retention and connector/terminal keep-outs |
| `speaker_left` | Square speaker | 1 | `ENVELOPE_ONLY` | Ø40 aperture, 25 mm depth and conservative ~50 × 50 face region | `NON_BLOCKING` | Verify one speaker's mount/seal geometry and choose acoustic target |
| `speaker_right` | Square speaker | 1 | `ENVELOPE_ONLY` | Derive/mirror left placeholder | `NON_BLOCKING` | No independent blocker; inherits shared speaker definition |
| `passive_radiator` | Oval passive radiator | 1 | `ENVELOPE_ONLY` | Conservative ~78 × 42 reserved envelope, kept adjustable | `NON_BLOCKING` | Verify mount/seal geometry and acoustic data needed by chosen enclosure target |
| `speaker_enclosure` | Rear sealed speaker/PR enclosure | 1 | `DESIGN_NEW` | Parametric reserved volume around two speakers + one PR; can drive body layout now | `NON_BLOCKING` | No independent blocker; final seal/tuning depends on speaker/PR data |
| `ip2368` | Rear charging board | 1 | `ENVELOPE_ONLY` | Conservative rear board volume below blower; USB-C points rear; local flat and service opening allowed | `NON_BLOCKING` | Verify envelope, USB-C datum, retention and hot-region/component heights |
| `blower_3010` | 5 V centrifugal blower | 1 | `ENVELOPE_ONLY` | Locked 30 × 30 × 10 box with conservative inlet/outlet zones | `NON_BLOCKING` | Verify purchased blower mount, inlet and outlet geometry |
| `cooling_duct` | IP2368/blower duct and exhaust | 1 | `DESIGN_NEW` | Parametric duct reserved from IP2368 placeholder to blower placeholder; separated from mic/speaker | `NON_BLOCKING` | No independent blocker; final interfaces depend on IP2368/blower verification |
| `air_intake` | Lower/body slanted parallel intake slots | 1 pattern | `DESIGN_NEW` | Fish-gill pattern; calculate area from final verified blower inlet later | `NON_BLOCKING` | None; pattern is a calculated shell feature |
| `power_button` | HUSA metal tri-colour momentary switch | 1 | `ENVELOPE_ONLY` | Ø12 through-hole plus oversized/open rear internal service keep-out | `NON_BLOCKING` | None; do not create a tight blind cavity until body depth is known |
| `upper_shell` | Upper body shell | 1 | `DESIGN_NEW` | Parametric shell around all current envelopes/placeholders; affected interfaces remain editable | `NON_BLOCKING` | No independent blocker; only dependent final interfaces wait for their source data |
| `lower_shell` | Lower load-bearing shell/chassis | 1 | `DESIGN_NEW` | Same; use adjustable/open mounts for unresolved blocks | `NON_BLOCKING` | No independent blocker |
| `shell_joint` | M2.5 bosses, pilot holes and locating lip | 1 set | `DESIGN_NEW` | Position/count can be designed now; keep hole/boss/lip dimensions parametric | `NON_BLOCKING` | Select print material/process/tolerance and actual M2.5 fastener data before releasing fit dimensions |

## Items intentionally absorbed into blocks

- BMS is internal to `battery_block`; no separate layout object.
- YD-ESP32-S3, two SimpleFOCMini boards, BNO085, two MAX98357A, INA226 and D24V90F5 are internal to `aux_electronics_block`; they do not receive separate shell mounts in this pass.
- Pi, display, Smraza cooler and existing spacer stack remain internal children of `main_compute_display`; they are not independently repositioned.

## Current readiness summary

- Layout gate: **READY_WITH_PLACEHOLDERS**. Every listed instance has an assembly, envelope or constraint strategy.
- Final-manufacturing gate: **NOT_READY** until the limited shared `TRUE_BLOCKER` definitions above are verified.
- Missing exact CAD or repo object mapping alone is never a blocker.
- Continue with layout, collision envelopes, optical rays, module arrangement, shell studies, service sequence and parametric mounts now; label unresolved mating geometry `NOT FOR MANUFACTURE`.
