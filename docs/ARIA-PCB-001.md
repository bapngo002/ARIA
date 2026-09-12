# ARIA-PCB-001 — Mainboard development rules

Purchased module identity and quantity come only from [`docs/ARIA-BOM-001.md`](ARIA-BOM-001.md).

- Do not choose footprints from product photos or from planned components.
- Confirm the delivered revision, pinout, connector orientation and mechanical drawing first.
- Review power entry, protection, current paths, grounding, audio noise and motor noise.
- Complete schematic review, ERC, PCB DRC and a 1:1 mechanical check before fabrication.
- Generated Gerbers must identify their source commit and explicit approval.

This file intentionally contains no second BOM.

## Compact module stack R2 — photo-based placement concept

User supplied two bench photos and authorizes stacking modules to minimize footprint. Photo 2 shows a perforated prototyping board, YD-style dual-USB ESP module, loose SimpleFOC boards, two amplifier boards, and a blue board visibly marked INA260. Photo 1 shows a round display and multiple loose wired peripherals. Individual solder joints, wire functions, exact dimensions, module health and power paths cannot be verified from these photos. The apparent INA260 is a new visual observation; confirm receipt/use before treating the prior pending-delivery record as resolved. No photo-derived pad spacing or footprint is released.

[Exploded top views of the proposed stack](../electronics/layout/ARIA-stack-layout-R2.svg). Concept only, not to scale, not a solder map. It supersedes the R1 single-plane placement assumption; the R1 proposed signal assignment remains unchanged in ARIA-WIRING-001.md. User confirms replacement ESP same family. User subsequently confirms the available perfboard is 70 × 100 mm and requests compact stacking instead of spreading all modules over its area. Allowable total height still requires measurement; no claim this is the smallest possible envelope or that all modules fit the photographed board.

### Proposed organization

| Level | Placement role | Access and routing |
|---|---|---|
| Base | Two driver modules side by side; power entry/distribution, Pololu, IP2368 and one INA260 position | High-current harness stays low/peripheral; charger at accessible edge. Not every module need share the same small island; isolate connectors and maintain ventilation. Current-monitor insertion point/address remains undecided. |
| Middle | Replaceable ESP on sockets plus two MAX98357A modules | Standoffs, not loose stacking. ESP antenna protrudes into a clear outer region across ALL levels; native USB/BOOT/RESET accessible. Audio at an outside edge with short I2S and separate speaker pairs. Offset audio from converter inductors/driver hot spots when actual positions are measured. |
| Top | Pi on its own mounting posts, cooler unobstructed | Leave USB/FFC/GPIO and fan airflow accessible; Pi must not overhang ESP antenna. Pi is a removable assembly, not soldered to perfboard. If stack heat/height fails, place Pi adjacent on the same mechanical base instead. |
| Functional mounts | Screen/camera at face; ToF at actual viewing positions; mic acoustically open; BME280 exposed to representative ambient air; BNO085 rigid to chassis reference; motors/speakers/battery on dedicated supports | Edge connectors bring these to the central assembly. They are not arbitrarily packed onto the electrical carrier; geometry controls sensing and acoustic performance. Keep IMU away from switching heat, vibration hot spots and magnetic sources such as motors/speakers. |

### Assembly and wiring method

1. Keep everything unpowered during the current incident recovery. Label each existing cable at both ends before disconnecting: motor-left phases, motor-right phases, ENC-L, ENC-R, ToF S1–S4, IMU, BME, speaker-L/R and supply voltage/domain. Wire color alone is not pin identity. Do not reconnect the burned ESP or assume the encoders passed after the incident.
2. Dry-place the modules on paper/perfboard and measure footprints including solder tails, raised capacitors, connector plugs and cable bend/strain relief. Level height is the tallest occupied envelope plus verified electrical/mechanical clearance; no universal standoff height is assigned. Use rigid insulating supports/verified mounting points and avoid screw contact with traces. Tape alone is not a structural spacer.
3. Do not run traction current through perfboard pad chains, Dupont jumpers or Pi/USB returns. Use suitable dedicated protected power wiring/distribution selected after actual current and connector review. Keep 3.3V/5V/motor-supply identities distinct; do not parallel regulator outputs. Preserve the power/EN restrictions in ARIA-WIRING-001.md.
4. Give each encoder its own short bus harness to ESP; keep it physically separated from phase wires. Route Pi I2C as a short trunk with short peripheral branches where geometry permits, account for aggregate pull-ups/capacitance, and validate on the real harness. I2C branches to remote ToF still require an achievable layout; a connector hub does not cure excessive cable length.
5. Use a small labeled detachable harness between levels: a power group, a motor-control/encoder group and a Pi sensor/audio group, with distinct/keyed connectors. Standardize connector families only after voltage/current, pin count and cable mating order are verified; no guessed universal pin order. Avoid unnecessary connectors in fast or low-level signal paths.
6. Retain USB and DSI/CSI factory cable connections. Do not solder substitute FFC/USB high-speed traces across perfboard. Leave service loops sufficient to lift one tier without pulling connectors; secure bundles at their exits. Do not cover fan intake/exhaust or trap driver/buck heat inside the stack.
7. Check the unpowered continuity/polarity plan first, then isolated rails/module tests, then controlled assembled thermal and noise checks. No encoder re-use, new firmware flash or motion is authorized merely by this mechanical drawing.

### Review boundaries

Espressif recommends the antenna outside the baseboard edge and sufficient clearance in the final assembly; apply this to every stacked board, wire and metal support, not just the layer carrying ESP. [Official module placement guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html#general-principles-of-pcb-layout-for-modules-positioning-a-module-on-a-base-board).

Copilot Pro reviewed the earlier single-plane proposal (1.73 AI credits; no file changes). Retained concerns: phase/encoder coupling, shared noisy return paths, uncertain fit and post-incident isolation. Rejected suggestions to invent a universal IMU standoff distance or cut a generic ground moat; actual mechanical/return-path design and measurements are needed. Stacked R2 is the primary agent's response to the subsequent user instruction and is not a Copilot-approved hardware release. Generated diagram was visually checked for readable labels; no CAD fit, schematic ERC, electrical test or thermal test has occurred.

### Power edge refinement — user-confirmed 70 × 100 mm base

Arrange power connection points along ONE accessible edge across tiers, with each bank explicitly labeled by voltage and source, not by generic VCC/VIN. This meets the request for orderly common rows without electrically shorting incompatible supplies. Available base size is confirmed, but there is no module-envelope fit proof; upper carriers may be smaller, with supports and clearances determined by measurement. Do not yet cut perfboard or assign hole coordinates.

| Proposed bank at service edge | Sharing rule | Scope |
|---|---|---|
| GND / returns | Common electrical reference, deliberate separate branch returns | Motor/buck/input high-current returns go directly to rated distribution; no traction return through sensor/USB/perfboard pad chains |
| VBAT_PROTECTED | Protected battery-voltage distribution, separately protected branches | Motor drivers and buck input only as allowed by reviewed power tree; no Pi/ESP/sensor/amplifier input here |
| 5V_SYS | Regulated 5V supply with individually identified branches | Approved 5V loads; Pi power entry and USB backfeed rules remain unresolved/reviewed separately |
| 3V3_PI | Pi-side logic domain | Only compatible Pi-side sensor logic/load after carrier revision and current-budget review |
| 3V3_ESP | ESP-side logic domain | Encoder supply after isolation/health/current-budget checks; never connected to 3V3_PI or driver auxiliary 3.3V output |

These are segregated terminal banks in a shared physical row, NOT one continuous positive rail. No generic VCC/VIN wire is assigned until its module input requirement is checked. Per-module current/polarity, busbar/wire sizing, fuse ratings and a common power-source scheme remain schematic tasks. Keep these banks distinct by labels and spacing/keying; color alone is insufficient. Leave motor phases and differential speaker outputs off both positive and GND buses. Ground is not galvanic isolation. Use suitable distribution terminals/wiring, not a long bridged chain of small perfboard pads for power.

Do not interpret the latest answer as confirmation that INA260 has arrived; it only specifies base dimensions and desired wiring organization. Its label is visible in the photo, while explicit receipt/use confirmation remains pending.


## SolidWorks-viewable 3D concept R3

User requested a SolidWorks drawing to view the stack. [Assembled STEP](../electronics/layout/stack-r3/ARIA_STACK_R3_ASSEMBLED_CONCEPT.step) and [exploded STEP](../electronics/layout/stack-r3/ARIA_STACK_R3_EXPLODED_CONCEPT.step) are generated from simplified solids, not verified component STEP models. See [scope and assumptions](../electronics/layout/stack-r3/README.txt). Base 70x100 mm is confirmed; illustrative tier elevations 0/30/60 mm and approximate full envelope 70x120x79.6 mm are not released dimensions. Extra length is antenna overhang. Shape validity and preview readability checked; no fit/interference, mounting, electrical or thermal release. Native FreeCAD files and PNG previews are under D:/UserData/ARIA/current-task/outputs/SolidWorks-layout. SolidWorks COM startup did not return during the bounded attempt; native SLDPRT save/import verification is not complete. STEP format is provided for manual opening in SolidWorks.
