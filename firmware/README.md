# ARIA firmware

The board ordered as inventory item 16 is identified as the 44-pin, dual-USB-C YD-ESP32-S3 with an ESP32-S3-WROOM-1-N16R8 module. The supplied pinout places the onboard RGB LED on GPIO48.

Firmware may target this YD board family for development, but production pin assignments and external power behavior must not be frozen until the delivered PCB/revision is checked against [`docs/ARIA-BOM-001.md`](../docs/ARIA-BOM-001.md). Generated build output is not committed.

Power-sensing documentation and future firmware comments must use INA260, as specified in the canonical BOM. No sensor driver implementation is currently present in this directory.
