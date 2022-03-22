#!/usr/bin/env python3
"""Solys2Tracker Runner Module

This module starts the Solys2Tracker GUI when executed.
"""

"""___Built-In Modules___"""
from enum import Enum
from typing import Union
from pathlib import Path
import sys
from os import path as os_path

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui

"""___Solys2Tracker Modules___"""
try:
    from . import constants
    from . import ifaces
    from . import noconflict
    from .tabs import ConfigurationWidget, SunTabWidget
    from .s2ttypes import ConnectionStatus
except:
    import constants
    import ifaces
    import noconflict
    from tabs import ConfigurationWidget, SunTabWidget
    from s2ttypes import ConnectionStatus

class NavBarWidget(QtWidgets.QWidget):
    """
    Navigaton bar that allows the user to change between tabs.
    """
    def __init__(self, conn_status: ConnectionStatus, solys2_w : ifaces.ISolys2Widget):
        """
        Parameters
        ----------
        conn_status : ConnectionStatus
            Current status of the GUI connection with the Solys2.
        solys2_w : ISolys2Widget
            Main parent widget that contains the main functionality and other widgets.
        """
        self.conn_status = conn_status
        self.solys2_w = solys2_w
        self._build_layout()

    def _build_layout(self):
        super().__init__()
        self.sun_but = QtWidgets.QPushButton("SUN")
        self.sun_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sun_but.clicked.connect(self.press_sun)
        self.moon_but = QtWidgets.QPushButton("MOO")
        self.moon_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.moon_but.clicked.connect(self.press_moon)
        self.conf_but = QtWidgets.QPushButton("CON")
        self.conf_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.conf_but.clicked.connect(self.press_conf)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.sun_but, 1)
        self.layout.addWidget(self.moon_but, 1)
        self.layout.addWidget(self.conf_but)
        self.update_button_enabling()

    def update_button_enabling(self):
        enabled = self.conn_status.is_connected
        self.sun_but.setEnabled(enabled)
        self.moon_but.setEnabled(enabled)
        self.conf_but.setEnabled(enabled)
    
    @QtCore.Slot()
    def press_sun(self):
        self.solys2_w.change_tab_sun()

    @QtCore.Slot()
    def press_moon(self):
        self.solys2_w.change_tab_moon()

    @QtCore.Slot()
    def press_conf(self):
        self.solys2_w.change_tab_conf()

class Solys2Widget(QtWidgets.QWidget, ifaces.ISolys2Widget, metaclass=noconflict.makecls()):
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
        self.navbar_w = NavBarWidget(self.conn_status, self)
        self.content_w: Union[ConfigurationWidget, SunTabWidget] = \
            ConfigurationWidget(self.conn_status, self)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.navbar_w)
        self.main_layout.addWidget(self.content_w)
    
    def connection_changed(self):
        """
        Function called when the connection status (self.conn_status) has changed.
        It will update the navigation bar and the GUI.
        """
        self.navbar_w.update_button_enabling()

    class TabEnum(Enum):
        SUN = 0
        MOON = 1
        CONF = 2

    def _change_tab(self, tab: TabEnum):
        self.main_layout.removeWidget(self.content_w)
        self.content_w.deleteLater()
        if tab == Solys2Widget.TabEnum.SUN:
            self.content_w = SunTabWidget(self)
        #elif tab == Solys2Widget.TabEnum.MOON:
            #self.content_w = MoonTabWidget(self)
        else:
            self.content_w = ConfigurationWidget(self.conn_status, self)
        self.main_layout.addWidget(self.content_w)

    def change_tab_sun(self):
        """
        Change the tab to the SUN tab.
        """
        self._change_tab(Solys2Widget.TabEnum.SUN)

    def change_tab_moon(self):
        """
        Change the tab to the MOON tab.
        """
        self._change_tab(Solys2Widget.TabEnum.MOON)

    def change_tab_conf(self):
        """
        Change the tab to the CONFIGURATION tab.
        """
        self._change_tab(Solys2Widget.TabEnum.CONF)
        

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