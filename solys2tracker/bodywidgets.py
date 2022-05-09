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
from asdcontroller import asd_controller as asdc, asd_types as asdt

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
        # ASD Input
        self.asd_input_layout = QtWidgets.QHBoxLayout()
        # ASD Checkbox
        self.asd_checkbox = QtWidgets.QCheckBox("Measure automatically with ASD")
        # ASD itime checkbox
        self.asd_itime_checkbox = QtWidgets.QCheckBox("Use 544ms as integration time")
        # Finish ASD Input
        self.asd_checkbox.stateChanged.connect(self.asd_checkbox_changed)
        if self.session_status.asd_ip is not None and self.session_status.asd_ip != "":
            self.asd_checkbox.setChecked(True)
            self.asd_itime_checkbox.setChecked(True)
        else:
            self.asd_checkbox.setChecked(False)
            self.asd_checkbox.setDisabled(True)
            self.asd_itime_checkbox.setChecked(False)
            self.asd_itime_checkbox.setDisabled(True)
        add_spacer(self.asd_input_layout, self.h_spacers)
        self.asd_input_layout.addLayout(self.asd_checkbox)
        add_spacer(self.asd_input_layout, self.h_spacers)
        self.asd_input_layout.addLayout(self.asd_itime_checkbox)
        # Finish input
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.seconds_layout)
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.asd_input_layout)
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
    def asd_checkbox_changed(self):
        using_asd = self.asd_checkbox.isChecked()
        if using_asd:
            self.asd_itime_checkbox.setDisabled(False)
        else:
            self.asd_itime_checkbox.setChecked(False)
            self.asd_itime_checkbox.setDisabled(True)

    def _initiate_asd_ctr(self, use_custom_itime: bool, custom_itime: asdc.ITimeEnum = asdc.ITimeEnum.t544ms):
        self.asd_ctr = asdc.ASDController()
        self.asd_ctr.restore()
        self.asd_ctr.optimize()
        if use_custom_itime:
            self.asd_ctr.set_itime(custom_itime)

    def asd_acquire(self):
        spec: asdt.FRInterpSpec = self.asd_ctr.acquire(10)
        dt = datetime.utcnow()
        filename = dt.strftime("%Y_%m_%d_%H_%M_%S.txt")
        filename = path.join(self.session_status.asd_folder, filename)
        with open(filename, 'w') as f:
            print("it: {}. Drift: {}".format(spec.fr_spectrum_header.v_header.it,
                spec.fr_spectrum_header.v_header.drift), file=f)
            s1h = spec.fr_spectrum_header.s1_header
            print("gain1: {}, offset1: {}".format(s1h.gain, s1h.offset), file=f)
            s2h = spec.fr_spectrum_header.s2_header
            print("gain2: {}, offset2: {}".format(s2h.gain, s2h.offset), file=f)
            print("", file=f)
            spec.to_npl_format()
            for i in range(0, asdc.MAX_WLEN - asdc.MIN_WLEN + 1):
                print("{:.3f}\t{:.3f}".format(i + asdc.MIN_WLEN, spec.spec_buffer[i]).replace(".",","), file=f)
            f.close()

    @QtCore.Slot()
    def track_button_press(self):
        """
        Slot for the GUI action of pressing the start tracking button.
        """
        self.track_button.setEnabled(False)
        self.asd_checkbox.setEnabled(False)
        self.asd_itime_checkbox.setEnabled(False)
        self.body_tab.set_disabled_navbar(True)
        self.seconds_input.setDisabled(True)
        self.log_handler.setVisible(True)
        self.log_handler.start_handler()
        self.body_tab.set_enabled_close_button(False)
        self.logfile = _create_log_file_name(self.session_status.logfolder, _TRACK_LOGTITLE)
        self.call_asd = self.asd_checkbox.isChecked()
        self.use_custom_itime = self.asd_itime_checkbox.isChecked()
        try:
            cs = self.session_status
            seconds = self.seconds_input.value()
            altitude = cs.height
            self.logger = common.create_file_logger(self.logfile, self.log_handlers, logging.WARNING)

            callback = None
            if self.call_asd:
                self.logger.info("Connecting to ASD...")
                self._initiate_asd_ctr(self.use_custom_itime)
                self.logger.info("Connected to ASD")
                callback = self.asd_acquire

            if self.body == BodyEnum.SUN:
                library = psc.SunLibrary.SPICEDSUN
                if self.kernels_path is None or self.kernels_path == "":
                    library = psc.SunLibrary.PYSOLAR
                self.tracker = aut.SunTracker(cs.ip, seconds, cs.port, cs.password, self.logger,
                    library, altitude, self.kernels_path, inst_callback=callback, instrument_delay=4)
            else:
                library = psc.MoonLibrary.SPICEDMOON
                if self.kernels_path is None or self.kernels_path == "":
                    library = psc.MoonLibrary.EPHEM_MOON
                self.tracker = aut.MoonTracker(cs.ip, seconds, cs.port, cs.password, self.logger,
                    library, altitude, self.kernels_path, inst_callback=callback, instrument_delay=4)
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
        if self.session_status.asd_ip is not None and self.session_status.asd_ip != "":
            self.asd_checkbox.setEnabled(True)
            self.asd_itime_checkbox.setEnabled(True)

DEFAULT_VALUE_COUNTDOWN_AUTOMATIC = 1
DEFAULT_VALUE_COUNTDOWN_MANUAL = 3

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
        self.call_asd = False
        self.asd_ctr: asdc.ASDController = None
        self._build_layout()

    class QLabelCrossCountdownLogger(logging.Handler):
        def __init__(self, label: QtWidgets.QLabel):
            super().__init__()
            self.widget = label
            self.zero_msg = "MEASURE NOW"
        
        def set_zero_msg(self, zero_msg: str):
            self.zero_msg = zero_msg
        
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
                    label_msg = self.zero_msg
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
        self.countdown_input.setValue(DEFAULT_VALUE_COUNTDOWN_MANUAL)
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
        self.remaining_steps_label = QtWidgets.QLabel("Performed steps:", alignment=QtCore.Qt.AlignCenter)
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
        # ASD Checkbox
        self.asd_checkbox = QtWidgets.QCheckBox("Measure automatically with ASD")
        if self.session_status.asd_ip is not None and self.session_status.asd_ip != "":
            self.asd_checkbox.setChecked(True)
            self.countdown_input.setValue(DEFAULT_VALUE_COUNTDOWN_AUTOMATIC)
        else:
            self.asd_checkbox.setChecked(False)
            self.asd_checkbox.setDisabled(True)
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
        self.content_layout.addWidget(self.asd_checkbox)
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
        self.rem_steps.setText("{}/{}".format(self.measured_steps, len(self.steps)))

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

    def asd_acquire(self):
        spec: asdt.FRInterpSpec = self.asd_ctr.acquire(10)
        dt = datetime.utcnow()
        filename = dt.strftime("%Y_%m_%d_%H_%M_%S.txt")
        filename = path.join(self.session_status.asd_folder, filename)
        with open(filename, 'w') as f:
            print("it: {}. Drift: {}".format(spec.fr_spectrum_header.v_header.it,
                spec.fr_spectrum_header.v_header.drift), file=f)
            s1h = spec.fr_spectrum_header.s1_header
            print("gain1: {}, offset1: {}".format(s1h.gain, s1h.offset), file=f)
            s2h = spec.fr_spectrum_header.s2_header
            print("gain2: {}, offset2: {}".format(s2h.gain, s2h.offset), file=f)
            print("", file=f)
            spec.to_npl_format()
            for i in range(0, asdc.MAX_WLEN - asdc.MIN_WLEN + 1):
                print("{:.3f}\t{:.3f}".format(i + asdc.MIN_WLEN, spec.spec_buffer[i]).replace(".",","), file=f)
            f.close()

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
        self.call_asd = self.asd_checkbox.isChecked()
        if self.call_asd:
            self.log_countdown.set_zero_msg("MEASURING...")
        self.log_countdown.start_handler()
        self.body_tab.set_enabled_close_button(False)
        self.asd_checkbox.setDisabled(True)
        option = _CROSS_LOGTITLE
        if self.is_mesh:
            option = _MESH_LOGTITLE
        self.logfile = _create_log_file_name(self.session_status.logfolder, option)
        try:
            self.logger = get_custom_logger(self.logfile, self.log_handlers)

            if self.call_asd:
                self.connect_asd_then_start()
            else:
                self.start_cross()
        except Exception as e:
            self.logger.error(e)
            self.finished_crossing()
    
    def initiate_crosser(self):
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

        callback = None
        if self.call_asd:
            callback = self.asd_acquire
        if self.body == BodyEnum.SUN:
            library = psc.SunLibrary.SPICEDSUN
            if self.kernels_path is None or self.kernels_path == "":
                library = psc.SunLibrary.PYSOLAR
            args = [cs.ip, cp, library, self.logger, cs.port,
                    cs.password, altitude, self.kernels_path]
            if self.is_mesh:
                self.crosser = cali.SolarMesh(*args, inst_callback=callback)
            else:
                self.crosser = cali.SolarCross(*args, inst_callback=callback)
        else:
            library = psc.MoonLibrary.SPICEDMOON
            if self.kernels_path is None or self.kernels_path == "":
                library = psc.MoonLibrary.EPHEM_MOON
            args = [cs.ip, cp, library, self.logger, cs.port,
                    cs.password, altitude, self.kernels_path]
            if self.is_mesh:
                self.crosser = cali.LunarMesh(*args, inst_callback=callback)
            else:
                self.crosser = cali.LunarCross(*args, inst_callback=callback)

    def start_cross(self):
        try:
            self.initiate_crosser()
        except Exception as e:
            self.logger.error(e)
            self.finished_crossing()
        else:
            self.crosser.start()
            self.cancel_button.setVisible(True)
            self.start_checking_cross_end()

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

    class ConnectASDWorker(QtCore.QObject):
        finished = QtCore.Signal()
        exception = QtCore.Signal(Exception)

        def __init__(self, cross_widget: 'BodyCrossWidget', ip: str, port: int):
            super().__init__()
            self.cross_widget = cross_widget
            self.ip = ip
            self.port = port
        
        def _start_tracking_body(self):
            logger = get_custom_logger(self.cross_widget.logfile, [])
            cs = self.cross_widget.session_status
            kp = self.cross_widget.kernels_path
            seconds = 10
            altitude = cs.height
            if self.cross_widget.body == BodyEnum.SUN:
                library = psc.SunLibrary.SPICEDSUN
                if kp is None or kp == "":
                    library = psc.SunLibrary.PYSOLAR
                self.tracker = aut.SunTracker(cs.ip, seconds, cs.port, cs.password, logger,
                    library, altitude, kp)
            else:
                library = psc.MoonLibrary.SPICEDMOON
                if kp is None or kp == "":
                    library = psc.MoonLibrary.EPHEM_MOON
                self.tracker = aut.MoonTracker(cs.ip, seconds, cs.port, cs.password, logger,
                    library, altitude, kp)
            self.tracker.start()
        
        def _stop_tracking_sync(self):
            if not self.tracker.is_finished():
                self.tracker.stop()
                while not self.tracker.is_finished():
                    time.sleep(1)

        def run(self):
            try:
                self._start_tracking_body()
                self.cross_widget.asd_ctr = asdc.ASDController(self.ip, self.port)
                self.cross_widget.asd_ctr.restore()
                self.cross_widget.asd_ctr.optimize()
                self._stop_tracking_sync()
                self.cross_widget.logger.info("Stopped tracking after optimization.")
                self.finished.emit()
            except Exception as e:
                self.exception.emit(e)

    def exception_connecting_asd(self, e: Exception):
        self.logger.error(e)
        self.finished_crossing()

    def connect_asd_then_start(self):
        self.asd_th = QtCore.QThread()
        self.asd_worker = BodyCrossWidget.ConnectASDWorker(self, self.session_status.asd_ip,
            self.session_status.asd_port)
        self.asd_worker.moveToThread(self.asd_th)
        self.asd_th.started.connect(self.asd_worker.run)
        self.asd_worker.finished.connect(self.asd_th.quit)
        self.asd_worker.finished.connect(self.asd_worker.deleteLater)
        self.asd_worker.finished.connect(self.start_cross)
        self.asd_worker.exception.connect(self.asd_th.quit)
        self.asd_worker.exception.connect(self.asd_worker.deleteLater)
        self.asd_worker.exception.connect(self.exception_connecting_asd)
        self.asd_th.finished.connect(self.asd_th.deleteLater)
        self.logger.info("Connecting to ASD...")
        self.asd_th.start()

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
        self.asd_checkbox.setDisabled(False)
        if self.call_asd and self.asd_ctr is not None:
            self.asd_ctr.close()

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
