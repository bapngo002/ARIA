# ARIA V1 — BOM Rev A Working Draft

**Document ID:** ARIA-BOM-001  
**Revision:** Draft A0  
**Date:** 2026-07-25  
**Status:** Budgetary estimate — **DO NOT BUY FULL BOM**  
**Currency:** VND

Prices below are target prices for selection, not supplier quotations. Shipping,
tools, enclosure printing, replacement parts, taxes, ChatGPT/Gemini usage and
other subscriptions are excluded.

## 1. Base BOM

| ID | Subsystem | Candidate / minimum specification | Qty | Target unit | Target total | Gate |
|---|---|---|---:|---:|---:|---|
| C01 | Main compute | Orange Pi 3B 4 GB, exact revision recorded | 1 | 1,450,000 | 1,450,000 | M1-1, M1-2 |
| C02 | Storage | 64 GB high-endurance/A2 microSD, genuine | 1 | 200,000 | 200,000 | M1-1 |
| C03 | Cooling | Board-specific heatsink + 5 V fan | 1 | 120,000 | 120,000 | M1-1 |
| D01 | Display | 7-inch IPS HDMI, 1024×600 or better, USB capacitive touch | 1 | 950,000 | 950,000 | M1-1 |
| V01 | Camera | UVC USB, 1080p, ≥100° diagonal FOV | 1 | 350,000 | 350,000 | M1-2 |
| A01 | Direction audio | 4× matched INMP441 I2S microphones + rigid circular fixture | 1 set | 200,000 | 200,000 | M1-3 |
| A02 | Playback | 3 W class-D amplifier + 4 Ω speaker | 1 set | 180,000 | 180,000 | M1-3 |
| M01 | Safety MCU | ESP32-S3 dev board with PSRAM | 1 | 180,000 | 180,000 | M1-4 |
| M02 | Drive motors | 6 V metal gear motors with quadrature/Hall encoders; stall current must be measured | 2 | 250,000 | 500,000 | M1-4 |
| M03 | Motor driver | TB6612FNG module; conditional on measured stall current | 1 | 90,000 | 90,000 | M1-4 |
| M04 | Running gear | 2 wheels + caster | 1 set | 150,000 | 150,000 | M1-4 |
| S01 | Range/cliff | VL53L0X modules: 3 forward + 2 downward | 5 | 65,000 | 325,000 | M1-4 |
| S02 | I²C expansion | TCA9548A multiplexer | 1 | 50,000 | 50,000 | M1-4 |
| S03 | IMU | 6-axis IMU module, ICM-42688 class preferred | 1 | 100,000 | 100,000 | M1-4 |
| S04 | Bumper | Lever microswitches + physical bumper bar | 2 | 15,000 | 30,000 | M1-4 |
| S05 | Presence | HLK-LD2410C-class 24 GHz presence module | 1 | 100,000 | 100,000 | Functional |
| S06 | Environment | SHT31 temperature/humidity module | 1 | 100,000 | 100,000 | Functional |
| P01 | Battery | Reputable 2S Li-ion pack, ~3 Ah, with documented cells | 1 | 450,000 | 450,000 | M1-5 |
| P02 | Regulation | 5 V ≥4 A logic buck + motor rail regulator, fused | 1 set | 250,000 | 250,000 | M1-5 |
| P03 | Safety/wiring | BMS, fuse, E-stop, privacy switches, LEDs, connectors, wire | 1 set | 200,000 | 200,000 | M1-4, M1-5 |
| K01 | Mechanical | Prototype plates, standoffs, brackets and fasteners | 1 set | 250,000 | 250,000 | M3 |
|  |  | **Base estimate** |  |  | **6,225,000** |  |
|  |  | **Recommended 10% contingency** |  |  | **622,500** |  |
|  |  | **Responsible funding envelope** |  |  | **6,847,500** |  |

## 2. Budget actions

To approach 6,000,000₫ without removing a frozen requirement:

1. Obtain two quotes for C01 and D01; a combined saving of 225,000₫ reaches the
   nominal target.
2. Reuse a genuine 64 GB microSD or prototype chassis only if already owned and
   tested. Record reused items at fair cost and as “owner supplied”.
3. A 5-inch display can save about 200,000–300,000₫, but approve it only after a
   YouTube/readability demo.
4. Do **not** save money by removing bumpers, cliff sensors, fuse, emergency stop,
   encoder feedback, BMS or independent ESP32 safety control.

## 3. Conditional upgrade paths

| Trigger | Replace/add | Expected budget effect |
|---|---|---:|
| Orange Pi 3B fails compute/thermal test | Orange Pi 5 4 GB + radio if needed | +800,000 to +1,200,000 |
| Low-cost mic array fails wake/DOA/AEC test | Processed USB 4-mic array | +1,000,000 to +1,500,000 |
| Motor stall current exceeds driver margin | Higher-current dual motor driver | +100,000 to +300,000 |
| Front ToF coverage is too narrow | Add/replace with wider-FOV ToF or scanning mount | +150,000 to +600,000 |
| Battery test is below required runtime | Higher-capacity certified pack | +200,000 to +500,000 |

## 4. Quote sheet

Fill this table before ordering. A URL alone is not enough; record the exact
variant, stock status, warranty and delivered price.

| BOM ID | Supplier A / delivered price / date | Supplier B / delivered price / date | Selected | Reason |
|---|---|---|---|---|
| C01 | TBD | TBD | TBD | |
| D01 | TBD | TBD | TBD | |
| V01 | TBD | TBD | TBD | |
| M02 | TBD | TBD | TBD | |
| P01 | TBD | TBD | TBD | |

## 5. Procurement waves

- **Wave 0 — no purchase:** confirm which tools/parts are already owned.
- **Wave 1 — platform test:** C01, C02, C03 only.
- **Wave 2 — interaction bench:** D01, V01, A01, A02, M01.
- **Wave 3 — raised-wheel safety rig:** M02–M04, S01–S04, P02–P03 using a bench
  supply where possible.
- **Wave 4 — battery/mobile build:** S05–S06, P01 and K01 only after Waves 1–3
  pass.

This wave plan limits sunk cost if the board, microphone concept or motor driver
fails validation.

