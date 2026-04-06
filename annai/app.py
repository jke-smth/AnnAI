import sys
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from controllers.main_controller import MainController


class App:
    def __init__(self):
        self.qt_app = QApplication(sys.argv)

        self.window = MainWindow()
        self.controller = MainController(self.window)

    def run(self):
        self.window.show()
        sys.exit(self.qt_app.exec())