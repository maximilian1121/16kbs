#!/usr/bin/env python3

import sys

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
import os

from ffmpeg_utils import check_ffmpeg
from constants import APP_NAME
from ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    if os.path.isfile(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    if not check_ffmpeg():
        QMessageBox.critical(
            None,
            "Missing FFmpeg",
            "FFmpeg is not installed.\n\nsudo apt install ffmpeg",
        )
        sys.exit(1)

    window = MainWindow()
    window.show()

    if len(sys.argv) > 1:
        window._load_file(sys.argv[1])

    sys.exit(app.exec())


if __name__ == "__main__":
    main()