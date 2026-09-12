import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).with_name("aria_sensors.py")
SPEC = importlib.util.spec_from_file_location("aria_sensors", MODULE_PATH)
aria_sensors = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(aria_sensors)


class FakeTof:
    def __init__(self, *, ready=True, distance=12.3):
        self.data_ready = ready
        self.distance = distance
        self.cleared = False
        self.stopped = False

    def clear_interrupt(self):
        self.cleared = True

    def stop_ranging(self):
        self.stopped = True


class FakePin:
    def __init__(self):
        self.off_called = False
        self.close_called = False

    def off(self):
        self.off_called = True

    def close(self):
        self.close_called = True


class FakeI2C:
    def __init__(self):
        self.deinit_called = False

    def deinit(self):
        self.deinit_called = True


class SensorMonitorTests(unittest.TestCase):
    def test_tof_converts_centimetres_to_millimetres(self):
        monitor = aria_sensors.SensorMonitor(tof_timeout=0)
        sensors = [FakeTof(distance=value) for value in (1.0, 12.3, 45.67, 100.0)]
        monitor.tof = sensors

        result = monitor.read_tof()

        self.assertEqual([item["distance_mm"] for item in result], [10.0, 123.0, 456.7, 1000.0])
        self.assertTrue(all(sensor.cleared for sensor in sensors))

    def test_tof_none_and_timeout_are_not_reported_as_zero(self):
        monitor = aria_sensors.SensorMonitor(tof_timeout=0)
        monitor.tof = [FakeTof(distance=None), FakeTof(ready=False), None, None]
        monitor.init_errors["tof3"] = "missing"
        monitor.init_errors["tof4"] = "missing"

        result = monitor.read_tof()

        self.assertEqual(result[0], {"status": "no_data", "distance_mm": None})
        self.assertEqual(result[1], {"status": "timeout", "distance_mm": None})
        self.assertEqual(result[2]["status"], "error")
        self.assertNotIn("distance_mm", result[2])

    def test_sample_is_degraded_when_any_sensor_is_not_ok(self):
        monitor = aria_sensors.SensorMonitor(tof_timeout=0)
        monitor.tof = [FakeTof() for _ in range(4)]
        monitor.bme = type("BME", (), {
            "temperature": 26.7,
            "relative_humidity": 71.0,
            "pressure": 948.9,
        })()
        monitor.bno = type("BNO", (), {"acceleration": (0.1, 0.2, -10.16)})()
        monitor.init_errors["ina260"] = "offline"

        sample = monitor.sample()

        self.assertEqual(sample["status"], "degraded")
        self.assertEqual(sample["ina260"]["status"], "error")

    def test_cleanup_stops_tof_and_releases_gpio_and_i2c(self):
        monitor = aria_sensors.SensorMonitor()
        sensors = [FakeTof() for _ in range(4)]
        pins = [FakePin() for _ in range(4)]
        i2c = FakeI2C()
        monitor.tof = sensors
        monitor.xshut = pins
        monitor.i2c = i2c

        monitor.cleanup()

        self.assertTrue(all(sensor.stopped for sensor in sensors))
        self.assertTrue(all(pin.off_called and pin.close_called for pin in pins))
        self.assertTrue(i2c.deinit_called)


if __name__ == "__main__":
    unittest.main()
