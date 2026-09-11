#include <Arduino.h>
#include <Wire.h>
#include <SimpleFOC.h>

// =====================================================
// ARIA ESP32-S3 DRIVE V0.3
// 2x FIT1035 + 2x AS5600 + HEARTBEAT FAILSAFE
// BNO085 đã chuyển sang Raspberry Pi
// =====================================================

// MOTOR LEFT
#define L_IN1 15
#define L_IN2 16
#define L_IN3 17
#define L_EN  18

// MOTOR RIGHT
#define R_IN1 11
#define R_IN2 12
#define R_IN3 13
#define R_EN  14

// AS5600 LEFT
#define LEFT_SDA 38
#define LEFT_SCL 35

// AS5600 RIGHT
#define RIGHT_SDA 36
#define RIGHT_SCL 37

TwoWire I2C_LEFT  = TwoWire(0);
TwoWire I2C_RIGHT = TwoWire(1);

// ---------------- ENCODERS ----------------

MagneticSensorI2C sensorL = MagneticSensorI2C(AS5600_I2C);
MagneticSensorI2C sensorR = MagneticSensorI2C(AS5600_I2C);

// FIT1035 = 7 pole pairs
BLDCMotor motorL = BLDCMotor(7);
BLDCMotor motorR = BLDCMotor(7);

BLDCDriver3PWM driverL(
  L_IN1, L_IN2, L_IN3, L_EN
);

BLDCDriver3PWM driverR(
  R_IN1, R_IN2, R_IN3, R_EN
);

// ---------------- DRIVE ----------------

float driveSpeed = 8.0f;

enum DriveMode {
  DRIVE_STOP,
  DRIVE_FORWARD,
  DRIVE_BACKWARD,
  DRIVE_LEFT,
  DRIVE_RIGHT
};

DriveMode driveMode = DRIVE_STOP;

// ---------------- FAILSAFE ----------------

unsigned long lastHeartbeat = 0;

const unsigned long HEARTBEAT_TIMEOUT_MS = 500;

bool heartbeatSeen = false;
bool failsafeActive = false;


// =====================================================
// DRIVE TARGET
// =====================================================

void applyDrive() {

  switch (driveMode) {

    case DRIVE_FORWARD:
      motorL.target = driveSpeed;
      motorR.target = driveSpeed;
      break;

    case DRIVE_BACKWARD:
      motorL.target = -driveSpeed;
      motorR.target = -driveSpeed;
      break;

    case DRIVE_LEFT:
      motorL.target = driveSpeed * 0.45f;
      motorR.target = driveSpeed;
      break;

    case DRIVE_RIGHT:
      motorL.target = driveSpeed;
      motorR.target = driveSpeed * 0.45f;
      break;

    default:
      motorL.target = 0;
      motorR.target = 0;
      break;
  }
}


void forceStop() {

  driveMode = DRIVE_STOP;

  motorL.target = 0;
  motorR.target = 0;
}


// =====================================================
// SERIAL COMMANDS
// =====================================================

void handleSerial() {

  while (Serial.available()) {

    char c = Serial.read();

    switch (c) {

      case 'H':
      case 'h':

        lastHeartbeat = millis();
        heartbeatSeen = true;

        if (failsafeActive) {
          failsafeActive = false;
          Serial.println("HEARTBEAT RESTORED");
        }

        break;


      case 'F':
      case 'f':

        driveMode = DRIVE_FORWARD;
        applyDrive();

        Serial.printf(
          "FORWARD speed=%.2f\n",
          driveSpeed
        );

        break;


      case 'B':
      case 'b':

        driveMode = DRIVE_BACKWARD;
        applyDrive();

        Serial.printf(
          "BACKWARD speed=%.2f\n",
          driveSpeed
        );

        break;


      case 'L':
      case 'l':

        driveMode = DRIVE_LEFT;
        applyDrive();

        Serial.printf(
          "LEFT speed=%.2f\n",
          driveSpeed
        );

        break;


      case 'R':
      case 'r':

        driveMode = DRIVE_RIGHT;
        applyDrive();

        Serial.printf(
          "RIGHT speed=%.2f\n",
          driveSpeed
        );

        break;


      case 'S':
      case 's':
      case ' ':

        forceStop();

        Serial.println("STOP");

        break;


      case '+':

        driveSpeed += 2.0f;

        if (driveSpeed > 20.0f)
          driveSpeed = 20.0f;

        applyDrive();

        Serial.printf(
          "SPEED = %.2f\n",
          driveSpeed
        );

        break;


      case '-':

        driveSpeed -= 2.0f;

        if (driveSpeed < 2.0f)
          driveSpeed = 2.0f;

        applyDrive();

        Serial.printf(
          "SPEED = %.2f\n",
          driveSpeed
        );

        break;
    }
  }
}


// =====================================================
// HEARTBEAT FAILSAFE
// =====================================================

void checkHeartbeat() {

  if (!heartbeatSeen)
    return;

  if (
    !failsafeActive &&
    millis() - lastHeartbeat > HEARTBEAT_TIMEOUT_MS
  ) {

    forceStop();

    failsafeActive = true;

    Serial.println(
      "FAILSAFE STOP - HEARTBEAT LOST"
    );
  }
}


// =====================================================
// SETUP
// =====================================================

void setup() {

  Serial.begin(115200);
  delay(1500);

  Serial.println();
  Serial.println("==============================");
  Serial.println("ARIA ESP DRIVE V0.3");
  Serial.println("==============================");

  // Encoder buses
  I2C_LEFT.begin(
    LEFT_SDA,
    LEFT_SCL,
    400000
  );

  I2C_RIGHT.begin(
    RIGHT_SDA,
    RIGHT_SCL,
    400000
  );

  sensorL.init(&I2C_LEFT);
  sensorR.init(&I2C_RIGHT);

  Serial.println("AS5600 LEFT READY");
  Serial.println("AS5600 RIGHT READY");

  // Driver power
  driverL.voltage_power_supply = 12.0;
  driverR.voltage_power_supply = 12.0;

  driverL.voltage_limit = 3.0;
  driverR.voltage_limit = 3.0;

  driverL.init();
  driverR.init();

  // Motors
  motorL.linkSensor(&sensorL);
  motorR.linkSensor(&sensorR);

  motorL.linkDriver(&driverL);
  motorR.linkDriver(&driverR);

  motorL.controller =
    MotionControlType::velocity;

  motorR.controller =
    MotionControlType::velocity;

  motorL.voltage_limit = 3.0;
  motorR.voltage_limit = 3.0;

  motorL.velocity_limit = 20.0;
  motorR.velocity_limit = 20.0;

  motorL.voltage_sensor_align = 1.5;
  motorR.voltage_sensor_align = 1.5;

  // PID LOCKED - bản đã PASS
  motorL.PID_velocity.P = 0.15;
  motorL.PID_velocity.I = 1.0;
  motorL.PID_velocity.D = 0.0;

  motorR.PID_velocity.P = 0.15;
  motorR.PID_velocity.I = 1.0;
  motorR.PID_velocity.D = 0.0;

  motorL.PID_velocity.output_ramp = 500;
  motorR.PID_velocity.output_ramp = 500;

  motorL.LPF_velocity.Tf = 0.02;
  motorR.LPF_velocity.Tf = 0.02;

  motorL.foc_modulation =
    FOCModulationType::SpaceVectorPWM;

  motorR.foc_modulation =
    FOCModulationType::SpaceVectorPWM;

  Serial.println("MOTOR INIT");

  motorL.init();
  motorR.init();

  Serial.println("FOC ALIGN");

  motorL.initFOC();
  motorR.initFOC();

  forceStop();

  Serial.println("FOC READY");
  Serial.println("==============================");
}


// =====================================================
// LOOP
// =====================================================

void loop() {

  motorL.loopFOC();
  motorR.loopFOC();

  motorL.move();
  motorR.move();

  handleSerial();

  checkHeartbeat();
}
