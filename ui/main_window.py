import os
import shutil
import mimetypes

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QProgressBar,
    QFileDialog, QMessageBox, QSlider, QCheckBox,
    QComboBox, QGroupBox, QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
import os

from constants import (
    APP_NAME, APP_SUBTITLE,
    QUALITY_PRESETS, DEFAULT_PRESET_INDEX,
    AUDIO_FORMATS, IMAGE_FORMATS,
)
from workers import EncoderProbeWorker, FFmpegWorker
from commands import build_video_cmd, build_audio_cmd, build_image_cmd
from ui.stylesheet import STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(APP_NAME)
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.png")
        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setMinimumSize(960, 700)
        self.setAcceptDrops(True)

        self.worker: FFmpegWorker | None = None
        self.probe_worker: EncoderProbeWorker | None = None
        self.hw_encoders: list = []
        self.loaded_file: str | None = None
        self.last_output_file: str | None = None

        self._build_ui()
        self.setStyleSheet(STYLESHEET)

        self.log(f"{APP_NAME} ready.")
        self.log("Probing hardware encoders...")
        self.pick_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self._run_encoder_probe()

    def _run_encoder_probe(self) -> None:
        self.probe_worker = EncoderProbeWorker()
        self.probe_worker.done_signal.connect(self._on_probe_done)
        self.probe_worker.start()

    def _on_probe_done(self, encoders: list) -> None:
        self.hw_encoders = encoders
        self.probe_worker = None

        self.log("")
        self.log("Hardware encoder probe results:")
        for enc in encoders:
            tag = "[HW]" if enc.is_hardware else "[SW]"
            self.log(f"  {tag} {enc}")

        self.log("")
        self.log(f"Best encoder: {encoders[0].name}")
        self.log("Awaiting victims...")
        self.log("")

        self.pick_button.setEnabled(True)

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        title = QLabel(APP_NAME)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")

        picker_row = QHBoxLayout()
        picker_row.setSpacing(8)

        self.pick_button = QPushButton("Select File")
        self.pick_button.setObjectName("pickButton")
        self.pick_button.setMinimumHeight(44)
        self.pick_button.clicked.connect(self.pick_file)

        self.file_label = QLabel("no file loaded")
        self.file_label.setObjectName("fileLabel")
        self.file_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        picker_row.addWidget(self.pick_button)
        picker_row.addWidget(self.file_label)

        self.drop_label = QLabel("or drag and drop a file here")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setObjectName("dropLabel")

        options_group = QGroupBox("Options")
        options_group.setObjectName("optionsGroup")
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(10)

        slider_row = QHBoxLayout()

        quality_label = QLabel("Quality:")
        quality_label.setObjectName("optLabel")
        quality_label.setFixedWidth(60)

        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setMinimum(0)
        self.quality_slider.setMaximum(len(QUALITY_PRESETS) - 1)
        self.quality_slider.setValue(DEFAULT_PRESET_INDEX)
        self.quality_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.quality_slider.setTickInterval(1)
        self.quality_slider.setSingleStep(1)
        self.quality_slider.setObjectName("qualitySlider")
        self.quality_slider.valueChanged.connect(self._on_slider_changed)

        self.preset_name_label = QLabel()
        self.preset_name_label.setObjectName("presetName")
        self.preset_name_label.setFixedWidth(160)

        self.preset_desc_label = QLabel()
        self.preset_desc_label.setObjectName("presetDesc")

        slider_row.addWidget(quality_label)
        slider_row.addWidget(self.quality_slider)
        slider_row.addWidget(self.preset_name_label)

        tick_row = QHBoxLayout()
        tick_row.addSpacing(64)
        for preset in QUALITY_PRESETS:
            lbl = QLabel(preset[0])
            lbl.setObjectName("tickLabel")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tick_row.addWidget(lbl)
        tick_row.addSpacing(168)

        options_layout.addLayout(slider_row)
        options_layout.addLayout(tick_row)
        options_layout.addWidget(self.preset_desc_label)

        video_row = QHBoxLayout()
        video_row.setSpacing(16)

        video_label = QLabel("Video:")
        video_label.setObjectName("optLabel")
        video_label.setFixedWidth(60)

        self.opt_strip_audio = QCheckBox("Strip audio")
        self.opt_strip_audio.setObjectName("optCheck")

        self.opt_grayscale = QCheckBox("Grayscale")
        self.opt_grayscale.setObjectName("optCheck")

        self.opt_denoise = QCheckBox("Extra denoise (slower)")
        self.opt_denoise.setObjectName("optCheck")

        video_row.addWidget(video_label)
        video_row.addWidget(self.opt_strip_audio)
        video_row.addWidget(self.opt_grayscale)
        video_row.addWidget(self.opt_denoise)
        video_row.addStretch()

        audio_row = QHBoxLayout()
        audio_row.setSpacing(16)

        audio_label = QLabel("Audio:")
        audio_label.setObjectName("optLabel")
        audio_label.setFixedWidth(60)

        self.opt_mono = QCheckBox("Force mono")
        self.opt_mono.setChecked(True)
        self.opt_mono.setObjectName("optCheck")

        audio_fmt_label = QLabel("Format:")
        audio_fmt_label.setObjectName("optLabel")

        self.audio_format_combo = QComboBox()
        self.audio_format_combo.setObjectName("optCombo")
        self.audio_format_combo.addItems(AUDIO_FORMATS)

        audio_row.addWidget(audio_label)
        audio_row.addWidget(self.opt_mono)
        audio_row.addSpacing(16)
        audio_row.addWidget(audio_fmt_label)
        audio_row.addWidget(self.audio_format_combo)
        audio_row.addStretch()

        image_row = QHBoxLayout()
        image_row.setSpacing(16)

        image_label = QLabel("Image:")
        image_label.setObjectName("optLabel")
        image_label.setFixedWidth(60)

        self.opt_img_grayscale = QCheckBox("Grayscale")
        self.opt_img_grayscale.setObjectName("optCheck")

        image_fmt_label = QLabel("Format:")
        image_fmt_label.setObjectName("optLabel")

        self.image_format_combo = QComboBox()
        self.image_format_combo.setObjectName("optCombo")
        self.image_format_combo.addItems(IMAGE_FORMATS)

        image_row.addWidget(image_label)
        image_row.addWidget(self.opt_img_grayscale)
        image_row.addSpacing(16)
        image_row.addWidget(image_fmt_label)
        image_row.addWidget(self.image_format_combo)
        image_row.addStretch()

        options_layout.addLayout(video_row)
        options_layout.addLayout(audio_row)
        options_layout.addLayout(image_row)

        action_row = QHBoxLayout()
        action_row.setSpacing(8)

        self.compress_button = QPushButton("Compress")
        self.compress_button.setObjectName("compressButton")
        self.compress_button.setMinimumHeight(44)
        self.compress_button.clicked.connect(self._on_compress_clicked)

        self.export_button = QPushButton("Export to...")
        self.export_button.setObjectName("exportButton")
        self.export_button.setMinimumHeight(44)
        self.export_button.setToolTip("Save the last compressed output to a chosen location")
        self.export_button.clicked.connect(self._on_export_clicked)

        action_row.addWidget(self.compress_button, stretch=3)
        action_row.addWidget(self.export_button, stretch=1)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        self.progress.setObjectName("progress")

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.output.setFont(QFont("monospace", 10))

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addLayout(picker_row)
        root.addWidget(self.drop_label)
        root.addWidget(options_group)
        root.addLayout(action_row)
        root.addWidget(self.progress)
        root.addWidget(self.output)

        self._on_slider_changed(self.quality_slider.value())

    def _on_slider_changed(self, idx: int) -> None:
        preset = QUALITY_PRESETS[idx]
        self.preset_name_label.setText(preset[0])
        self.preset_desc_label.setText(f"  {preset[7]}")

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_label.setText("drop it like it's hot")
        else:
            event.ignore()

    def dragLeaveEvent(self, event) -> None:
        self.drop_label.setText("or drag and drop a file here")

    def dropEvent(self, event) -> None:
        self.drop_label.setText("or drag and drop a file here")
        urls = event.mimeData().urls()
        if urls:
            self._load_file(urls[0].toLocalFile())

    def pick_file(self) -> None:
        file, _ = QFileDialog.getOpenFileName(
            self, "Select media to absolutely flatten"
        )
        if file:
            self._load_file(file)

    def _load_file(self, path: str) -> None:
        if not os.path.isfile(path):
            QMessageBox.critical(self, "Error", "File does not exist.")
            return
        self.loaded_file = path
        self.file_label.setText(os.path.basename(path))
        self.log(f"Loaded: {path}")

    def _on_compress_clicked(self) -> None:
        if not self.loaded_file:
            QMessageBox.information(self, "No file", "Load a file first.")
            return
        self.process_file(self.loaded_file)

    def _on_export_clicked(self) -> None:
        if not self.last_output_file or not os.path.isfile(self.last_output_file):
            QMessageBox.information(
                self, "Nothing to export", "Compress something first, then export."
            )
            return

        ext = os.path.splitext(self.last_output_file)[1]
        dest, _ = QFileDialog.getSaveFileName(
            self,
            "Export compressed file",
            os.path.basename(self.last_output_file),
            f"*{ext}",
        )
        if not dest:
            return

        try:
            shutil.copy2(self.last_output_file, dest)
            self.log(f"Exported to: {dest}")
            QMessageBox.information(self, "Exported", f"Saved to:\n{dest}")
        except Exception as e:
            QMessageBox.critical(self, "Export failed", str(e))

    def log(self, text: str) -> None:
        self.output.append(text)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

    def _current_preset(self) -> tuple:
        return QUALITY_PRESETS[self.quality_slider.value()]

    def process_file(self, file_path: str) -> None:
        if not self.hw_encoders:
            QMessageBox.warning(self, "Not ready", "Still probing encoders, hang on.")
            return

        if not os.path.isfile(file_path):
            QMessageBox.critical(self, "Error", "File does not exist.")
            return

        mime, _ = mimetypes.guess_type(file_path)
        if mime is None:
            mime = "application/octet-stream"

        preset = self._current_preset()
        _, vbr, abr, qv, scale, fps, hz, desc = preset

        base = os.path.splitext(file_path)[0]
        slug = preset[0].replace(" ", "_")

        self.log("=" * 60)
        self.log(f"Detected MIME: {mime}")
        self.log(f"Input: {file_path}")
        self.log(f"Preset: {preset[0]}  |  {desc}")

        if mime.startswith("video"):
            output_file = f"{base}_{slug}.mp4"
            self.log("Video detected.")
            self.log(f"Using encoder: {self.hw_encoders[0].name}")
            cmd = build_video_cmd(
                file_path, output_file,
                encoder=self.hw_encoders[0],
                vbr=vbr, abr=abr, scale=scale, fps=fps, hz=hz,
                grayscale=self.opt_grayscale.isChecked(),
                denoise=self.opt_denoise.isChecked(),
                strip_audio=self.opt_strip_audio.isChecked(),
                mono=self.opt_mono.isChecked(),
            )

        elif mime.startswith("audio"):
            fmt = self.audio_format_combo.currentText()
            output_file = f"{base}_{slug}.{fmt}"
            self.log("Audio detected.")
            self.log("Converting to drive-thru speaker quality...")
            cmd = build_audio_cmd(
                file_path, output_file,
                abr=abr, hz=hz, fmt=fmt,
                mono=self.opt_mono.isChecked(),
            )

        elif mime.startswith("image"):
            fmt = self.image_format_combo.currentText()
            output_file = f"{base}_{slug}.{fmt}"
            self.log("Image detected.")
            self.log("Deep frying pixels...")
            cmd = build_image_cmd(
                file_path, output_file,
                qv=qv, scale=scale,
                grayscale=self.opt_img_grayscale.isChecked(),
            )

        else:
            QMessageBox.information(
                self, "Unsupported", f"Unsupported file type:\n{mime}"
            )
            return

        self._start_worker(cmd, output_file)

    def _start_worker(self, cmd: list[str], output_file: str) -> None:
        self.pick_button.setEnabled(False)
        self.compress_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.progress.setVisible(True)

        self.worker = FFmpegWorker(cmd, output_file)
        self.worker.log_signal.connect(self.log)
        self.worker.done_signal.connect(self._on_done)
        self.worker.start()

    def _on_done(self, code: int, output_file: str) -> None:
        self.progress.setVisible(False)
        self.pick_button.setEnabled(True)
        self.compress_button.setEnabled(True)
        self.worker = None

        if code == 0:
            self.last_output_file = output_file
            self.export_button.setEnabled(True)
            self.log("")
            self.log("DONE.")
            self.log(f"Output: {output_file}")
            QMessageBox.information(
                self, "Finished", f"Compression complete.\n\n{output_file}"
            )
        else:
            self.export_button.setEnabled(False)
            QMessageBox.critical(
                self, "Error", "FFmpeg failed.\nYour media fought back."
            )