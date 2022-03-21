"""
This module contains
"""

"""___Built-In Modules___"""
# import here

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from solys2 import solys2 as s2

"""___Solys2Tracker Modules___"""
try:
    from .s2ttypes import ConnectionStatus
    from . import constants
except:
    import constants
    from s2ttypes import ConnectionStatus

def _try_conn(ip: str, port: int, password: str) -> bool:
    try:
        _ = s2.Solys2(ip, port, password)
    except:
        return False
    return True

class ConfigurationWidget(QtWidgets.QWidget):
    def __init__(self, conn_status: ConnectionStatus):
        super().__init__()
        self.conn_status = conn_status
        self._build_layout()
    
    def _build_layout(self):
        self.ip_label = QtWidgets.QLabel("IP:")
        self.port_label = QtWidgets.QLabel("Port:")
        self.pass_label = QtWidgets.QLabel("Password:")

        self.ip_input = QtWidgets.QLineEdit(self.conn_status.ip)
        self.port_input = QtWidgets.QSpinBox()
        self.port_input.setMaximum(100000)
        self.port_input.setValue(self.conn_status.port)
        self.pass_input = QtWidgets.QLineEdit(self.conn_status.password)

        self.lay_labels = QtWidgets.QVBoxLayout()
        self.lay_labels.addWidget(self.ip_label)
        self.lay_labels.addWidget(self.port_label)
        self.lay_labels.addWidget(self.pass_label)
        self.lay_inputs = QtWidgets.QVBoxLayout()
        self.lay_inputs.addWidget(self.ip_input)
        self.lay_inputs.addWidget(self.port_input)
        self.lay_inputs.addWidget(self.pass_input)

        self.connect_but = QtWidgets.QPushButton("Connect")
        self.connect_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.content_layout = QtWidgets.QVBoxLayout()
        self.input_layout = QtWidgets.QHBoxLayout()
        self.input_layout.addLayout(self.lay_labels, 1)
        self.input_layout.addLayout(self.lay_inputs, 1)
        self.content_layout.addLayout(self.input_layout, 1)
        self.content_layout.addWidget(self.connect_but, 1)

        self.title = QtWidgets.QLabel("Configuration", alignment=QtCore.Qt.AlignCenter)
        self.title.setObjectName("section_title")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.content_layout, 1)

    @QtCore.Slot()
    def check_connection(self):
        ip = self.ip_input.text()
        port = self.port_input.value()
        password = self.port_input.value()
        is_connected = _try_conn(ip, port, password)
        self.conn_status.ip = ip
        self.conn_status.port = port
        self.conn_status.password = password
        self.conn_status.is_connected = is_connected
        if is_connected:
            pass