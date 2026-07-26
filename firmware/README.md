# ARIA firmware

This directory owns the `ARIA-MCU-001` real-time and safety firmware.

Its responsibilities are limited to:

- closed-loop motor control;
- encoder, IMU, ToF, bumper, and power-monitor acquisition;
- bounded motion commands and local safety interlocks;
- the framed UART protocol and heartbeat watchdog;
- safe startup, shutdown, and fault reporting.

AI, camera processing, speech, UI, and long-term memory do not run here.
Generated build output is not committed.
