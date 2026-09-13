import io
import json
import os
import sys
import tempfile
import threading
import unittest
import struct
import wave
from unittest.mock import patch
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aria_app import Server
from aria_assistant import AppError, Assistant, Providers, Store, telemetry
from aria_voice import Voice
from aria_sensors import write_snapshot, positive_float, nonnegative_float


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def wait(self, app):
        app.worker.join(3)
        self.assertFalse(app.busy())

    def test_memory_persists_only_explicit_saves(self):
        app = Assistant(self.store)
        app.start("Mấy giờ rồi?")
        self.wait(app)
        self.assertIn("Bây giờ", app.history[-1]["content"])
        self.store.add("Tôi thích cà phê")
        fresh = Assistant(Store(self.temp.name))
        self.assertEqual(fresh.history, [])
        self.assertEqual(fresh.store.memories()[0]["text"], "Tôi thích cà phê")
        app.change("forget", {"id": self.store.memories()[0]["id"]})
        self.assertEqual(app.history, [])
        self.assertEqual(self.store.memories(), [])

    def test_configuration_and_memory_limits(self):
        for values in ({"provider":"other"}, {"speak":1}, {"shell":"echo test"}):
            with self.assertRaises(AppError):
                self.store.configure(values)
        for _ in range(30):
            self.store.add("ghi nhớ")
        with self.assertRaises(AppError):
            self.store.add("vượt giới hạn")

    def test_unconfigured_ai_does_not_fake_reply(self):
        self.store.configure({"provider":"openai"})
        app = Assistant(self.store, Providers(env={}))
        app.start("Xin chào")
        self.wait(app)
        self.assertEqual(app.state, "error")
        self.assertIn("chưa được cấu hình", app.error)
        self.assertFalse(app.history)

    def test_cancel_discards_late_reply_and_blocks_parallel_turn(self):
        entered, release = threading.Event(), threading.Event()
        class Slow(Providers):
            def reply(self, *_):
                entered.set()
                release.wait(3)
                return "late reply"
        self.store.configure({"provider":"openai"})
        app = Assistant(self.store, Slow(env={}))
        app.start("hello")
        self.assertTrue(entered.wait(2))
        try:
            app.change("cancel", {})
            with self.assertRaises(AppError):
                app.start("second")
            with self.assertRaises(AppError):
                app.change("remember", {"text":"new"})
        finally:
            release.set()
        self.wait(app)
        self.assertEqual(app.history, [])
        self.assertEqual(app.state, "idle")

    def test_provider_wire_formats_and_no_tool_execution(self):
        requests = []
        def opener(request, **kwargs):
            body = json.loads(request.data)
            requests.append((request.full_url, body))
            if "openai" in request.full_url:
                return io.BytesIO(json.dumps({"status":"completed", "output":[
                    {"type":"function_call","name":"drive","arguments":"{}"},
                    {"type":"message","content":[{"type":"output_text","text":"Xin chào"}]}]}).encode())
            return io.BytesIO(json.dumps({"candidates":[{"finishReason":"STOP","content":{"parts":[
                {"text":"private thought", "thought":True}, {"text":"Chào bạn"}]}}]}).encode())
        providers = Providers({"OPENAI_API_KEY":"test", "ARIA_OPENAI_MODEL":"configured-model",
                               "GEMINI_API_KEY":"test", "ARIA_GEMINI_MODEL":"configured-model"}, opener)
        messages = [{"role":"user","content":"Chào"}, {"role":"assistant","content":"Xin chào"}]
        self.assertEqual(providers.reply("openai", messages, "persona"), "Xin chào")
        self.assertFalse(requests[0][1]["store"])
        self.assertNotIn("tools", requests[0][1])
        self.assertEqual(providers.reply("gemini", messages, "persona"), "Chào bạn")
        self.assertEqual(requests[1][1]["contents"][1]["role"], "model")

    def test_provider_errors_redacted_and_not_retried(self):
        calls = []
        def opener(request, **kwargs):
            calls.append(request)
            raise urllib.error.HTTPError(request.full_url, 429, "secret-test", {}, None)
        provider = Providers({"OPENAI_API_KEY":"secret-test", "ARIA_OPENAI_MODEL":"test"}, opener)
        with self.assertRaises(AppError) as error:
            provider.reply("openai", [], "test")
        self.assertNotIn("secret-test", str(error.exception))
        self.assertEqual(len(calls), 1)

    def test_bad_provider_payloads(self):
        for payload in (b"no json", b"{}", b'{"status":"incomplete"}', b"x" * 1048577):
            p = Providers({"OPENAI_API_KEY":"test", "ARIA_OPENAI_MODEL":"test"},
                          lambda *a, **k: io.BytesIO(payload))
            with self.assertRaises(AppError):
                p.reply("openai", [], "test")

    def test_stale_sensor_data_never_reported_fresh(self):
        path = Path(self.temp.name) / "sensors.json"
        for offset, expected in ((-30,"stale"),(30,"stale"),(0,"fresh")):
            path.write_text(json.dumps({"timestamp": (datetime.now(timezone.utc)+timedelta(seconds=offset)).isoformat()}))
            self.assertEqual(telemetry(path)["status"], expected)
        path.write_text('{"timestamp":"bad"}')
        self.assertEqual(telemetry(path)["status"], "unavailable")

    def test_atomic_snapshot_and_local_environment_reply(self):
        path = Path(self.temp.name) / "sensor.json"
        sample = {"timestamp": datetime.now(timezone.utc).isoformat(),
                  "bme280":{"status":"ok", "temperature_c":26.5, "humidity_percent":60}}
        write_snapshot(path, sample)
        app = Assistant(self.store, sensor_path=path)
        app.start("Nhiệt độ")
        self.wait(app)
        self.assertIn("26.5°C", app.history[-1]["content"])
        sample["bme280"]["temperature_c"] = float('nan')
        with self.assertRaises(ValueError):
            write_snapshot(path, sample)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["bme280"]["temperature_c"], 26.5)
        self.assertFalse(list(path.parent.glob('.sensor-*.tmp')))
        for value in ('nan','inf','-inf'):
            for validate in (positive_float, nonnegative_float):
                with self.assertRaises(Exception):
                    validate(value)

    def test_whisper_pipeline_downmix_and_temporary_cleanup(self):
        voice = Voice(self.temp.name, {"ARIA_CAPTURE_DEVICE":"plughw:CARD=Array,DEV=0",
                     "ARIA_WHISPER_BIN":"whisper-cli", "ARIA_WHISPER_MODEL":"test.bin"})
        commands = []
        def fake_run(args, *_args, **_kwargs):
            commands.append(args)
            if args[0] == 'arecord':
                with wave.open(args[-1], 'wb') as wav:
                    wav.setparams((2,2,16000,0,'NONE','not compressed'))
                    wav.writeframes(struct.pack('<hhhh',1000,-500,2000,0))
            else:
                with wave.open(args[args.index('-f')+1], 'rb') as wav:
                    self.assertEqual(wav.getnchannels(),1)
                    self.assertEqual(struct.unpack('<hh',wav.readframes(2)),(250,1000))
                Path(args[args.index('-of')+1]+'.txt').write_text('Xin chào',encoding='utf-8')
        with patch.object(voice,'availability',return_value={"listen":True}), patch.object(voice,'run',side_effect=fake_run):
            self.assertEqual(voice.listen(threading.Event()),'Xin chào')
        self.assertEqual(len(commands),2)
        self.assertFalse(list(Path(self.temp.name).glob('voice-*')))

    def test_voice_cancel_and_timeout_reap_child(self):
        voice = Voice(self.temp.name, {})
        with self.assertRaises(AppError):
            voice.run([sys.executable,"-c","import time; time.sleep(10)"], threading.Event(), .1)
        cancel = threading.Event()
        cancel.set()
        with self.assertRaises(AppError):
            voice.run([sys.executable,"-c","raise SystemExit(1)"], cancel, 1)


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.server = Server(("127.0.0.1",0), Assistant(Store(self.temp.name), Providers(env={})))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def test_ui_and_origin_guard(self):
        with urllib.request.urlopen(self.url) as response:
            self.assertIn("frame-ancestors 'none'", response.headers['Content-Security-Policy'])
            self.assertIn(b"ARIA", response.read())
        with urllib.request.urlopen(self.url + "/api/state") as response:
            state = json.load(response)
        for origin, token, status in (("https://evil.invalid",state["token"],403),
                                      (self.url,"wrong",403),(self.url,state["token"],200)):
            request = urllib.request.Request(self.url + "/api/remember", data=b'{"text":"hello"}',
                headers={"Content-Type":"application/json","Origin":origin,"X-ARIA-Token":token})
            try:
                with urllib.request.urlopen(request) as response:
                    actual = response.status
            except urllib.error.HTTPError as error:
                actual = error.code
                error.close()
            self.assertEqual(actual, status)
        self.assertEqual(len(self.server.assistant.store.memories()), 1)

    def test_no_arbitrary_files_or_commands(self):
        for path in ("/../aria_core.py", "/api/drive", "/assistant.sqlite3"):
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(self.url + path)
            self.assertEqual(error.exception.code, 404)
            error.exception.close()
        request = urllib.request.Request(self.url + "/api/drive", data=b'{}', headers={
            "Content-Type":"application/json","Origin":self.url,"X-ARIA-Token":self.server.token})
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(request)
        self.assertEqual(error.exception.code, 400)
        error.exception.close()


if __name__ == "__main__":
    unittest.main()
