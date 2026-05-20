# 16kbs

A PyQt6-based desktop application for aggressively compressing video, audio, and images to extremely low bitrates.

## Features

- **Multiple media support**: Video, audio, and image compression
- **Hardware acceleration**: Automatic detection of GPU encoders (NVENC, AMF, VideoToolbox, QSV, VAAPI)
- **Quality presets**: From "Potato" (8kbps video) to "Decent" (2Mbps video)
- **Drag and drop**: Drop files directly into the application
- **Dark mode UI**: Clean, minimal interface

## Requirements

- Python 3.10+
- PyQt6
- FFmpeg (system dependency)

## Installation

```bash
pip install PyQt6
```

## Usage

```bash
python -m 16kbs
```

Or run directly:

```bash
python __main__.py
```

## Quality Presets

| Preset         | Video Bitrate | Audio Bitrate | Description                              |
| -------------- | ------------- | ------------- | ---------------------------------------- |
| Potato         | 8kbps         | 4kbps         | Slideshow from a fever dream             |
| 16kbps Classic | 16kbps        | 8kbps         | The original suffering                   |
| Dial-up        | 32kbps        | 16kbps        | 1998 called, it wants its bandwidth back |
| Mildly Cursed  | 96kbps        | 32kbps        | Questionable but watchable               |
| Acceptable     | 512kbps       | 96kbps        | Your mom could tell the difference       |
| Decent         | 2Mbps         | 192kbps       | Almost respectable                       |
