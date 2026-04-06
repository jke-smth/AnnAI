import logging
from PySide6.QtCore import QObject, Signal


class QtHandler(QObject, logging.Handler):
    log_signal = Signal(str)

    def __init__(self):
        QObject.__init__(self)
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        self.log_signal.emit(msg)


def setup_logger():
    logger = logging.getLogger('textsynth_logger')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    qt_handler = None

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        qt_handler = next(
            (h for h in logger.handlers if isinstance(h, QtHandler)),
            None
        )

        if qt_handler:
            return logger, qt_handler

    # Console handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)

    # File handler
    f_handler = logging.FileHandler('textsynth.log')
    f_handler.setLevel(logging.DEBUG)

    # Formatters
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    # Qt handler
    qt_handler = QtHandler()
    qt_handler.setLevel(logging.DEBUG)
    qt_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(qt_handler)

    return logger, qt_handler