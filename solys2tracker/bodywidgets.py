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
from typing import Callable, List, Union, Tuple
import time
from threading import Thread
import logging
from os import path
from datetime import datetime

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from solys2.automation import autotrack as aut
from solys2.automation import calibration as cali
from solys2.automation import positioncalc as psc
from solys2 import common
import numpy as np

"""___Solys2Tracker Modules___"""
try:
    from solys2tracker.s2ttypes import SessionStatus, BodyEnum
    from solys2tracker import constants
    from solys2tracker import ifaces
    from solys2tracker.common import add_spacer, LoggerDialog, get_custom_logger, LogWorker
except:
    import constants
    import ifaces
    from s2ttypes import SessionStatus, BodyEnum
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
        but = QtWidgets.QPushButton(option.upper())
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
        self.description = QtWidgets.QLabel(self.description_str, alignment=QtCore.Qt.AlignCenter)
        self.description.setObjectName("section_description")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.description)
        # Content
        self.content_layout = QtWidgets.QVBoxLayout()
        self.buttons = []
        for option in self.options:
            but = self._assign_button(option)
            but.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
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

_TRACK_LOGTITLE = "TRACK"
_CROSS_LOGTITLE = "CROSS"
_MESH_LOGTITLE = "MESH"
_BLACK_LOGTITLE = "BLACK"

def _create_log_file_name(logfolder: str, option: str) -> str:
    dt = datetime.utcnow()
    dt_st = dt.strftime("%Y%m%d%H%M%S")
    logfile = "{}_{}.log.txt".format(option, dt_st)
    logfile = path.join(logfolder, logfile)
    return logfile

def _close_logger(logger: logging.Logger):
    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()

class BodyTrackWidget(QtWidgets.QWidget):
    """
    Body page that contains the tracking functionality.
    """
    def __init__(self, body_tab: ifaces.IBodyTabWidget, body: BodyEnum, session_status: SessionStatus,
        kernels_path: str = ""):
        """
        Parameters
        ----------
        body_tab : ifaces.IBodyTabWidget
            Parent body tab that contains this page.
        body : BodyEnum
            Body (moon or sun) of the body_tab.
        session_status : SessionStatus
            Connection data and status.
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
        self.session_status = session_status
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
        self.seconds_label = QtWidgets.QLabel("Seconds:", alignment=QtCore.Qt.AlignCenter)
        self.seconds_input = QtWidgets.QDoubleSpinBox()
        self.seconds_input.setMinimum(1)
        self.seconds_input.setMaximum(10000)
        self.seconds_input.setValue(10)
        add_spacer(self.seconds_layout, self.h_spacers)
        self.seconds_layout.addWidget(self.seconds_label)
        add_spacer(self.seconds_layout, self.h_spacers)
        self.seconds_layout.addWidget(self.seconds_input)
        add_spacer(self.seconds_layout, self.h_spacers)
        # Finish input
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.seconds_layout)
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
        self.log_handler.setVisible(True)
        self.log_handler.start_handler()
        self.body_tab.set_enabled_close_button(False)
        self.logfile = _create_log_file_name(self.session_status.logfolder, _TRACK_LOGTITLE)
        try:
            cs = self.session_status
            seconds = self.seconds_input.value()
            altitude = cs.height
            self.logger = common.create_file_logger(self.logfile, self.log_handlers, logging.WARNING)
            if self.body == BodyEnum.SUN:
                library = psc.SunLibrary.SPICEDSUN
                if self.kernels_path is None or self.kernels_path == "":
                    library = psc.SunLibrary.PYSOLAR
                self.tracker = aut.SunTracker(cs.ip, seconds, cs.port, cs.password, self.logger,
                    library, altitude, self.kernels_path)
            else:
                library = psc.MoonLibrary.SPICEDMOON
                if self.kernels_path is None or self.kernels_path == "":
                    library = psc.MoonLibrary.EPHEM_MOON
                self.tracker = aut.MoonTracker(cs.ip, seconds, cs.port, cs.password, self.logger,
                    library, altitude, self.kernels_path)
            self.tracker.start()
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
            self.bt.stop()
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
        _close_logger(self.logger)
        self.log_handler.end_handler()
        self.cancel_button.setDisabled(False)
        self.cancel_button.setVisible(False)
        self.seconds_input.setDisabled(False)
        self.track_button.setEnabled(True)
        self.body_tab.set_disabled_navbar(False)

class BodyCrossWidget(QtWidgets.QWidget):
    """
    Body page that contains the cross and mesh functionalities.
    """
    def __init__(self, body_tab: ifaces.IBodyTabWidget, body: BodyEnum, session_status: SessionStatus,
        kernels_path: str = "", is_mesh: bool = False):
        """
        Parameters
        ----------
        body_tab : ifaces.IBodyTabWidget
            Parent body tab that contains this page.
        body : BodyEnum
            Body (moon or sun) of the body_tab.
        session_status : SessionStatus
            Connection data and status.
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
        self.session_status = session_status
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
    
    class StepInfoHandler(logging.Handler):
        def __init__(self, callback_next_step: Callable):
            super().__init__()
            self.callback_next_step = callback_next_step
        
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
            if "COUNTDOWN:0" in msg:
                self.callback_next_step()

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
        self.range_first_input.setValue(-1)
        self.range_second_input.setMinimum(-100)
        self.range_second_input.setMaximum(100)
        self.range_second_input.setValue(1)
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
        self.step_input.setValue(0.1)
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
        self.countdown_input.setValue(3)
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
        self.rest_input.setValue(0)
        add_spacer(self.rest_layout, self.h_spacers)
        self.rest_layout.addWidget(self.rest_label)
        add_spacer(self.rest_layout, self.h_spacers)
        self.rest_layout.addWidget(self.rest_input)
        add_spacer(self.rest_layout, self.h_spacers)
        # Current step and remaining
        self.step_info_lay = QtWidgets.QHBoxLayout()
        self.next_step_label = QtWidgets.QLabel("Next step:", alignment=QtCore.Qt.AlignCenter)
        self.next_step = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.remaining_steps_label = QtWidgets.QLabel("Remaining steps:", alignment=QtCore.Qt.AlignCenter)
        self.rem_steps = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        add_spacer(self.step_info_lay, self.h_spacers)
        self.step_info_lay.addWidget(self.next_step_label)
        add_spacer(self.step_info_lay, self.h_spacers)
        self.step_info_lay.addWidget(self.next_step)
        add_spacer(self.step_info_lay, self.h_spacers)
        self.step_info_lay.addWidget(self.remaining_steps_label)
        add_spacer(self.step_info_lay, self.h_spacers)
        self.step_info_lay.addWidget(self.rem_steps)
        add_spacer(self.step_info_lay, self.h_spacers)
        self.step_info_set_visible(False)
        self.step_info_handler = BodyCrossWidget.StepInfoHandler(self.next_step_detected)
        self.log_handlers = [self.step_info_handler]
        # Countdown
        self.log_countdown_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.log_countdown_label.setObjectName("countdown")
        self.log_countdown = BodyCrossWidget.QLabelCrossCountdownLogger(self.log_countdown_label)
        self.log_handlers += [self.log_countdown]
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
        self.content_layout.addLayout(self.step_info_lay)
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

    def step_info_set_visible(self, visible: bool):
        self.next_step_label.setVisible(visible)
        self.next_step.setVisible(visible)
        self.remaining_steps_label.setVisible(visible)
        self.rem_steps.setVisible(visible)

    def update_info_steps(self):
        if self.measured_steps < len(self.steps):
            next_offset = self.steps[self.measured_steps]
            self.next_step.setText("A{:+.2f}; Z{:+.2f}".format(next_offset[0], next_offset[1]))
        else:
            self.next_step.setText("Finished")
        self.rem_steps.setText("{}".format(len(self.steps)-self.measured_steps))

    def next_step_detected(self):
        self.measured_steps += 1
        self.update_info_steps()

    def generate_steps(self, cp: cali.CalibrationParameters):
        # Generating the offsets for the visual feedback
        if self.is_mesh:
            offsets: List[Tuple[float, float]] = []
            for i in np.arange(cp.azimuth_min_offset, cp.azimuth_max_offset + cp.azimuth_step,
                    cp.azimuth_step):
                for j in np.arange(cp.zenith_min_offset, cp.zenith_max_offset + cp.zenith_step,
                        cp.zenith_step):
                    offsets.append((i,j))
        else:
            offsets: List[Tuple[float, float]] = \
                [(i, 0) for i in np.arange(cp.azimuth_min_offset, cp.azimuth_max_offset +
                    cp.azimuth_step, cp.azimuth_step)]
            offsets += [(0, i) for i in np.arange(cp.zenith_min_offset, cp.zenith_max_offset +
                cp.zenith_step, cp.zenith_step)]
        self.steps = offsets
        self.measured_steps = 0
        self.update_info_steps()

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
        self.step_info_set_visible(True)
        self.log_countdown.start_handler()
        self.body_tab.set_enabled_close_button(False)
        option = _CROSS_LOGTITLE
        if self.is_mesh:
            option = _MESH_LOGTITLE
        self.logfile = _create_log_file_name(self.session_status.logfolder, option)
        try:
            cs = self.session_status
            az_min = ze_min = self.range_first_input.value()
            az_max = ze_max = self.range_second_input.value()
            az_step = ze_step = self.step_input.value()
            countdown = self.countdown_input.value()
            rest = self.rest_input.value()
            cp = cali.CalibrationParameters(az_min, az_max, az_step, ze_min, ze_max, ze_step,
                countdown, rest)
            self.generate_steps(cp)
            altitude = self.session_status.height
            self.logger = get_custom_logger(self.logfile, self.log_handlers)
            if self.body == BodyEnum.SUN:
                library = psc.SunLibrary.SPICEDSUN
                if self.kernels_path is None or self.kernels_path == "":
                    library = psc.SunLibrary.PYSOLAR
                if self.is_mesh:
                    self.crosser = cali.SolarMesh(cs.ip, cp, library, self.logger, cs.port,
                        cs.password, altitude, self.kernels_path)
                else:
                    self.crosser = cali.SolarCross(cs.ip, cp, library, self.logger, cs.port,
                        cs.password, altitude, self.kernels_path)
            else:
                library = psc.MoonLibrary.SPICEDMOON
                if self.kernels_path is None or self.kernels_path == "":
                    library = psc.MoonLibrary.EPHEM_MOON
                if self.is_mesh:
                    self.crosser = cali.LunarMesh(cs.ip, cp, library, self.logger, cs.port,
                        cs.password, altitude, self.kernels_path)
                else:
                    self.crosser = cali.LunarCross(cs.ip, cp, library, self.logger, cs.port,
                        cs.password, altitude, self.kernels_path)
            self.crosser.start()
            self.cancel_button.setVisible(True)
            self.start_checking_cross_end()
        except:
            self.finished_crossing()
    
    class CrossWorker(QtCore.QObject):
        """
        Worker that will check for the cross to finish.
        """
        finished = QtCore.Signal()

        def __init__(self, crosser: Union[cali._BodyCross, cali._BodyMesh]):
            """
            Parameters
            ----------
            crosser : _BodyCross | _BodyMesh
                bodycrosser or bodymesher that will track the celestial body.
            """
            super().__init__()
            self.crs = crosser

        def run(self):
            while not self.crs.is_finished():
                time.sleep(1)
            self.finished.emit()

    def start_checking_cross_end(self):
        self.th = QtCore.QThread()
        self.worker = BodyCrossWidget.CrossWorker(self.crosser)
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
        self.crosser.stop()
    
    def finished_crossing(self):
        """Crossing finished/stopped. Perform the needed actions."""
        self.body_tab.set_enabled_close_button(True)
        _close_logger(self.logger)
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
    def __init__(self, body_tab: ifaces.IBodyTabWidget, body: BodyEnum, session_status: SessionStatus,
        kernels_path: str = ""):
        """
        Parameters
        ----------
        body_tab : ifaces.IBodyTabWidget
            Parent body tab that contains this page.
        body : BodyEnum
            Body (moon or sun) of the body_tab.
        session_status : SessionStatus
            Connection data and status.
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
        self.session_status = session_status
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
        self.start_button = QtWidgets.QPushButton("Perform Black")
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
        self.is_finished = common.ContainedBool(False)
        self.logfile = _create_log_file_name(self.session_status.logfolder, _BLACK_LOGTITLE)
        try:
            cs = self.session_status
            altitude = cs.height
            self.logger = get_custom_logger(self.logfile, self.log_handlers)
            library = psc.MoonLibrary.SPICEDMOON
            if self.kernels_path is None or self.kernels_path == "":
                library = psc.MoonLibrary.EPHEM_MOON
            self.black_thread = Thread(target=cali.black_moon, args=[cs.ip, self.logger, cs.port,
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

        def __init__(self, is_finished: common.ContainedBool):
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
        _close_logger(self.logger)
        self.log_handler.end_handler()
        self.start_button.setEnabled(True)
        self.body_tab.set_disabled_navbar(False)
        self.body_tab.set_disabled_navbar(False)
