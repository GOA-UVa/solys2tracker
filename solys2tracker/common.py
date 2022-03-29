"""Common
This module contains functionalities that are used in multiple modules.

It exports the following functions:
    * add_spacer: Adds a QSpacerItem to the layout, and adds it to the spacers list.
"""

"""___Built-In Modules___"""
from typing import List
import logging
import random
import string

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore

"""___Solys2Tracker Modules___"""
# import here

"""___Authorship___"""
__author__ = 'Javier Gatón Herguedas'
__created__ = "2022/03/22"
__maintainer__ = "Javier Gatón Herguedas"
__email__ = "gaton@goa.uva.es"
__status__ = "Development"

def add_spacer(layout: QtWidgets.QBoxLayout, spacers: List[QtWidgets.QSpacerItem], w: int = 0, h: int = 0):
    """
    Adds a QSpacerItem to the layout, and adds it to the spacers list.

    Parameters
    ----------
    layout : QBoxLayout
        QBoxLayout where the spacer will be added to.
    spacers : list of QSpacerItem
        List of QSpacerItem where the created spacer will be appended to.
    w : int
        Width of the spacer. Default 0.
    h : int
        Height of the spacer. Default 0.
    """
    spacer = QtWidgets.QSpacerItem(w, h)
    layout.addSpacerItem(spacer)
    spacers.append(spacer)

class LogWorker(QtCore.QObject):
    data_ready = QtCore.Signal(str)

    def callback(self, msg: str):
        self.data_ready.emit(msg)

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
    
    def start_handler(self):
        self.worker = LogWorker()

        # Mover worker to thread and connect signal
        self.th = QtCore.QThread()
        self.worker.data_ready.connect(self.handle_data)
        self.worker.moveToThread(self.th)
        self.th.finished.connect(self.th.deleteLater)
        self.th.start()

    def end_logger(self):
        self.th.quit()
        self.worker.deleteLater()

    def emit(self, record):
        msg = self.format(record)
        self.worker.callback(msg)

    def handle_data(self, msg: str):
        self.widget.appendPlainText(msg)
        self.widget.verticalScrollBar().setValue(self.widget.verticalScrollBar().maximum())

class LoggerDialog(QtWidgets.QDialog, QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logTextBox.setLevel(logging.INFO)

        layout = QtWidgets.QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(self.logTextBox.widget)
        self.setLayout(layout)
    
    def end_handler(self):
        self.logTextBox.end_logger()
    
    def start_handler(self):
        self.logTextBox.start_handler()

    def get_handler(self) -> logging.Handler:
        return self.logTextBox

def _gen_random_str(len: int) -> str:
    """
    Return a random str of the specified length.

    Parameters
    ----------
    len : int
        Length of the desired str.

    Returns
    -------
    rand_str : str
        Generated random str of the specified length.
    """
    return ''.join(random.choice(string.ascii_letters) for i in range(len))

def get_custom_logger(logfile: str, extra_log_handlers: List[logging.Handler]) -> logging.Logger:
    """Configure the logging output
    
    Shell logging at warning level and file logger at debug level if log is True.

    Parameters
    ----------
    log : bool
        True if some logging is required. Otherwise silent except for warnings and errors.
    logfile : str
        Path of the file where the logging will be stored. In case that it's not used, it will be
        printed in stderr.
    extra_log_handlers : list of logging.Handler
        Custom handlers which the log will also log to.
    """
    randstr = _gen_random_str(20)
    logging.basicConfig(level=logging.WARNING)
    for handler in logging.getLogger().handlers:
        handler.setLevel(logging.WARNING)
    logger = logging.getLogger('solys2tracker-{}'.format(randstr))
    for hand in extra_log_handlers:
        logger.addHandler(hand)
    if logfile != "":
        log_handler = logging.FileHandler(logfile, mode='a')
        log_handler.setFormatter(logging.Formatter('%(levelname)s:%(message)s'))
        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
    return logger
