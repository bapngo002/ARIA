# ARIA final CAD master specification

- **Document ID:** ARIA-CAD-MASTER-SPEC
- **Version:** 1.0.0
- **Captured:** 2026-08-27
- **Repo baseline:** `main@e3a6a83f4384d188aee4c76c771f4b8fce5c523e`
- **Units:** millimetres
- **Status:** design decisions frozen; geometry release blocked by pending inputs

## 1. Authority and conflict handling

- Product intent comes from `docs/ARIA-PRD-001.md`.
- Purchased component identity/quantity/CAD status comes only from `purchased-hardware/README.md`.
- Mechanical, PCB and wiring release rules come from `docs/ARIA-MECH-001.md`, `docs/ARIA-HW-001.md`, `docs/ARIA-PCB-001.md` and `docs/ARIA-WIRING-001.md`.
- This workspace is the operational authority for the **final CAD layout, constraints, object mapping, workflow and validation** after it is merged to `main`.
- `docs/ARIA-BOM-001.md` did not exist in the baseline and must not be fabricated from memory.
- If a conversation-era component identity conflicts with `main`, `main` wins. In particular, do not carry the old “BMS 3S 40A không NTC” description forward: current canonical inventory records a 3S 20A + NTC BMS. CAD treats it only as part of the locked Battery Block unless the canonical inventory is deliberately revised.
- Unknown geometry remains `UNKNOWN/PENDING`. No photo scaling, generic-datasheet substitution or AI estimation is permitted.

## 2. Overall architecture

### 2.1 External form

- The former fixed `Ø200 mm` body constraint is removed.
- The early `150 × 150 × 150 mm` target in the PRD remains an aspiration, not a manufacturing dimension.
- Generate the smallest practical external envelope around verified components, mounts, structural material, clearances and service paths.
- Exterior styling should follow the approved ARIA concept language: rounded/organic body, large round front display, sci-fi panel treatment, camera/IR group above the display and a top mic cap. The reference image is style guidance, not dimensional evidence.
- Local growth is allowed only when a documented collision, service, optical, acoustic or airflow requirement needs it. IR sensor housings may grow locally to preserve external symmetry.

### 2.2 Shell split and load path

- The body is split into `UPPER_SHELL` and `LOWER_SHELL`.
- The seam may follow exterior panel lines and may move locally to avoid the display, wheels, speaker enclosure, charge port and service features; it need not be a perfectly horizontal plane.
- `LOWER_SHELL` is the load-bearing chassis. Motors, wheel supports, Battery Block, AUX Electronics Block and lower sensors mount to it or to structures transferring load to it.
- `UPPER_SHELL` carries the front Pi/display assembly, camera/IR head and related cosmetic geometry.
- The mic top is a separate serviceable module; the upper/lower seam must not pass through its isolated acoustic chamber.
- Opening the body must expose the lower chassis without leaving heavy parts hanging from the upper shell. Inter-shell connectors must be disconnectable before full separation.

### 2.3 Upper/lower joint

- Fastener family: M2.5.
- CAD creates screw bosses and pilot/centering holes only. Do not model threads or decorative screw models.
- Boss count, diameter, pilot diameter, depth and exact positions are `PENDING` until print material/process and actual fasteners are recorded.
- Bosses must not collide with parts, must retain sufficient surrounding material and must be reachable by the intended screwdriver.
- A small locating lip/tongue at the seam aligns the shells and resists lateral slip. It is not a load-bearing snap-fit.
- Lip clearance and detailed section are `PENDING` until print process/tolerance is known.
- Fasteners provide clamping; the locating lip only locates.

## 3. Mechanical modules

### 3.1 Main compute/display assembly

Treat the complete existing `Pi 5 + Waveshare round display + Smraza active cooler + current spacers/fasteners/mounting` as one rigid assembly.

- Do not position Pi, display or cooler as separate layout items.
- Do not change their relative translation, rotation, spacer stack or mounting pattern.
- Only transform the complete assembly as one rigid body.
- Align the active display face with the front opening.
- Preserve cooler intake/exhaust clearance and service clearance for all connectors actually used.
- The enclosure creates mounts for the whole assembly, not a new independent Pi mounting scheme.
- Removal direction and screw/tool access must allow the whole assembly to leave from inside after the upper shell/front area is opened.
- Repo baseline does not contain the authoritative integrated assembly. Import and map it before layout release. The current Pi DWG in `cad-review/` uses the wrong cooler and is not an acceptable substitute.

### 3.2 Camera

- One Raspberry Pi Camera Module 3 Wide NoIR, centered directly above the display.
- Lens axis points `FRONT`; camera connector points `DOWN` toward the display. `DOWN` is locked and must not be flipped to solve a bracket collision.
- Only the lens/open optical window is visible externally. PCB, connector and mounting holes remain inside.
- Compute the aperture from verified lens/FOV/optical keep-out geometry; do not size it from lens outside diameter alone.
- No bezel, rib, decoration or mount may enter the camera FOV/optical keep-out.
- Use existing PCB mounting holes if verified; never add holes to the camera PCB.
- Allow cable connection/disconnection below the connector and removal from inside.
- Camera pitch remains `PENDING/CALCULATED` until the assembly position, ground plane and verified FOV are available.
- Repo has a same-model DWG, but scale, holes, lens keep-out and dimensions are not verified; it is not `CAD_EXACT` yet.

### 3.3 Paired IR modules

- Two physically identical IR modules sit left/right of the camera.
- External housings and all optical openings are mirror-symmetric about the center plane of the camera/display.
- Each IR module has two distinct optical eyes: one large and one small. Both require an unobstructed optical path.
- Validation must test four paths independently: left-large, left-small, right-large and right-small.
- Because the boards are identical rather than handed parts, one PCB may rotate 180° about the viewing axis so the visible eye pattern is a mirror pair.
- Internal PCB orientations may differ. External symmetry is higher priority than identical internal orientation.
- The shell/head may grow locally to clear the rotated board/connector, but left/right exterior geometry must remain symmetric.
- Exact IR model, eye centers/diameters, mounting and object mapping are absent from the repo baseline and are critical `PENDING` inputs.

### 3.4 Microphone top module

- The microphone assembly is on top in a completely isolated acoustic chamber.
- A solid sealed wall separates the mic chamber from electronics, charging cooling, Pi fan noise path and speaker chamber. Do not perforate or borrow this volume for another component.
- The upper/lower body seam does not cut through the chamber.
- A separate curved/domed mic roof/cap is `DESIGN_NEW` and follows the exterior language.
- The roof does not press against the microphone carrier. Provide an acoustic opening/gap around the roof of approximately `2–3 mm` as already approved; final detailed gap geometry must follow the real microphone CAD and acoustic openings.
- Roof/mic support legs and fasteners must not block the acoustic paths and must be tool-accessible.
- Only a required cable pass-through may penetrate the chamber wall; seal/isolate it as part of the acoustic design.
- Blower duct, intake and exhaust must never use the mic acoustic gap.
- Exact mic revision, CAD, mounting points, port locations, carrier dimensions and removal direction remain critical `PENDING`.

### 3.5 Drive: motors, encoders and wheels

- Two DFRobot FIT1035 2208 BLDC motors with integrated AS5600 encoder function per canonical inventory.
- The motor stator/body stays inside and is supported/covered by the shell or chassis. Expose only the rotor output required to connect the wheel.
- No shell, wheel stop or mount may contact a rotating part.
- Wheel envelope only: outside diameter `61 mm`, width `24 mm`; internal hub/adapter geometry is explicitly user-owned and must not be designed by the API.
- For each side, `WHEEL_AXIS` equals `MOTOR_ROTOR_AXIS` exactly. Do not offset axes to avoid a collision.
- Provide a shell/chassis wheel stop/housing and full 360° rotation clearance.
- The outside face of each encoder PCB is `5 mm` from the fixed/stator face due to the locked 5 mm brass spacer. Include motor + 5 mm spacer + encoder PCB in the keep-out.
- Encoder axis is coaxial with motor/rotor axis.
- Ground plane, axle height, wheel-to-shell running clearance and support details are `PENDING/CALCULATED` from verified drive CAD and full layout.

### 3.6 Four VL53L1X ToF modules

- Four modules: two forward and two side-facing, one left and one right in each role as applicable.
- Connector/wire header direction is `UP`; optical face points out through a small optical aperture.
- Authoritative board reference envelope from the approved design decision is `25 × 10 mm`; verify against physical/CAD source before release.
- Authoritative mounting-hole center spacing is `20.00 mm`. If the imported CAD differs, edit only the mounting-hole feature. Do not uniformly scale the model.
- Each optical axis must intersect the floor at radial distance `200 ± 10 mm` measured from robot center.
- Pitch/height are calculated from real geometry, not guessed from screenshots.
- Front sensors start as a layout intent around `±15°` yaw and may reduce yaw only enough to clear wheels/motors. Side sensor yaw/position is optimized by geometry to cover side blind areas.
- Left/right external apertures should be symmetric. Report any unavoidable internal asymmetry.
- No sensor, bracket or beam may collide with wheel, motor, encoder or wheel swept volume.
- Approximate old bracket thickness `1 mm` is not a released manufacturing dimension; it remains `PENDING` pending material/process.
- Exact CAD files and FreeCAD object names are absent from the repo baseline and are critical `PENDING` inputs.

### 3.7 Battery Block

- One locked `ENVELOPE_ONLY` block represents the already assembled cells plus integrated BMS.
- Final locked envelope: `60 × 74 × 65 mm`.
- Do not separate cells or BMS and do not redesign their internal arrangement.
- Orientation is free among orthogonal 90° rotations only; no arbitrary diagonal tilt.
- Place low and near the mass center where practical, but a small offset is allowed when the complete mass/clearance analysis supports it.
- Support it from `LOWER_SHELL` with a bottom cradle and lateral stops. Use a removable upper retaining bar/cover with M2.5 fasteners; do not suspend the pack from the upper shell or seal it inside an unserviceable box.
- Battery must be removable after opening the shell without removing unrelated speaker, display or drive modules.
- Installation clearance, restraint padding, cable exit and actual mass are `PENDING`; the prior conversational suggestion of `0.5–1 mm per side` is not released until print tolerance and pack measurement are recorded.

### 3.8 AUX Electronics Block

- One serviceable envelope represents the perfboard carrier and small modules: YD-ESP32-S3, two SimpleFOCMini/ESC modules, BNO085, two MAX98357A, INA226, D24V90F5 and other explicitly approved small modules.
- The purchased `90 × 150 mm` perforated PCB is raw stock only. It is not the final board size and no `90 × 150 mm` cavity may be reserved.
- After physical module layout, trim unused perfboard and measure final length × width × height plus connector/terminal keep-outs.
- Until measured, use only a clearly labeled provisional visualization envelope “slightly larger than the ESP board”; it must not drive shell release or mounting hole placement.
- Final envelope, outline, layer count/stack, mounting pattern and connector exits are `UNKNOWN/PENDING`.
- D24V90F5 may be mounted on this block. Preserve airflow/thermal clearance around its hot components.
- Do not route motor or main high-current power through Dupont wiring or low-current perfboard traces; this is an electrical release constraint that also affects terminal access.

### 3.9 Rear speaker module

- One removable, sealed acoustic enclosure at the rear contains two square speakers and one oval passive radiator.
- Speaker aperture: `Ø40 mm` each.
- Preserve approximately `5 mm` of structural/mounting region on each side of the aperture; the resulting provisional face region is about `50 × 50 mm` per speaker, but actual mounting holes remain `PENDING`.
- Measured speaker depth from square frame face to magnet back: `25 mm`.
- Passive radiator provisional outside envelope: approximately `78 × 42 mm`; active-area values from product imagery are not authoritative manufacturing dimensions.
- The two speakers and passive radiator share the intended acoustic volume. They may be angled/rearranged to follow the rear shell only after real geometry/mounts are available.
- Enclosure is isolated from electronics, airflow duct and shell leaks. MAX98357A boards remain outside the sealed acoustic volume.
- Speaker/PR CAD, hole patterns, gasket compression, enclosure volume/tuning and final arrangement are critical `PENDING` for acoustic release.

### 3.10 Charging and cooling module

- IP2368 is in the rear service zone, directly below the 3010 blower as a functional stack.
- IP2368 USB-C faces the rear and remains externally accessible. A small local flat on the rear shell is allowed.
- The hot face must not contact printed plastic. Exact air gap/standoff is `PENDING`; the earlier `4–6 mm` suggestion is not released without the real board/thermal test.
- Blower envelope: `30 × 30 × 10 mm`, 5 V. Hole pattern, inlet, outlet and exact purchased revision remain `PENDING`; never infer them from “3010”.
- The blower is an exhaust device for the charging thermal path and is intended to run only while charging; control implementation is outside CAD.
- Air path: lower/body intake → across the hot region of IP2368 → blower → dedicated upper/rear exhaust.
- Intake uses multiple narrow, parallel, slanted “fish-gill” slots following the approved sketch. Slot count, width, pitch and angle are `DESIGN_NEW/CALCULATED` from the final shell and airflow area.
- Total unobstructed intake area must be at least the blower's verified useful inlet area. Internal walls/components must not block it.
- Intake and exhaust must be separated enough to avoid recirculating hot exhaust.
- Duct is separate from mic chamber and sealed speaker enclosure, avoids the battery where practical, and uses a short path with no unnecessary sharp restrictions.
- IP2368 board dimensions, mount holes, connector position and thermal hotspot are critical `PENDING`.

### 3.11 Power button

- HUSA waterproof metal tri-colour momentary switch, 12 mm variant, one instance.
- Locked mounting aperture/envelope datum: `Ø12 mm`.
- Preferred mechanical location is rear near the charging service zone, with enough finger/cable clearance.
- Only button/bezel is exposed externally.
- Body diameter, bezel diameter, insertion depth, total terminal depth, anti-rotation feature and exact thread are `UNKNOWN/PENDING`. Do not build a tight rear cavity from the 12 mm hole alone.

## 4. Wiring scope

- Detailed internal cable routing, channels and tie points are outside this CAD pass; the user will route and bundle wiring during assembly.
- CAD must still preserve connector plug/unplug access, service disconnects and wire pass-through holes wherever a cable crosses a sealed/isolated wall.
- Do not compromise mic or speaker sealing with an unplanned pass-through.
- Battery/motor/high-current access must follow `docs/ARIA-WIRING-001.md`.

## 5. Service and assembly requirements

- Normal sequence is derived and validated after layout; it is not assumed to make an impossible layout pass.
- Target modular order: lower chassis → motors/encoders/wheels → Battery Block → AUX Block → high-current/service wiring → upper/front Pi/display assembly → camera/IR → rear speaker enclosure → charging/cooling module → top mic module → test → shell closure.
- Battery removal must not require removal of display, speaker or motors.
- Pi/display removal must preserve internal assembly geometry and not require disassembling Pi from display.
- Speaker and charging modules must each be removable without opening their sealed/isolated neighbor.
- Every screw must have driver approach clearance. Every connector intended for service must have a defined unplug direction.
- No critical part may require destructive shell flexing, cutting, breaking a glued joint or removing an unrelated major module.

## 6. Release blockers

The following must be supplied/scanned/measured before manufacturing export:

1. Authoritative integrated Pi/display/cooler FreeCAD assembly and exact object names.
2. Exact IR model(s), both optical eye datums, mounts and connector keep-outs.
3. Exact four VL53L1X models after verifying/correcting only the 20 mm hole pattern.
4. Exact motor/encoder CAD and physical verification of critical dimensions.
5. Camera DWG verification: units, envelope, holes, lens/FOV keep-out and connector location.
6. Microphone revision, CAD/measurement, acoustic port geometry and mounting.
7. Final AUX block length × width × height, mounting pattern and connector keep-outs after the perfboard is populated and cut.
8. IP2368 board envelope, mount holes, USB-C datum, component heights/hot face and thermal test.
9. Purchased blower mount/inlet/outlet geometry.
10. Speaker and passive radiator outlines, hole patterns, gasket interfaces and enclosure volume/tuning target.
11. Power button body/bezel/depth/terminal dimensions.
12. Print process/material/tolerance, shell wall thickness, boss dimensions, pilot holes and locating-lip clearance.
13. Ground plane, axle height, wheel running clearance and stabilizing/bumper geometry.

Until these are resolved, output may be exploratory layout only and must be stamped `NOT FOR MANUFACTURE`.
