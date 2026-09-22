# Waveshare Infrared LED Board (B) — SKU 10670

## Decision

This is the **selected infrared illuminator model for ARIA**, intended as two boards placed to the left and right of the Raspberry Pi Camera Module 3 Wide NoIR.

- Manufacturer: Waveshare
- Product: Infrared LED Board (B)
- Manufacturer SKU: `10670`
- RobotShop SKU: `RB-Wav-09`
- IR emitter: 3 W, 850 nm
- Optical field of view: 100° per board
- ARIA design quantity: 2
- Repository status: selected CAD candidate; **not released for manufacture**
- Purchase status: no purchase evidence recorded in the canonical inventory

Official product reference: <https://www.waveshare.com/product/infrared-led-board-b.htm>

The screenshot [`robotshop-rb-wav-09-selection.png`](robotshop-rb-wav-09-selection.png) records the exact RobotShop listing selected by the project owner.

## CAD provenance

The user supplied `raspberry-pi-5mp-night-vision-camera-1.snapshot.1.zip`, SHA-256:

`63EA9A10E6D23304096D88A139792C1F82A79A3FB730A4E7C74A19EAEC5717F9`

The normalized component model was extracted from `Camera Module NVision Assem.STEP` in that archive. Its header identifies a SolidWorks 2018 STEP AP214 assembly dated 2018-10-12.

This is third-party CAD, not a manufacturer CAD release. The PCB outline, two-hole interface, reflector and photoresistor visually match official Waveshare 10670 product images. Dimensions below are read from the supplied CAD and were not inferred from photographs. A physical caliper check remains required before mechanical freeze.

## Coordinate system and dimensions

Units are millimetres. Origin is the minimum corner of the normalized component envelope: `X0 Y0 Z0`.

| Feature | CAD value |
|---|---|
| PCB and pad envelope | 28 × 20 × 2.1 |
| Complete assembled envelope | 28 × 20 × 15.1 |
| Mounting/power holes | 2 × Ø4 |
| Hole centres | (26, 3), (26, 17) |
| Hole pitch | 14 |
| LED optical axis | (10, 10) |
| Reflector cup | Ø19 × 14 high |
| Front lens maximum diameter | Ø19.435213 |
| Photoresistor axis | (20.650707, 16.807658) |
| Photoresistor body | Ø6 × 8 high |

## Power and wire-routing constraint

The board has no plug connector in this CAD. Waveshare specifies that the two mounting holes are used for both attachment and power on compatible Waveshare camera PCBs.

ARIA uses Raspberry Pi Camera Module 3 Wide NoIR, so its mounting holes must not be assumed to provide this powered interface. External wiring to the board pads, wire diameter, bend radius and strain relief remain assembly-level work and are not included in this component CAD.

## Files

- [`ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670.step`](ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670.step): normalized six-solid STEP model
- [`ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670.stl`](ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670.stl): 6,892-facet STL
- [`ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670_MOUNTING_2D.dxf`](ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670_MOUNTING_2D.dxf): board profile, mounting holes, LED and photoresistor references
- [`ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670_KEEPOUT.step`](ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670_KEEPOUT.step): 28 × 20 × 15.1 basic keep-out
- [`ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670.FCStd`](ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670.FCStd): editable FreeCAD file
- [`ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670_PREVIEW.png`](ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670_PREVIEW.png): preview
- [`ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670_validation.json`](ARIA-IR-001_Waveshare_Infrared_LED_Board_B_10670_validation.json): export validation and machine-readable dimensions

## Validation

- STEP re-import: 6 solids, envelope 28 × 20 × 15.1
- STL re-read: 6,892 facets, envelope 28 × 20 × 15.1
- DXF re-import: envelope 28 × 20

## SHA-256

| File | SHA-256 |
|---|---|
| `..._KEEPOUT.step` | `218FCFCDAFD5A48CA3DC877E8D4E019091B62036FDBFC70DBEF0A6B1A2068346` |
| `..._MOUNTING_2D.dxf` | `9DBAFA0270708AEA6220592EFBA8F8306B278EB1D038857707F9D3B514BE1850` |
| `..._PREVIEW.png` | `3A6EF02BD63ACE17F6E7885340E5AB86990662D1DC8503FC1E7C181CAB020323` |
| `..._validation.json` | `615CE4763F9461826B2D141B3DFD7DA677491647D9C3C656F4179E0E92DEFFE8` |
| `...10670.FCStd` | `F027C86CEDF64B58AF162C65CF0F52F160589BE60A899D7F4AE4B469783BAF00` |
| `...10670.step` | `DEC72E7C5FCF6C018DC6EBD0830F4F0A3010A900988AD393128B1DD4272E2CF3` |
| `...10670.stl` | `9559A9F4B88E002CD72693AFB25DD81B2ED26765E0FE738BCED166F676659000` |
| `robotshop-rb-wav-09-selection.png` | `8ED6BA02B1A2F292F104B424B50AC9871D6DDA216DE60E8FC0D65C061AA0A18D` |
