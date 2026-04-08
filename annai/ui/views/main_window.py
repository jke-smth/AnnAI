from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from annai.ui.widgets.led_indicator import LedIndicator
from annai.ui.views.log_view import LogView
from annai.ui.views.main_view import MainView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lagostryx Text-Synth")
        self.resize(1000, 700)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        ##Todo: add a multi-document interface with tabs to select between views: main view, log view, matrix view

        #Maybe move the main view code into a seperate view file

        main_layout = QtWidgets.QVBoxLayout(central)

        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)

        self.main_view = MainView()

        self.tabs.addTab(self.main_view, "Main")

        self.log_view = LogView()
        self.tabs.addTab(self.log_view, "Log")


    @Slot(str)
    def update_log(self, message):
        self.log_view.append(message)