#include <Arduino.h>
#include <Wire.h>

// ARIA encoder diagnostic R1 v0.1.0 -- NOT drive firmware.
// Keep motor power physically disconnected, including during reset/upload.
// Right AS5600: SDA4/SCL5. Failed left encoder must remain disconnected.
// No left bus, PWM, SimpleFOC, calibration, EEPROM writes or motion commands.
constexpr uint8_t kLeftEnable = 18;
constexpr uint8_t kRightEnable = 14;
constexpr uint8_t kPhasePins[] = {15, 16, 17, 11, 12, 13};
constexpr uint8_t kAddress = 0x36;
TwoWire rightBus(1);
bool busReady = false;

void holdLow(uint8_t pin) {
  digitalWrite(pin, LOW);
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}

bool readRegister(uint8_t reg, uint8_t *data, size_t count) {
  rightBus.beginTransmission(kAddress);
  rightBus.write(reg);  // Register pointer only; never writes register data.
  if (rightBus.endTransmission(false) != 0) return false;
  if (rightBus.requestFrom(kAddress, count, true) != count) {
    while (rightBus.available()) rightBus.read();
    return false;
  }
  for (size_t i = 0; i < count; ++i) data[i] = rightBus.read();
  return true;
}

void setup() {
  holdLow(kLeftEnable);
  holdLow(kRightEnable);
  for (uint8_t pin : kPhasePins) holdLow(pin);
  Serial.begin(115200);
  busReady = rightBus.begin(4, 5, 100000);
  rightBus.setTimeOut(25);
}

void loop() {
  digitalWrite(kLeftEnable, LOW);
  digitalWrite(kRightEnable, LOW);
  // Never interpret serial input as motion commands; bound input work per loop.
  for (uint8_t i = 0; i < 64 && Serial.available(); ++i) Serial.read();
  static uint32_t lastReport = 0;
  if (millis() - lastReport < 500) return;
  lastReport = millis();
  // Repeat identification so late serial connections also identify the build.
  Serial.print("ARIA_ENCODER_CHECK_R1 v0.1.0 RIGHT SDA=4 SCL=5 EN_L=0 EN_R=0 ");
  if (!busReady) {
    Serial.println("I2C_INIT_ERROR");
    return;
  }
  uint8_t status = 0;
  uint8_t angle[2] = {0, 0};
  if (!readRegister(0x0B, &status, 1) || !readRegister(0x0C, angle, 2)) {
    Serial.println("READ_ERROR addr=0x36");
    return;
  }
  const uint16_t raw = ((uint16_t(angle[0]) << 8) | angle[1]) & 0x0FFF;
  const bool detected = (status & 0x20) != 0;
  const bool weak = (status & 0x10) != 0;
  const bool strong = (status & 0x08) != 0;
  Serial.printf("status=0x%02X MD=%u ML=%u MH=%u raw=%u deg=%.2f magnet=%s\n",
                unsigned(status), unsigned(detected), unsigned(weak), unsigned(strong),
                unsigned(raw), raw * (360.0 / 4096.0),
                detected && !weak && !strong ? "DETECTED" : "CHECK");
}
