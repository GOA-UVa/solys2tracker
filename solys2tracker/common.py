"""Common
This module contains functionalities that are used in multiple modules.

It exports the following functions:
    * add_spacer: Adds a QSpacerItem to the layout, and adds it to the spacers list.
"""

"""___Built-In Modules___"""
from typing import List
import logging
import random
import sys
import string
from os import path as os_path, system as os_system, getpid as os_getpid, kill as os_kill

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from asdcontroller import asd_types as asdt

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

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os_path.join(sys._MEIPASS, relative_path)
    return os_path.join(os_path.abspath('.'), relative_path)

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


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes: Axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    def resizeEvent(self, event):
        result = super().resizeEvent(event)
        fig = self.axes.get_figure()
        if fig:
            fig.tight_layout()
        return result

class GraphWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.xlabel = ""
        self.ylabel = ""
        self._build_layout()

    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.canvas = MplCanvas(self)
        self.main_layout.addWidget(self.canvas)

    def update_plot(self, x_data: list, y_data: list):
        self.x_data = x_data
        self.y_data = y_data
        self.redraw()

    def update_labels(self, title: str, xlabel: str, ylabel: str):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
    
    def redraw(self):
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.x_data, self.y_data, "o",  markersize=2)
        self.canvas.axes.set_title(self.title)
        self.canvas.axes.set_xlabel(self.xlabel)
        self.canvas.axes.set_ylabel(self.ylabel)
        self.canvas.axes.grid(True)
        fig = self.canvas.axes.get_figure()
        if fig:
            fig.tight_layout()
        self.canvas.draw()
        if fig:
            fig.tight_layout()

class CaptureDataWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._build_layout()

    def _build_layout(self):
        self.v_spacers = []
        self.h_spacers = []
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # Headers
        self.headers_layout = QtWidgets.QHBoxLayout()
        self.label_itime = QtWidgets.QLabel("Integration time:")
        self.label_drift = QtWidgets.QLabel("VNIR Drift:")
        self.label_gain1 = QtWidgets.QLabel("Swir1 gain:")
        self.label_gain2 = QtWidgets.QLabel("Swir2 gain:")
        self.label_v_itime = QtWidgets.QLabel("")
        self.label_v_drift = QtWidgets.QLabel("")
        self.label_v_gain1 = QtWidgets.QLabel("")
        self.label_v_gain2 = QtWidgets.QLabel("")
        self.sep_labels = [QtWidgets.QLabel(" | ") for _ in range(3)]
        add_spacer(self.headers_layout, self.h_spacers)
        self.headers_layout.addWidget(self.label_itime)
        self.headers_layout.addWidget(self.label_v_itime)
        add_spacer(self.headers_layout, self.h_spacers)
        self.headers_layout.addWidget(self.sep_labels[0])
        add_spacer(self.headers_layout, self.h_spacers)
        self.headers_layout.addWidget(self.label_drift)
        self.headers_layout.addWidget(self.label_v_drift)
        add_spacer(self.headers_layout, self.h_spacers)
        self.headers_layout.addWidget(self.sep_labels[1])
        add_spacer(self.headers_layout, self.h_spacers)
        self.headers_layout.addWidget(self.label_gain1)
        self.headers_layout.addWidget(self.label_v_gain1)
        add_spacer(self.headers_layout, self.h_spacers)
        self.headers_layout.addWidget(self.sep_labels[2])
        add_spacer(self.headers_layout, self.h_spacers)
        self.headers_layout.addWidget(self.label_gain2)
        self.headers_layout.addWidget(self.label_v_gain2)
        add_spacer(self.headers_layout, self.h_spacers)
        # Graph
        self.graph = GraphWidget()
        # Finish main layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.headers_layout)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.graph, 1)
        add_spacer(self.main_layout, self.v_spacers)

    def update_plot(self, x_data: list, y_data: list):
        self.graph.update_plot(x_data, y_data)

    def update_labels(self, title: str, xlabel: str, ylabel: str):
        self.graph.update_labels(title, xlabel, ylabel)
    
    def update_headers(self, spec: asdt.FRInterpSpec):
        vh = spec.fr_spectrum_header.v_header
        s1 = spec.fr_spectrum_header.s1_header
        s2 = spec.fr_spectrum_header.s2_header
        self.label_v_itime.setText(asdt.ITimeEnum(vh.it).to_str())
        self.label_v_drift.setText(str(vh.drift))
        self.label_v_gain1.setText(str(s1.gain))
        self.label_v_gain2.setText(str(s2.gain))

class GraphWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph = CaptureDataWidget()
        self.should_close = False
        self.setCentralWidget(self.graph)
    
    def closeEvent(self, event: QtGui.QCloseEvent):
        if self.should_close:
            super().closeEvent(event)
        else:
            event.ignore()
    
    def force_close(self):
        self.should_close = True
        self.close()

    def update_plot(self, x_data: list, y_data: list):
        self.graph.update_plot(x_data, y_data)

    def update_labels(self, title: str, xlabel: str, ylabel: str):
        self.graph.update_labels(title, xlabel, ylabel)
    
    def update_headers(self, spec: asdt.FRInterpSpec):
        self.graph.update_headers(spec)

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
