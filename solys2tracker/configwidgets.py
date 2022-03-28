"""
This module contains the configuration pages.

It exports the following classes:
    * ConfigurationWidget: The Configuration Tab.
"""

"""___Built-In Modules___"""
from ctypes import alignment
from typing import Tuple

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from solys2 import solys2 as s2

"""___Solys2Tracker Modules___"""
try:
    from solys2tracker.s2ttypes import ConnectionStatus
    from solys2tracker import constants
    from solys2tracker import ifaces
    from solys2tracker.common import add_spacer
except:
    import constants
    import ifaces
    from s2ttypes import ConnectionStatus
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
    def __init__(self, config_w : ifaces.IConfigWidget, conn_status: ConnectionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        """
        self.conn_status = conn_status
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
        self.update_button_enabling()

    def set_enabled_buttons(self, enabled: bool):
        """
        Enables or disables all the navigation buttons.
        """
        self.conn_but.setEnabled(enabled)
        self.spice_but.setEnabled(enabled)
        self.log_but.setEnabled(enabled)
        self.adjust_but.setEnabled(enabled)

    def update_button_enabling(self):
        """
        Updates the enabled status of the buttons based on if the connection_status
        is connected.
        """
        enabled = self.conn_status.is_connected
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

class ConnectionWidget(QtWidgets.QWidget):
    """
    Configuration page containing the Solys2 connection functionality.
    """
    def __init__(self, config_w : ifaces.IConfigWidget, conn_status: ConnectionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.conn_status = conn_status
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
        self.ip_input = QtWidgets.QLineEdit(self.conn_status.ip)
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
        self.port_input.setValue(self.conn_status.port)
        add_spacer(self.lay_port, self.h_spacers)
        self.lay_port.addWidget(self.port_label)
        add_spacer(self.lay_port, self.h_spacers)
        self.lay_port.addWidget(self.port_input)
        add_spacer(self.lay_port, self.h_spacers)
        # Third row (Password)
        self.lay_pass = QtWidgets.QHBoxLayout()
        self.pass_label = QtWidgets.QLabel("Password:", alignment=QtCore.Qt.AlignCenter)
        self.pass_input = QtWidgets.QLineEdit(self.conn_status.password)
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
        if self.conn_status.is_connected:
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
        self.conn_status.ip = ip
        self.conn_status.port = port
        self.conn_status.password = password

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
            self.conn_status.save_ip_data()
            label_color = constants.COLOR_GREEN
            connect_msg = "Reconnect"
        self.connect_but.setText(connect_msg)
        self.message_l.setStyleSheet("background-color: {}".format(label_color))
        self.message_l.repaint()
        self.conn_status.is_connected = is_connected
        self.config_w.connection_changed()
        self.connect_but.setEnabled(True)

class SpiceWidget(QtWidgets.QWidget):
    def __init__(self, config_w : ifaces.IConfigWidget, conn_status: ConnectionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | SPICE"
        self.config_w = config_w
        self.conn_status = conn_status
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
        self.kernels_path = self.conn_status.kernels_path
        self.dir_str = self.kernels_path
        if self.dir_str == "":
            self.dir_str = "No directory selected"
        self.selected_label = QtWidgets.QLabel(self.dir_str, alignment=QtCore.Qt.AlignCenter)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.select_label)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.select_btn)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.selected_label)
        add_spacer(self.input_layout, self.h_spacers)
        # Save button
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_directory)
        # Finish main layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.input_layout)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.save_button)
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
        self.conn_status.kernels_path = self.kernels_path
        self.conn_status.save_kernels_path_data()

class LogWidget(QtWidgets.QWidget):
    def __init__(self, config_w : ifaces.IConfigWidget, conn_status: ConnectionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | Log"
        self.config_w = config_w
        self.conn_status = conn_status
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
        try:
            rindex_slash = self.conn_status.logfile.rindex('/')
        except:
            rindex_slash = -1
        self.log_folder = "."
        if rindex_slash >= 0:
            self.log_folder = self.conn_status.logfile[:rindex_slash]
        self.dir_str = self.log_folder
        if self.dir_str == "":
            self.dir_str = "No directory selected"
        self.selected_label = QtWidgets.QLabel(self.dir_str, alignment=QtCore.Qt.AlignCenter)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.select_label)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.select_btn)
        add_spacer(self.input_layout, self.h_spacers)
        self.input_layout.addWidget(self.selected_label)
        add_spacer(self.input_layout, self.h_spacers)
        # Save button
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_directory)
        # Finish main layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.input_layout)
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addWidget(self.save_button)
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
        self.conn_status.set_logfolder(self.log_folder)
        self.conn_status.save_logfile_data()

class AdjustWidget(QtWidgets.QWidget):
    def __init__(self, config_w : ifaces.IConfigWidget, conn_status: ConnectionStatus):
        """
        Parameters
        ----------
        config_w : IConfigWidget
            Parent widget that contains the configuration page.
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.title_str = "Configuration | Adjust"
        self.config_w = config_w
        self.conn_status = conn_status
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
        self.az_extra_adjustment.setMinimum(-0.2)
        self.az_extra_adjustment.setMaximum(0.2)
        self.ze_label_input = QtWidgets.QLabel("Zenith: ", alignment=QtCore.Qt.AlignRight)
        self.ze_extra_adjustment = QtWidgets.QDoubleSpinBox()
        self.ze_extra_adjustment.setMinimum(-0.2)
        self.ze_extra_adjustment.setMaximum(0.2)
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
        # Adjust button
        self.save_button = QtWidgets.QPushButton("Adjust")
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.adjust)
        self.main_layout.addWidget(self.save_button)
        add_spacer(self.main_layout, self.v_spacers)
        # Error message
        self.err_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.err_label)
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
        self.err_label.setText("")
        self.th = QtCore.QThread()
        cs = self.conn_status
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
        self.az_curr_adjustment.setText(az)
        self.ze_curr_adjustment.setText(ze)
    
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
            try:
                solys = s2.Solys2(self.ip, self.port, self.password)
                solys.adjust_azimuth(self.az)
                solys.adjust_zenith(self.ze)
                self.success.emit()
            except Exception as e:
                self.error.emit(str(e))
            finally:
                self.finished.emit()

    @QtCore.Slot()
    def adjust(self):
        self.err_label.setText("")
        self.th = QtCore.QThread()
        cs = self.conn_status
        az = self.az_extra_adjustment.value()
        ze = self.ze_extra_adjustment.value()
        self.worker = AdjustWidget.SendAdjustWorker(cs.ip, cs.port, cs.password, az, ze)
        self.worker.moveToThread(self.th)
        self.th.started.connect(self.worker.run)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.show_error)
        self.worker.success.connect(self.update_adjustment_labels)
        self.worker.finished.connect(self.thread_finished)
        self.th.finished.connect(self.th.deleteLater)
        self.thread_started()
        self.th.start()

    def show_error(self, msg: str):
        self.err_label.setText("Error: {}".format(msg))