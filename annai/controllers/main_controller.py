from PySide6.QtCore import QObject, Slot
from controllers.logger import setup_logger


class MainController(QObject):
    def __init__(self, view):
        super().__init__()

        self.view = view
        self.updating = False

        self.logger, qt_handler = setup_logger()
        self.qt_handler = qt_handler  # prevent GC

        qt_handler.log_signal.connect(self.view.update_log)

        self.logger.info("Logger connected")

        self._connect_signals()

    def _connect_signals(self):
        self.view.run_button.clicked.connect(self.start_updates)
        self.view.stop_button.clicked.connect(self.stop_updates)
        self.view.step_button.clicked.connect(self.step_update)

        self.view.trigger_A_button.clicked.connect(self.trigger_A)
        self.view.trigger_B_button.clicked.connect(self.trigger_B)
        self.view.trigger_C_button.clicked.connect(self.trigger_C)

        self.view.clear_instructions_A_button.clicked.connect(self.clear_instructions_A)
        self.view.clear_instructions_B_button.clicked.connect(self.clear_instructions_B)
        self.view.clear_instructions_C_button.clicked.connect(self.clear_instructions_C)

        self.view.clear_prompt_A_button.clicked.connect(self.clear_prompt_A)
        self.view.clear_prompt_B_button.clicked.connect(self.clear_prompt_B)
        self.view.clear_prompt_C_button.clicked.connect(self.clear_prompt_C)

        self.view.clear_response_A_button.clicked.connect(self.clear_response_A)
        self.view.clear_response_B_button.clicked.connect(self.clear_response_B)
        self.view.clear_response_C_button.clicked.connect(self.clear_response_C)

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

    @Slot()
    def clear_instructions_B(self):
        self.logger.info("Clearing instructions B")

    @Slot()
    def clear_instructions_C(self):
        self.logger.info("Clearing instructions C")

    @Slot()
    def clear_prompt_A(self):
        self.logger.info("Clearing prompt A")

    @Slot()
    def clear_prompt_B(self):
        self.logger.info("Clearing prompt B")

    @Slot()
    def clear_prompt_C(self):
        self.logger.info("Clearing prompt C")

    @Slot()
    def clear_response_A(self):
        self.logger.info("Clearing response A")

    @Slot()
    def clear_response_B(self):
        self.logger.info("Clearing response B")

    @Slot()
    def clear_response_C(self):
        self.logger.info("Clearing response C")