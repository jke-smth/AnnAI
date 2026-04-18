from PySide6.QtCore import QObject, Slot

from annai.controllers.logger import setup_logger
from annai.services.main_state_machine import MainStateMachine
from annai.services.panel_state_machine import PanelState, PanelStateMachine
from annai.services.panel_worker import PanelStepThread, PanelWorker


class MainController(QObject):
    def __init__(self, view):
        super().__init__()

        self.view = view
        self.main_view = self.view.main_view

        # Register panels
        self.panels = {
            "A": self.main_view.panel_A,
            "B": self.main_view.panel_B,
            "C": self.main_view.panel_C,
        }

        # Logger
        self.logger, qt_handler = setup_logger()
        self.qt_handler = qt_handler
        qt_handler.log_signal.connect(self.view.update_log)
        self.logger.info("Logger connected")

        self.main_state_machine = MainStateMachine(logger=self.logger)

        # Populate combos
        self._setup_combos()

        # Connect signals
        self._connect_signals()

        # Create a state machine and worker per panel
        self.machines = {}
        self.workers = {}
        self.active_threads = {}
        for key, panel in self.panels.items():
            sm = PanelStateMachine(panel_name=key, logger=self.logger)
            sm.attach_led(panel.led)
            self.machines[key] = sm
            self.workers[key] = PanelWorker(panel_name=key, logger=self.logger)
            self.active_threads[key] = None

    # -------------------------
    # Setup
    # -------------------------
    def _setup_combos(self):
        valid_response_sends = [
            "None", "Prompt A", "Prompt B", "Prompt C",
            "Instructions A", "Instructions B", "Instructions C", "TTS"
        ]

        valid_instruction_pulls = ["None", "Response A", "Response B", "Response C"]
        valid_prompt_pulls = ["None", "Response A", "Response B", "Response C"]
        valid_pull_modes = ["Append", "Replace"]

        for panel in self.panels.values():
            panel.send_target_combo.addItems(valid_response_sends)
            panel.pull_instructions_target_combo.addItems(valid_instruction_pulls)
            panel.pull_instructions_mode_combo.addItems(valid_pull_modes)
            panel.pull_to_prompt_target_combo.addItems(valid_prompt_pulls)
            panel.pull_to_prompt_mode_combo.addItems(valid_pull_modes)

    def _connect_signals(self):
        # Global controls
        self.main_view.run_button.clicked.connect(self.start_updates)
        self.main_view.stop_button.clicked.connect(self.stop_updates)
        self.main_view.step_button.clicked.connect(self.step_update)

        # Panel controls
        for key, panel in self.panels.items():
            panel.run_button.clicked.connect(lambda _, k=key: self.start_panel(k))
            panel.stop_button.clicked.connect(lambda _, k=key: self.stop_panel(k))
            panel.step_button.clicked.connect(lambda _, k=key: self.step_panel(k))

            panel.trigger_button.clicked.connect(lambda _, k=key: self.trigger(k))

            panel.clear_prompt_button.clicked.connect(lambda _, p=panel: p.prompt.clear())
            panel.clear_response_button.clicked.connect(lambda _, p=panel: p.response.clear())
            panel.clear_instructions_button.clicked.connect(lambda _, p=panel: p.prompt_instructions.clear())

            panel.send_response_button.clicked.connect(lambda _, k=key: self.send_response(k))

            panel.send_target_combo.currentTextChanged.connect(
                lambda text, k=key: self.update_send_target(k, text)
            )

    # -------------------------
    # Global Controls
    # -------------------------
    @Slot()
    def start_updates(self):
        self.main_state_machine.start()

    @Slot()
    def stop_updates(self):
        self.main_state_machine.stop()

    @Slot()
    def step_update(self):
        self.logger.info("Stepping update")

    # -------------------------
    # Panel Actions
    # -------------------------
    def start_panel(self, key):
        self.logger.info(f"Starting {key}")
        sm = self.machines.get(key)
        worker = self.workers.get(key)
        if not sm:
            return

        if self._panel_is_busy(key):
            self.logger.warning(f"{key} is already processing a step")
            return

        if worker:
            worker.reset()
        sm.reset()
        sm.trigger()
        self.panels[key].response.clear()

    def stop_panel(self, key):
        self.logger.info(f"Stopping {key}")
        sm = self.machines.get(key)
        worker = self.workers.get(key)
        if sm:
            sm.stop()
        if worker:
            worker.reset()

    def step_panel(self, key):
        panel = self.panels[key]
        sm = self.machines.get(key)
        worker = self.workers.get(key)

        if not sm or not worker:
            return

        if self._panel_is_busy(key):
            self.logger.warning(f"{key} is already processing a step")
            return

        current_state = sm.get_state()
        if current_state == PanelState.STOPPED:
            self.logger.warning(f"{key} is stopped; reset or start it before stepping")
            return

        if current_state == PanelState.IDLE:
            worker.set_initial_input(
                panel.prompt.toPlainText(),
                panel.prompt_instructions.toPlainText(),
            )
            success = sm.trigger()
            if not success:
                self.logger.warning(f"Failed to start step for {key}")
                return
            current_state = sm.get_state()

        self.logger.info(f"Stepping {key} ({current_state.value})")
        self.logger.info(f"[{key}] [{current_state.value}] processing...")

        thread = PanelStepThread(worker, current_state)
        thread.step_started.connect(lambda state_name, k=key: self.logger.info(f"[{k}] Running {state_name}"))
        thread.step_finished.connect(
            lambda result, k=key, state=current_state: self._handle_panel_step_finished(k, state, result)
        )
        thread.step_failed.connect(
            lambda message, k=key, state=current_state: self._handle_panel_step_failed(k, state, message)
        )
        thread.finished.connect(lambda k=key: self._clear_panel_thread(k))
        self.active_threads[key] = thread
        thread.start()

    def trigger(self, key):
        self.logger.info(f"Triggering {key}")
        sm = self.machines.get(key)
        if sm:
            success = sm.trigger()
            if not success:
                self.logger.warning(f"Failed to trigger {key} - invalid state")

    def send_response(self, key):
        self.logger.info(f"Sending response {key}")

    def update_send_target(self, key, target):
        self.logger.info(f"{key} send target -> {target}")

    def _panel_is_busy(self, key):
        thread = self.active_threads.get(key)
        return bool(thread and thread.isRunning())

    def _handle_panel_step_finished(self, key, state, result):
        panel = self.panels[key]
        sm = self.machines.get(key)
        worker = self.workers.get(key)
        self.logger.info(f"[{key}] [{state.value}] {result}")
        if state == PanelState.END_TRIGGER:
            panel.response.setPlainText(result)

        if not sm:
            return

        if sm.get_state() != state:
            self.logger.info(
                f"[{key}] Completed {state.value}, but panel is now in {sm.get_state().value}; not advancing"
            )
            return

        sm.advance()
        self.logger.info(f"[{key}] Advanced to {sm.get_state().value}")

        if sm.get_state() == PanelState.IDLE and worker:
            worker.reset()

    def _handle_panel_step_failed(self, key, state, message):
        sm = self.machines.get(key)
        worker = self.workers.get(key)

        self.logger.error(f"[{key}] Step failed in {state.value}: {message}")

        if sm:
            sm.stop()
        if worker:
            worker.reset()

    def _clear_panel_thread(self, key):
        thread = self.active_threads.get(key)
        if thread:
            thread.deleteLater()
        self.active_threads[key] = None
