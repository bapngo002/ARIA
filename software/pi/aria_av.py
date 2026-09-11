import subprocess


class AriaAV:

    def __init__(self):
        self.camera_ok = False
        self.mic_ok = False
        self.audio_ok = False

    def _run(self, cmd):
        try:
            r = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=8
            )
            return r.returncode, r.stdout
        except Exception as e:
            return -1, str(e)

    def check_camera(self):
        code, out = self._run(
            ["rpicam-hello", "--list-cameras"]
        )

        self.camera_ok = (
            code == 0
            and "imx708_wide_noir" in out.lower()
        )

        return self.camera_ok

    def check_mic(self):
        code, out = self._run(
            ["arecord", "-l"]
        )

        self.mic_ok = (
            code == 0
            and "respeaker xvf3800" in out.lower()
        )

        return self.mic_ok

    def check_audio(self):
        code, out = self._run(
            ["aplay", "-l"]
        )

        self.audio_ok = (
            code == 0
            and "max98357a" in out.lower()
        )

        return self.audio_ok

    def check_all(self):
        return {
            "camera": self.check_camera(),
            "mic": self.check_mic(),
            "audio": self.check_audio()
        }

    def capture(self, path="/tmp/aria_camera.jpg"):
        code, out = self._run([
            "rpicam-still",
            "-n",
            "-t", "500",
            "-o", path
        ])

        return code == 0

    def record(self, path="/tmp/aria_mic.wav", seconds=3):
        code, out = self._run([
            "arecord",
            "-D", "hw:1,0",
            "-f", "S16_LE",
            "-r", "16000",
            "-c", "2",
            "-d", str(seconds),
            path
        ])

        return code == 0

    def play(self, path):
        code, out = self._run([
            "pw-play",
            path
        ])

        return code == 0
