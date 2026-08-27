# ARIA final CAD workflow

This workflow is mandatory. A phase may produce an exploratory report while pending inputs exist, but no downstream manufacturing geometry may bypass its gate.

## Output labels

- `LAYOUT / PLACEHOLDERS / NOT FOR MANUFACTURE`: incomplete final inputs, but every item has an approved assembly/envelope/constraint fallback; geometry may be developed, saved and reviewed.
- `GEOMETRY VERIFIED / NOT RELEASED`: inputs verified and geometry checks pass, but release approval is absent.
- `RELEASED`: all critical checks PASS, sources/hashes are recorded and the user explicitly approves export.

`PENDING` alone never stops work. Only a `BLOCKED_NO_AUTHORITY_OR_FALLBACK` item stops layout. `TRUE_BLOCKER` stops only the dependent final manufacturing interface/export.

## Phase 0 — freeze source state

1. Fetch the latest `main` and record its full commit SHA.
2. Work on a dedicated branch/worktree, never directly on `main`.
3. Read the workspace files in the order specified by `README.md`.
4. Compare the workspace `repo_baseline` to current `main`.
5. If canonical inventory or engineering rules changed, reconcile and commit the workspace update before touching CAD.
6. Run `python scripts/01_validate_workspace.py --stage layout` to validate JSON structure, placeholder authority and layout readiness.

**Gate 0:** workspace parses; no conflicting duplicate object IDs; all repo paths/hashes that claim to exist are valid; layout validator reports zero layout blockers.

## Phase 1 — collect and quarantine inputs

1. Put candidate FreeCAD/STEP/DWG files in `input/cad/` only after recording their origin.
2. Put physical measurement records in `input/measurements/`; every record includes component ID, revision/marking, instrument, date, units, measured dimensions and uncertainty/resolution.
3. Put images in `input/reference-images/`; tag each as style, identity, connector orientation or measurement evidence. Images alone are never dimensional authority.
4. Calculate SHA-256 for every input.
5. A reviewed/unverified file may be used only as an explicitly labeled placement reference when constraints allow it. It cannot become final mating geometry merely because it removes a placeholder.

**Gate 1:** every used candidate has provenance/hash/state; every item without a verified candidate has an explicit envelope/constraint fallback.

## Phase 2 — scan FreeCAD

Run the read-only scanner with FreeCAD's command-line runtime:

```text
FreeCADCmd scripts/00_scan_freecad.py input/cad/<assembly>.FCStd output/reports/freecad-scan.json
```

The scan report must contain:

- document path and SHA-256;
- FreeCAD `Object.Name`, `Label`, `TypeId` and parent/group context;
- placement and shape bounding box;
- empty/invalid shape flags;
- duplicate labels and suspiciously duplicated bounding boxes;
- file/open errors.

Do not modify geometry in the scan step.

**Gate 2:** if a real assembly is available, it opens without repair errors and has a scan report. If unavailable, generate the approved placeholder and continue; this does not block layout.

## Phase 3 — map objects exactly

1. Match components to exact FreeCAD `Object.Name`, not display `Label` and not a fuzzy string search.
2. Update `ARIA-OBJECT-MAP.json` with exact object names, source file and SHA-256.
3. Map the integrated Pi/display/cooler assembly to one parent assembly object and list its internal children only for collision/verification; never expose them as independently movable layout objects.
4. Map each IR optical eye and each ToF optical datum explicitly where the CAD provides child objects/datums.
5. If an object is absent, duplicated ambiguously or nested unexpectedly, do not guess the match. Keep it `NOT_MAPPED_NON_BLOCKING`, instantiate its approved placeholder and continue layout.

**Gate 3:** every object has either an exact unambiguous map or an approved placeholder authority; no fuzzy match is used.

## Phase 4 — verify dimensions and functional datums

For every imported component:

1. Confirm units and overall envelope against manufacturer mechanical data or physical measurement.
2. Confirm mounting holes, connectors, component heights and removal direction.
3. Confirm optical/acoustic/thermal datums and keep-outs.
4. Confirm source/revision matches the purchased part.
5. Record deviations and their authority.

Special corrections:

- Camera DWG: verify scale, outline, mounting holes, lens/FOV and connector position before promotion.
- Pi DWG with official cooler: reject for final assembly because purchased cooler is Smraza.
- YD-ESP32 CAD in `cad-review/`: nominal/reference only until the delivered board is measured; the final CAD object is the measured AUX block, not an independent shell-mounted ESP board.
- VL53L1X: if hole spacing is not `20.00 mm`, edit only mounting-hole geometry. Never uniformly scale the module.

**Gate 4:** a dimension/open-items report exists. Each unknown is classified `NON_BLOCKING` or `TRUE_BLOCKER`. Non-blocking placeholder geometry continues; only the affected final mating/aperture/sealing geometry waits for a true blocker.

## Phase 5 — create locked envelopes and datums

1. Create Battery Block `60 × 74 × 65 mm` as one solid; do not expose cells/BMS.
2. Create two wheel envelopes `Ø61 × 24 mm` with central axes; do not design hub interiors.
3. Create conservative speaker, PR, IP2368, blower and button envelopes as allowed by constraints; mark partial geometry `PLACEHOLDER / NOT FOR MANUFACTURE`.
4. Do not create a `90 × 150 mm` AUX block. Create an oversized editable AUX placeholder slightly larger than the ESP board; let it drive spatial layout but not final retention or a tight shell closure.
5. Establish semantic datums: robot center plane, ground plane, FRONT, motor axes, wheel swept volumes, optical rays and service/removal vectors.

**Gate 5:** every generated envelope is traceable to a locked constraint or documented conservative fallback and contains no invented hidden detail.

## Phase 6 — layout

Order of priority:

1. verified motors/encoders/wheels and ground relationship;
2. Battery Block, using only orthogonal rotations;
3. locked Pi/display/cooler assembly as one rigid body;
4. rear speaker module reserved volume;
5. charging/cooling module;
6. measured AUX block;
7. camera/IR and four ToF modules;
8. isolated mic module.

Layout rules:

- preserve exact wheel/motor coaxiality and encoder 5 mm spacing;
- support heavy parts on the lower shell;
- keep battery low/near center while preserving removal;
- keep external camera/IR geometry centered and symmetric;
- leave room for real connectors and tool/removal vectors;
- minimize final envelope only after functional constraints pass.

**Gate 6:** no hard collision between current authorities/placeholders; every major module has a feasible insertion/removal vector. Placeholder-driven clearances remain parametric.

## Phase 7 — mounts and module interfaces

1. Build parametric motor/stator mount reservations and wheel housing/stop without touching rotating geometry; do not freeze final hole geometry until shared drive data is verified.
2. Build a lower-shell battery cradle, lateral stops and removable M2.5 retainer.
3. Mount the entire Pi/display assembly at its existing assembly interfaces.
4. Mount sensors only through verified holes; do not drill virtual PCB holes.
5. Build removable, adjustable/open interfaces for AUX, speaker, charging and mic placeholders; tighten them only after final source data arrives.
6. Add only necessary cable pass-throughs across isolated walls.

**Gate 7:** loads reach lower chassis appropriately; current fasteners/connectors are accessible; unresolved final interfaces remain visibly parametric/placeholder.

## Phase 8 — acoustic and cooling subsystems

### Acoustic

1. Reserve and shape a parametric sealed rear enclosure now. Freeze gasket seats, mounting holes and final acoustic volume only after exact geometry and tuning target exist.
2. Keep MAX98357A modules outside the sealed volume.
3. Build a fully isolated top mic chamber with a separate roof, approximately 2–3 mm acoustic gap and unobstructed acoustic paths.
4. Do not share mic, speaker or airflow volumes.

### Cooling

1. Put the conservative IP2368 placeholder below the 30 × 30 × 10 blower placeholder; point USB-C service direction to rear and allow a local flat.
2. Route lower/body intake air over the verified hot region into blower exhaust.
3. Create parallel slanted fish-gill intake slots.
4. Verify open area, internal blockage and hot-air recirculation.

**Gate 8:** conceptual/parametric speaker separation, mic isolation and complete intake-to-exhaust path all PASS for layout. Final leak/flow evidence is deferred to final release.

## Phase 9 — shell generation

1. Generate the outer envelope from the verified internal layout, not from a fixed Ø200 body.
2. Follow ARIA exterior language without copying screenshot dimensions.
3. Split into upper/lower shells along a serviceable seam that avoids the mic chamber and critical apertures.
4. Preserve local flat/service surfaces only where required.
5. Add only verified windows/apertures for display, camera, four IR eyes, four ToF beams, speakers/PR, intake/exhaust, USB-C and button.

**Gate 9:** collision, wall integrity, reserved aperture and service checks pass on both shell halves. Placeholder-derived apertures remain uncommitted manufacturing features.

## Phase 10 — M2.5 bosses and locating lip

1. Place/count parametric M2.5 bosses and locating lip now using the locked joint concept.
2. Before final release, load recorded print material/process/tolerance and exact fastener data, then resolve boss, pilot-hole and lip-fit parameters. Do not model threads.
3. The locating lip aligns but does not snap or carry clamp load.
4. Place bosses away from keep-outs and add driver-access volumes.
5. Validate shell alignment without forcing or overconstraint.

**Gate 10 layout:** boss locations and tool paths are feasible. **Gate 10 final:** print/tolerance/fastener values are verified and all joint fit checks PASS.

## Phase 11 — validation

Execute and record every line in `ARIA-VALIDATION-CHECKLIST.md`:

1. collision and minimum clearance;
2. camera orientation/FOV and connector DOWN;
3. all four IR eye paths;
4. four ToF floor intersections and wheel/drive clearance;
5. wheel/motor/encoder axes and swept volumes;
6. speaker sealing and mic isolation;
7. intake/duct/exhaust and recirculation;
8. battery, Pi/display and other module removal simulations;
9. upper/lower alignment, fastener and connector accessibility.

For layout, `NOT_RUN/PENDING` is permitted when an approved placeholder/fallback is recorded. For final manufacturing export, every final-critical row must PASS with evidence and no `TRUE_BLOCKER` may remain.

## Phase 12 — export and release

1. Recompute and save the final FCStd.
2. Run `python scripts/01_validate_workspace.py --stage final-release`.
3. Record source commit, FCStd SHA-256, constraint version and validation report.
4. Export neutral assembly STEP plus print files only for approved design-new parts; choose STL/3MF tolerances intentionally and record them.
5. Put final files in `output/export/` with a release manifest.
6. Do not overwrite a previous release; use versioned filenames/directories.
7. Require explicit user approval before labeling `RELEASED` or merging release geometry to `main`.

## Change control

- Never ask the user to restate a decision already recorded in this workspace. Read the source files and continue from the approved constraint/placeholder.
- Request new user input only when the exact dependent final interface has reached a recorded `TRUE_BLOCKER` that cannot be resolved by measurement already present in the repo/workspace.
- A new measurement updates the measurement record, constraints/object map as needed and triggers every dependent validation again.
- A changed component revision returns the affected object to `PENDING`, selects its approved placeholder and blocks only the dependent final interface until reverified.
- A manual CAD deviation must state reason, affected objects/checks and user approval.
- Never fix a failed check by weakening/deleting the constraint without explicit approval.
