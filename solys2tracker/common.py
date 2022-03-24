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

class LogWorker(QtCore.QObject):
    data_ready = QtCore.Signal(str)

    def callback(self, msg: str):
        self.data_ready.emit(msg)

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
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

    def get_handler(self) -> logging.Handler:
        return self.logTextBox