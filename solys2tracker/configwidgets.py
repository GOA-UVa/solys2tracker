"""
This module contains the configuration pages.

It exports the following classes:
    * ConfigurationWidget: The Configuration Tab.
"""

"""___Built-In Modules___"""
from ctypes import alignment
from typing import Tuple
import math

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from solys2 import solys2 as s2

"""___Solys2Tracker Modules___"""
try:
    from solys2tracker.s2ttypes import SessionStatus
    from solys2tracker import constants
    from solys2tracker import ifaces
    from solys2tracker.common import add_spacer
except:
    import constants
    import ifaces
    from s2ttypes import SessionStatus
    from common import add_spacer

"""___Authorship___"""
__author__ = 'Javier Gatón Herguedas'
__created__ = "2022/03/25"
__maintainer__ = "Javier Gatón Herguedas"
__email__ = "gaton@goa.uva.es"
__status__ = "Development"


def _try_conn(ip: str, port: int, password: str) -> Tuple[bool, str]:
    """
    Tries to connect to the Solys2 through the given IP and Port using the given password.

    Parameters
    ----------
    ip : str
        IP where the Solys2 should be.
    port : int
        Solys2 port at which the connection will be done.
    password : str
        Password used for connecting to the Solys2.

    Returns
    -------
    is_connected : bool
        Flag that indicates if the connection was successful. True if it was.
    msg : str
        Error message in case it wasn't successful, success message in case it was.
    """
    try:
        solys = s2.Solys2(ip, port, password)
        solys.close()
    except Exception as e:
        return False, str(e)
    return True, constants.MSG_CONNECTED_SUCCESSFULLY

class ConfigNavBarWidget(QtWidgets.QWidget):
    """
    Configuration sub navigaton bar that allows the user to change between tabs.
    """
    def __init__(self, config_w : ifaces.IConfigWidget, session_status: SessionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        session_status : SessionStatus
            Current status of the GUI connection with the Solys2.
        """
        self.session_status = session_status
        self.config_w = config_w
        self._build_layout()

    def _build_layout(self):
        super().__init__()
        self.h_spacers = []
        self.v_spacers = []
        self.conn_but = QtWidgets.QPushButton("Connection")
        self.conn_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.conn_but.clicked.connect(self.press_connection)
        self.spice_but = QtWidgets.QPushButton("SPICE")
        self.spice_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.spice_but.clicked.connect(self.press_spice)
        self.log_but = QtWidgets.QPushButton("Log")
        self.log_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.log_but.clicked.connect(self.press_log)
        self.adjust_but = QtWidgets.QPushButton("Adjust")
        self.adjust_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.adjust_but.clicked.connect(self.press_adjust)
        self.position_but = QtWidgets.QPushButton("Position")
        self.position_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.position_but.clicked.connect(self.press_move_pos)
        self.other_but = QtWidgets.QPushButton("Other")
        self.other_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.other_but.clicked.connect(self.press_other)
        self.other_but = QtWidgets.QPushButton("ASD")
        self.other_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.other_but.clicked.connect(self.press_asd)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        add_spacer(self.main_layout, self.h_spacers)
        self.main_layout.addWidget(self.conn_but, 1)
        add_spacer(self.main_layout, self.h_spacers)
        self.main_layout.addWidget(self.spice_but, 1)
        add_spacer(self.main_layout, self.h_spacers)
        self.main_layout.addWidget(self.log_but, 1)
        add_spacer(self.main_layout, self.h_spacers)
        self.main_layout.addWidget(self.adjust_but, 1)
        add_spacer(self.main_layout, self.h_spacers)
        self.main_layout.addWidget(self.position_but, 1)
        add_spacer(self.main_layout, self.h_spacers)
        self.main_layout.addWidget(self.other_but, 1)
        add_spacer(self.main_layout, self.h_spacers)
        self.update_button_enabling()

    def set_enabled_buttons(self, enabled: bool):
        """
        Enables or disables all the navigation buttons.
        """
        self.conn_but.setEnabled(enabled)
        self.spice_but.setEnabled(enabled)
        self.log_but.setEnabled(enabled)
        self.adjust_but.setEnabled(enabled)
        self.position_but.setEnabled(enabled)
        self.other_but.setEnabled(enabled)

    def update_button_enabling(self):
        """
        Updates the enabled status of the buttons based on if the connection_status
        is connected.
        """
        enabled = self.session_status.is_connected
        self.set_enabled_buttons(enabled)
    
    @QtCore.Slot()
    def press_connection(self):
        """Press the CONNECTION button."""
        self.config_w.change_tab_connection()

    @QtCore.Slot()
    def press_spice(self):
        """Press the SPICE button."""
        self.config_w.change_tab_spice()

    @QtCore.Slot()
    def press_log(self):
        """Press the LOG button."""
        self.config_w.change_tab_log()

    @QtCore.Slot()
    def press_adjust(self):
        """Press the ADJUST button."""
        self.config_w.change_tab_adjust()
    
    @QtCore.Slot()
    def press_move_pos(self):
        """Press the POSITION button."""
        self.config_w.change_tab_move_pos()

    @QtCore.Slot()
    def press_other(self):
        """Press the OTHER button."""
        self.config_w.change_tab_other()

    @QtCore.Slot()
    def press_asd(self):
        """Press the ASD button."""
        self.config_w.change_tab_asd()

class ConnectionWidget(QtWidgets.QWidget):
    """
    Configuration page containing the Solys2 connection functionality.
    """
    def __init__(self, config_w : ifaces.IConfigWidget, session_status: SessionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        session_status : SessionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.session_status = session_status
        self.config_w = config_w
        self._build_layout()
    
    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.v_spacers = []
        self.h_spacers = []
        # Title
        self.title = QtWidgets.QLabel("Configuration | Connection", alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Content
        self.content_layout = QtWidgets.QVBoxLayout()
        # Input
        self.input_layout = QtWidgets.QVBoxLayout()
        # First row (IP)
        self.lay_ip = QtWidgets.QHBoxLayout()
        self.ip_label = QtWidgets.QLabel("IP:", alignment=QtCore.Qt.AlignCenter)
        self.ip_input = QtWidgets.QLineEdit(self.session_status.ip)
        add_spacer(self.lay_ip, self.h_spacers)
        self.lay_ip.addWidget(self.ip_label)
        add_spacer(self.lay_ip, self.h_spacers)
        self.lay_ip.addWidget(self.ip_input)
        add_spacer(self.lay_ip, self.h_spacers)
        # Second row (Port)
        self.lay_port = QtWidgets.QHBoxLayout()
        self.port_label = QtWidgets.QLabel("Port:", alignment=QtCore.Qt.AlignCenter)
        self.port_input = QtWidgets.QSpinBox()
        self.port_input.setMaximum(1000000)
        self.port_input.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
            self.port_input.sizePolicy().verticalPolicy()))
        self.port_input.setValue(self.session_status.port)
        add_spacer(self.lay_port, self.h_spacers)
        self.lay_port.addWidget(self.port_label)
        add_spacer(self.lay_port, self.h_spacers)
        self.lay_port.addWidget(self.port_input)
        add_spacer(self.lay_port, self.h_spacers)
        # Third row (Password)
        self.lay_pass = QtWidgets.QHBoxLayout()
        self.pass_label = QtWidgets.QLabel("Password:", alignment=QtCore.Qt.AlignCenter)
        self.pass_input = QtWidgets.QLineEdit(self.session_status.password)
        add_spacer(self.lay_pass, self.h_spacers)
        self.lay_pass.addWidget(self.pass_label)
        add_spacer(self.lay_pass, self.h_spacers)
        self.lay_pass.addWidget(self.pass_input)
        add_spacer(self.lay_pass, self.h_spacers)
        # Finish input
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.lay_ip)
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.lay_port)
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.lay_pass)
        add_spacer(self.input_layout, self.v_spacers)
        # Message
        self.message_l = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.message_l.setObjectName("message")
        # Connect button
        connect_msg = "Connect"
        if self.session_status.is_connected:
            connect_msg = "Reconnect"
        self.connect_but = QtWidgets.QPushButton(connect_msg)
        self.connect_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connect_but.clicked.connect(self.check_connection)
        # Finish content
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addLayout(self.input_layout)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.message_l)
        add_spacer(self.content_layout, self.v_spacers)
        self.content_layout.addWidget(self.connect_but)
        add_spacer(self.content_layout, self.v_spacers)
        # Finish layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.content_layout, 1)
        add_spacer(self.main_layout, self.v_spacers)

    class TryConnectionWorker(QtCore.QObject):
        """
        Worker that will perform the connection check against the Solys2
        """
        finished = QtCore.Signal(bool, str)

        def __init__(self, ip: str, port: int, password: str):
            """
            Parameters
            ----------
            ip : str
                Solys2 connection ip.
            port : int
                Solys2 connection port.
            password : str
                Solys2 connection password.
            """
            super().__init__()
            self.ip = ip
            self.port = port
            self.password = password

        def run(self):
            is_connected, msg = _try_conn(self.ip, self.port, self.password)
            self.finished.emit(is_connected, msg)

    @QtCore.Slot()
    def check_connection(self):
        """
        Check if the GUI can connect to the Solys2 with the inputed parameters.
        """
        self.connect_but.setEnabled(False)
        ip = self.ip_input.text()
        port = self.port_input.value()
        password = self.pass_input.text()
        self.session_status.ip = ip
        self.session_status.port = port
        self.session_status.password = password

        self.th = QtCore.QThread()
        self.worker = ConnectionWidget.TryConnectionWorker(ip, port, password)
        self.worker.moveToThread(self.th)
        self.th.started.connect(self.worker.run)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.set_connection_result)
        self.th.finished.connect(self.th.deleteLater)
        self.th.start()

    def set_connection_result(self, is_connected: bool, msg: str):
        """
        When the connection try is done, this function is called,
        and it will do the needed actions.

        Parameters
        ----------
        is_connected : bool
            Flag that indicates if the connection was successful. True if it was.
        msg : str
            Error message in case it wasn't successful, success message in case it was.
        """
        self.message_l.setText(msg)
        label_color = constants.COLOR_RED
        connect_msg = "Connect"
        if is_connected:
            self.session_status.save_ip_data()
            label_color = constants.COLOR_GREEN
            connect_msg = "Reconnect"
        self.connect_but.setText(connect_msg)
        self.message_l.setStyleSheet("background-color: {}".format(label_color))
        self.message_l.repaint()
        self.session_status.is_connected = is_connected
        self.config_w.connection_changed()
        self.connect_but.setEnabled(True)

class SpiceWidget(QtWidgets.QWidget):
    def __init__(self, config_w : ifaces.IConfigWidget, session_status: SessionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        session_status : SessionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | SPICE"
        self.config_w = config_w
        self.session_status = session_status
        self._build_layout()
    
    def _build_layout(self):
        self.v_spacers = []
        self.h_spacers = []
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Input
        self.input_layout = QtWidgets.QHBoxLayout()
        self.select_label = QtWidgets.QLabel("Kernels directory:", alignment=QtCore.Qt.AlignCenter)
        self.select_btn = QtWidgets.QPushButton("Select folder")
        self.select_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.select_btn.clicked.connect(self.open_file_dialog)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.select_label)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.select_btn)
        add_spacer(self.input_layout, self.h_spacers)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.input_layout)
        # Selected directory
        self.kernels_path = self.session_status.kernels_path
        self.dir_str = self.kernels_path
        if self.dir_str == "":
            self.dir_str = "No directory selected"
        self.selected_label = QtWidgets.QLabel(self.dir_str, alignment=QtCore.Qt.AlignCenter)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.selected_label)
        # Message
        self.message_l = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.message_l.setObjectName("message")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.message_l)
        # Save button
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_directory)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.save_button)
        # Finish main layout
        add_spacer(self.main_layout, self.v_spacers)

    @QtCore.Slot()
    def open_file_dialog(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        if dlg.exec_():
            folderpaths = dlg.selectedFiles()
            self.kernels_path = folderpaths[0]
            self.selected_label.setText(self.kernels_path)
    
    @QtCore.Slot()
    def save_directory(self):
        self.session_status.kernels_path = self.kernels_path
        try:
            self.session_status.save_kernels_path_data()
        except:
            msg = "Error saving the kernels directory data"
            label_color = constants.COLOR_RED
        else:
            msg = "Saved successfully"
            label_color = constants.COLOR_GREEN
        finally:
            self.message_l.setText(msg)
            self.message_l.setStyleSheet("background-color: {}".format(label_color))
            self.message_l.repaint()

class LogWidget(QtWidgets.QWidget):
    def __init__(self, config_w : ifaces.IConfigWidget, session_status: SessionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        session_status : SessionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | Log"
        self.config_w = config_w
        self.session_status = session_status
        self._build_layout()
    
    def _build_layout(self):
        self.v_spacers = []
        self.h_spacers = []
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Input
        self.input_layout = QtWidgets.QHBoxLayout()
        self.select_label = QtWidgets.QLabel("Log directory:", alignment=QtCore.Qt.AlignCenter)
        self.select_btn = QtWidgets.QPushButton("Select folder")
        self.select_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.select_btn.clicked.connect(self.open_file_dialog)
        self.log_folder = self.session_status.logfolder
        self.dir_str = self.log_folder
        if self.dir_str == "":
            self.dir_str = "No directory selected"
        elif self.dir_str == ".":
            self.dir_str = "Using current execution directory"
        self.selected_label = QtWidgets.QLabel(self.dir_str, alignment=QtCore.Qt.AlignCenter)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.select_label)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.select_btn)
        add_spacer(self.input_layout, self.h_spacers)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.input_layout)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.selected_label)
        # Message
        self.message_l = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.message_l.setObjectName("message")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.message_l)
        # Save button
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_directory)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.save_button)
        # Finish main layout
        add_spacer(self.main_layout, self.v_spacers)

    @QtCore.Slot()
    def open_file_dialog(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        if dlg.exec_():
            folderpaths = dlg.selectedFiles()
            self.log_folder = folderpaths[0]
            self.selected_label.setText(self.log_folder)
    
    @QtCore.Slot()
    def save_directory(self):
        self.session_status.logfolder = self.log_folder
        try:
            self.session_status.save_logfolder_data()
        except:
            msg = "Error saving the logging directory data"
            label_color = constants.COLOR_RED
        else:
            msg = "Saved successfully"
            label_color = constants.COLOR_GREEN
        finally:
            self.message_l.setText(msg)
            self.message_l.setStyleSheet("background-color: {}".format(label_color))
            self.message_l.repaint()

class AdjustWidget(QtWidgets.QWidget):
    def __init__(self, config_w : ifaces.IConfigWidget, session_status: SessionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        session_status : SessionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | Adjust"
        self.config_w = config_w
        self.session_status = session_status
        self._build_layout()
        self.update_adjustment_labels()
    
    def _build_layout(self):
        self.v_spacers = []
        self.h_spacers = []
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Current adjustment
        self.adjust_layout = QtWidgets.QHBoxLayout()
        self.az_label = QtWidgets.QLabel("Azimuth: ", alignment=QtCore.Qt.AlignRight)
        self.az_curr_adjustment = QtWidgets.QLabel("?", alignment=QtCore.Qt.AlignLeft)
        self.ze_label = QtWidgets.QLabel("Zenith: ", alignment=QtCore.Qt.AlignRight)
        self.ze_curr_adjustment = QtWidgets.QLabel("?", alignment=QtCore.Qt.AlignLeft)
        add_spacer(self.adjust_layout, self.h_spacers)
        self.adjust_layout.addWidget(self.az_label, 1)
        add_spacer(self.adjust_layout, self.h_spacers)
        self.adjust_layout.addWidget(self.az_curr_adjustment, 1)
        add_spacer(self.adjust_layout, self.h_spacers)
        self.adjust_layout.addWidget(self.ze_label, 1)
        add_spacer(self.adjust_layout, self.h_spacers)
        self.adjust_layout.addWidget(self.ze_curr_adjustment, 1)
        add_spacer(self.adjust_layout, self.h_spacers)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.adjust_layout)
        # Input
        # Input title
        self.input_title = QtWidgets.QLabel("Add adjustments", alignment=QtCore.Qt.AlignCenter)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.input_title)
        # Input fields
        self.input_layout = QtWidgets.QHBoxLayout()
        self.az_label_input = QtWidgets.QLabel("Azimuth: ", alignment=QtCore.Qt.AlignRight)
        self.az_extra_adjustment = QtWidgets.QDoubleSpinBox()
        self.az_extra_adjustment.setMinimum(-2)
        self.az_extra_adjustment.setMaximum(2)
        self.az_extra_adjustment.setSingleStep(0.01)
        self.az_extra_adjustment.setDecimals(3)
        self.ze_label_input = QtWidgets.QLabel("Zenith: ", alignment=QtCore.Qt.AlignRight)
        self.ze_extra_adjustment = QtWidgets.QDoubleSpinBox()
        self.ze_extra_adjustment.setMinimum(-2)
        self.ze_extra_adjustment.setMaximum(2)
        self.ze_extra_adjustment.setSingleStep(0.01)
        self.ze_extra_adjustment.setDecimals(3)
        add_spacer(self.adjust_layout, self.h_spacers)
        self.input_layout.addWidget(self.az_label_input, 1)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.az_extra_adjustment, 1)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.ze_label_input, 1)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.ze_extra_adjustment, 1)
        add_spacer(self.input_layout, self.h_spacers)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.input_layout)
        # Message
        self.message_l = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.message_l.setObjectName("message")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.message_l)
        # Adjust button
        self.save_button = QtWidgets.QPushButton("Adjust")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.adjust)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.save_button)
        add_spacer(self.main_layout, self.v_spacers)

    class AdjustWorker(QtCore.QObject):
        """
        Worker that will obtain the adjustment from the Solys2
        """
        finished = QtCore.Signal()
        success = QtCore.Signal(float, float)
        error = QtCore.Signal(str)

        def __init__(self, ip: str, port: int, password: str):
            """
            Parameters
            ----------
            ip : str
                Solys2 connection ip.
            port : int
                Solys2 connection port.
            password : str
                Solys2 connection password.
            """
            super().__init__()
            self.ip = ip
            self.port = port
            self.password = password

        def run(self):
            try:
                solys = s2.Solys2(self.ip, self.port, self.password)
                az, ze, _ = solys.adjust()
                self.success.emit(az, ze)
            except Exception as e:
                self.error.emit(str(e))
            finally:
                self.finished.emit()

    def update_adjustment_labels(self):
        self.th = QtCore.QThread()
        cs = self.session_status
        self.worker = AdjustWidget.AdjustWorker(cs.ip, cs.port, cs.password)
        self.worker.moveToThread(self.th)
        self.th.started.connect(self.worker.run)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.show_error)
        self.worker.success.connect(self._update_adjustment_labels)
        self.worker.finished.connect(self.thread_finished)
        self.th.finished.connect(self.th.deleteLater)
        self.thread_started()
        self.th.start()

    def _update_adjustment_labels(self, az: float, ze: float):
        self.az_curr_adjustment.setText("{:+.4f}".format(az))
        self.ze_curr_adjustment.setText("{:+.4f}".format(ze))
    
    def thread_finished(self):
        self.az_extra_adjustment.setDisabled(False)
        self.ze_extra_adjustment.setDisabled(False)
        self.save_button.setDisabled(False)
        self.config_w.set_disabled_config_navbar(False)
        self.config_w.set_disabled_navbar(False)

    def thread_started(self):
        self.az_extra_adjustment.setDisabled(True)
        self.ze_extra_adjustment.setDisabled(True)
        self.save_button.setDisabled(True)
        self.config_w.set_disabled_config_navbar(True)
        self.config_w.set_disabled_navbar(True)

    class SendAdjustWorker(QtCore.QObject):
        """
        Worker that will send the adjustment from the Solys2
        """
        finished = QtCore.Signal()
        success = QtCore.Signal()
        error = QtCore.Signal(str)

        def __init__(self, ip: str, port: int, password: str, az: float, ze: float):
            """
            Parameters
            ----------
            ip : str
                Solys2 connection ip.
            port : int
                Solys2 connection port.
            password : str
                Solys2 connection password.
            """
            super().__init__()
            self.ip = ip
            self.port = port
            self.password = password
            self.az = az
            self.ze = ze

        def run(self):
            az = self.az
            ze = self.ze
            try:
                solys = s2.Solys2(self.ip, self.port, self.password)
                azi = math.copysign(0.2, az)
                while abs(az) >= abs(azi):
                    solys.adjust_azimuth(azi)
                    az -= azi
                if az != 0:
                    solys.adjust_azimuth(az)
                zei = math.copysign(0.2, ze)
                while abs(ze) >= abs(zei):
                    solys.adjust_zenith(zei)
                    ze -= zei
                if ze != 0:
                    solys.adjust_zenith(ze)
                self.success.emit()
            except Exception as e:
                self.error.emit(str(e))
            finally:
                self.finished.emit()

    def success_adjusting_solys2(self):
        self.show_success("Updated successfully")
        self.update_adjustment_labels()

    @QtCore.Slot()
    def adjust(self):
        self.empty_message_label()
        self.th_send_adj = QtCore.QThread()
        cs = self.session_status
        az = self.az_extra_adjustment.value()
        ze = self.ze_extra_adjustment.value()
        self.worker = AdjustWidget.SendAdjustWorker(cs.ip, cs.port, cs.password, az, ze)
        self.worker.moveToThread(self.th_send_adj)
        self.th_send_adj.started.connect(self.worker.run)
        self.worker.finished.connect(self.th_send_adj.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.show_error)
        self.worker.success.connect(self.success_adjusting_solys2)
        self.worker.finished.connect(self.thread_finished)
        self.th_send_adj.finished.connect(self.th_send_adj.deleteLater)
        self.thread_started()
        self.th_send_adj.start()

    def empty_message_label(self):
        self.message_l.setText("")
        label_color = constants.COLOR_TRANSPARENT
        self.message_l.setStyleSheet("background: {}".format(label_color))
        self.message_l.repaint()

    def show_error(self, msg: str):
        msg = "Error: {}".format(msg)
        label_color = constants.COLOR_RED
        self.message_l.setText(msg)
        self.message_l.setStyleSheet("background-color: {}".format(label_color))
        self.message_l.repaint()

    def show_success(self, msg: str):
        label_color = constants.COLOR_GREEN
        self.message_l.setText(msg)
        self.message_l.setStyleSheet("background-color: {}".format(label_color))
        self.message_l.repaint()

class PositionWidget(QtWidgets.QWidget):

    def __init__(self, config_w : ifaces.IConfigWidget, session_status: SessionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        session_status : SessionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | Position"
        self.config_w = config_w
        self.session_status = session_status
        self._build_layout()
        self.update_position_labels()
    
    def _build_layout(self):
        self.v_spacers = []
        self.h_spacers = []
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Current position
        self.current_layout = QtWidgets.QHBoxLayout()
        self.az_label = QtWidgets.QLabel("Azimuth: ", alignment=QtCore.Qt.AlignRight)
        self.az_curr_pos = QtWidgets.QLabel("?", alignment=QtCore.Qt.AlignLeft)
        self.ze_label = QtWidgets.QLabel("Zenith: ", alignment=QtCore.Qt.AlignRight)
        self.ze_curr_pos = QtWidgets.QLabel("?", alignment=QtCore.Qt.AlignLeft)
        add_spacer(self.current_layout, self.h_spacers)
        self.current_layout.addWidget(self.az_label, 1)
        add_spacer(self.current_layout, self.h_spacers)
        self.current_layout.addWidget(self.az_curr_pos, 1)
        add_spacer(self.current_layout, self.h_spacers)
        self.current_layout.addWidget(self.ze_label, 1)
        add_spacer(self.current_layout, self.h_spacers)
        self.current_layout.addWidget(self.ze_curr_pos, 1)
        add_spacer(self.current_layout, self.h_spacers)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.current_layout)
        # Input
        # Input title
        self.input_title = QtWidgets.QLabel("Set position", alignment=QtCore.Qt.AlignCenter)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.input_title)
        # Input fields
        self.input_layout = QtWidgets.QHBoxLayout()
        self.az_label_input = QtWidgets.QLabel("Azimuth: ", alignment=QtCore.Qt.AlignRight)
        self.az_sending_position = QtWidgets.QDoubleSpinBox()
        self.az_sending_position.setMinimum(-1)
        self.az_sending_position.setMaximum(361)
        self.ze_label_input = QtWidgets.QLabel("Zenith: ", alignment=QtCore.Qt.AlignRight)
        self.ze_sending_position = QtWidgets.QDoubleSpinBox()
        self.ze_sending_position.setMinimum(-4)
        self.ze_sending_position.setMaximum(94.9)
        add_spacer(self.current_layout, self.h_spacers)
        self.input_layout.addWidget(self.az_label_input, 1)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.az_sending_position, 1)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.ze_label_input, 1)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.ze_sending_position, 1)
        add_spacer(self.input_layout, self.h_spacers)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.input_layout)
        # Message
        self.message_l = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.message_l.setObjectName("message")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.message_l)
        # Move button
        self.save_button = QtWidgets.QPushButton("Move")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.adjust)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.save_button)
        add_spacer(self.main_layout, self.v_spacers)

    class PositionWorker(QtCore.QObject):
        """
        Worker that will obtain the position from the Solys2
        """
        finished = QtCore.Signal()
        success = QtCore.Signal(float, float)
        error = QtCore.Signal(str)

        def __init__(self, ip: str, port: int, password: str):
            """
            Parameters
            ----------
            ip : str
                Solys2 connection ip.
            port : int
                Solys2 connection port.
            password : str
                Solys2 connection password.
            """
            super().__init__()
            self.ip = ip
            self.port = port
            self.password = password

        def run(self):
            try:
                solys = s2.Solys2(self.ip, self.port, self.password)
                az, ze, _ = solys.get_planned_position()
                self.success.emit(az, ze)
            except Exception as e:
                self.error.emit(str(e))
            finally:
                self.finished.emit()

    def update_position_labels(self):
        self.th = QtCore.QThread()
        cs = self.session_status
        self.worker = PositionWidget.PositionWorker(cs.ip, cs.port, cs.password)
        self.worker.moveToThread(self.th)
        self.th.started.connect(self.worker.run)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.show_error)
        self.worker.success.connect(self._update_position_labels)
        self.worker.finished.connect(self.thread_finished)
        self.th.finished.connect(self.th.deleteLater)
        self.thread_started()
        self.th.start()

    def _update_position_labels(self, az: float, ze: float):
        self.az_curr_pos.setText(str(az))
        self.ze_curr_pos.setText(str(ze))
        self.az_sending_position.setValue(az)
        self.ze_sending_position.setValue(ze)
    
    def thread_finished(self):
        self.az_sending_position.setDisabled(False)
        self.ze_sending_position.setDisabled(False)
        self.save_button.setDisabled(False)
        self.config_w.set_disabled_config_navbar(False)
        self.config_w.set_disabled_navbar(False)

    def thread_started(self):
        self.az_sending_position.setDisabled(True)
        self.ze_sending_position.setDisabled(True)
        self.save_button.setDisabled(True)
        self.config_w.set_disabled_config_navbar(True)
        self.config_w.set_disabled_navbar(True)

    class SendPositionWorker(QtCore.QObject):
        """
        Worker that will send the position from the Solys2
        """
        finished = QtCore.Signal()
        success = QtCore.Signal()
        error = QtCore.Signal(str)

        def __init__(self, ip: str, port: int, password: str, az: float, ze: float):
            """
            Parameters
            ----------
            ip : str
                Solys2 connection ip.
            port : int
                Solys2 connection port.
            password : str
                Solys2 connection password.
            """
            super().__init__()
            self.ip = ip
            self.port = port
            self.password = password
            self.az = az
            self.ze = ze

        def run(self):
            try:
                solys = s2.Solys2(self.ip, self.port, self.password)
                solys.set_azimuth(self.az)
                solys.set_zenith(self.ze)
                self.success.emit()
            except Exception as e:
                self.error.emit(str(e))
            finally:
                self.finished.emit()

    def success_sending_pos_solys2(self):
        self.show_success("Order sent successfully")
        self.update_position_labels()

    @QtCore.Slot()
    def adjust(self):
        self.empty_message_label()
        self.th_send_adj = QtCore.QThread()
        cs = self.session_status
        az = self.az_sending_position.value()
        ze = self.ze_sending_position.value()
        self.worker = PositionWidget.SendPositionWorker(cs.ip, cs.port, cs.password, az, ze)
        self.worker.moveToThread(self.th_send_adj)
        self.th_send_adj.started.connect(self.worker.run)
        self.worker.finished.connect(self.th_send_adj.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.show_error)
        self.worker.success.connect(self.success_sending_pos_solys2)
        self.worker.finished.connect(self.thread_finished)
        self.th_send_adj.finished.connect(self.th_send_adj.deleteLater)
        self.thread_started()
        self.th_send_adj.start()

    def empty_message_label(self):
        self.message_l.setText("")
        label_color = constants.COLOR_TRANSPARENT
        self.message_l.setStyleSheet("background: {}".format(label_color))
        self.message_l.repaint()

    def show_error(self, msg: str):
        msg = "Error: {}".format(msg)
        label_color = constants.COLOR_RED
        self.message_l.setText(msg)
        self.message_l.setStyleSheet("background-color: {}".format(label_color))
        self.message_l.repaint()

    def show_success(self, msg: str):
        label_color = constants.COLOR_GREEN
        self.message_l.setText(msg)
        self.message_l.setStyleSheet("background-color: {}".format(label_color))
        self.message_l.repaint()

class OtherWidget(QtWidgets.QWidget):
    def __init__(self, config_w : ifaces.IConfigWidget, session_status: SessionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        session_status : SessionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | Other"
        self.config_w = config_w
        self.session_status = session_status
        self._build_layout()
    
    def _build_layout(self):
        self.v_spacers = []
        self.h_spacers = []
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Input
        self.input_layout = QtWidgets.QVBoxLayout()
        # Height input (Row 1)
        self.lay_height = QtWidgets.QHBoxLayout()
        self.height_label = QtWidgets.QLabel("Height (meters):", alignment=QtCore.Qt.AlignCenter)
        self.height_input = QtWidgets.QSpinBox()
        self.height_input.setMaximum(10000000)
        self.height_input.setMinimum(0)
        self.height_input.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
            self.height_input.sizePolicy().verticalPolicy()))
        self.height_input.setValue(self.session_status.height)
        add_spacer(self.lay_height, self.h_spacers)
        self.lay_height.addWidget(self.height_label)
        add_spacer(self.lay_height, self.h_spacers)
        self.lay_height.addWidget(self.height_input)
        add_spacer(self.lay_height, self.h_spacers)
        # Finish input
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.lay_height)
        add_spacer(self.input_layout, self.v_spacers)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.input_layout)
        # Message
        self.message_l = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.message_l.setObjectName("message")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.message_l)
        # Save button
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_others)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.save_button)
        # Finish main layout
        add_spacer(self.main_layout, self.v_spacers)
    
    @QtCore.Slot()
    def save_others(self):
        self.session_status.height = self.height_input.value()
        try:
            self.session_status.save_height_data()
        except:
            msg = "Error saving the data"
            label_color = constants.COLOR_RED
        else:
            msg = "Saved successfully"
            label_color = constants.COLOR_GREEN
        finally:
            self.message_l.setText(msg)
            self.message_l.setStyleSheet("background-color: {}".format(label_color))
            self.message_l.repaint()

class ASDWidget(QtWidgets.QWidget):
    def __init__(self, config_w : ifaces.IConfigWidget, session_status: SessionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        session_status : SessionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | ASD"
        self.config_w = config_w
        self.session_status = session_status
        self._build_layout()

    def _build_layout(self):
        self.v_spacers = []
        self.h_spacers = []
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # Title
        self.title = QtWidgets.QLabel(self.title_str, alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.title)
        # Input
        self.input_layout = QtWidgets.QVBoxLayout()
        # Ip input (Row 1)
        self.lay_ip = QtWidgets.QHBoxLayout()
        self.ip_label = QtWidgets.QLabel("IP:", alignment=QtCore.Qt.AlignCenter)
        self.ip_input = QtWidgets.QLineEdit(self.session_status.asd_ip)
        add_spacer(self.lay_ip, self.h_spacers)
        self.lay_ip.addWidget(self.ip_label)
        add_spacer(self.lay_ip, self.h_spacers)
        self.lay_ip.addWidget(self.ip_input)
        add_spacer(self.lay_ip, self.h_spacers)
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.lay_ip)
        # Port input (Row 2)
        self.lay_port = QtWidgets.QHBoxLayout()
        self.port_label = QtWidgets.QLabel("Port:", alignment=QtCore.Qt.AlignCenter)
        self.port_input = QtWidgets.QSpinBox()
        self.port_input.setMaximum(1000000)
        self.port_input.setMinimum(1)
        prev_port = self.session_status.asd_port
        if prev_port is None or prev_port == 0:
            prev_port = 8080
        self.port_input.setValue(prev_port)
        add_spacer(self.lay_port, self.h_spacers)
        self.lay_port.addWidget(self.port_label)
        add_spacer(self.lay_port, self.h_spacers)
        self.lay_port.addWidget(self.port_input)
        add_spacer(self.lay_port, self.h_spacers)
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.lay_port)
        # Folder input (Row 3)
        self.lay_folder = QtWidgets.QVBoxLayout()
        self.lay_folder_input = QtWidgets.QHBoxLayout()
        self.select_label = QtWidgets.QLabel("ASD directory:", alignment=QtCore.Qt.AlignCenter)
        self.select_btn = QtWidgets.QPushButton("Select folder")
        self.select_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.select_btn.clicked.connect(self.open_file_dialog)
        self.asd_folder = self.session_status.asd_folder
        self.dir_str = self.asd_folder
        if self.dir_str == "":
            self.dir_str = "No directory selected"
        elif self.dir_str == ".":
            self.dir_str = "Using current execution directory"
        self.selected_label = QtWidgets.QLabel(self.dir_str, alignment=QtCore.Qt.AlignCenter)
        add_spacer(self.lay_folder_input, self.h_spacers)
        self.lay_folder_input.addWidget(self.select_label)
        add_spacer(self.lay_folder_input, self.h_spacers)
        self.lay_folder_input.addWidget(self.select_btn)
        add_spacer(self.lay_folder_input, self.h_spacers)
        add_spacer(self.lay_folder, self.v_spacers)
        self.lay_folder.addLayout(self.lay_folder_input)
        add_spacer(self.lay_folder, self.v_spacers)
        self.lay_folder.addWidget(self.selected_label)
        add_spacer(self.lay_folder, self.v_spacers)
        add_spacer(self.input_layout, self.v_spacers)
        self.input_layout.addLayout(self.lay_folder)
        # Finish input
        add_spacer(self.input_layout, self.v_spacers)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.input_layout)
        # Message
        self.message_l = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.message_l.setObjectName("message")
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.message_l)
        # Save button
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_values)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.save_button)
        # Finish main layout
        add_spacer(self.main_layout, self.v_spacers)

    @QtCore.Slot()
    def open_file_dialog(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        if dlg.exec_():
            folderpaths = dlg.selectedFiles()
            self.asd_folder = folderpaths[0]
            self.selected_label.setText(self.asd_folder)

    @QtCore.Slot()
    def save_values(self):
        self.session_status.asd_ip = self.ip_input.text()
        self.session_status.asd_port = self.port_input.value()
        self.session_status.asd_folder = self.asd_folder
        try:
            self.session_status.save_asd_ip_data()
            self.session_status.save_asd_port_data()
            self.session_status.save_asd_folder_data()
        except:
            msg = "Error saving the data"
            label_color = constants.COLOR_RED
        else:
            msg = "Saved successfully"
            label_color = constants.COLOR_GREEN
        finally:
            self.message_l.setText(msg)
            self.message_l.setStyleSheet("background-color: {}".format(label_color))
            self.message_l.repaint()
