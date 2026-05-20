import subprocess
from typing import NamedTuple


class Encoder(NamedTuple):
    name: str
    hwaccel: str | None
    extra_opts: list[str]

    @property
    def is_hardware(self) -> bool:
        return self.name != "libx264"

    def __str__(self) -> str:
        if self.is_hardware:
            return f"{self.name} via {self.hwaccel}"
        return f"{self.name} (software fallback)"


_HW_CANDIDATES: list[Encoder] = [
    Encoder("h264_nvenc",        "cuda",  ["-gpu", "any"]),
    Encoder("h264_amf",          "auto",  []),
    Encoder("h264_videotoolbox", "auto",  []),
    Encoder("h264_qsv",          "qsv",   []),
    Encoder("h264_vaapi",        "vaapi", ["-vaapi_device", "/dev/dri/renderD128"]),
    Encoder("h264_v4l2m2m",      None,    []),
]

_SW_FALLBACK = Encoder("libx264", None, [])


def _probe_encoder(enc: Encoder) -> bool:
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "nullsrc=s=64x64:r=1",
    ]
    if enc.hwaccel:
        cmd += ["-hwaccel", enc.hwaccel]
    if enc.name == "h264_vaapi":
        cmd += ["-vf", "format=nv12,hwupload"]
    cmd += ["-frames:v", "1", "-c:v", enc.name] + enc.extra_opts + ["-f", "null", "-"]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


def detect_hw_encoders() -> list[Encoder]:
    working = [enc for enc in _HW_CANDIDATES if _probe_encoder(enc)]
    working.append(_SW_FALLBACK)
    return working