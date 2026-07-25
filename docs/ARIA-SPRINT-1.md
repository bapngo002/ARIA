# ARIA — Sprint 1 Procedure for a First-Time Builder

**Goal:** select hardware safely and produce BOM Rev A.  
**Current state:** M0 complete; M1 in progress; M2 is only a draft.

## Before you start

Do not buy the complete robot in one order. Sprint 1 is successful when choices
are supported by measurements and quotes, not when the most parts have arrived.

Create an evidence folder for each experiment (future recommendation:
`evidence/sprint-1/`). Save a photo of the setup, exact part revision, OS image
name, test command/application, result and date.

## Step 1 — Inventory what you already own

Record:

- microSD card and USB card reader;
- HDMI monitor/TV and keyboard/mouse usable for the first boot;
- 5 V power supplies and multimeter;
- soldering iron, wire, connectors and bench supply;
- any camera, speaker, battery or chassis parts.

Do not count an unknown/old battery as reusable until its condition and protection
are verified.

**Output:** owner-supplied list and money genuinely saved.

## Step 2 — Get quotes, but buy only Wave 1

For each critical line, compare:

- exact model and RAM/revision;
- delivered price;
- stock status;
- return policy and warranty;
- whether cables, power adapter and heatsink are included.

Buy only Orange Pi 3B 4 GB, genuine microSD and cooling first. Keep screenshots
or invoices and update the quote sheet in `ARIA-BOM-001.md`.

**Stop condition:** if the exact board revision cannot be confirmed, do not order.

## Step 3 — Platform smoke test

1. Photograph the board label/revision.
2. Flash the vendor-supported Linux desktop image and save its full filename and
   checksum.
3. Boot 20 times.
4. Test Wi-Fi reconnect and Bluetooth pairing.
5. Play 1080p YouTube for 60 minutes.
6. Record peak temperature, CPU/RAM use, dropped frames and any crash.

**Pass:** no failed boot, no crash, no thermal throttling, stable networking.

## Step 4 — Compute and camera test

Connect any temporary UVC webcam. Run a lightweight person detector at 640×480
while the face UI placeholder and audio capture are active.

Record:

- average and minimum FPS;
- average/peak CPU and RAM;
- temperature after 30 minutes;
- person detection under normal and low room light.

**Initial pass:** ≥8 FPS and <85% sustained RAM use. This is not a final product
performance promise; it is a platform-selection threshold.

## Step 5 — Audio feasibility test

Build the four-microphone fixture rigidly and symmetrically. Do not test loose
microphones on wires because their geometry determines direction accuracy.

Test from front/right/back/left at 1 m and 3 m:

- quiet room;
- cooling fan running;
- robot speaker playing at normal volume.

For each condition, perform 20 wake-word trials and 20 direction trials. Record
false wakes and whether the correct 90° sector was selected.

**Pass:** 18/20 quiet wake trials, 16/20 noisy wake trials and 16/20 direction
trials. If it fails, do not spend weeks hiding the failure in software; price a
processed USB microphone array and revise the budget.

## Step 6 — Motor and safety rig

Keep the wheels off the floor.

1. Measure each motor's no-load and brief stall current at its intended voltage.
2. Confirm motor-driver thermal/current margin.
3. Make ESP32 boot with motor enable off.
4. Implement encoder read, speed clamp, acceleration clamp and local stop.
5. Send high-level velocity commands from the SBC at a 10 Hz heartbeat.
6. Disconnect/reboot the SBC; verify stop within 300 ms.
7. Unplug each cliff/range sensor; a missing/invalid sensor must cause a stop.
8. Press each bumper and emergency stop.

**Pass:** all faults stop motion, and restarting communication alone does not
unexpectedly restart the wheels.

## Step 7 — Power test

First use a current-limited bench supply if available. Then test the intended
battery, BMS, fuse and regulators.

Worst-case test:

- display at full brightness;
- Wi-Fi transfer/YouTube active;
- camera and audio active;
- speaker playing;
- motors repeatedly starting and reversing on the raised rig.

Record rail voltage, peak current, regulator temperature and any brownout for 30
minutes.

**Pass:** no reboot, no hot connector/wire, no regulator beyond its rating and no
unsafe battery behavior.

## Step 8 — Freeze M1 and promote BOM

Only after Steps 3–7:

1. choose Orange Pi 3B or trigger the Orange Pi 5 fallback;
2. select the microphone implementation;
3. select motor driver from measured current;
4. replace target prices with selected quotes;
5. add 10% contingency;
6. mark architecture “Accepted” and BOM “Rev A”.

Do not alter `ARIA-PRD-001.md`; any requirement change needs the formal revision
process defined in that document.

## Immediate next action

Fill the inventory in Step 1, then obtain two delivered-price quotes for:

- Orange Pi 3B 4 GB;
- 64 GB genuine high-endurance/A2 microSD;
- compatible heatsink and fan.

The first authorized purchase should contain only those Wave 1 items.

