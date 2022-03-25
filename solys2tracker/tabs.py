"""
This module contains the main tabs that will be present in the application.

It exports the following classes:
    * ConfigurationWidget: The Configuration Tab.
"""

"""___Built-In Modules___"""
from typing import Tuple, List

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from solys2 import solys2 as s2

"""___Solys2Tracker Modules___"""
try:
    from .s2ttypes import ConnectionStatus, BodyEnum
    from . import constants
    from . import ifaces
    from . import noconflict
    from .common import add_spacer
    from .bodywidgets import BodyMenuWidget, BodyTrackWidget, BodyCrossWidget, BodyBlackWidget
except:
    import constants
    import ifaces
    import noconflict
    from s2ttypes import ConnectionStatus, BodyEnum
    from common import add_spacer
    from bodywidgets import BodyMenuWidget, BodyTrackWidget, BodyCrossWidget, BodyBlackWidget

"""___Authorship___"""
__author__ = 'Javier Gatón Herguedas'
__created__ = "2022/03/18"
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

class ConfigurationWidget(QtWidgets.QWidget):
    """
    The configuration tab.
    
    Attributes
    ----------
    conn_status : ConnectionStatus
        Current status of the GUI connection with the Solys2.
    solys2_w : ISolys2Widget
        Main parent widget that contains the main functionality and other widgets.
    v_spacers : list of QSpacerItem
    h_spacers : list of QSpacerItem
    title : QLabel
    main_layout : QBoxLayout
    content_layout : QBoxLayout
    input_layout : QBoxLayout
    lay_ip : QBoxLayout
    ip_label : QLabel
    ip_input : QLineEdit
    lay_port : QBoxLayout
    port_label : QLabel
    port_input : QSpinBox
    lay_pass : QBoxLayout
    pass_label : QLabel
    pass_input : QLineEdit
    message_l : QLabel
    connect_but : QPushButton
    """
    def __init__(self, solys2_w : ifaces.ISolys2Widget, conn_status: ConnectionStatus):
        """
        Parameters
        ----------
        solys2_w : ISolys2Widget
            Main parent widget that contains the main functionality and other widgets.
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.conn_status = conn_status
        self.solys2_w = solys2_w
        self._build_layout()
    
    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.v_spacers = []
        self.h_spacers = []
        # Title
        self.title = QtWidgets.QLabel("Configuration", alignment=QtCore.Qt.AlignCenter)
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
        self.worker = ConfigurationWidget.TryConnectionWorker(ip, port, password)
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
        self.solys2_w.connection_changed()
        self.connect_but.setEnabled(True)
    
    def set_disabled_navbar(self, disabled: bool):
        """
        Set the disabled status for all navbar buttons.

        Parameters
        ----------
        disabled : bool
            Chosen disabled status.
        """
        self.solys2_w.set_disabled_navbar(disabled)
    
    def set_enabled_close_button(self, enabled: bool):
        """
        Set the enabled status for the close button.

        Parameters
        ----------
        enabled : bool
            Enabled status.
        """
        self.solys2_w.set_enabled_close_button(enabled)

class SunTabWidget(QtWidgets.QWidget, ifaces.IBodyTabWidget, metaclass=noconflict.makecls()):
    """
    The sun tab.
    """
    def __init__(self, solys2_w : ifaces.ISolys2Widget, conn_status: ConnectionStatus):
        """
        Parameters
        ----------
        solys2_w : ISolys2Widget
            Main parent widget that contains the main functionality and other widgets.
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.solys2_w = solys2_w
        self.conn_status = conn_status
        self.title_str = "SUN"
        self.menu_options = ["Track", "Cross", "Mesh"]
        self._build_layout()
    
    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.page_w = BodyMenuWidget(self, self.title_str, self.menu_options)
        self.main_layout.addWidget(self.page_w)

    def change_to_view(self, option: str) -> None:
        """
        Changes the page view to the selected option. It must be in self.get_menu_options()

        Parameters
        ----------
        option : str
            Selected option that the GUI will change its page to.
        """
        if option not in self.menu_options:
            raise Exception("Object has no function \"{}\"".format(option))
        self.main_layout.removeWidget(self.page_w)
        self.page_w.deleteLater()
        body = BodyEnum.SUN
        if option == self.menu_options[0]:
            self.page_w = BodyTrackWidget(self, body, self.conn_status)
        elif option == self.menu_options[1]:
            self.page_w = BodyCrossWidget(self, body, self.conn_status)
        else:
            self.page_w = BodyCrossWidget(self, body, self.conn_status, is_mesh = True)
        self.main_layout.addWidget(self.page_w)
    
    def set_disabled_navbar(self, disabled: bool):
        """
        Set the disabled status for all navbar buttons.

        Parameters
        ----------
        disabled : bool
            Chosen disabled status.
        """
        self.solys2_w.set_disabled_navbar(disabled)

    def get_menu_options(self) -> List[str]:
        """
        Obtain all available page options.

        Returns
        -------
        options : list of str
            List with all available options.
        """
        return self.menu_options
    
    def set_enabled_close_button(self, enabled: bool):
        """
        Set the enabled status for the close button.

        Parameters
        ----------
        enabled : bool
            Enabled status.
        """
        self.solys2_w.set_enabled_close_button(enabled)

class MoonTabWidget(QtWidgets.QWidget, ifaces.IBodyTabWidget, metaclass=noconflict.makecls()):
    """
    The moon tab.
    """
    def __init__(self, solys2_w : ifaces.ISolys2Widget, conn_status: ConnectionStatus):
        """
        Parameters
        ----------
        solys2_w : ISolys2Widget
            Main parent widget that contains the main functionality and other widgets.
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        """
        super().__init__()
        self.solys2_w = solys2_w
        self.conn_status = conn_status
        self.title_str = "MOON"
        self.menu_options = ["Track", "Cross", "Mesh", "Black"]
        self._build_layout()
    
    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.page_w = BodyMenuWidget(self, self.title_str, self.menu_options)
        self.main_layout.addWidget(self.page_w)

    def change_to_view(self, option: str) -> None:
        """
        Changes the page view to the selected option. It must be in self.get_menu_options()

        Parameters
        ----------
        option : str
            Selected option that the GUI will change its page to.
        """
        if option not in self.menu_options:
            raise Exception("Object has no function \"{}\"".format(option))
        self.main_layout.removeWidget(self.page_w)
        self.page_w.deleteLater()
        body = BodyEnum.MOON
        if option == self.menu_options[0]:
            self.page_w = BodyTrackWidget(self, body, self.conn_status)
        elif option == self.menu_options[1]:
            self.page_w = BodyCrossWidget(self, body, self.conn_status)
        elif option == self.menu_options[2]:
            self.page_w = BodyCrossWidget(self, body, self.conn_status, is_mesh = True)
        else:
            self.page_w = BodyBlackWidget(self, body, self.conn_status)
        self.main_layout.addWidget(self.page_w)

    def set_disabled_navbar(self, disabled: bool):
        """
        Set the disabled status for all navbar buttons.

        Parameters
        ----------
        disabled : bool
            Chosen disabled status.
        """
        self.solys2_w.set_disabled_navbar(disabled)

    def get_menu_options(self) -> List[str]:
        """
        Obtain all available page options.

        Returns
        -------
        options : list of str
            List with all available options.
        """
        return self.menu_options

    def set_enabled_close_button(self, enabled: bool):
        """
        Set the enabled status for the close button.

        Parameters
        ----------
        enabled : bool
            Enabled status.
        """
        self.solys2_w.set_enabled_close_button(enabled)
