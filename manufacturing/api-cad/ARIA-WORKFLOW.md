# ARIA final CAD workflow

This workflow is mandatory. A phase may produce an exploratory report while pending inputs exist, but no downstream manufacturing geometry may bypass its gate.

## Output labels

- `EXPLORATORY / NOT FOR MANUFACTURE`: incomplete inputs or failed checks; geometry may be used only to discuss layout.
- `GEOMETRY VERIFIED / NOT RELEASED`: inputs verified and geometry checks pass, but release approval is absent.
- `RELEASED`: all critical checks PASS, sources/hashes are recorded and the user explicitly approves export.

## Phase 0 — freeze source state

1. Fetch the latest `main` and record its full commit SHA.
2. Work on a dedicated branch/worktree, never directly on `main`.
3. Read the workspace files in the order specified by `README.md`.
4. Compare the workspace `repo_baseline` to current `main`.
5. If canonical inventory or engineering rules changed, reconcile and commit the workspace update before touching CAD.
6. Run `python scripts/01_validate_workspace.py --allow-pending` to validate JSON structure and enumerate blockers.

**Gate 0:** workspace parses; no conflicting duplicate object IDs; all repo paths/hashes that claim to exist are valid.

## Phase 1 — collect and quarantine inputs

1. Put candidate FreeCAD/STEP/DWG files in `input/cad/` only after recording their origin.
2. Put physical measurement records in `input/measurements/`; every record includes component ID, revision/marking, instrument, date, units, measured dimensions and uncertainty/resolution.
3. Put images in `input/reference-images/`; tag each as style, identity, connector orientation or measurement evidence. Images alone are never dimensional authority.
4. Calculate SHA-256 for every input.
5. Do not copy an item from `purchased-hardware/cad-review/` into the approved flow merely to remove a blocker. Resolve the exact mismatch/verification issue first.

**Gate 1:** every candidate has provenance, hash and explicit verification state.

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

**Gate 2:** authoritative assembly opens without repair errors and scan report is committed or attached to the CAD run.

## Phase 3 — map objects exactly

1. Match components to exact FreeCAD `Object.Name`, not display `Label` and not a fuzzy string search.
2. Update `ARIA-OBJECT-MAP.json` with exact object names, source file and SHA-256.
3. Map the integrated Pi/display/cooler assembly to one parent assembly object and list its internal children only for collision/verification; never expose them as independently movable layout objects.
4. Map each IR optical eye and each ToF optical datum explicitly where the CAD provides child objects/datums.
5. If an object is absent, duplicated ambiguously or nested unexpectedly, stop and report it as `NOT_MAPPED`.

**Gate 3:** all critical imported objects have an exact unambiguous map; no banned legacy file is used.

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

**Gate 4:** a dimension report exists. Critical `UNKNOWN/PENDING/NOT_VERIFIED` causes a hard stop for dependent geometry.

## Phase 5 — create locked envelopes and datums

1. Create Battery Block `60 × 74 × 65 mm` as one solid; do not expose cells/BMS.
2. Create two wheel envelopes `Ø61 × 24 mm` with central axes; do not design hub interiors.
3. Create only provisional speaker/blower/button envelopes as allowed by constraints; mark them `NOT FOR MANUFACTURE` where geometry is partial.
4. Do not create a `90 × 150 mm` AUX block. Until measured, a temporary clearly labeled visualization block may be slightly larger than the ESP board, but it cannot drive shell or mount release.
5. Establish semantic datums: robot center plane, ground plane, FRONT, motor axes, wheel swept volumes, optical rays and service/removal vectors.

**Gate 5:** every generated envelope is traceable to a locked number and contains no invented detail.

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

**Gate 6:** no hard collision; every major module has a feasible insertion/removal vector.

## Phase 7 — mounts and module interfaces

1. Build motor/stator mounts and wheel housing/stop without touching rotating geometry.
2. Build a lower-shell battery cradle, lateral stops and removable M2.5 retainer.
3. Mount the entire Pi/display assembly at its existing assembly interfaces.
4. Mount sensors only through verified holes; do not drill virtual PCB holes.
5. Build removable interfaces for AUX, speaker, charging and mic modules.
6. Add only necessary cable pass-throughs across isolated walls.

**Gate 7:** loads reach lower chassis appropriately; all fasteners/connectors are accessible.

## Phase 8 — acoustic and cooling subsystems

### Acoustic

1. Build a sealed rear enclosure for two speakers plus one passive radiator only after exact geometry and tuning target exist.
2. Keep MAX98357A modules outside the sealed volume.
3. Build a fully isolated top mic chamber with a separate roof, approximately 2–3 mm acoustic gap and unobstructed acoustic paths.
4. Do not share mic, speaker or airflow volumes.

### Cooling

1. Put IP2368 below the blower; point USB-C to rear and allow a local flat.
2. Route lower/body intake air over the verified hot region into blower exhaust.
3. Create parallel slanted fish-gill intake slots.
4. Verify open area, internal blockage and hot-air recirculation.

**Gate 8:** speaker leak check, mic isolation check and complete intake-to-exhaust path all PASS.

## Phase 9 — shell generation

1. Generate the outer envelope from the verified internal layout, not from a fixed Ø200 body.
2. Follow ARIA exterior language without copying screenshot dimensions.
3. Split into upper/lower shells along a serviceable seam that avoids the mic chamber and critical apertures.
4. Preserve local flat/service surfaces only where required.
5. Add only verified windows/apertures for display, camera, four IR eyes, four ToF beams, speakers/PR, intake/exhaust, USB-C and button.

**Gate 9:** collision, wall integrity, aperture and service checks pass on both shell halves.

## Phase 10 — M2.5 bosses and locating lip

1. Load recorded print material/process/tolerance and exact fastener data.
2. Create M2.5 bosses and pilot holes; do not model threads.
3. Create a small locating lip with assembly clearance; it aligns but does not snap or carry clamp load.
4. Place bosses away from keep-outs and add driver-access volumes.
5. Validate shell alignment without forcing or overconstraint.

**Gate 10:** print/tolerance values are verified; all joint checks PASS.

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

Any critical `FAIL`, `NOT_RUN`, `UNKNOWN` or unsupported `PASS` blocks export.

## Phase 12 — export and release

1. Recompute and save the final FCStd.
2. Run strict workspace validation without `--allow-pending`.
3. Record source commit, FCStd SHA-256, constraint version and validation report.
4. Export neutral assembly STEP plus print files only for approved design-new parts; choose STL/3MF tolerances intentionally and record them.
5. Put final files in `output/export/` with a release manifest.
6. Do not overwrite a previous release; use versioned filenames/directories.
7. Require explicit user approval before labeling `RELEASED` or merging release geometry to `main`.

## Change control

- A new measurement updates the measurement record, constraints/object map as needed and triggers every dependent validation again.
- A changed component revision returns the affected object to `PENDING`.
- A manual CAD deviation must state reason, affected objects/checks and user approval.
- Never fix a failed check by weakening/deleting the constraint without explicit approval.
