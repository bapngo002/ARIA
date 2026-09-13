"""Opt-in local arecord -> whisper.cpp and Piper -> ALSA voice pipeline."""
import os
import shutil
import struct
import subprocess
import tempfile
import time
import wave
from pathlib import Path

from aria_assistant import AppError


class Voice:
    def __init__(self, directory, env=None):
        self.directory = Path(directory).resolve()
        self.env = os.environ if env is None else env

    def availability(self):
        e = self.env
        def exists(name):
            return bool(e.get(name) and Path(e[name]).is_file())
        return {"listen": bool(shutil.which("arecord") and e.get("ARIA_CAPTURE_DEVICE")
                               and exists("ARIA_WHISPER_BIN") and exists("ARIA_WHISPER_MODEL")),
                "speak": bool(shutil.which("aplay") and e.get("ARIA_PLAYBACK_DEVICE")
                              and exists("ARIA_PIPER_BIN") and exists("ARIA_PIPER_MODEL")
                              and Path(e["ARIA_PIPER_MODEL"] + ".json").is_file())}

    def run(self, args, cancel, timeout, input_text=None):
        if cancel.is_set():
            raise AppError("Đã dừng.")
        # Files prevent unbounded pipe buffering, and contain no persistent audio/logs.
        with tempfile.TemporaryFile(dir=self.directory) as incoming, tempfile.TemporaryFile(dir=self.directory) as output:
            if input_text is not None:
                incoming.write(input_text.encode("utf-8"))
                incoming.seek(0)
            try:
                process = subprocess.Popen(args, stdin=incoming, stdout=output, stderr=output,
                                           shell=False)
            except OSError:
                raise AppError("Không mở được chương trình âm thanh đã cấu hình.") from None
            deadline = time.monotonic() + timeout
            try:
                while process.poll() is None:
                    if cancel.wait(0.05):
                        raise AppError("Đã dừng.")
                    if time.monotonic() >= deadline:
                        raise AppError("Xử lý âm thanh quá thời gian cho phép.")
                if process.returncode:
                    raise AppError(f"Chương trình {Path(args[0]).name} trả lỗi {process.returncode}.")
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()

    def listen(self, cancel):
        if not self.availability()["listen"]:
            raise AppError("Chưa cấu hình micro/Whisper.")
        e = self.env
        with tempfile.TemporaryDirectory(dir=self.directory, prefix="voice-") as work:
            raw, mono, output = [str(Path(work) / name) for name in ("capture.wav", "mono.wav", "words")]
            self.run(["arecord", "-q", "-D", e["ARIA_CAPTURE_DEVICE"], "-f", "S16_LE",
                      "-r", "16000", "-c", "2", "-d", "5", "-t", "wav", raw], cancel, 10)
            with wave.open(raw, "rb") as source, wave.open(mono, "wb") as target:
                if (source.getsampwidth(), source.getnchannels(), source.getframerate()) != (2, 2, 16000):
                    raise AppError("Định dạng thu âm không đúng PCM16 stereo 16kHz.")
                target.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
                frames = 0
                while chunk := source.readframes(4096):
                    if len(chunk) % 4:
                        raise AppError("Bản thu WAV bị thiếu dữ liệu; hãy thử thu lại.")
                    frames += len(chunk) // 4
                    samples = struct.iter_unpack("<hh", chunk)
                    target.writeframes(b"".join(struct.pack("<h", int((l + r) / 2)) for l, r in samples))
                if not frames or frames != source.getnframes():
                    raise AppError("Bản thu WAV rỗng hoặc bị cắt ngang.")
            self.run([e["ARIA_WHISPER_BIN"], "-m", e["ARIA_WHISPER_MODEL"], "-f", mono,
                      "-l", "vi", "-otxt", "-of", output, "-nt"], cancel, 90)
            try:
                with open(output + ".txt", encoding="utf-8") as result:
                    text = result.read(2001).strip()
            except OSError:
                raise AppError("Whisper không tạo bản chép lời.") from None
            if not text:
                raise AppError("Chưa nghe rõ lời nói. Hãy thử lại.")
            return text

    def speak(self, text, cancel):
        if not self.availability()["speak"]:
            raise AppError("Đã có câu trả lời chữ; chưa cấu hình Piper và đầu ra loa.")
        e = self.env
        with tempfile.TemporaryDirectory(dir=self.directory, prefix="voice-") as work:
            output = str(Path(work) / "answer.wav")
            self.run([e["ARIA_PIPER_BIN"], "-m", e["ARIA_PIPER_MODEL"], "-f", output],
                     cancel, 90, input_text=text + "\n")
            self.run(["aplay", "-q", "-D", e["ARIA_PLAYBACK_DEVICE"], output], cancel, 120)
