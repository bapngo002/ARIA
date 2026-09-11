import time
import threading
import serial
import socket
import os

import board
import adafruit_vl53l1x
import adafruit_bme280.basic as adafruit_bme280

from gpiozero import DigitalOutputDevice
from aria_av import AriaAV

from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_ROTATION_VECTOR,
)


# ============================================================
# ARIA CORE V0.6
#
# Raspberry Pi:
#   - 4x VL53L1X
#   - BME280
#   - BNO085
#
# ESP32-S3:
#   - 2 motors
#   - 2 AS5600
#   - heartbeat failsafe
# ============================================================

ESP_PORT = "/dev/ttyACM0"
ESP_BAUD = 115200

HEARTBEAT_INTERVAL = 0.1

# 4 ToF
XSHUT_PINS = [22, 23, 24, 25]
TOF_ADDRS = [0x30, 0x31, 0x32, 0x33]

BME_ADDR = 0x76
BNO_ADDR = 0x4A


class AriaCore:

    def __init__(self):

        self.running = True

        # ESP
        self.ser = None
        self.serial_lock = threading.Lock()

        # Pi I2C
        self.i2c = None

        # ToF
        self.xshut = []
        self.tof = [None, None, None, None]
        self.tof_mm = [None, None, None, None]

        # BME280
        self.bme = None
        self.temperature = None
        self.humidity = None
        self.pressure = None

        # BNO085
        self.bno = None
        self.acc = None
        self.gyro = None
        self.rot = None

        # CAMERA / MIC / AUDIO
        self.av = AriaAV()
        self.av_status = {
            "camera": False,
            "mic": False,
            "audio": False
        }


    # ========================================================
    # ESP
    # ========================================================

    def connect_esp(self):

        while self.running:

            try:

                print(
                    f"[CORE] Connecting ESP: {ESP_PORT}",
                    flush=True
                )

                self.ser = serial.Serial(
                    ESP_PORT,
                    ESP_BAUD,
                    timeout=0.05,
                    write_timeout=0.2
                )

                time.sleep(1)

                print(
                    "[CORE] ESP CONNECTED",
                    flush=True
                )

                return True

            except Exception as e:

                print(
                    f"[CORE] ESP unavailable: {e}",
                    flush=True
                )

                self.ser = None
                time.sleep(2)

        return False


    def close_esp(self):

        try:
            if self.ser:
                self.ser.close()
        except:
            pass

        self.ser = None


    def send_esp(self, data: bytes):

        if self.ser is None:
            return False

        try:

            with self.serial_lock:

                self.ser.write(data)
                self.ser.flush()

            return True

        except Exception as e:

            print(
                f"[CORE] ESP write error: {e}",
                flush=True
            )

            self.close_esp()

            return False


    # ========================================================
    # HEARTBEAT
    # ========================================================

    def heartbeat_loop(self):

        while self.running:

            if self.ser is None:

                self.connect_esp()

                time.sleep(0.1)

                continue

            self.send_esp(b"H")

            time.sleep(HEARTBEAT_INTERVAL)


    # ========================================================
    # ESP SERIAL RESPONSE
    # ========================================================

    def serial_loop(self):

        while self.running:

            if self.ser is None:

                time.sleep(0.1)

                continue

            try:

                line = self.ser.readline()

                if not line:
                    continue

                text = line.decode(
                    errors="ignore"
                ).strip()

                if text:

                    print(
                        f"[ESP] {text}",
                        flush=True
                    )

            except Exception as e:

                print(
                    f"[CORE] ESP read error: {e}",
                    flush=True
                )

                self.close_esp()

                time.sleep(1)


    # ========================================================
    # DRIVE
    # ========================================================

    def drive(self, command):

        command = command.upper()

        if command not in [
            "F",
            "B",
            "L",
            "R",
            "S",
            "+",
            "-"
        ]:
            return

        self.send_esp(
            command.encode()
        )


    # ========================================================
    # PI I2C
    # ========================================================

    def init_i2c(self):

        try:

            self.i2c = board.I2C()

            print(
                "[CORE] Pi I2C READY",
                flush=True
            )

            return True

        except Exception as e:

            print(
                f"[CORE] Pi I2C FAIL: {e}",
                flush=True
            )

            return False


    # ========================================================
    # BNO085
    # ========================================================

    def init_bno(self):

        self.bno = None

        for attempt in range(1, 4):

            try:

                print(
                    f"[CORE] BNO085 init attempt {attempt}/3",
                    flush=True
                )

                self.bno = BNO08X_I2C(
                    self.i2c,
                    address=BNO_ADDR
                )

                # BNO085 cần thời gian sau khi mở SHTP/I2C
                time.sleep(1.0)

                self.bno.enable_feature(
                    BNO_REPORT_ACCELEROMETER
                )

                time.sleep(0.25)

                self.bno.enable_feature(
                    BNO_REPORT_GYROSCOPE
                )

                time.sleep(0.25)

                self.bno.enable_feature(
                    BNO_REPORT_ROTATION_VECTOR
                )

                time.sleep(0.5)

                print(
                    "[CORE] BNO085 PASS @0x4A",
                    flush=True
                )

                return True

            except Exception as e:

                print(
                    f"[CORE] BNO085 attempt {attempt} FAIL: {e}",
                    flush=True
                )

                self.bno = None
                time.sleep(1.5)

        print(
            "[CORE] BNO085 DISABLED AFTER 3 FAILS",
            flush=True
        )

        return False


    def read_bno(self):

        if self.bno is None:
            return

        try:

            ax, ay, az = self.bno.acceleration

            gx, gy, gz = self.bno.gyro

            qi, qj, qk, qr = self.bno.quaternion

            self.acc = (
                ax,
                ay,
                az
            )

            self.gyro = (
                gx,
                gy,
                gz
            )

            self.rot = (
                qi,
                qj,
                qk,
                qr
            )

        except Exception as e:

            print(
                f"[BNO] read error: {e}",
                flush=True
            )


    # ========================================================
    # BME280
    # ========================================================

    def init_bme(self):

        try:

            self.bme = (
                adafruit_bme280.Adafruit_BME280_I2C(
                    self.i2c,
                    address=BME_ADDR
                )
            )

            print(
                "[CORE] BME280 PASS @0x76",
                flush=True
            )

        except Exception as e:

            self.bme = None

            print(
                f"[CORE] BME280 FAIL: {e}",
                flush=True
            )


    def read_bme(self):

        if self.bme is None:
            return

        try:

            self.temperature = (
                self.bme.temperature
            )

            self.humidity = (
                self.bme.relative_humidity
            )

            self.pressure = (
                self.bme.pressure
            )

        except Exception as e:

            print(
                f"[BME] read error: {e}",
                flush=True
            )


    # ========================================================
    # VL53L1X
    # ========================================================

    def init_tof(self):

        print(
            "[CORE] Init 4x VL53L1X...",
            flush=True
        )

        try:

            self.xshut = [
                DigitalOutputDevice(
                    pin,
                    active_high=True,
                    initial_value=False
                )
                for pin in XSHUT_PINS
            ]

        except Exception as e:

            print(
                f"[TOF] XSHUT FAIL: {e}",
                flush=True
            )

            return

        # shutdown tất cả ToF
        for pin in self.xshut:
            pin.off()

        time.sleep(0.2)

        # bật từng con và đổi address
        for i in range(4):

            try:

                self.xshut[i].on()

                time.sleep(0.15)

                sensor = (
                    adafruit_vl53l1x.VL53L1X(
                        self.i2c,
                        address=0x29
                    )
                )

                sensor.set_address(
                    TOF_ADDRS[i]
                )

                sensor.distance_mode = 2
                sensor.timing_budget = 100

                sensor.start_ranging()

                self.tof[i] = sensor

                print(
                    f"[TOF] S{i+1} PASS "
                    f"GPIO{XSHUT_PINS[i]} "
                    f"@0x{TOF_ADDRS[i]:02X}",
                    flush=True
                )

            except Exception as e:

                self.tof[i] = None

                print(
                    f"[TOF] S{i+1} FAIL: {e}",
                    flush=True
                )


    def read_tof(self):

        for i, sensor in enumerate(
            self.tof
        ):

            if sensor is None:

                self.tof_mm[i] = None

                continue

            try:

                if sensor.data_ready:

                    distance_cm = (
                        sensor.distance
                    )

                    sensor.clear_interrupt()

                    if distance_cm is None:

                        self.tof_mm[i] = None

                    else:

                        self.tof_mm[i] = int(
                            distance_cm * 10
                        )

            except Exception as e:

                print(
                    f"[TOF] S{i+1} error: {e}",
                    flush=True
                )

                self.tof_mm[i] = None


    # ========================================================
    # CAMERA / MIC / AUDIO
    # ========================================================

    def init_av(self):

        print(
            "[CORE] Checking CAMERA / MIC / AUDIO...",
            flush=True
        )

        self.av_status = self.av.check_all()

        print(
            f"[CORE] CAMERA {'PASS' if self.av_status['camera'] else 'FAIL'}",
            flush=True
        )

        print(
            f"[CORE] MIC    {'PASS' if self.av_status['mic'] else 'FAIL'}",
            flush=True
        )

        print(
            f"[CORE] AUDIO  {'PASS' if self.av_status['audio'] else 'FAIL'}",
            flush=True
        )


    # ========================================================
    # STATUS
    # ========================================================

    def status_loop(self):

        while self.running:

            self.read_tof()

            self.read_bme()

            self.read_bno()

            # ---------------- TOF ----------------

            tof_text = []

            for i, value in enumerate(
                self.tof_mm
            ):

                if value is None:

                    tof_text.append(
                        f"S{i+1}: ---"
                    )

                else:

                    tof_text.append(
                        f"S{i+1}:{value:4d}mm"
                    )

            # ---------------- BME ----------------

            if self.temperature is None:

                env_text = (
                    "TEMP:--- "
                    "HUM:--- "
                    "PRESS:---"
                )

            else:

                env_text = (
                    f"T:{self.temperature:.2f}C "
                    f"H:{self.humidity:.1f}% "
                    f"P:{self.pressure:.1f}hPa"
                )

            # ---------------- IMU ----------------

            if self.acc is None:

                acc_text = "ACC:---"

            else:

                ax, ay, az = self.acc

                acc_text = (
                    f"ACC "
                    f"{ax:+.2f},"
                    f"{ay:+.2f},"
                    f"{az:+.2f}"
                )


            if self.gyro is None:

                gyro_text = "GYRO:---"

            else:

                gx, gy, gz = self.gyro

                gyro_text = (
                    f"GYRO "
                    f"{gx:+.2f},"
                    f"{gy:+.2f},"
                    f"{gz:+.2f}"
                )


            if self.rot is None:

                rot_text = "ROT:---"

            else:

                qi, qj, qk, qr = self.rot

                rot_text = (
                    f"ROT "
                    f"{qi:+.3f},"
                    f"{qj:+.3f},"
                    f"{qk:+.3f},"
                    f"{qr:+.3f}"
                )


            print(
                "[CORE] "
                + " | ".join(tof_text)
                + " || "
                + env_text
                + " || "
                + acc_text
                + " || "
                + gyro_text
                + " || "
                + rot_text,
                flush=True
            )

            time.sleep(1)


    # ========================================================
    # KEYBOARD DRIVE TEST
    # ========================================================

    def keyboard_loop(self):

        print()
        print("DRIVE TEST")
        print("F = forward")
        print("B = backward")
        print("L = left")
        print("R = right")
        print("S = stop")
        print("+/- = speed")
        print("Q = quit")
        print()

        while self.running:

            try:

                cmd = input().strip()

            except EOFError:

                return

            if not cmd:
                continue

            cmd = cmd[0]

            if cmd.upper() == "Q":

                self.drive("S")

                self.running = False

                return

            self.drive(cmd)


    # ========================================================
    # LOCAL COMMAND SOCKET
    # ========================================================

    def command_server(self):

        sock_path = "/tmp/aria-core.sock"

        try:
            os.unlink(sock_path)
        except FileNotFoundError:
            pass

        server = socket.socket(
            socket.AF_UNIX,
            socket.SOCK_STREAM
        )

        server.bind(sock_path)
        server.listen(5)

        print(
            "[CORE] COMMAND SOCKET READY",
            flush=True
        )

        while self.running:

            try:
                conn, _ = server.accept()

                data = conn.recv(256)

                cmd = data.decode(
                    errors="ignore"
                ).strip().upper()

                response = "OK"

                if cmd in [
                    "F", "B", "L", "R",
                    "S", "+", "-"
                ]:

                    self.drive(cmd)

                    response = f"DRIVE {cmd} SENT"

                elif cmd == "CAM":

                    path="/home/aria/aria_camera.jpg"

                    ok = self.av.capture(path)

                    response = (
                        f"CAM PASS {path}"
                        if ok
                        else "CAM FAIL"
                    )

                elif cmd == "MIC":

                    path="/home/aria/aria_mic.wav"

                    ok = self.av.record(
                        path,
                        seconds=3
                    )

                    response = (
                        f"MIC PASS {path}"
                        if ok
                        else "MIC FAIL"
                    )

                elif cmd == "STATUS":

                    response = (
                        f"CAM={self.av_status['camera']} "
                        f"MIC={self.av_status['mic']} "
                        f"AUDIO={self.av_status['audio']} "
                        f"ESP={'ON' if self.ser else 'OFF'} "
                        f"BNO={'ON' if self.bno else 'OFF'}"
                    )

                else:

                    response = (
                        "UNKNOWN COMMAND"
                    )

                conn.sendall(
                    response.encode()
                )

                conn.close()

            except Exception as e:

                print(
                    f"[CORE] command error: {e}",
                    flush=True
                )

        try:
            server.close()
            os.unlink(sock_path)
        except:
            pass


    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        print()
        print("========================================")
        print("ARIA CORE V0.6")
        print("ESP DRIVE + ToF + BME280 + BNO085")
        print("========================================")

        # ------------------------------------------------
        # 1. PI SENSOR BUS FIRST
        # BNO085 được init trước mọi thread / ESP serial
        # ------------------------------------------------
        if self.init_i2c():

            self.init_bno()

            self.init_bme()

            self.init_tof()

        self.init_av()

        # ------------------------------------------------
        # 2. ESP AFTER PI SENSORS ARE READY
        # ------------------------------------------------
        self.connect_esp()

        threading.Thread(
            target=self.heartbeat_loop,
            daemon=True
        ).start()

        threading.Thread(
            target=self.serial_loop,
            daemon=True
        ).start()

        # ------------------------------------------------
        # 3. KEYBOARD DRIVE
        # ------------------------------------------------
        threading.Thread(
            target=self.keyboard_loop,
            daemon=True
        ).start()

        # ------------------------------------------------
        # 4. MAIN STATUS LOOP
        # ------------------------------------------------
        threading.Thread(
            target=self.command_server,
            daemon=True
        ).start()

        self.status_loop()


    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        self.running = False

        try:
            self.drive("S")
        except:
            pass

        self.close_esp()

        for sensor in self.tof:

            try:
                if sensor:
                    sensor.stop_ranging()
            except:
                pass

        for pin in self.xshut:

            try:
                pin.off()
                pin.close()
            except:
                pass


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    core = AriaCore()

    try:

        core.run()

    except KeyboardInterrupt:

        print()
        print("[CORE] STOP")

    finally:

        core.stop()
