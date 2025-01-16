from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import  QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import  Qt, QSize

class Main_UI(QWidget):
    """UI 구성 및 관리하는 클래스"""
    def __init__(self):
        super().__init__()

        # UI 초기화
        self.init_ui()

    def init_ui(self):
        """UI 구성"""
        # Layouts
        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.label_layout = QHBoxLayout()
        self.input_layout = QHBoxLayout()
        self.status_layout = QHBoxLayout()

        self.style_outline = "color: #000000; border-style: solid; border-width: 2px; border-color: #000000; border-radius: 10px; "

        # Buttons
        self.filling_btn = QPushButton("Filling LN2")
        self.info_btn = QPushButton("Info")
        self.refresh_btn = QPushButton("Refresh")

        # Add buttons to button layout
        self.button_layout.addWidget(self.filling_btn)
        self.button_layout.addWidget(self.info_btn)
        self.button_layout.addWidget(self.refresh_btn)

        # QLabel for video
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        # Label layout
        self.puck_label = QLabel("Puck")
        self.puck_label.setMinimumSize(QSize(400, 30))
        self.puck_label.setFont(QFont("SansSerif", 10, QFont.Bold))
        self.barcode_label = QLabel("Barcode")
        self.barcode_label.setMinimumSize(QSize(160, 30))
        self.barcode_label.setFont(QFont("SansSerif", 10, QFont.Bold))

        # Add input elements to label layout (side by side)
        self.label_layout.addWidget(self.puck_label, 7)
        self.label_layout.addWidget(self.barcode_label, 3)

        # QLabel and QLineEdit for input section
        self.detected_puck_label = QLabel("")
        self.detected_puck_label.setStyleSheet(self.style_outline)
        self.detected_puck_label.setMinimumSize(QSize(400, 100))
        self.detected_puck_label.setFont(QFont("SansSerif", 30, QFont.Bold))

        self.barcode_input = QLineEdit()
        self.barcode_input.setStyleSheet(self.style_outline)
        self.barcode_input.setMinimumSize(QSize(160, 100))
        self.barcode_input.setFont(QFont("SansSerif", 20, QFont.Bold))

        # Add input elements to input layout (side by side)
        self.input_layout.addWidget(self.detected_puck_label, 7)
        self.input_layout.addWidget(self.barcode_input, 3)

        self.state_label = QLabel("")
        self.state_label.setStyleSheet(self.style_outline)
        self.state_label.setMinimumSize(QSize(400, 30))
        self.state_label.setFont(QFont("SansSerif", 10, QFont.Bold))
        self.beamline_label = QLabel("BL5C")
        self.beamline_label.setStyleSheet(self.style_outline)
        self.beamline_label.setMinimumSize(QSize(160, 30))
        self.beamline_label.setFont(QFont("SansSerif", 10, QFont.Bold))

        self.status_layout.addWidget(self.state_label, 7)
        self.status_layout.addWidget(self.beamline_label, 3)

        # Add layouts to main layout
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.video_label)
        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.status_layout)

        # Set the main layout
        self.setLayout(self.main_layout)
