STYLESHEET = """
    QMainWindow, QWidget {
        background-color: #0d0d0d;
        color: #e8e8e8;
    }

    QLabel#title {
        font-size: 26px;
        font-weight: bold;
        color: #ffffff;
        padding-bottom: 2px;
    }

    QLabel#subtitle {
        font-size: 11px;
        color: #666666;
        letter-spacing: 2px;
        padding-bottom: 4px;
    }

    QLabel#fileLabel {
        font-size: 11px;
        color: #666666;
        padding-left: 8px;
    }

    QLabel#dropLabel {
        font-size: 11px;
        color: #444444;
        padding: 4px;
    }

    QLabel#optLabel {
        font-size: 11px;
        color: #888888;
    }

    QLabel#tickLabel {
        font-size: 9px;
        color: #555555;
    }

    QLabel#presetName {
        font-size: 12px;
        font-weight: bold;
        color: #e8e8e8;
        padding-left: 8px;
    }

    QLabel#presetDesc {
        font-size: 11px;
        color: #666666;
        font-style: italic;
    }

    QGroupBox#optionsGroup {
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        margin-top: 8px;
        padding: 10px;
        font-size: 11px;
        color: #666666;
    }

    QGroupBox#optionsGroup::title {
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 4px;
        color: #555555;
        font-size: 10px;
        letter-spacing: 1px;
    }

    QPushButton#pickButton {
        background-color: #161616;
        color: #cccccc;
        border: 1px solid #2e2e2e;
        border-radius: 4px;
        font-size: 13px;
        padding: 8px 16px;
        min-width: 120px;
    }

    QPushButton#pickButton:hover {
        background-color: #202020;
        border-color: #444444;
    }

    QPushButton#pickButton:disabled {
        color: #383838;
        border-color: #1e1e1e;
    }

    QPushButton#compressButton {
        background-color: #1a1a1a;
        color: #e8e8e8;
        border: 1px solid #3a3a3a;
        border-radius: 4px;
        font-size: 14px;
        font-weight: bold;
        padding: 8px;
    }

    QPushButton#compressButton:hover {
        background-color: #252525;
        border-color: #666666;
    }

    QPushButton#compressButton:disabled {
        color: #383838;
        border-color: #1e1e1e;
    }

    QPushButton#exportButton {
        background-color: #111111;
        color: #888888;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        font-size: 13px;
        padding: 8px;
    }

    QPushButton#exportButton:hover {
        background-color: #1a1a1a;
        color: #cccccc;
        border-color: #444444;
    }

    QPushButton#exportButton:disabled {
        color: #2e2e2e;
        border-color: #1a1a1a;
    }

    QSlider#qualitySlider::groove:horizontal {
        height: 4px;
        background: #2a2a2a;
        border-radius: 2px;
    }

    QSlider#qualitySlider::handle:horizontal {
        background: #e8e8e8;
        width: 14px;
        height: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }

    QSlider#qualitySlider::sub-page:horizontal {
        background: #555555;
        border-radius: 2px;
    }

    QCheckBox#optCheck {
        font-size: 11px;
        color: #aaaaaa;
        spacing: 6px;
    }

    QCheckBox#optCheck::indicator {
        width: 14px;
        height: 14px;
        border: 1px solid #3a3a3a;
        border-radius: 3px;
        background: #111111;
    }

    QCheckBox#optCheck::indicator:checked {
        background: #e8e8e8;
    }

    QComboBox#optCombo {
        background-color: #111111;
        color: #aaaaaa;
        border: 1px solid #2e2e2e;
        border-radius: 3px;
        padding: 2px 6px;
        font-size: 11px;
        min-width: 70px;
    }

    QComboBox#optCombo::drop-down {
        border: none;
        width: 16px;
    }

    QComboBox#optCombo QAbstractItemView {
        background-color: #161616;
        color: #aaaaaa;
        border: 1px solid #2e2e2e;
        selection-background-color: #252525;
    }

    QProgressBar#progress {
        border: 1px solid #2a2a2a;
        border-radius: 3px;
        background-color: #0a0a0a;
        height: 5px;
        text-align: center;
    }

    QProgressBar#progress::chunk {
        background-color: #cccccc;
        border-radius: 3px;
    }

    QTextEdit#output {
        background-color: #080808;
        color: #888888;
        border: 1px solid #1e1e1e;
        border-radius: 4px;
        padding: 8px;
        font-size: 11px;
    }

    QScrollBar:vertical {
        background: #0d0d0d;
        width: 6px;
        border-radius: 3px;
    }

    QScrollBar::handle:vertical {
        background: #2e2e2e;
        border-radius: 3px;
    }
"""