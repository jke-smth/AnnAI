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