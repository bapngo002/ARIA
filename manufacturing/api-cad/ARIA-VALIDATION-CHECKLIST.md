# ARIA final CAD validation checklist

- **Run ID:** `PENDING`
- **Source commit:** `PENDING`
- **FCStd path / SHA-256:** `PENDING`
- **Constraint version:** `1.1.0`
- **Reviewer/date:** `PENDING`
- **Allowed status:** `PASS`, `FAIL`, `NOT_RUN`, `NOT_APPLICABLE`

Rules:

- Default status is `NOT_RUN`.
- A `PASS` requires a value, screenshot/report/object reference or repeatable method in Evidence.
- `NOT_APPLICABLE` requires written approval and reason.
- A critical row not `PASS` blocks **final manufacturing export only**, not layout work covered by an approved placeholder.
- Layout may continue when a row is `NOT_RUN` if the object map says layout-ready and the evidence names the assembly/envelope/constraint fallback.
- A layout item stops only when it has neither usable authority nor approved fallback (`BLOCKED_NO_AUTHORITY_OR_FALLBACK`).
- This checklist is copied into a dated run report; do not overwrite this template with unsupported PASS values.

## A. Inputs and object mapping

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | Source commit and all input SHA-256 values recorded | NOT_RUN | — |
| Yes | Integrated Pi/display/Smraza cooler assembly is captured before its final mount/shell interface release | NOT_RUN | Layout may use the real assembly as a locked group or a rigid placeholder |
| Yes | Every imported release component is mapped by exact FreeCAD `Object.Name`; unmapped layout items use approved placeholders | NOT_RUN | — |
| Yes | No fuzzy Label match or unmapped legacy CAD is used | NOT_RUN | — |
| Yes | Units, envelope, holes, connectors and keep-outs are verified for every `CAD_EXACT` promotion | NOT_RUN | — |
| Yes | Every UNKNOWN/PENDING/NOT_MAPPED/NOT_VERIFIED item is classified NON_BLOCKING or TRUE_BLOCKER with fallback/dependent scope | NOT_RUN | — |
| Yes | Layout validator reports zero `layout_blockers` | NOT_RUN | — |
| Yes | Existing reviewed/reference-only CAD is not treated as manufacturing authority | NOT_RUN | — |

## B. General collision and clearance

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | No solid-solid collision between components, mounts and shell | NOT_RUN | — |
| Yes | No shell/mount intersects any moving/swept volume | NOT_RUN | — |
| Yes | Final minimum clearances use documented print/process values; layout clearances remain explicit parameters | NOT_RUN | — |
| Yes | Connectors have plug/unplug and cable-entry clearance | NOT_RUN | — |
| Yes | No local shell growth exists without a documented functional reason | NOT_RUN | — |
| Yes | Final envelope is minimized after all functional checks | NOT_RUN | — |

## C. Camera and front optics

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | Camera is centered directly above the display | NOT_RUN | — |
| Yes | Camera lens axis points FRONT | NOT_RUN | — |
| Yes | Camera connector points DOWN toward display | NOT_RUN | — |
| Yes | Connector can be plugged/unplugged below camera | NOT_RUN | — |
| Yes | Only lens/optical window is externally exposed; PCB and mount remain hidden | NOT_RUN | — |
| Yes | Full verified FOV/optical keep-out clears bezel, ribs, bracket and decoration | NOT_RUN | — |
| Yes | Camera is removable from inside without destructive work | NOT_RUN | — |
| Yes | IR left/right external locations are mirror-symmetric | NOT_RUN | — |
| Yes | `IR_LEFT_LARGE_EYE_CLEAR` | NOT_RUN | — |
| Yes | `IR_LEFT_SMALL_EYE_CLEAR` | NOT_RUN | — |
| Yes | `IR_RIGHT_LARGE_EYE_CLEAR` | NOT_RUN | — |
| Yes | `IR_RIGHT_SMALL_EYE_CLEAR` | NOT_RUN | — |
| Yes | Rotated identical IR PCB(s) clear shell/connectors without breaking exterior symmetry | NOT_RUN | — |

## D. Four ToF sensors

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | Exactly four mapped sensor instances: front-left, front-right, side-left, side-right | NOT_RUN | — |
| Yes | Every connector points UP and every optical face points out | NOT_RUN | — |
| Yes | Each mounting-hole spacing is 20.00 mm; no whole-model scaling was used | NOT_RUN | — |
| Yes | Front-left beam meets floor at R200 ±10 mm from robot center | NOT_RUN | — |
| Yes | Front-right beam meets floor at R200 ±10 mm from robot center | NOT_RUN | — |
| Yes | Side-left beam meets floor at R200 ±10 mm from robot center | NOT_RUN | — |
| Yes | Side-right beam meets floor at R200 ±10 mm from robot center | NOT_RUN | — |
| Yes | Every optical aperture/beam is unobstructed | NOT_RUN | — |
| Yes | Sensors/brackets/beams clear wheels, motors, encoders and wheel swept volumes | NOT_RUN | — |
| Yes | Left/right external apertures are symmetric; any internal deviation is documented | NOT_RUN | — |

## E. Wheels, motors and encoders

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | Left wheel envelope is Ø61 × 24 mm | NOT_RUN | — |
| Yes | Right wheel envelope is Ø61 × 24 mm | NOT_RUN | — |
| Yes | Left wheel axis equals left motor rotor axis exactly | NOT_RUN | — |
| Yes | Right wheel axis equals right motor rotor axis exactly | NOT_RUN | — |
| Yes | Encoder axes are coaxial with respective motor axes | NOT_RUN | — |
| Yes | Each encoder outer PCB face is 5 mm from fixed/stator face | NOT_RUN | — |
| Yes | Motor stators/bodies are inside and supported; only required rotor output is exposed | NOT_RUN | — |
| Yes | Shell wheel stops/housings do not contact rotors or wheels | NOT_RUN | — |
| Yes | Both wheels have full 360° running clearance under tolerance/load assumptions | NOT_RUN | — |
| Yes | Internal wheel/hub adapter was not designed or constrained by the API | NOT_RUN | — |
| Yes | Ground plane, axle height and underside clearance are documented | NOT_RUN | — |

## F. Battery and AUX block

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | Battery is one 60 × 74 × 65 mm envelope including BMS | NOT_RUN | — |
| Yes | Battery uses only orthogonal 90° rotations | NOT_RUN | — |
| Yes | Battery load is supported by lower shell cradle/stops and removable retainer | NOT_RUN | — |
| Yes | Battery cannot shift into wheel/motor/encoder/speaker/electronics volumes | NOT_RUN | — |
| Yes | Battery can be removed without display, speaker or motor removal | NOT_RUN | — |
| Yes | Battery cable exit and service clearance are verified | NOT_RUN | — |
| Yes | Final AUX envelope comes from populated, trimmed and measured carrier—not raw 90 × 150 stock; layout uses an oversized editable placeholder | NOT_RUN | — |
| Yes | AUX block mount and all connector/terminal keep-outs are verified | NOT_RUN | — |
| Yes | D24V90F5 thermal clearance is preserved | NOT_RUN | — |

## G. Speaker and microphone acoustic integrity

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | Rear module includes two speakers and one passive radiator | NOT_RUN | — |
| Yes | Each speaker aperture is Ø40 mm and does not clip the active area | NOT_RUN | — |
| Yes | Verified speaker mounting/gasket geometry and 25 mm depth clear enclosure | NOT_RUN | — |
| Yes | Passive radiator outline, mount and gasket are verified | NOT_RUN | — |
| Yes | Speaker enclosure is sealed from electronics, shell leaks and cooling duct | NOT_RUN | — |
| Yes | Amplifier boards are outside sealed acoustic volume | NOT_RUN | — |
| Yes | Speaker enclosure volume/tuning target is documented and met | NOT_RUN | — |
| Yes | Mic chamber has a complete sealed wall to machine space | NOT_RUN | — |
| Yes | Upper/lower shell seam does not cross mic chamber | NOT_RUN | — |
| Yes | Separate mic roof and approximately 2–3 mm acoustic gap follow verified mic geometry | NOT_RUN | — |
| Yes | Roof supports, fasteners, ribs and decorations do not block mic acoustic paths | NOT_RUN | — |
| Yes | Cooling duct/intake/exhaust do not connect to mic chamber or acoustic gap | NOT_RUN | — |
| Yes | Mic module can be serviced without destroying chamber or unrelated modules | NOT_RUN | — |

## H. Charging and airflow

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | IP2368 is below blower in rear service zone | NOT_RUN | — |
| Yes | USB-C faces rear and is externally accessible with plug/finger clearance | NOT_RUN | — |
| Yes | IP2368 hot face does not contact printed shell | NOT_RUN | — |
| Yes | IP2368 board, mounts, connector, component heights and hotspot are verified | NOT_RUN | — |
| Yes | Purchased blower envelope, mount, inlet and outlet are verified | NOT_RUN | — |
| Yes | Airflow is intake → IP2368 hot region → blower → dedicated exhaust | NOT_RUN | — |
| Yes | Intake uses multiple parallel slanted fish-gill slots | NOT_RUN | — |
| Yes | Unobstructed intake open area is at least verified useful blower inlet area | NOT_RUN | — |
| Yes | Internal components/walls do not block intake or duct | NOT_RUN | — |
| Yes | Exhaust is separated from intake; hot-air recirculation check passes | NOT_RUN | — |
| Yes | Duct is separate from sealed speaker and isolated mic volumes | NOT_RUN | — |
| Yes | Duct has no unsupported sharp restriction and avoids heating battery | NOT_RUN | — |

## I. Button, shell joint and serviceability

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | Power-button mounting aperture is Ø12 mm | NOT_RUN | — |
| Yes | Button uses Ø12 through-hole plus open/oversized rear service keep-out; exact body data is required only if a tight cavity is introduced | NOT_RUN | — |
| Yes | Upper/lower shells align using a small locating lip without forced fit | NOT_RUN | — |
| Yes | Locating lip only locates; M2.5 screws provide clamping | NOT_RUN | — |
| Yes | Boss/pilot/lip dimensions come from documented print process, material and fasteners | NOT_RUN | — |
| Yes | Every M2.5 fastener has tool approach and installation clearance | NOT_RUN | — |
| Yes | Bosses have sufficient material and do not intersect component/keep-out volumes | NOT_RUN | — |
| Yes | Opening upper shell exposes lower chassis safely and connectors can be disconnected | NOT_RUN | — |
| Yes | Pi/display assembly removes as one rigid unit without internal disassembly | NOT_RUN | — |
| Yes | Battery, speaker, charging and mic modules each have verified removal vectors | NOT_RUN | — |
| Yes | No critical service action requires cutting, breaking glue, destructive flexing or unrelated major module removal | NOT_RUN | — |

## J. Export release

| Critical | Check | Status | Evidence |
|---|---|---|---|
| Yes | All sections A–I critical rows are PASS with evidence | NOT_RUN | — |
| Yes | `python scripts/01_validate_workspace.py --stage final-release` passes | NOT_RUN | — |
| Yes | No `true_blockers_final` remain | NOT_RUN | — |
| Yes | Final FCStd recomputes cleanly and final SHA-256 is recorded | NOT_RUN | — |
| Yes | Collision/optical/acoustic/airflow/assembly reports are present | NOT_RUN | — |
| Yes | STEP/STL/3MF export settings and source objects are recorded | NOT_RUN | — |
| Yes | Release manifest names source commit, constraints, input hashes and reviewer | NOT_RUN | — |
| Yes | Explicit user release approval is recorded | NOT_RUN | — |

- **Overall result:** `NOT_RUN`
- **Open deviations:** `PENDING`
- **Release approval:** `PENDING`
