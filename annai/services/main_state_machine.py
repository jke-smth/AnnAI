from enum import Enum

class MainState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"


class MainStateMachine:
    def __init__(self, logger=None):
        self.state = MainState.STOPPED
        self.logger = logger

    def _log(self, msg):
        if self.logger:
            try:
                self.logger.info(msg)
            except Exception:
                pass

    def start(self):
        if self.state == MainState.RUNNING:
            self._log("Already running")
            return
        self.state = MainState.RUNNING
        self._log("Started")

    def stop(self):
        if self.state == MainState.STOPPED:
            self._log("Already stopped")
            return
        self.state = MainState.STOPPED
        self._log("Stopped")

