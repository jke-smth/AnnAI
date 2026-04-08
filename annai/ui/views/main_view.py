from PySide6 import QtWidgets

from annai.ui.widgets.led_indicator import LedIndicator
from annai.ui.views.prompt_panel import PromptPanel

class MainView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout(self)

        # Top buttons
        button_layout = QtWidgets.QHBoxLayout()

        self.run_button = QtWidgets.QPushButton("Run")
        self.step_button = QtWidgets.QPushButton("Step")
        self.stop_button = QtWidgets.QPushButton("Stop")

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.step_button)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)
        self.panel_A = PromptPanel("A")
        self.panel_B = PromptPanel("B")
        self.panel_C = PromptPanel("C")

        main_layout.addWidget(self.panel_A)
        main_layout.addWidget(self.panel_B)
        main_layout.addWidget(self.panel_C)