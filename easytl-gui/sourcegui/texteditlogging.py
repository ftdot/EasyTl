import logging
from PyQt5.QtCore import QObject, pyqtSignal


class TextEditHandler(QObject):
    flush_signal = pyqtSignal()
    clear_signal = pyqtSignal()
    buffer = ''
    handler = None

    def initialize(self, log_level: int | str):
        self.handler = logging.StreamHandler(self)
        self.handler.setLevel(log_level)

        self.clear_signal.connect(self.clear_buffer)

    def write(self, data):
        try:
            self.buffer += data
        except Exception as e:
            import traceback
            traceback.print_exception(e)

    def flush(self):
        try:
            self.flush_signal.emit()
        except Exception as e:
            import traceback
            traceback.print_exception(e)

    def clear_buffer(self):
        self.buffer = ''
