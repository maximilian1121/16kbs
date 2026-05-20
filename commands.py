from encoders import Encoder
from constants import AUDIO_CODEC_MAP


def build_video_cmd(
    file_path: str,
    output_file: str,
    encoder: Encoder,
    vbr: str,
    abr: str,
    scale: str,
    fps: int,
    hz: int,
    grayscale: bool = False,
    denoise: bool = False,
    strip_audio: bool = False,
    mono: bool = True,
) -> list[str]:
    filters: list[str] = []

    if grayscale:
        filters.append("hue=s=0")

    if denoise:
        filters.append("hqdn3d=4:4:3:3")

    if encoder.name == "h264_vaapi":
        filters.append(f"format=nv12,hwupload,scale_vaapi={scale}")
        filters.append(f"fps={fps}")
    else:
        filters.append(f"scale={scale}")
        filters.append(f"fps={fps}")

    vf = ",".join(filters)

    cmd = ["ffmpeg", "-y"]

    if encoder.hwaccel:
        cmd += ["-hwaccel", encoder.hwaccel]

    if encoder.name == "h264_vaapi":
        cmd += ["-vaapi_device", "/dev/dri/renderD128"]

    cmd += ["-i", file_path, "-vf", vf, "-c:v", encoder.name]
    cmd += encoder.extra_opts
    cmd += ["-b:v", vbr, "-maxrate", vbr, "-bufsize", "64k"]

    if encoder.name == "libx264":
        cmd += ["-preset", "fast", "-pix_fmt", "yuv420p"]

    if strip_audio:
        cmd += ["-an"]
    else:
        channels = "1" if mono else "2"
        cmd += ["-c:a", "aac", "-b:a", abr, "-ac", channels, "-ar", str(hz)]

    cmd.append(output_file)
    return cmd


def build_audio_cmd(
    file_path: str,
    output_file: str,
    abr: str,
    hz: int,
    fmt: str = "mp3",
    mono: bool = True,
) -> list[str]:
    codec = AUDIO_CODEC_MAP.get(fmt, "libmp3lame")
    channels = "1" if mono else "2"

    return [
        "ffmpeg", "-y",
        "-i", file_path,
        "-c:a", codec,
        "-b:a", abr,
        "-ac", channels,
        "-ar", str(hz),
        output_file,
    ]


def build_image_cmd(
    file_path: str,
    output_file: str,
    qv: int,
    scale: str,
    grayscale: bool = False,
) -> list[str]:
    width = scale.split(":")[0]

    filters = [f"scale={width}:-1"]
    if grayscale:
        filters.append("hue=s=0")

    vf = ",".join(filters)

    return [
        "ffmpeg", "-y",
        "-i", file_path,
        "-vf", vf,
        "-q:v", str(qv),
        output_file,
    ]