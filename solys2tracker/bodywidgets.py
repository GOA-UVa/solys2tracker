"""
This module contains the main tabs that will be present in the application.

It exports the following classes:
    * ConfigurationWidget: The Configuration Tab.
"""

"""___Built-In Modules___"""
from typing import List, Tuple
import time

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from solys2 import solys2 as s2
from solys2 import autotrack as aut

"""___Solys2Tracker Modules___"""
try:
    from .s2ttypes import ConnectionStatus, BodyEnum
    from . import constants
    from . import ifaces
    from . import noconflict
    from .common import add_spacer, LoggerDialog
except:
    import constants
    import ifaces
    import noconflict
    from s2ttypes import ConnectionStatus, BodyEnum
    from common import add_spacer, LoggerDialog

"""___Authorship___"""
__author__ = 'Javier Gatón Herguedas'
__created__ = "2022/03/18"
__maintainer__ = "Javier Gatón Herguedas"
__email__ = "gaton@goa.uva.es"
__status__ = "Development"

class BodyMenuWidget(QtWidgets.QWidget):
    """
    Body page representing the menu, which will contain the available options for the user.
    """
    def __init__(self, body_tab: ifaces.IBodyTabWidget, title_str: str, options: List[str]):
        """
        Parameters
        ----------
        body_tab : ifaces.IBodyTabWidget
            Parent body tab that contains this page.
        title_str : str
            Title string that will be shown
        options : list of str
            Options that the menu tab will have
        """
        super().__init__()
        self.body_tab = body_tab
        self.title_str = title_str
        self.options = options
        self._build_layout()
    
    def _assign_button(self, option):
        but = QtWidgets.QPushButton(option)
        but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        but.clicked.connect(lambda: self.button_press(option))
        return but

    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.v_spacers = []
        self.h_spacers = []
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Content
        self.content_layout = QtWidgets.QVBoxLayout()
        self.buttons = []
        for option in self.options:
            but = self._assign_button(option)
            add_spacer(self.content_layout, self.v_spacers)
            self.content_layout.addWidget(but)
            self.buttons.append(but)
        add_spacer(self.content_layout, self.v_spacers)
        # Finish layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.content_layout, 1)
        add_spacer(self.main_layout, self.v_spacers)
    
    @QtCore.Slot()
    def button_press(self, option: str):
        """
        Option button has been pressed.
        
        Parameters
        ----------
        option : str
            Pressed option.
        """
        self.body_tab.change_to_view(option)

class BodyTrackWidget(QtWidgets.QWidget):
    """
    Body page that contains the tracking functionality.
    """
    def __init__(self, body_tab: ifaces.IBodyTabWidget, body: BodyEnum, conn_status: ConnectionStatus,
        logfile: str = "log.temp.out.txt", kernels_path: str = ""):
        """
        Parameters
        ----------
        body_tab : ifaces.IBodyTabWidget
            Parent body tab that contains this page.
        body : BodyEnum
            Body (moon or sun) of the body_tab.
        conn_status : ConnectionStatus
            Connection data and status.
        logfile : str
            Output logfile. By default is "log.temp.out.txt".
        kernels_path : str
            In case that SPICE is used, the path where the kernels directory is located
            must be specified.
        """
        super().__init__()
        self.body_tab = body_tab
        self.body = body
        self.title_str = "SUN"
        if body != BodyEnum.SUN:
            self.title_str = "MOON"
        self.title_str = self.title_str + " | " + constants.TRACK_STR
        self.conn_status = conn_status
        self.logfile = logfile
        self.kernels_path = kernels_path
        self._build_layout()

    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.v_spacers = []
        self.h_spacers = []
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Content
        self.content_layout = QtWidgets.QVBoxLayout()
        # Input
        self.input_layout = QtWidgets.QVBoxLayout()
        # Seconds
        self.seconds_layout = QtWidgets.QHBoxLayout()
        self.seconds_label = QtWidgets.QLabel("Seconds:")
        self.seconds_input = QtWidgets.QDoubleSpinBox()
        self.seconds_input.setMinimum(1)
        self.seconds_input.setMaximum(10000)
        self.seconds_input.setValue(10)
        add_spacer(self.seconds_layout, self.h_spacers)
        self.seconds_layout.addWidget(self.seconds_label)
        add_spacer(self.seconds_layout, self.h_spacers)
        self.seconds_layout.addWidget(self.seconds_input)
        add_spacer(self.seconds_layout, self.h_spacers)
        # Altitude
        self.altitude_layout = QtWidgets.QHBoxLayout()
        self.altitude_label = QtWidgets.QLabel("Height:")
        self.altitude_input = QtWidgets.QDoubleSpinBox()
        self.altitude_input.setMaximum(1000000)
        add_spacer(self.altitude_layout, self.h_spacers)
        self.altitude_layout.addWidget(self.altitude_label)
        add_spacer(self.altitude_layout, self.h_spacers)
        self.altitude_layout.addWidget(self.altitude_input)
        add_spacer(self.altitude_layout, self.h_spacers)
        # Finish input
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.seconds_layout)
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.altitude_layout)
        add_spacer(self.input_layout, self.v_spacers)
        self.content_layout.addLayout(self.input_layout)
        # Logger
        self.log_handler = LoggerDialog()
        self.content_layout.addWidget(self.log_handler)
        self.log_handlers = [self.log_handler.get_handler()]
        self.log_handler.setVisible(False)
        # Finish content
        self.track_button = QtWidgets.QPushButton("Start")
        self.track_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.track_button.clicked.connect(self.track_button_press)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_button.clicked.connect(self.cancel_button_press)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.track_button)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.cancel_button)
        add_spacer(self.content_layout, self.v_spacers)
        self.cancel_button.setVisible(False)
        # Finish layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.content_layout, 1)
        add_spacer(self.main_layout, self.v_spacers)

    @QtCore.Slot()
    def track_button_press(self):
        """
        Slot for the GUI action of pressing the start tracking button.
        """
        self.track_button.setEnabled(False)
        self.body_tab.set_disabled_navbar(True)
        self.seconds_input.setDisabled(True)
        self.altitude_input.setDisabled(True)
        self.log_handler.setVisible(True)
        self.body_tab.set_enabled_close_button(False)
        try:
            cs = self.conn_status
            seconds = self.seconds_input.value()
            altitude = self.altitude_input.value()
            if self.body == BodyEnum.SUN:
                library = aut.psc.SunLibrary.SPICEDSUN
                if self.kernels_path is None or self.kernels_path == "":
                    library = aut.psc.SunLibrary.PYSOLAR
                self.tracker = aut.SunTracker(cs.ip, seconds, cs.port, cs.password, True,
                    self.logfile, library, altitude, self.kernels_path, self.log_handlers)
            else:
                library = aut.psc.MoonLibrary.SPICEDMOON
                if self.kernels_path is None or self.kernels_path == "":
                    library = aut.psc.MoonLibrary.EPHEM_MOON
                self.tracker = aut.MoonTracker(cs.ip, seconds, cs.port, cs.password, True, self.logfile,
                    library, altitude, self.kernels_path, self.log_handlers)
            self.cancel_button.setVisible(True)
            add_spacer(self.content_layout, self.v_spacers)
        except:
            self.finished_tracking()

    class TrackFinisherWorker(QtCore.QObject):
        """
        Worker that will finish the tracking.
        """
        finished = QtCore.Signal()

        def __init__(self, tracker: aut._BodyTracker):
            """
            Parameters
            ----------
            tracker : _BodyTracker
                bodytracker that will track the celestial body.
            """
            super().__init__()
            self.bt = tracker

        def run(self):
            self.bt.stop_tracking()
            while not self.bt.is_finished():
                time.sleep(1)
            self.finished.emit()

    @QtCore.Slot()
    def cancel_button_press(self):
        "Slot for the GUI action of pressing the cancel tracking button."
        self.cancel_button.setDisabled(True)
        self.th = QtCore.QThread()
        self.worker = BodyTrackWidget.TrackFinisherWorker(self.tracker)
        self.worker.moveToThread(self.th)
        self.th.started.connect(self.worker.run)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.finished_tracking)
        self.th.finished.connect(self.th.deleteLater)
        self.th.start()
    
    def finished_tracking(self):
        """Tracking finished/stopped. Perform the needed actions."""
        self.body_tab.set_enabled_close_button(True)
        self.log_handler.end_handler()
        self.cancel_button.setDisabled(False)
        self.cancel_button.setVisible(False)
        self.seconds_input.setDisabled(False)
        self.altitude_input.setDisabled(False)
        self.track_button.setEnabled(True)
        self.body_tab.set_disabled_navbar(False)

class BodyCrossWidget(QtWidgets.QWidget):
    def __init__(self, body_tab: ifaces.IBodyTabWidget, title_str: str):
        super().__init__()
        self.body_tab = body_tab
        self.title_str = title_str + " | " + constants.CROSS_STR
        self._build_layout()

    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.v_spacers = []
        self.h_spacers = []
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Content
        self.content_layout = QtWidgets.QVBoxLayout()
        # Finish layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.content_layout, 1)
        add_spacer(self.main_layout, self.v_spacers)

class BodyBlackWidget(QtWidgets.QWidget):
    def __init__(self, body_tab: ifaces.IBodyTabWidget, title_str: str):
        super().__init__()
        self.body_tab = body_tab
        self.title_str = title_str + " | " + constants.BLACK_STR
        self._build_layout()

    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.v_spacers = []
        self.h_spacers = []
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Content
        self.content_layout = QtWidgets.QVBoxLayout()
        # Finish layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.content_layout, 1)
        add_spacer(self.main_layout, self.v_spacers)
