from PySide6 import QtWidgets
from PySide6.QtCore import Slot

class LogView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.log_text = QtWidgets.QPlainTextEdit()
        self.log_text.setReadOnly(True)

        layout.addWidget(self.log_text)

    @Slot(str)
    def append(self, message: str):
        self.log_text.appendPlainText(message)