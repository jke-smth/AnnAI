from PySide6.QtCore import QObject, Slot, QTimer
from PySide6 import QtWidgets
from annai.controllers.logger import setup_logger


class ExecutionStateMachine:
    def __init__(self, logger=None):
        self.logger = logger

        # Centralized state storage
        self.states = {
            "main": "stopped",
            "A": "stopped",
            "B": "stopped",
            "C": "stopped",
        }

    # -------------------------
    # Internal Helpers
    # -------------------------
    def _log(self, message):
        if self.logger:
            self.logger.info(message)

    def _transition(self, key, new_state):
        old_state = self.states[key]
        self.states[key] = new_state
        self._log(f"{key}: {old_state} → {new_state}")

    def _start(self, key):
        if self.states[key] == "stopped":
            self._transition(key, "running")
            return True

        self._log(f"Invalid start: {key} already {self.states[key]}")
        return False

    def _stop(self, key):
        if self.states[key] == "running":
            self._transition(key, "stopped")
            return True

        self._log(f"Invalid stop: {key} already {self.states[key]}")
        return False

    def _step(self, key):
        if self.states[key] in ["stopped"]:
            self._log(f"{key}: step")
            return True

        self._log(f"Invalid step: {key} in state {self.states[key]}")
        return False

    # -------------------------
    # Global Controls
    # -------------------------
    def start(self):
        return self._start("main")

    def stop(self):
        result = self._stop("main")

        # Optional: stopping main stops everything
        if result:
            for key in ["A", "B", "C"]:
                if self.states[key] == "running":
                    self._transition(key, "stopped")

        return result

    def step(self):
        return self._step("main")

    # -------------------------
    # Panel A
    # -------------------------
    def start_A(self):
        return self._start("A")

    def stop_A(self):
        return self._stop("A")

    def step_A(self):
        return self._step("A")

    # -------------------------
    # Panel B
    # -------------------------
    def start_B(self):
        return self._start("B")

    def stop_B(self):
        return self._stop("B")

    def step_B(self):
        return self._step("B")

    # -------------------------
    # Panel C
    # -------------------------
    def start_C(self):
        return self._start("C")

    def stop_C(self):
        return self._stop("C")

    def step_C(self):
        return self._step("C")

    # -------------------------
    # Utility
    # -------------------------
    def get_state(self, key):
        return self.states.get(key)
    


class MainController(QObject):
    def __init__(self, view):
        super().__init__()

        self.state_machine = ExecutionStateMachine()

        self.view = view
        self.updating = False

        self.logger, qt_handler = setup_logger()
        self.qt_handler = qt_handler  # prevent GC

        qt_handler.log_signal.connect(self.view.update_log)
        self.logger.info("Logger connected")

        valid_response_sends = ["None", "Prompt A", "Prompt B", "Prompt C", "Instructions A", "Instructions B", "Instructions C", "TTS"]
        self.view.send_target_A_combo.addItems(valid_response_sends)
        self.view.send_target_B_combo.addItems(valid_response_sends)
        self.view.send_target_C_combo.addItems(valid_response_sends)

        valid_instruction_pulls = ["None", "Response A", "Response B", "Response C"]
        self.view.pull_instructions_target_A_combo.addItems(valid_instruction_pulls)
        self.view.pull_instructions_target_B_combo.addItems(valid_instruction_pulls)
        self.view.pull_instructions_target_C_combo.addItems(valid_instruction_pulls)

        valid_prompt_pulls = ["None", "Response A", "Response B", "Response C"]
        self.view.pull_to_prompt_target_A_combo.addItems(valid_prompt_pulls)
        self.view.pull_to_prompt_target_B_combo.addItems(valid_prompt_pulls)
        self.view.pull_to_prompt_target_C_combo.addItems(valid_prompt_pulls)

        self._connect_signals()

    def _connect_signals(self):
        self.view.run_button.clicked.connect(self.start_updates)
        self.view.stop_button.clicked.connect(self.stop_updates)
        self.view.step_button.clicked.connect(self.step_update)

        self.view.run_A_button.clicked.connect(self.start_updates_A)
        self.view.run_B_button.clicked.connect(self.start_updates_B)
        self.view.run_C_button.clicked.connect(self.start_updates_C)

        self.view.step_A_button.clicked.connect(self.step_update_A)
        self.view.step_B_button.clicked.connect(self.step_update_B)
        self.view.step_C_button.clicked.connect(self.step_update_C)

        self.view.stop_A_button.clicked.connect(self.stop_updates_A)
        self.view.stop_B_button.clicked.connect(self.stop_updates_B)
        self.view.stop_C_button.clicked.connect(self.stop_updates_C)

        self.view.trigger_pull_to_prompt_A_button.clicked.connect(self.trigger_pull_to_prompt_A)
        self.view.trigger_pull_to_prompt_B_button.clicked.connect(self.trigger_pull_to_prompt_B)
        self.view.trigger_pull_to_prompt_C_button.clicked.connect(self.trigger_pull_to_prompt_C)

        self.view.trigger_A_button.clicked.connect(self.trigger_A)
        self.view.trigger_B_button.clicked.connect(self.trigger_B)
        self.view.trigger_C_button.clicked.connect(self.trigger_C)

        self.view.pull_to_instructions_A_button.clicked.connect(self.trigger_pull_to_instructions_A)
        self.view.pull_to_instructions_B_button.clicked.connect(self.trigger_pull_to_instructions_B)
        self.view.pull_to_instructions_C_button.clicked.connect(self.trigger_pull_to_instructions_C)

        self.view.clear_instructions_A_button.clicked.connect(self.clear_instructions_A)
        self.view.clear_instructions_B_button.clicked.connect(self.clear_instructions_B)
        self.view.clear_instructions_C_button.clicked.connect(self.clear_instructions_C)

        self.view.clear_prompt_A_button.clicked.connect(self.clear_prompt_A)
        self.view.clear_prompt_B_button.clicked.connect(self.clear_prompt_B)
        self.view.clear_prompt_C_button.clicked.connect(self.clear_prompt_C)

        self.view.clear_response_A_button.clicked.connect(self.clear_response_A)
        self.view.clear_response_B_button.clicked.connect(self.clear_response_B)
        self.view.clear_response_C_button.clicked.connect(self.clear_response_C)

        self.view.send_response_A_button.clicked.connect(self.send_response_A)
        self.view.send_response_B_button.clicked.connect(self.send_response_B)
        self.view.send_response_C_button.clicked.connect(self.send_response_C)

        self.view.send_target_A_combo.currentTextChanged.connect(self.update_send_target_A)
        self.view.send_target_B_combo.currentTextChanged.connect(self.update_send_target_B)
        self.view.send_target_C_combo.currentTextChanged.connect(self.update_send_target_C)

    @Slot()
    def start_updates(self):
        self.updating = True
        self.logger.info("Starting updates")

    @Slot()
    def stop_updates(self):
        self.updating = False
        self.logger.info("Stopping updates")

    @Slot()
    def step_update(self):
        self.logger.info("Stepping update")

    @Slot()
    def trigger_A(self):
        self.logger.info("Triggering A")

    @Slot()
    def trigger_B(self):
        self.logger.info("Triggering B")

    @Slot()
    def trigger_C(self):
        self.logger.info("Triggering C")

    @Slot()
    def clear_instructions_A(self):
        self.logger.info("Clearing instructions A")
        try:
            self.view.prompt_instructions_A.clear()
        except Exception:
            self.logger.exception("Failed to clear instructions A")

    @Slot()
    def clear_instructions_B(self):
        self.logger.info("Clearing instructions B")
        try:
            self.view.prompt_instructions_B.clear()
        except Exception:
            self.logger.exception("Failed to clear instructions B")

    @Slot()
    def clear_instructions_C(self):
        self.logger.info("Clearing instructions C")
        try:
            self.view.prompt_instructions_C.clear()
        except Exception:
            self.logger.exception("Failed to clear instructions C")

    @Slot()
    def clear_prompt_A(self):
        self.logger.info("Clearing prompt A")
        try:
            self.view.prompt_A.clear()
        except Exception:
            self.logger.exception("Failed to clear prompt A")

    @Slot()
    def clear_prompt_B(self):
        self.logger.info("Clearing prompt B")
        try:
            self.view.prompt_B.clear()
        except Exception:
            self.logger.exception("Failed to clear prompt B")

    @Slot()
    def clear_prompt_C(self):
        self.logger.info("Clearing prompt C")
        try:
            self.view.prompt_C.clear()
        except Exception:
            self.logger.exception("Failed to clear prompt C")

    @Slot()
    def clear_response_A(self):
        self.logger.info("Clearing response A")
        try:
            self.view.response_A.clear()
        except Exception:
            self.logger.exception("Failed to clear response A")

    @Slot()
    def clear_response_B(self):
        self.logger.info("Clearing response B")
        try:
            self.view.response_B.clear()
        except Exception:
            self.logger.exception("Failed to clear response B")

    @Slot()
    def clear_response_C(self):
        self.logger.info("Clearing response C")
        try:
            self.view.response_C.clear()
        except Exception:
            self.logger.exception("Failed to clear response C")

    @Slot()
    def trigger_pull_to_prompt_A(self):
        self.logger.info("Triggering pull A")

    @Slot()
    def trigger_pull_to_prompt_B(self):
        self.logger.info("Triggering pull B")

    @Slot()
    def trigger_pull_to_prompt_C(self):
        self.logger.info("Triggering pull C")

    @Slot()
    def trigger_pull_to_instructions_A(self):
        self.logger.info("Triggering pull to instructions A")

    @Slot()
    def trigger_pull_to_instructions_B(self):
        self.logger.info("Triggering pull to instructions B")
    
    @Slot()
    def trigger_pull_to_instructions_C(self):
        self.logger.info("Triggering pull to instructions C")

    @Slot()
    def send_response_A(self):
        self.logger.info("Sending response A")

    @Slot()
    def send_response_B(self):
        self.logger.info("Sending response B")

    @Slot()
    def send_response_C(self):
        self.logger.info("Sending response C")

    @Slot()
    def update_send_target_A(self, target):
        self.logger.info(f"Updating send target A to {target}")

    @Slot()
    def update_send_target_B(self, target):
        self.logger.info(f"Updating send target B to {target}")

    @Slot()
    def update_send_target_C(self, target):
        self.logger.info(f"Updating send target C to {target}")

    @Slot()
    def start_updates_A(self):
        if self.state_machine.start_A():
            self.logger.info("Starting updates A")
            self.update_led_A()

    @Slot()
    def stop_updates_A(self):
        if self.state_machine.stop_A():
            self.logger.info("Stopping updates A")
            self.update_led_A()


    @Slot()
    def step_update_A(self):
        if self.state_machine.step_A():
            self.logger.info("Stepping update A")
            self.view.led_A.set_color("yellow")
            QTimer.singleShot(300, self.update_led_A)
            

    @Slot()
    def start_updates_B(self):
        if self.state_machine.start_B():
            self.logger.info("Starting updates B")
            self.update_led_B()


    @Slot()
    def stop_updates_B(self):
        if self.state_machine.stop_B():
            self.logger.info("Stopping updates B")
            self.update_led_B()


    @Slot()
    def step_update_B(self):
        if self.state_machine.step_B():
            self.logger.info("Stepping update B")
            self.update_led_B()


    @Slot()
    def start_updates_C(self):
        if self.state_machine.start_C():
            self.logger.info("Starting updates C")
            self.update_led_C()


    @Slot()
    def stop_updates_C(self):
        if self.state_machine.stop_C():
            self.logger.info("Stopping updates C")
            self.update_led_C()

    @Slot()
    def step_update_C(self):
        if self.state_machine.step_C():
            self.logger.info("Stepping update C")
            self.update_led_C()

    def update_led_A(self):
        state = self.state_machine.get_state("A")
        if state == "running":
            self.view.led_A.set_color("green")
        elif state == "stopped":
            self.view.led_A.set_color("red")
        elif state == "step":
            self.view.led_A.set_color("yellow")

    def update_led_B(self):
        state = self.state_machine.get_state("B")
        if state == "running":
            self.view.led_B.set_color("green")
        elif state == "stopped":
            self.view.led_B.set_color("red")
        elif state == "step":
            self.view.led_B.set_color("yellow")

    def update_led_C(self):
        state = self.state_machine.get_state("C")
        if state == "running":
            self.view.led_C.set_color("green")
        elif state == "stopped":
            self.view.led_C.set_color("red")
        elif state == "step":
            self.view.led_C.set_color("yellow")
