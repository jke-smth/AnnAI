from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from .widgets.led_indicator import LedIndicator

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lagostryx Text-Synth")
        self.resize(1000, 700)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        self.valid_sends = []

        main_layout = QtWidgets.QVBoxLayout(central)

        button_layout = QtWidgets.QHBoxLayout()

        self.run_button = QtWidgets.QPushButton("Run")
        self.step_button = QtWidgets.QPushButton("Step")
        self.stop_button = QtWidgets.QPushButton("Stop")


        

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.step_button)
        button_layout.addWidget(self.stop_button)
        

        main_layout.addLayout(button_layout)

        layout_A = QtWidgets.QVBoxLayout()
        layout_B = QtWidgets.QVBoxLayout()
        layout_C = QtWidgets.QVBoxLayout()

        prompt_response_A_layout = QtWidgets.QHBoxLayout()

        self.prompt_instructions_A = QtWidgets.QPlainTextEdit()
        prompt_response_A_layout.addWidget(self.prompt_instructions_A)

        self.prompt_A = QtWidgets.QPlainTextEdit()
        prompt_response_A_layout.addWidget(self.prompt_A)

        self.response_A = QtWidgets.QPlainTextEdit()
        prompt_response_A_layout.addWidget(self.response_A)

        layout_A.addLayout(prompt_response_A_layout)

        controls_A = QtWidgets.QHBoxLayout()

        self.led_A = LedIndicator()
        controls_A.addWidget(self.led_A)

        self.run_A_button = QtWidgets.QPushButton("Run")
        controls_A.addWidget(self.run_A_button)

        self.step_A_button = QtWidgets.QPushButton("Step")
        controls_A.addWidget(self.step_A_button)

        self.stop_A_button = QtWidgets.QPushButton("Stop")
        controls_A.addWidget(self.stop_A_button)

        self.pull_to_instructions_A_button = QtWidgets.QPushButton("Pull Instructions")
        controls_A.addWidget(self.pull_to_instructions_A_button)

        self.clear_instructions_A_button = QtWidgets.QPushButton("Clear Instructions")
        controls_A.addWidget(self.clear_instructions_A_button)

        self.trigger_pull_to_prompt_A_button = QtWidgets.QPushButton("Pull Prompt")
        controls_A.addWidget(self.trigger_pull_to_prompt_A_button)

        self.trigger_A_button = QtWidgets.QPushButton("Prompt")
        controls_A.addWidget(self.trigger_A_button)

        self.clear_prompt_A_button = QtWidgets.QPushButton("Clear Prompt")
        controls_A.addWidget(self.clear_prompt_A_button)

        self.send_response_A_button = QtWidgets.QPushButton("Send Response")
        controls_A.addWidget(self.send_response_A_button)

        self.send_target_A_combo = QtWidgets.QComboBox()
        controls_A.addWidget(self.send_target_A_combo)

        self.clear_response_A_button = QtWidgets.QPushButton("Clear Response")
        controls_A.addWidget(self.clear_response_A_button)

        layout_A.addLayout(controls_A)
        

        prompt_response_B_layout = QtWidgets.QHBoxLayout()

        self.prompt_instructions_B = QtWidgets.QPlainTextEdit()
        prompt_response_B_layout.addWidget(self.prompt_instructions_B)

        self.prompt_B = QtWidgets.QPlainTextEdit()
        prompt_response_B_layout.addWidget(self.prompt_B)

        self.response_B = QtWidgets.QPlainTextEdit()
        prompt_response_B_layout.addWidget(self.response_B)

        layout_B.addLayout(prompt_response_B_layout)

        controls_B = QtWidgets.QHBoxLayout()

        self.led_B = LedIndicator()
        controls_B.addWidget(self.led_B)

        self.run_B_button = QtWidgets.QPushButton("Run")
        controls_B.addWidget(self.run_B_button)

        self.step_B_button = QtWidgets.QPushButton("Step")
        controls_B.addWidget(self.step_B_button)

        self.stop_B_button = QtWidgets.QPushButton("Stop")
        controls_B.addWidget(self.stop_B_button)

        self.pull_to_instructions_B_button = QtWidgets.QPushButton("Pull Instructions")
        controls_B.addWidget(self.pull_to_instructions_B_button)

        self.clear_instructions_B_button = QtWidgets.QPushButton("Clear Instructions")
        controls_B.addWidget(self.clear_instructions_B_button)
    
        self.trigger_pull_to_prompt_B_button = QtWidgets.QPushButton("Pull Prompt")
        controls_B.addWidget(self.trigger_pull_to_prompt_B_button)

        self.trigger_B_button = QtWidgets.QPushButton("Prompt")
        controls_B.addWidget(self.trigger_B_button)

        self.clear_prompt_B_button = QtWidgets.QPushButton("Clear Prompt")
        controls_B.addWidget(self.clear_prompt_B_button)

        self.send_response_B_button = QtWidgets.QPushButton("Send Response")
        controls_B.addWidget(self.send_response_B_button)

        self.send_target_B_combo = QtWidgets.QComboBox()
        controls_B.addWidget(self.send_target_B_combo)

        self.clear_response_B_button = QtWidgets.QPushButton("Clear Response")
        controls_B.addWidget(self.clear_response_B_button)

        layout_B.addLayout(controls_B)
        

        prompt_response_C_layout = QtWidgets.QHBoxLayout()

        self.prompt_instructions_C = QtWidgets.QPlainTextEdit()
        prompt_response_C_layout.addWidget(self.prompt_instructions_C)

        self.prompt_C = QtWidgets.QPlainTextEdit()
        prompt_response_C_layout.addWidget(self.prompt_C)

        self.response_C = QtWidgets.QPlainTextEdit()
        prompt_response_C_layout.addWidget(self.response_C)

        layout_C.addLayout(prompt_response_C_layout)

        controls_C = QtWidgets.QHBoxLayout()

        self.led_C = LedIndicator()
        controls_C.addWidget(self.led_C)

        self.run_C_button = QtWidgets.QPushButton("Run")
        controls_C.addWidget(self.run_C_button)

        self.step_C_button = QtWidgets.QPushButton("Step")
        controls_C.addWidget(self.step_C_button)

        self.stop_C_button = QtWidgets.QPushButton("Stop")
        controls_C.addWidget(self.stop_C_button)

        self.pull_to_instructions_C_button = QtWidgets.QPushButton("Pull Instructions")
        controls_C.addWidget(self.pull_to_instructions_C_button)

        self.clear_instructions_C_button = QtWidgets.QPushButton("Clear Instructions")
        controls_C.addWidget(self.clear_instructions_C_button)

        self.trigger_pull_to_prompt_C_button = QtWidgets.QPushButton("Pull Prompt")
        controls_C.addWidget(self.trigger_pull_to_prompt_C_button)

        self.trigger_C_button = QtWidgets.QPushButton("Prompt")
        controls_C.addWidget(self.trigger_C_button)

        self.clear_prompt_C_button = QtWidgets.QPushButton("Clear Prompt")
        controls_C.addWidget(self.clear_prompt_C_button)

        self.send_response_C_button = QtWidgets.QPushButton("Send Response")
        controls_C.addWidget(self.send_response_C_button)

        self.send_target_C_combo = QtWidgets.QComboBox()
        controls_C.addWidget(self.send_target_C_combo)

        self.clear_response_C_button = QtWidgets.QPushButton("Clear Response")
        controls_C.addWidget(self.clear_response_C_button)

        layout_C.addLayout(controls_C)

        main_layout.addLayout(layout_A)
        main_layout.addLayout(layout_B)
        main_layout.addLayout(layout_C)

        self.log_text = QtWidgets.QPlainTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

    @Slot(str)
    def update_log(self, message):
        self.log_text.appendPlainText(message)