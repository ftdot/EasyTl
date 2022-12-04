import logging
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class TextEditHandler(QObject):
    """Object that helps to use the logging from one thread to the TextEdit from other thread

    :ivar flush_signal: Signals that emits then TextEditHandler.flush() method is called
    :type flush_signal: pyqtSignal
    :ivar buffer: Temporary buffer of the handler
    :type buffer: str
    """

    flush_signal = pyqtSignal(str)

    def __init__(self, log_level: int | str):
        """
        :param log_level: Log level of the logger handler
        :type log_level: int | str
        """
        super().__init__()

        self.buffer = ''

        self.handler = logging.StreamHandler(self)
        self.handler.setLevel(log_level)

    @pyqtSlot()
    def write(self, data):
        self.buffer += data

    @pyqtSlot()
    def flush(self):
        self.flush_signal.emit(str(self.buffer))
        self.buffer = ''
