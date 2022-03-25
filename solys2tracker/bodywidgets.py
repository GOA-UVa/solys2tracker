"""
This module contains the pages widgets that will be present in each body tab.

It exports the following classes:
    * BodyMenuWidget: Body page representing the menu, which will contain the available
        options for the user.
    * BodyTrackWidget Body page that contains the tracking functionality.
    * BodyCrossWidget: Body page that contains the cross and mesh functionalities.
    * BodyBlackWidget: Body page that contains the black moon functionality.
"""

"""___Built-In Modules___"""
from typing import List, Tuple
import time
from threading import Thread, Lock
import logging

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
    from .common import add_spacer, LoggerDialog, get_custom_logger, LogWorker
except:
    import constants
    import ifaces
    import noconflict
    from s2ttypes import ConnectionStatus, BodyEnum
    from common import add_spacer, LoggerDialog, get_custom_logger, LogWorker

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
    def __init__(self, body_tab: ifaces.IBodyTabWidget, title_str: str, options: List[str], description_str: str):
        """
        Parameters
        ----------
        body_tab : ifaces.IBodyTabWidget
            Parent body tab that contains this page.
        title_str : str
            Title string that will be shown
        options : list of str
            Options that the menu tab will have
        description_str : str
            Description string that will be shown
        """
        super().__init__()
        self.body_tab = body_tab
        self.title_str = title_str
        self.description_str = description_str
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
        # Description
        self.title = QtWidgets.QLabel(self.description_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_description")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.description_str)
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
        self.log_handler.start_handler()
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
    """
    Body page that contains the cross and mesh functionalities.
    """
    def __init__(self, body_tab: ifaces.IBodyTabWidget, body: BodyEnum, conn_status: ConnectionStatus,
        logfile: str = "log.temp.out.txt", kernels_path: str = "", is_mesh: bool = False):
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
        is_mesh : bool
            Flag that indicates that the operation should be a mesh instead of a cross.
        """
        super().__init__()
        self.body_tab = body_tab
        self.body = body
        self.title_str = "SUN"
        self.is_mesh = is_mesh
        if body != BodyEnum.SUN:
            self.title_str = "MOON"
        self.op_name = constants.CROSS_STR
        if is_mesh:
            self.op_name = constants.MESH_STR
        self.title_str = self.title_str + " | " + self.op_name
        self.conn_status = conn_status
        self.logfile = logfile
        self.kernels_path = kernels_path
        self._build_layout()

    class QLabelCrossCountdownLogger(logging.Handler):
        def __init__(self, label: QtWidgets.QLabel):
            super().__init__()
            self.widget = label
        
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
            if "COUNTDOWN:" in msg:
                num_str = msg[msg.rindex(':')+1:]
                self.worker.callback(num_str)

        def handle_data(self, msg: str):
            try:
                num = float(msg)
                if num > 0:
                    label_msg = msg
                else:
                    label_msg = "MEASURE NOW"
            except:
                label_msg = "ERROR"
            self.widget.setText(label_msg)

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
        # Range
        self.range_layout = QtWidgets.QHBoxLayout()
        self.range_label = QtWidgets.QLabel("Range (°):", alignment=QtCore.Qt.AlignCenter)
        self.range_first_input = QtWidgets.QDoubleSpinBox()
        self.range_second_input = QtWidgets.QDoubleSpinBox()
        self.range_first_input.setMinimum(-100)
        self.range_first_input.setMaximum(100)
        self.range_first_input.setValue(-1.5)
        self.range_second_input.setMinimum(-100)
        self.range_second_input.setMaximum(100)
        self.range_second_input.setValue(1.5)
        add_spacer(self.range_layout, self.h_spacers)
        self.range_layout.addWidget(self.range_label)
        add_spacer(self.range_layout, self.h_spacers)
        self.range_layout.addWidget(self.range_first_input)
        add_spacer(self.range_layout, self.h_spacers)
        self.range_layout.addWidget(self.range_second_input)
        add_spacer(self.range_layout, self.h_spacers)
        # Step
        self.step_layout = QtWidgets.QHBoxLayout()
        self.step_label = QtWidgets.QLabel("Step (°):", alignment=QtCore.Qt.AlignCenter)
        self.step_input = QtWidgets.QDoubleSpinBox()
        self.step_input.setMinimum(-100)
        self.step_input.setMaximum(100)
        self.step_input.setValue(0.3)
        add_spacer(self.step_layout, self.h_spacers)
        self.step_layout.addWidget(self.step_label)
        add_spacer(self.step_layout, self.h_spacers)
        self.step_layout.addWidget(self.step_input)
        add_spacer(self.step_layout, self.h_spacers)
        # Countdown
        self.countdown_layout = QtWidgets.QHBoxLayout()
        self.countdown_label = QtWidgets.QLabel("Countdown (sec.):", alignment=QtCore.Qt.AlignCenter)
        self.countdown_input = QtWidgets.QSpinBox()
        self.countdown_input.setMinimum(-100)
        self.countdown_input.setMaximum(100)
        self.countdown_input.setValue(5)
        add_spacer(self.countdown_layout, self.h_spacers)
        self.countdown_layout.addWidget(self.countdown_label)
        add_spacer(self.countdown_layout, self.h_spacers)
        self.countdown_layout.addWidget(self.countdown_input)
        add_spacer(self.countdown_layout, self.h_spacers)
        # Rest
        self.rest_layout = QtWidgets.QHBoxLayout()
        self.rest_label = QtWidgets.QLabel("Rest (sec.):", alignment=QtCore.Qt.AlignCenter)
        self.rest_input = QtWidgets.QSpinBox()
        self.rest_input.setMinimum(-100)
        self.rest_input.setMaximum(100)
        self.rest_input.setValue(1)
        add_spacer(self.rest_layout, self.h_spacers)
        self.rest_layout.addWidget(self.rest_label)
        add_spacer(self.rest_layout, self.h_spacers)
        self.rest_layout.addWidget(self.rest_input)
        add_spacer(self.rest_layout, self.h_spacers)
        # Height
        self.height_layout = QtWidgets.QHBoxLayout()
        self.height_label = QtWidgets.QLabel("Height (m):", alignment=QtCore.Qt.AlignCenter)
        self.height_input = QtWidgets.QSpinBox()
        self.height_input.setMinimum(-1000)
        self.height_input.setMaximum(1000000)
        self.height_input.setValue(0)
        add_spacer(self.height_layout, self.h_spacers)
        self.height_layout.addWidget(self.height_label)
        add_spacer(self.height_layout, self.h_spacers)
        self.height_layout.addWidget(self.height_input)
        add_spacer(self.height_layout, self.h_spacers)
        # Countdown
        self.log_countdown_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.log_countdown_label.setObjectName("countdown")
        self.log_countdown = BodyCrossWidget.QLabelCrossCountdownLogger(self.log_countdown_label)
        self.log_handlers = [self.log_countdown]
        self.log_countdown_label.setVisible(False)
        # Logger
        self.log_handler = LoggerDialog()
        self.log_handlers += [self.log_handler.get_handler()]
        self.log_handler.setVisible(False)
        # Start button
        self.start_button = QtWidgets.QPushButton("Start {}".format(self.op_name))
        self.start_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start_button.clicked.connect(self.press_start_cross)
        # Cancel button
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_button.clicked.connect(self.cancel_button_press)
        self.cancel_button.setVisible(False)
        # Finish content
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addLayout(self.range_layout)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addLayout(self.step_layout)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addLayout(self.countdown_layout)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addLayout(self.rest_layout)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.log_countdown_label)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.log_handler)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.start_button)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.cancel_button)
        add_spacer(self.content_layout, self.v_spacers)
        # Finish layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.content_layout, 1)
        add_spacer(self.main_layout, self.v_spacers)

    @QtCore.Slot()
    def press_start_cross(self):
        """
        Slot for the GUI action of pressing the start cross/mesh button.
        """
        self.start_button.setEnabled(False)
        self.body_tab.set_disabled_navbar(True)
        self.range_first_input.setDisabled(True)
        self.range_second_input.setDisabled(True)
        self.step_input.setDisabled(True)
        self.countdown_input.setDisabled(True)
        self.rest_input.setDisabled(True)
        self.log_handler.setVisible(True)
        self.log_handler.start_handler()
        self.log_countdown_label.setVisible(True)
        self.log_countdown.start_handler()
        self.body_tab.set_enabled_close_button(False)
        self.is_finished = aut._ContainedBool(False)
        try:
            cs = self.conn_status
            az_min = ze_min = self.range_first_input.value()
            az_max = ze_max = self.range_second_input.value()
            az_step = ze_step = self.step_input.value()
            countdown = self.countdown_input.value()
            rest = self.rest_input.value()
            cp = aut.CrossParameters(az_min, az_max, az_step, ze_min, ze_max, ze_step, countdown, rest)
            altitude = self.height_input.value()
            logger = get_custom_logger(self.logfile, self.log_handlers)
            self.mutex_cont = Lock()
            self.cont_cross = aut._ContainedBool(True)
            if self.body == BodyEnum.SUN:
                library = aut.psc.SunLibrary.SPICEDSUN
                if self.kernels_path is None or self.kernels_path == "":
                    library = aut.psc.SunLibrary.PYSOLAR
                func = aut.solar_cross
                if self.is_mesh:
                    func = aut.solar_mesh
            else:
                library = aut.psc.MoonLibrary.SPICEDMOON
                if self.kernels_path is None or self.kernels_path == "":
                    library = aut.psc.MoonLibrary.EPHEM_MOON
                func = aut.lunar_cross
                if self.is_mesh:
                    func = aut.lunar_mesh
            self.cross_thread = Thread(target=func, args=[cs.ip, logger, cp,
                cs.port, cs.password, self.is_finished, library, altitude,
                self.kernels_path, self.mutex_cont, self.cont_cross])
            self.cross_thread.start()
            self.cancel_button.setVisible(True)
            self.start_checking_cross_end()
        except:
            self.finished_crossing()
    
    class CrossWorker(QtCore.QObject):
        """
        Worker that will check for the cross to finish.
        """
        finished = QtCore.Signal()

        def __init__(self, is_finished: aut._ContainedBool):
            """
            Parameters
            ----------
            is_finished : _ContainedBool
                Contained bool that contains the info that if the cross has finished.
            """
            super().__init__()
            self.is_finished = is_finished

        def run(self):
            while not self.is_finished.value:
                time.sleep(1)
            self.finished.emit()

    def start_checking_cross_end(self):
        self.th = QtCore.QThread()
        self.worker = BodyCrossWidget.CrossWorker(self.is_finished)
        self.worker.moveToThread(self.th)
        self.th.started.connect(self.worker.run)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.finished_crossing)
        self.th.finished.connect(self.th.deleteLater)
        self.th.start()

    @QtCore.Slot()
    def cancel_button_press(self):
        "Slot for the GUI action of pressing the cancel crossing button."
        self.cancel_button.setDisabled(True)
        self.mutex_cont.acquire()
        self.cont_cross.value = False
        self.mutex_cont.release()
    
    def finished_crossing(self):
        """Crossing finished/stopped. Perform the needed actions."""
        self.body_tab.set_enabled_close_button(True)
        self.log_handler.end_handler()
        self.log_countdown.end_logger()
        self.cancel_button.setDisabled(False)
        self.cancel_button.setVisible(False)
        self.start_button.setEnabled(True)
        self.body_tab.set_disabled_navbar(False)
        self.range_first_input.setDisabled(False)
        self.range_second_input.setDisabled(False)
        self.step_input.setDisabled(False)
        self.countdown_input.setDisabled(False)
        self.rest_input.setDisabled(False)
        self.body_tab.set_disabled_navbar(False)

class BodyBlackWidget(QtWidgets.QWidget):
    """
    Body page that contains the black moon functionality.
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
        self.title_str = self.title_str + " | " + constants.BLACK_STR
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
        # Start button
        self.start_button = QtWidgets.QPushButton("Perform Black", alignment=QtCore.Qt.AlignCenter)
        self.start_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start_button.clicked.connect(self.press_start_black)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.start_button)
        # Logger
        self.log_handler = LoggerDialog()
        self.log_handlers = [self.log_handler.get_handler()]
        self.log_handler.setVisible(False)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.log_handler)
        # Finish content
        add_spacer(self.content_layout, self.v_spacers)
        # Finish layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.content_layout, 1)
        add_spacer(self.main_layout, self.v_spacers)
    
    @QtCore.Slot()
    def press_start_black(self):
        """
        Slot for the GUI action of pressing the start cross button.
        """
        self.start_button.setEnabled(False)
        self.body_tab.set_disabled_navbar(True)
        self.log_handler.setVisible(True)
        self.log_handler.start_handler()
        self.body_tab.set_enabled_close_button(False)
        self.is_finished = aut._ContainedBool(False)
        try:
            cs = self.conn_status
            altitude = 0
            logger = get_custom_logger(self.logfile, self.log_handlers)
            library = aut.psc.MoonLibrary.SPICEDMOON
            if self.kernels_path is None or self.kernels_path == "":
                library = aut.psc.MoonLibrary.EPHEM_MOON
            self.black_thread = Thread(target=aut.black_moon, args=[cs.ip, logger, cs.port,
                cs.password, self.is_finished, library, altitude, self.kernels_path])
            self.black_thread.start()
            self.start_checking_black_end()
        except:
            self.finished_black()

    class BlackWorker(QtCore.QObject):
        """
        Worker that will check for the black to finish.
        """
        finished = QtCore.Signal()

        def __init__(self, is_finished: aut._ContainedBool):
            """
            Parameters
            ----------
            is_finished : _ContainedBool
                Contained bool that contains the info that if the black has finished.
            """
            super().__init__()
            self.is_finished = is_finished

        def run(self):
            while not self.is_finished.value:
                time.sleep(1)
            self.finished.emit()

    def start_checking_black_end(self):
        self.th = QtCore.QThread()
        self.worker = BodyBlackWidget.BlackWorker(self.is_finished)
        self.worker.moveToThread(self.th)
        self.th.started.connect(self.worker.run)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.finished_black)
        self.th.finished.connect(self.th.deleteLater)
        self.th.start()
    
    def finished_black(self):
        """Black finished/stopped. Perform the needed actions."""
        self.body_tab.set_enabled_close_button(True)
        self.log_handler.end_handler()
        self.start_button.setEnabled(True)
        self.body_tab.set_disabled_navbar(False)
        self.body_tab.set_disabled_navbar(False)
