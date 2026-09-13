#!/usr/bin/env python3
"""Standalone Raspberry Pi sensor monitor for Project ARIA.

This program intentionally has no ESP32, motor, encoder, driver, service, camera,
microphone, or audio control code.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


XSHUT_PINS = (22, 23, 24, 25)
TOF_ADDRESSES = (0x30, 0x31, 0x32, 0x33)
BNO_ADDRESS = 0x4A
BME_ADDRESS = 0x76
INA_ADDRESS = 0x40


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def error_text(exc: BaseException) -> str:
    text = str(exc).strip()
    return f"{type(exc).__name__}: {text}" if text else type(exc).__name__


class SensorMonitor:
    def __init__(self, *, tof_timeout: float = 0.25) -> None:
        self.tof_timeout = tof_timeout
        self.i2c: Any = None
        self.xshut: list[Any] = []
        self.tof: list[Any | None] = [None] * len(TOF_ADDRESSES)
        self.bme: Any = None
        self.bno: Any = None
        self.ina: Any = None
        self.init_errors: dict[str, str] = {}

    def initialize(self) -> None:
        """Initialize the shared Pi I2C bus and every sensor independently."""
        try:
            import board

            self.i2c = board.I2C()
        except Exception as exc:
            detail = error_text(exc)
            self.init_errors["i2c"] = detail
            for name in ("tof1", "tof2", "tof3", "tof4", "bme280", "bno085", "ina260"):
                self.init_errors[name] = f"I2C unavailable: {detail}"
            return

        self._initialize_bno()
        self._initialize_bme()
        self._initialize_ina()
        self._initialize_tof()

    def _initialize_tof(self) -> None:
        try:
            import adafruit_vl53l1x
            from gpiozero import DigitalOutputDevice

            for pin in XSHUT_PINS:
                self.xshut.append(
                    DigitalOutputDevice(pin, active_high=True, initial_value=False)
                )
        except Exception as exc:
            detail = error_text(exc)
            for index in range(len(TOF_ADDRESSES)):
                self.init_errors[f"tof{index + 1}"] = f"XSHUT setup failed: {detail}"
            return

        for pin in self.xshut:
            pin.off()
        time.sleep(0.20)

        for index, (pin, address) in enumerate(zip(self.xshut, TOF_ADDRESSES)):
            name = f"tof{index + 1}"
            try:
                pin.on()
                time.sleep(0.15)
                sensor = adafruit_vl53l1x.VL53L1X(self.i2c, address=0x29)
                sensor.set_address(address)
                sensor.distance_mode = 2
                sensor.timing_budget = 100
                sensor.start_ranging()
                self.tof[index] = sensor
            except Exception as exc:
                self.init_errors[name] = error_text(exc)
                self.tof[index] = None
                # Prevent a failed device remaining at 0x29 from colliding with
                # the next VL53L1X brought out of shutdown.
                try:
                    pin.off()
                except Exception:
                    pass

    def _initialize_bme(self) -> None:
        try:
            from adafruit_bme280 import basic

            self.bme = basic.Adafruit_BME280_I2C(self.i2c, address=BME_ADDRESS)
        except Exception as exc:
            self.init_errors["bme280"] = error_text(exc)

    def _initialize_bno(self) -> None:
        try:
            from adafruit_bno08x import BNO_REPORT_ACCELEROMETER
            from adafruit_bno08x.i2c import BNO08X_I2C

            self.bno = BNO08X_I2C(self.i2c, address=BNO_ADDRESS)
            self.bno.enable_feature(BNO_REPORT_ACCELEROMETER)
        except Exception as exc:
            self.init_errors["bno085"] = error_text(exc)
            self.bno = None

    def _initialize_ina(self) -> None:
        try:
            import adafruit_ina260

            self.ina = adafruit_ina260.INA260(self.i2c, address=INA_ADDRESS)
        except Exception as exc:
            self.init_errors["ina260"] = error_text(exc)

    def _unavailable(self, name: str) -> dict[str, Any]:
        return {
            "status": "error",
            "error": self.init_errors.get(name, "not initialized"),
        }

    def read_tof(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any] | None] = [None] * len(self.tof)
        pending = {index for index, sensor in enumerate(self.tof) if sensor is not None}

        for index, sensor in enumerate(self.tof):
            if sensor is None:
                results[index] = self._unavailable(f"tof{index + 1}")

        deadline = time.monotonic() + self.tof_timeout
        first_poll = True
        while pending and (first_poll or time.monotonic() < deadline):
            first_poll = False
            for index in tuple(pending):
                sensor = self.tof[index]
                try:
                    if not sensor.data_ready:
                        continue
                    distance_cm = sensor.distance
                    sensor.clear_interrupt()
                    if distance_cm is None:
                        results[index] = {"status": "no_data", "distance_mm": None}
                    else:
                        results[index] = {
                            "status": "ok",
                            "distance_mm": round(float(distance_cm) * 10.0, 1),
                        }
                    pending.remove(index)
                except Exception as exc:
                    results[index] = {"status": "error", "error": error_text(exc)}
                    pending.remove(index)
            if pending:
                time.sleep(0.005)

        for index in pending:
            results[index] = {"status": "timeout", "distance_mm": None}

        return [result for result in results if result is not None]

    def read_bme(self) -> dict[str, Any]:
        if self.bme is None:
            return self._unavailable("bme280")
        try:
            return {
                "status": "ok",
                "temperature_c": round(float(self.bme.temperature), 2),
                "humidity_percent": round(float(self.bme.relative_humidity), 1),
                "pressure_hpa": round(float(self.bme.pressure), 1),
            }
        except Exception as exc:
            return {"status": "error", "error": error_text(exc)}

    def read_bno(self) -> dict[str, Any]:
        if self.bno is None:
            return self._unavailable("bno085")
        try:
            acceleration = self.bno.acceleration
            if acceleration is None or any(value is None for value in acceleration):
                return {"status": "no_data", "acceleration_m_s2": None}
            return {
                "status": "ok",
                "acceleration_m_s2": {
                    axis: round(float(value), 3)
                    for axis, value in zip(("x", "y", "z"), acceleration)
                },
            }
        except Exception as exc:
            return {"status": "error", "error": error_text(exc)}

    def read_ina(self) -> dict[str, Any]:
        if self.ina is None:
            return self._unavailable("ina260")
        try:
            return {
                "status": "ok",
                "voltage_v": round(float(self.ina.voltage), 3),
                "current_a": round(float(self.ina.current) / 1000.0, 4),
                "power_w": round(float(self.ina.power) / 1000.0, 3),
            }
        except Exception as exc:
            return {"status": "error", "error": error_text(exc)}

    def sample(self) -> dict[str, Any]:
        sample = {
            "timestamp": utc_timestamp(),
            "tof": self.read_tof(),
            "bme280": self.read_bme(),
            "bno085": self.read_bno(),
            "ina260": self.read_ina(),
        }
        statuses = [item["status"] for item in sample["tof"]]
        statuses.extend(sample[name]["status"] for name in ("bme280", "bno085", "ina260"))
        sample["status"] = "ok" if all(status == "ok" for status in statuses) else "degraded"
        return sample

    def cleanup(self) -> None:
        for sensor in self.tof:
            if sensor is not None:
                try:
                    sensor.stop_ranging()
                except Exception:
                    pass

        for pin in self.xshut:
            try:
                pin.off()
            except Exception:
                pass
            try:
                pin.close()
            except Exception:
                pass

        if self.i2c is not None and hasattr(self.i2c, "deinit"):
            try:
                self.i2c.deinit()
            except Exception:
                pass


def format_human(sample: dict[str, Any]) -> str:
    def unavailable(label: str, reading: dict[str, Any]) -> str:
        text = f"{label}={reading['status']}"
        if "error" in reading:
            text += f":{reading['error']}"
        return text

    parts = [sample["timestamp"], f"overall={sample['status']}"]
    for index, tof in enumerate(sample["tof"], start=1):
        if tof["status"] == "ok":
            value = tof["distance_mm"]
            parts.append(f"ToF{index}=ok:{value:g}mm")
        else:
            parts.append(unavailable(f"ToF{index}", tof))

    bme = sample["bme280"]
    if bme["status"] == "ok":
        parts.append(
            "BME=ok:"
            f"{bme['temperature_c']:.2f}C,"
            f"{bme['humidity_percent']:.1f}%,"
            f"{bme['pressure_hpa']:.1f}hPa"
        )
    else:
        parts.append(unavailable("BME", bme))

    bno = sample["bno085"]
    if bno["status"] == "ok":
        acc = bno["acceleration_m_s2"]
        parts.append(f"BNO=ok:acc({acc['x']:+.3f},{acc['y']:+.3f},{acc['z']:+.3f})m/s2")
    else:
        parts.append(unavailable("BNO", bno))

    ina = sample["ina260"]
    if ina["status"] == "ok":
        parts.append(
            f"INA=ok:{ina['voltage_v']:.3f}V,"
            f"{ina['current_a']:.4f}A,{ina['power_w']:.3f}W"
        )
    else:
        parts.append(unavailable("INA", ina))
    return " | ".join(parts)


def positive_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def nonnegative_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read ARIA Pi sensors without ESP/motor control")
    parser.add_argument("--interval", type=positive_float, default=1.0, help="seconds between samples")
    parser.add_argument(
        "--tof-timeout",
        type=nonnegative_float,
        default=0.25,
        help="seconds to wait for each ToF sample",
    )
    parser.add_argument("--jsonl", action="store_true", help="emit one JSON object per line")
    parser.add_argument("--snapshot", type=Path, help="atomically replace latest JSON sample for local app")
    return parser.parse_args(argv)


def write_snapshot(path: Path, sample: dict) -> None:
    payload = json.dumps(sample, ensure_ascii=False, allow_nan=False)
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".sensor-", suffix=".tmp", delete=False) as stream:
            name = stream.name
            stream.write(payload)
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    monitor = SensorMonitor(tof_timeout=args.tof_timeout)
    print(
        "ARIA Pi sensors: 4x VL53L1X + BME280 + BNO085 + INA260 "
        "(no ESP/motor control)",
        file=sys.stderr,
        flush=True,
    )

    try:
        monitor.initialize()
        while True:
            started = time.monotonic()
            sample = monitor.sample()
            if args.snapshot:
                write_snapshot(args.snapshot, sample)
            if args.jsonl:
                print(json.dumps(sample, ensure_ascii=False, separators=(",", ":")), flush=True)
            else:
                print(format_human(sample), flush=True)
            remaining = args.interval - (time.monotonic() - started)
            if remaining > 0:
                time.sleep(remaining)
    except KeyboardInterrupt:
        print("\nStopped; cleaning up sensors.", file=sys.stderr, flush=True)
        return 0
    finally:
        monitor.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
