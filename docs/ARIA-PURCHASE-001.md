# ARIA-PURCHASE-001 — Amazon/AliExpress Purchase Register

| Field | Value |
|---|---|
| Document ID | ARIA-PURCHASE-001 |
| Revision | A |
| Date | 2026-07-27 |
| Status | Search register; exact listings require verification |
| Authority | Component identity and quantity come only from ARIA-BOM-001 |

## Frozen purchasable components

| ARIA ID | Qty | Locked item | Amazon/AliExpress search text | Before order |
|---|---:|---|---|---|
| ARIA-CPU-001 | 1 | Raspberry Pi 5, 4 GB | `Raspberry Pi 5 4GB` | Confirm genuine board and revision |
| ARIA-MCU-001 | 1 | ESP32-S3-DevKitC-1, N16R8 target | `Espressif ESP32-S3 DevKitC-1 N16R8` | Confirm WROOM N16R8 marking and board dimensions |
| ARIA-THM-001 | 1 | Official Raspberry Pi Active Cooler | `Official Raspberry Pi 5 Active Cooler` | Confirm official Pi 5 part |
| ARIA-CAM-001 | 1 | Raspberry Pi Camera Module 3 Wide NoIR | `Raspberry Pi Camera Module 3 Wide NoIR` | Do not substitute standard, narrow, or IR-cut version |
| ARIA-DSP-001 | 1 | Waveshare 4-inch **round** DSI LCD (C), 720 × 720, 10-point touch, SKU 24603 | `Waveshare 4inch DSI Round LCD C 720x720 SKU 24603` | Confirm the round DSI model, SKU 24603, cables, rear carrier, and 4 × M4 mounting points; do not substitute a square DPI/HDMI model |
| ARIA-STO-001 | 1 | High Endurance microSD, 64 GB, A2 | `64GB High Endurance microSD A2` | Confirm endurance line and genuine seller |
| ARIA-AUD-001 | 1 | reSpeaker XVF3800 USB 4-Mic Array | `Seeed Studio ReSpeaker XVF3800 USB 4 Mic Array` | Confirm Seeed product/revision and USB version |
| ARIA-AUD-002 | 1 set | HP Pavilion 15/17 FX390R left/right speaker set | `HP FX390R laptop speaker left right` | Match seller photos to frozen geometry; measure impedance on receipt |
| ARIA-AUD-003 | 2 | MAX98357A I²S amplifier module | `MAX98357A I2S amplifier module` | Both modules must support channel selection and 5 V operation |
| ARIA-MOT-001 | 2 | DFRobot FIT1035 2208 BLDC with AS5600 | `DFRobot FIT1035 2208 BLDC AS5600` | Confirm integrated AS5600 and exact shaft/hub |
| ARIA-MOT-002 | 2 | DFRobot SimpleFOCmini DRI0058 | `DFRobot DRI0058 SimpleFOCmini` | Do not substitute an RC ESC |
| ARIA-WHL-001 | 2 | Custom wheel envelope Ø60 × 18–20 mm | `60mm rubber robot wheel 20mm wide` | Hub/transmission remains a CAD design item |
| ARIA-SEN-001 | 6 | VL53L1X ToF carrier module | `VL53L1X ToF distance sensor module` | Buy six identical carriers with XSHUT exposed |
| ARIA-SEN-002 | 1 | BNO085 IMU breakout | `BNO085 IMU breakout` | Confirm BNO085, not BNO055 |
| ARIA-SEN-003 | 1 | SHT45 temperature/humidity breakout | `Sensirion SHT45 I2C breakout` | Confirm genuine SHT45 and ventilation-compatible board |
| ARIA-PWR-001 | 1 | LiPo pouch pack, 3S, 8,000–8,500 mAh | `3S LiPo pouch 8000mAh balance lead` | Exact size, mass, C rating, connector, safety data, and charger must be approved |
| ARIA-PWR-002 | 1 | Enerkey EK-BM3r4S30A-NTC BMS | `Enerkey EK-BM3r4S30A NTC` | Verify authentic datasheet, 3S LiPo behavior, NTC, and dimensions |
| ARIA-PWR-003 | 1 | Pololu D24V90F5 5 V regulator | `Pololu D24V90F5` | Confirm genuine Pololu part |
| ARIA-PWR-005 | 1 | INA226 current/voltage monitor | `INA226 current voltage monitor module` | Exact module and shunt value must match the power design |
| ARIA-PWR-006 | 1 | Littelfuse Nano² 456 Series, 15 A | `Littelfuse Nano2 456 15A fuse` | Record the full Littelfuse part number and time-current curve |
| ARIA-PWR-007 | 1 | SMBJ15A TVS diode | `SMBJ15A TVS diode` | Confirm unidirectional/bidirectional suffix selected by schematic |
| ARIA-PWR-008 | 1 | Infineon IPT015N10N5 candidate MOSFET | `Infineon IPT015N10N5` | Exact suffix/package and N-channel topology must be approved first |
| ARIA-UI-001 | 1 | 12 mm metal momentary button with LED ring | `12mm metal momentary push button LED ring` | Momentary only; confirm LED voltage/color and body depth |

## Custom and unresolved items

Do not search for marketplace substitutes for these entries:

- `ARIA-PWR-004`: custom soft-latch circuit; AO3401A is the frozen
  low-current latch/control device, not the main pass MOSFET.
- `ARIA-BRD-001`: custom two-layer mainboard derived from the verified CAD
  assembly.
- Open bumper, mmWave, NoIR illumination, privacy-switch, caster, charger,
  service-disconnect, connector, harness, and fastener entries remain in the
  master BOM and are not frozen for purchase.

## Listing capture rule

For each actual order, add the exact URL, seller, price, listing screenshot or
revision date, selected option, and delivered part markings. A search phrase is
never proof that a listing is the correct component.
