from PySide6.QtCore import QObject, Slot, QTimer
from annai.controllers.logger import setup_logger
from annai.services.panel_state_machine import PanelStateMachine
from annai.services.main_state_machine import MainStateMachine

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

        # Create a state machine per panel and attach its LED
        self.machines = {}
        for key, panel in self.panels.items():
            sm = PanelStateMachine(panel_name=key, logger=self.logger)
            # attach_led returns an unregister callable if needed
            sm.attach_led(panel.led)
            self.machines[key] = sm

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

        for panel in self.panels.values():
            panel.send_target_combo.addItems(valid_response_sends)
            panel.pull_instructions_target_combo.addItems(valid_instruction_pulls)
            panel.pull_to_prompt_target_combo.addItems(valid_prompt_pulls)

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
        panel = self.panels[key]
        sm = self.machines.get(key)
        if sm:
            sm.reset()
            sm.trigger()

    def stop_panel(self, key):
        self.logger.info(f"Stopping {key}")
        panel = self.panels[key]
        sm = self.machines.get(key)
        if sm:
            sm.stop()


    def step_panel(self, key):
        self.logger.info(f"Stepping {key}")
        panel = self.panels[key]
        sm = self.machines.get(key)
        # Todo: call an async function and wait for it to complete before advancing the state machine
        if sm:
            sm.advance()
        

    def trigger(self, key):
        self.logger.info(f"Triggering {key}")
        panel = self.panels[key]
        sm = self.machines.get(key)
        if sm:
            success = sm.trigger()
            if not success:
                self.logger.warning(f"Failed to trigger {key} - invalid state")
                

    def send_response(self, key):
        self.logger.info(f"Sending response {key}")

    def update_send_target(self, key, target):
        self.logger.info(f"{key} send target → {target}")
