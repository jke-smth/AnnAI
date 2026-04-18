from PySide6 import QtWidgets
from annai.ui.widgets.led_indicator import LedIndicator


class PromptPanel(QtWidgets.QWidget):
    def __init__(self, name: str):
        super().__init__()

        self.name = name

        layout = QtWidgets.QVBoxLayout(self)

        # --- Text Areas ---
        prompt_response_layout = QtWidgets.QHBoxLayout()

        self.prompt_instructions = QtWidgets.QPlainTextEdit()
        self.prompt = QtWidgets.QPlainTextEdit()
        self.response = QtWidgets.QPlainTextEdit()

        prompt_response_layout.addWidget(self.prompt_instructions)
        prompt_response_layout.addWidget(self.prompt)
        prompt_response_layout.addWidget(self.response)

        layout.addLayout(prompt_response_layout)

        # --- Controls ---
        controls = QtWidgets.QHBoxLayout()

        self.led = LedIndicator()
        controls.addWidget(self.led)

        self.run_button = QtWidgets.QPushButton("Run")
        self.step_button = QtWidgets.QPushButton("Step")
        self.stop_button = QtWidgets.QPushButton("Stop")

        controls.addWidget(self.run_button)
        controls.addWidget(self.step_button)
        controls.addWidget(self.stop_button)

        self.pull_to_instructions_button = QtWidgets.QPushButton("Pull Instructions")
        self.pull_instructions_target_combo = QtWidgets.QComboBox()
        self.pull_instructions_mode_combo = QtWidgets.QComboBox()
        self.clear_instructions_button = QtWidgets.QPushButton("Clear Instructions")

        controls.addWidget(self.pull_to_instructions_button)
        controls.addWidget(self.pull_instructions_target_combo)
        controls.addWidget(self.pull_instructions_mode_combo)
        controls.addWidget(self.clear_instructions_button)

        self.pull_to_prompt_button = QtWidgets.QPushButton("Pull Prompt")
        self.pull_to_prompt_target_combo = QtWidgets.QComboBox()
        self.pull_to_prompt_mode_combo = QtWidgets.QComboBox()

        controls.addWidget(self.pull_to_prompt_button)
        controls.addWidget(self.pull_to_prompt_target_combo)
        controls.addWidget(self.pull_to_prompt_mode_combo)

        self.trigger_button = QtWidgets.QPushButton("Prompt")
        self.clear_prompt_button = QtWidgets.QPushButton("Clear Prompt")

        controls.addWidget(self.trigger_button)
        controls.addWidget(self.clear_prompt_button)

        self.send_response_button = QtWidgets.QPushButton("Send Response")
        self.send_target_combo = QtWidgets.QComboBox()
        self.clear_response_button = QtWidgets.QPushButton("Clear Response")

        controls.addWidget(self.send_response_button)
        controls.addWidget(self.send_target_combo)
        controls.addWidget(self.clear_response_button)

        layout.addLayout(controls)
