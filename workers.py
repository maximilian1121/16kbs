import subprocess

from PySide6.QtCore import QThread, Signal

from encoders import Encoder, detect_hw_encoders


class EncoderProbeWorker(QThread):
    done_signal = Signal(list)

    def run(self) -> None:
        self.done_signal.emit(detect_hw_encoders())


class FFmpegWorker(QThread):
    log_signal = Signal(str)
    done_signal = Signal(int, str)

    def __init__(self, cmd: list[str], output_file: str) -> None:
        super().__init__()
        self.cmd = cmd
        self.output_file = output_file

    def run(self) -> None:
        process = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        for line in process.stdout:
            self.log_signal.emit(line.strip())
        process.wait()
        self.done_signal.emit(process.returncode, self.output_file)