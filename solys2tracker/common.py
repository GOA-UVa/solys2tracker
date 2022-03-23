"""Common
This module contains functionalities that are used in multiple modules.

It exports the following functions:
    * add_spacer: Adds a QSpacerItem to the layout, and adds it to the spacers list.
"""

"""___Built-In Modules___"""
from typing import List
import logging

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

class QTextEditLogger(logging.Handler):
    def __init__(self, worker: 'LoggerWorker'):
        super().__init__()
        self.worker = worker

    def emit(self, record):
        msg = self.format(record)
        self.worker.log(msg)

class LoggerWorker(QtCore.QObject):
    """
    Worker that will log the messages
    """
    created = QtCore.Signal(logging.Handler)
    log_msg = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.handler = QTextEditLogger(self)
    
    def log(self, record):
        self.log_msg.emit(record)

    def run(self):
        self.created.emit(self.handler)

class LoggerDialog(QtWidgets.QDialog, QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.widget = QtWidgets.QPlainTextEdit(self)
        self.widget.setReadOnly(True)

        self.th = QtCore.QThread()
        self.worker = LoggerWorker()
        self.worker.moveToThread(self.th)
        self.th.started.connect(self.worker.run)
        #self.worker.finished.connect(self.th.quit)
        #self.worker.finished.connect(self.worker.deleteLater)
        self.worker.created.connect(self.save_handler)
        self.worker.log_msg.connect(self.log)
        self.th.finished.connect(self.th.deleteLater)
        self.th.start()

        self.logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        layout = QtWidgets.QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(self.widget)
        self.setLayout(layout)
    
    def save_handler(self, handler: logging.Handler):
        self.logTextBox = handler
    
    def log(self, msg: str):
        self.widget.appendPlainText(msg)
    
    def get_handler(self) -> logging.Handler:
        return self.logTextBox