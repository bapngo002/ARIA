# ARIA component reference

| Field | Value |
|---|---|
| Document ID | ARIA-COMPONENT-REFERENCE-001 |
| Revision | A |
| Date | 2026-07-29 |
| Status | Engineering reference; not a procurement release |
| Identity authority | `ARIA-BOM-001.md` |
| Units | millimetres (mm), grams (g) |

This document adds mechanical and visual evidence to frozen component identities
in `ARIA-BOM-001.md`. It does not create, rename, or replace BOM identities. If
the documents disagree, the BOM controls identity and quantity, and the affected
mechanical record returns to `VALIDATION-HOLD`.

## Validation rules

- `VERIFIED`: the exact SKU/revision and manufacturer source support the data.
- `PARTIAL`: only part of the installed envelope, mass, mounting pattern, or
  connector clearance is verified.
- `VALIDATION-HOLD`: the exact SKU or mechanical evidence is missing or
  contradictory. No missing value is estimated.
- `X × Y × Z` is the installed rectangular envelope. Circular parts use `Ø`.
- An official product page is the image reference when no stable direct
  manufacturer image URL is available.
- IC package dimensions are never substituted for module dimensions.

## Frozen-component index

| ARIA ID | Exact BOM identity | Official image/reference | Verified X × Y × Z | Mass | Status |
|---|---|---|---:|---:|---|
| ARIA-CPU-001 | Raspberry Pi 5, 4 GB | [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-5/) | 85 × 56 × — | — | PARTIAL |
| ARIA-MCU-001 | Espressif ESP32-S3-DevKitC-1, N16R8 target | [Espressif](https://documentation.espressif.com/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html) | 62.74 × 25.40 × — | — | VALIDATION-HOLD |
| ARIA-THM-001 | Official Raspberry Pi Active Cooler | [Raspberry Pi](https://www.raspberrypi.com/products/active-cooler/) | 63.50 × 42.50 × 13.70 | — | VERIFIED |
| ARIA-CAM-001 | Raspberry Pi Camera Module 3 Wide NoIR | [Raspberry Pi](https://www.raspberrypi.com/products/camera-module-3/) | 25 × 24 × 12.4 | — | VERIFIED |
| ARIA-DSP-001 | Waveshare 4-inch DSI LCD (C), 720 × 720 touch | [Official image](https://www.waveshare.com/img/devkit/LCD/4inch-DSI-LCD-C/4inch-DSI-LCD-C-details-1.jpg) | 126 × 126 × 17 | — | PARTIAL |
| ARIA-STO-001 | High Endurance microSD, 64 GB, A2 | — exact SKU not frozen | — | — | VALIDATION-HOLD |
| ARIA-AUD-001 | reSpeaker XVF3800 USB 4-Mic Array | [Official image](https://files.seeedstudio.com/wiki/respeaker_xvf3800_usb/no-xiao-xvf.jpg) | 102 × 102 × 10 | — | PARTIAL |
| ARIA-AUD-002 | HP Pavilion 15/17 FX390R speaker set | — authoritative exact-product source unavailable | — | — | VALIDATION-HOLD |
| ARIA-AUD-003 | MAX98357A I2S amplifier module | — exact module SKU not frozen | — | — | VALIDATION-HOLD |
| ARIA-MOT-001 | DFRobot FIT1035, 2208 BLDC + AS5600 | [Official image](https://dfimg.dfrobot.com/enshop/image/data/FIT1035/FIT1035_Main_01_360x240.jpg.webp) | Ø28 × 27.5 axial body | — | PARTIAL |
| ARIA-MOT-002 | DFRobot SimpleFOCmini DRI0058 | [DFRobot](https://wiki.dfrobot.com/dri0058) | 26 × 21.5 × — | — | PARTIAL |
| ARIA-WHL-001 | Custom wheel, Ø60 × 18–20 | — custom ARIA part | Ø60 × 18–20 | — | VALIDATION-HOLD |
| ARIA-SEN-001 | VL53L1X carrier module | — exact carrier SKU not frozen | — | — | VALIDATION-HOLD |
| ARIA-SEN-002 | BNO085 breakout | — exact breakout SKU not frozen | — | — | VALIDATION-HOLD |
| ARIA-SEN-003 | SHT45 breakout | — exact breakout SKU not frozen | — | — | VALIDATION-HOLD |
| ARIA-PWR-001 | LiPo pouch, 3S, 8000–8500 mAh | — exact pack SKU not frozen | — | — | VALIDATION-HOLD |
| ARIA-PWR-002 | Enerkey EK-BM3r4S30A-NTC BMS | — verified manufacturer mechanical source unavailable | — | — | VALIDATION-HOLD |
| ARIA-PWR-003 | Pololu D24V90F5 | [Pololu](https://www.pololu.com/product/2866) | 40.6 × 20.3 × 7.6 | 4.8 | VERIFIED |
| ARIA-PWR-004 | Custom soft-latch; AO3401A control device | [AOS AO3401A](https://www.aosmd.com/products/mosfets/p-channel-mosfets-8v-60v/ao3401a) | custom assembly; device package unresolved | — | VALIDATION-HOLD |
| ARIA-PWR-005 | INA226 current/voltage monitor | — IC versus module form not frozen | — | — | VALIDATION-HOLD |
| ARIA-PWR-006 | Littelfuse Nano² 456 Series, “15 A” target | [Official datasheet](https://www.littelfuse.com/assetdocs/littelfuse_fuse_456_datasheet.pdf?assetguid=d86b18f9-14fa-4764-87ff-8aec12e9a89d) | — | — | VALIDATION-HOLD |
| ARIA-PWR-007 | SMBJ15A TVS diode | — manufacturer and polarity variant not frozen | — | — | VALIDATION-HOLD |
| ARIA-PWR-008 | Infineon IPT015N10N5 candidate | [Infineon](https://www.infineon.com/cms/en/product/power/mosfet/n-channel/ipt015n10n5/) | 11.88 × 10.58 × 2.40 max | — | PARTIAL |
| ARIA-UI-001 | 12 mm waterproof metal momentary LED-ring button | — exact SKU not frozen | — | — | VALIDATION-HOLD |

## Verified and partially verified records

### ARIA-CPU-001 — Raspberry Pi 5, 4 GB

- Image: [official product page](https://www.raspberrypi.com/products/raspberry-pi-5/).
- Envelope: 85 × 56 mm board outline. No consolidated maximum Z is published.
- Mounting: 4 × Ø2.7 holes; use coordinates from the official drawing.
- Keep-outs: USB-C, dual micro-HDMI, USB, Ethernet, camera/display FFC, fan,
  PCIe FFC, and 40-pin GPIO mating space. Cooler volume is ARIA-THM-001.
- Mass: not stated in the cited drawing.
- Sources: [mechanical drawing](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf),
  [product information portal](https://pip.raspberrypi.com/categories/892-raspberry-pi-5).
- Validation: `PARTIAL`; resolve installed Z from the official STEP and cooler
  assembly before chassis release.

### ARIA-MCU-001 — ESP32-S3-DevKitC-1, N16R8 target

- Image: [official user guide](https://documentation.espressif.com/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html).
- Envelope: 62.74 × 25.40 mm PCB; maximum assembled Z is not published.
- Mounting: no dedicated holes; retained through two 22-pin, 2.54 mm header rows
  or a custom carrier.
- Keep-outs: both USB connectors and boot/reset controls.
- Sources: [PCB layout drawing](https://dl.espressif.com/dl/PCB_ESP32-S3-DevKitC-1_V1_20210312CB.pdf),
  [user guide](https://documentation.espressif.com/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html).
- Validation: `VALIDATION-HOLD`; reconcile `N16R8` with the purchased module
  marking, board revision, and official order code.

### ARIA-THM-001 — Official Raspberry Pi Active Cooler

- Image: [official product page](https://www.raspberrypi.com/products/active-cooler/).
- Envelope: 63.50 × 42.50 × 13.70 mm.
- Mounting: two spring-loaded push pins; coordinates and travel are in the
  official drawing.
- Keep-outs: fan lead/header access and unobstructed intake/exhaust.
- Source: [mechanical drawing](https://datasheets.raspberrypi.com/cooling/raspberry-pi-active-cooler-mechanical-drawing.pdf).
- Validation: `VERIFIED` for the cooler envelope.

### ARIA-CAM-001 — Raspberry Pi Camera Module 3 Wide NoIR

- Image: [official product family page](https://www.raspberrypi.com/products/camera-module-3/).
- Envelope: 25 × 24 × 12.4 mm.
- Mounting: 4 × Ø2.2 holes; coordinates are in the Wide drawing.
- Keep-outs: 15-contact, 1 mm-pitch FPC tail, lens barrel, autofocus travel, and
  optical field. The cited assembly uses a 200 mm ribbon.
- Sources: [Wide mechanical drawing](https://datasheets.raspberrypi.com/camera/camera-module-3-wide-mechanical-drawing.pdf),
  [product page](https://www.raspberrypi.com/products/camera-module-3/).
- Validation: `VERIFIED`; purchase imagery must explicitly identify Wide NoIR.

### ARIA-DSP-001 — Waveshare 4-inch DSI LCD (C)

- Image: [official product image](https://www.waveshare.com/img/devkit/LCD/4inch-DSI-LCD-C/4inch-DSI-LCD-C-details-1.jpg).
- Envelope: 126 × 126 × 17 mm, corroborated for the exact product by the
  distributor source below.
- Mounting: reconcile hole coordinates from the official dimension image with
  local CAD before release.
- Keep-outs: rear DSI/power/touch connectors and cable bends. Supplied cable
  lengths vary from 50 to 200 mm by cable type.
- Mass: the store value 0.188 kg is not accepted as bare-display mass because
  its packaging scope is undefined.
- Sources: [product page](https://www.waveshare.com/product/4inch-dsi-lcd-c.htm),
  [dimension image](https://www.waveshare.com/img/devkit/LCD/4inch-DSI-LCD-C/4inch-DSI-LCD-C-details-size.jpg),
  [wiki](https://www.waveshare.com/wiki/4inch_DSI_LCD_%28C%29),
  [exact-product distributor](https://eckstein-shop.de/WaveShare-4inch-DSI-Round-Touch-Display-720-x-720-IPS-10-Point-Touch-EN).
- Validation: `PARTIAL`; mounting, connector protrusions, and bare mass remain.

### ARIA-AUD-001 — reSpeaker XVF3800 USB 4-Mic Array

- Image: [official product image](https://files.seeedstudio.com/wiki/respeaker_xvf3800_usb/no-xiao-xvf.jpg).
- Envelope: 102 × 102 × 10 mm.
- Mounting: exact hole geometry is not published in the cited catalogue.
- Keep-outs: USB-C, 3.5 mm audio, JST speaker, I2C/I2S headers, and open acoustic
  paths over all microphones.
- Sources: [introduction](https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/),
  [product PDF](https://files.seeedstudio.com/Bazaar/product_pdf/114993702.pdf).
- Validation: `PARTIAL`; verify board revision and mounting on CAD or sample.

### ARIA-MOT-001 — DFRobot FIT1035

- Image: [official product image](https://dfimg.dfrobot.com/enshop/image/data/FIT1035/FIT1035_Main_01_360x240.jpg.webp).
- Envelope: manufacturer states 27.5 × 28 mm, recorded as an Ø28 mm body with
  27.5 mm axial body length. This excludes the full shaft/cable swept envelope.
- Mounting: obtain shaft, bolt pattern, encoder board, and rear protrusions from
  official STP/dimension drawing.
- Keep-outs: GH1.25 4-pin encoder connector, phase leads, shaft/coupler, and
  rotating clearance.
- Sources: [product](https://www.dfrobot.com/product-3007.html),
  [wiki](https://wiki.dfrobot.com/fit1035/),
  [dimension image](https://dfimg.dfrobot.com/wiki/24282/FIT1035_2208-three-phase-bldc-motor_dimension_V1.0.png).
- Validation: `PARTIAL`; check imported official STP before fixing wheel centre.

### ARIA-MOT-002 — DFRobot SimpleFOCmini DRI0058

- Image: [official wiki](https://wiki.dfrobot.com/dri0058).
- Envelope: 26 × 21.5 mm PCB; maximum assembled Z is not published.
- Mounting: no verified mounting-hole geometry recorded.
- Keep-outs: power, motor phase, sensor, and control pins/terminals.
- Source: [official downloadable resources](https://wiki.dfrobot.com/dri0058).
- Validation: `PARTIAL`; resolve Z and protrusions from official STP.

### ARIA-PWR-003 — Pololu D24V90F5

- Image: [official product page](https://www.pololu.com/product/2866).
- Envelope: 40.6 × 20.3 × 7.6 mm.
- Mass: 4.8 g without included hardware.
- Mounting: 4 × Ø2.18 holes on 35.56 × 15.24 mm pattern.
- Keep-outs: 2.54 mm headers or optional 5 mm terminal blocks and wire strain
  relief at both ends.
- Sources: [specifications](https://www.pololu.com/product/2866/specs),
  [dimension drawing](https://www.pololu.com/file/0J1581/step-down-voltage-regulator-d24vxf5-dimensions.pdf),
  [product image](https://www.pololu.com/picture/view/0J5586).
- Validation: `VERIFIED`.

### ARIA-PWR-006 — Littelfuse Nano² 456 Series, “15 A” target

- Image: [official series datasheet](https://www.littelfuse.com/assetdocs/littelfuse_fuse_456_datasheet.pdf?assetguid=d86b18f9-14fa-4764-87ff-8aec12e9a89d).
- Dimensions, mounting, and mass: not assigned to the BOM target.
- Validation: `VALIDATION-HOLD — BOM CONFLICT`. The current datasheet lists
  20, 25, 30, and 40 A ratings, but no 15 A orderable part. Procurement and PCB
  footprint release are blocked until the BOM identity is reviewed.

### ARIA-PWR-008 — Infineon IPT015N10N5 candidate

- Image: [official product page](https://www.infineon.com/cms/en/product/power/mosfet/n-channel/ipt015n10n5/).
- Exact OPN: IPT015N10N5ATMA1; package PG-HSOF-8 / TOLL.
- Maximum envelope: 11.88 × 10.58 × 2.40 mm.
- Mounting: SMD, no chassis holes. Use manufacturer land pattern, thermal
  copper, solder-mask, and assembly courtyard.
- Sources: [datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-ipt015n10n5-datasheet-en.pdf),
  [product](https://www.infineon.com/cms/en/product/power/mosfet/n-channel/ipt015n10n5/).
- Validation: `PARTIAL`; package is verified, circuit/thermal approval remains.

## Validation-hold register

These frozen-spec identities do not yet define an exact purchasable mechanical
object. They intentionally have no guessed image or dimensions.

| ARIA ID | Evidence required to clear hold |
|---|---|
| ARIA-STO-001 | Manufacturer, series, and exact 64 GB order code |
| ARIA-AUD-002 | Authoritative FX390R listing with housing, connector, cable, and mounts |
| ARIA-AUD-003 | Exact MAX98357A module manufacturer/SKU |
| ARIA-WHL-001 | Released wheel drawing: hub, bore, fastener, material, and mass |
| ARIA-SEN-001 | Exact VL53L1X carrier manufacturer/SKU |
| ARIA-SEN-002 | Exact BNO085 breakout manufacturer/SKU |
| ARIA-SEN-003 | Exact SHT45 breakout manufacturer/SKU |
| ARIA-PWR-001 | Exact certified battery SKU, pouch, lead exit, connector, and mass |
| ARIA-PWR-002 | Trustworthy Enerkey drawing/datasheet or measured sample |
| ARIA-PWR-004 | Released soft-latch PCB and exact AO3401A manufacturer/order code |
| ARIA-PWR-005 | Decision between bare INA226 IC and exact carrier SKU |
| ARIA-PWR-007 | TVS manufacturer/order code and uni-/bidirectional variant |
| ARIA-UI-001 | Exact button SKU, depth, thread, terminals, voltage, and gasket |

## Scope and release gate

Open or design-only items without frozen commercial identities in the BOM are
outside this revision: caster, bumper, optional mmWave sensor, illumination,
charger, service disconnect, privacy switches, wiring, connectors, fasteners,
and custom mainboard.

This revision supports CAD research and procurement clarification only. It does
not authorize bulk purchasing, PCB fabrication, or chassis release. Every
`VALIDATION-HOLD` needs an exact SKU and cited dimensional evidence. Every
`PARTIAL` record must be reconciled with manufacturer CAD or a measured
production sample before it becomes a released mechanical constraint.
