from PySide6 import QtWidgets
from PySide6.QtCore import Slot

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lagostryx Text-Synth")
        self.resize(1000, 700)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)

        button_layout = QtWidgets.QHBoxLayout()

        self.run_button = QtWidgets.QPushButton("Run")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.step_button = QtWidgets.QPushButton("Step")

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.step_button)

        main_layout.addLayout(button_layout)

        self.log_text = QtWidgets.QPlainTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

    @Slot(str)
    def update_log(self, message):
        self.log_text.appendPlainText(message)