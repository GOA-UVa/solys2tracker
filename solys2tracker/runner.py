#!/usr/bin/env python3
"""Solys2Tracker Runner Module

This module starts the Solys2Tracker GUI when executed.
"""

"""___Built-In Modules___"""
from typing import Union
from pathlib import Path
import sys
from os import path as os_path

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui

"""___Solys2Tracker Modules___"""
try:
    from . import constants
    from .tabs import ConfigurationWidget
    from .s2ttypes import ConnectionStatus
except:
    import constants
    from tabs import ConfigurationWidget
    from s2ttypes import ConnectionStatus

class NavBarWidget(QtWidgets.QWidget):
    def __init__(self):
        self._build_layout()

    def _build_layout(self):
        super().__init__()
        self.sun_but = QtWidgets.QPushButton("SUN")
        self.sun_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.moon_but = QtWidgets.QPushButton("MOO")
        self.moon_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.conf_but = QtWidgets.QPushButton("CON")
        self.conf_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.sun_but, 1)
        self.layout.addWidget(self.moon_but, 1)
        self.layout.addWidget(self.conf_but)

class Solys2Widget(QtWidgets.QWidget):
    """Main widget that will contain the main functionality and other widgets.
    
    Attributes
    ----------
    kernel_path : str
        Path where the kernels directory is located
    navbar_w : DateTimeWidget
        Widget that contains the navigation bar.
    content_w : ConfigurationWidget |
        Widget that contains the current visible functionality.
    layout : QtWidgets.QHBoxLayout
        Main layout of the widget.
    conn_status : ConnectionStatus
        Current status of the GUI connection with the Solys2.
    """
    def __init__(self, kernel_path: str = constants.KERNELS_PATH):
        """
        Parameters
        ----------
        kernel_path : str
            Path where the kernels directory is located
        """
        super().__init__()
        self.kernel_path = kernel_path
        self.is_connected = False
        self.conn_status = ConnectionStatus(None, None, None, False)
        self._build_layout()
    
    def _build_layout(self):
        self.navbar_w = NavBarWidget()
        self.content_w: Union[ConfigurationWidget, ConfigurationWidget] = \
            ConfigurationWidget(self.conn_status)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.navbar_w)
        self.layout.addWidget(self.content_w)

class MainWindow(QtWidgets.QMainWindow):
    """Main window that will contain the main widget."""
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Overwriting of the closeEvent.
        It tells the Solys2Widget to close the results windows, and then it calls super() closeEvent.
        """
        solys2_w: Solys2Widget = self.centralWidget()
        #solys2_w.close_results()
        return super().closeEvent(event)

def filepathToStr(filepath: str) -> str:
    """Given filepath it returns its contents as a string

    Parameters
    ----------
    filepath : str
        relative path of the file to read

    Returns
    -------
    content : str
        Contents of the file as a str
    """
    data = ""
    abs_path = str(Path(__file__).parent.absolute() / filepath)
    try:
        with open(abs_path) as styles:
            data = styles.read()
    except:
        print("Error opening file", abs_path)
    return data

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os_path.join(sys._MEIPASS, relative_path)
    return os_path.join(os_path.abspath('.'), relative_path)

def main():
    args = sys.argv[1:]
    kernels_path = constants.KERNELS_PATH
    if args and len(args) > 0:
        kernels_path = args[0]
    app = QtWidgets.QApplication([constants.APPLICATION_NAME])
    window = MainWindow()
    main_widget = Solys2Widget(kernels_path)
    window.setCentralWidget(main_widget)
    window.show()
    window.setWindowTitle(constants.APPLICATION_NAME)
    window.setStyleSheet(filepathToStr(constants.MAIN_QSS_PATH))
    window.setWindowIcon(QtGui.QIcon(resource_path(constants.ICON_PATH)))
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()