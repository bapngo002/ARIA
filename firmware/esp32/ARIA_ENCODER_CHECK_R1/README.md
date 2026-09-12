# ARIA encoder check R1 v0.1.0

Diagnostic only for replacement YD-ESP32-S3 N16R8. Original Drive V0.3 remains untouched.

- Right AS5600: SDA GPIO4, SCL GPIO5, 3.3V logic/supply, common GND.
- Left encoder is owner-reported damaged: leave disconnected. GPIO8/9 are reserved for a later repaired left encoder; this sketch does not initialize them.
- Keep BOTH motor driver power inputs disconnected during upload, boot and testing. Software LOW does not guarantee EN state before setup or during reset.
- Drives EN18/14 and phase GPIO15/16/17/11/12/13 LOW; never enables drivers, PWM or FOC. Serial input is discarded.
- Uses only Arduino ESP32 core and Wire. Reads AS5600 status 0x0B and raw angle 0x0C/0x0D at address 0x36, 100kHz, 25ms bus timeout, 2 reports/second. No sensor configuration or OTP writes.
- `READ_ERROR` means transaction failure, not a diagnosis of which wire/component failed. `MD=1 ML=0 MH=0` means magnet detected without field warning; it is not an encoder accuracy or drive PASS.
- After upload, capture logs with motor power still absent. Gently rotate the right shaft by hand and check angle changes/wraps; save stationary and rotation observations. Do not use a serial `F` or old Pi drive service to test this sketch.

Build target: `esp32:esp32:esp32s3:FlashSize=16M,PSRAM=opi,USBMode=hwcdc,CDCOnBoot=cdc`.
Serial: native USB CDC, 115200. Pi port and installed tools must be identified before giving the upload command; do not assume `/dev/ttyACM0` belongs to this ESP.

Register reference: [ams OSRAM AS5600 datasheet](https://look.ams-osram.com/m/7059eac7531a86fd/original/AS5600-DS000365.pdf).

Runtime, upload, encoder health, physical EN levels and motion safety remain NOT VERIFIED until actual logs/tests. This diagnostic is not a replacement drive release.

## Build evidence — 2026-09-13

Local Arduino CLI compile completed successfully using installed `esp32:esp32` core **3.3.11**, with the FQBN above. Program size 326756 bytes; global variables 24304 bytes. Build/cache/temp artifacts were directed to `D:/UserData/ARIA/current-task/work/encoder-r1`. No upload command was run. This proves compilation only; Pi tools, USB port, installed firmware and encoder runtime remain to verify.
