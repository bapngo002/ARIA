ARIA STACK R3 — CONCEPT FOR SOLIDWORKS VIEWING

Open ARIA_STACK_R3_ASSEMBLED_CONCEPT.step or ARIA_STACK_R3_EXPLODED_CONCEPT.step in SolidWorks (File > Open > STEP). Native FreeCAD sources are also provided. Native SLDPRT export was not verified because the installed SolidWorks COM startup did not return; no claim of successful SolidWorks import is made.

Units: mm. Base outline: 70 x 100, confirmed by user. Overall assembled concept envelope: approximately 70 x 120 x 79.6; the additional length is ESP antenna overhang. Layer elevations 0 / 30 / 60 are design assumptions, NOT selected standoff heights. Module blocks, connectors and cooler are representative envelopes, NOT dimensionally validated library parts. The Pi nominal outline and ESP nominal outline are used for illustration, not footprint release. No mounting-hole coordinates are released. The rear Pi support scheme is deliberately incomplete pending actual mounting geometry.

Green: carrier/board. Black: ESP, driver or ground bank. Purple: amplifier. Orange: power-module placeholder. Blue: INA260 or sensor connector. Front banks are physically adjacent but electrically distinct: GND / VBAT / 5V / 3V3_PI / 3V3_ESP. These are not connector part selections or a circuit diagram.

The exploded model raises middle and top levels by 32 and 64 mm beyond their assembled positions. No motion, firmware changes, electrical continuity, thermal/EMI test or assembly-fit release has been performed. All exported shapes passed geometric validity checks; PNGs were visually reviewed. Geometry validity does not prove mechanical fit.

Functional mounts (display, camera, ToF, mic, IMU/environment, battery/motors/speakers) remain outside this electronics-stack concept. INA260 label is visible in the user photo; its arrival/use and wiring are not yet confirmed. Keep the burned board and suspect harness unpowered until incident checks.