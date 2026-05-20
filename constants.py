# =========================================================
# constants.py
# quality presets and app-wide constants
# =========================================================
#
# preset tuple layout:
#   (label, video_bitrate, audio_bitrate, image_qv,
#    video_scale, video_fps, audio_hz, description)
#
# image_qv: ffmpeg -q:v, lower = better quality (1-31)
# =========================================================

APP_NAME = "16kbs.py"
APP_SUBTITLE = "weaponized compression technology"

QUALITY_PRESETS = [
    (
        "Potato",
        "8k", "4k", 31,
        "160:-2", 10, 8000,
        "slideshow from a fever dream",
    ),
    (
        "16kbps Classic",
        "16k", "8k", 24,
        "360:-2", 15, 22050,
        "the original suffering",
    ),
    (
        "Dial-up",
        "32k", "16k", 20,
        "480:-2", 20, 22050,
        "1998 called, it wants its bandwidth back",
    ),
    (
        "Mildly Cursed",
        "96k", "32k", 10,
        "640:-2", 24, 44100,
        "questionable but watchable",
    ),
    (
        "Acceptable",
        "512k", "96k", 4,
        "1280:-2", 30, 44100,
        "your mom could tell the difference",
    ),
    (
        "Decent",
        "2M", "192k", 2,
        "1920:-2", 30, 48000,
        "almost respectable",
    ),
]

DEFAULT_PRESET_INDEX = 1  # 16kbps Classic

AUDIO_FORMATS = ["mp3", "ogg", "aac", "opus"]

AUDIO_CODEC_MAP = {
    "mp3":  "libmp3lame",
    "ogg":  "libvorbis",
    "aac":  "aac",
    "opus": "libopus",
}

IMAGE_FORMATS = ["jpg", "png", "webp", "bmp"]
