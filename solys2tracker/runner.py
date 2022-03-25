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
    from .tabs import ConfigurationWidget, SunTabWidget, MoonTabWidget
    from .s2ttypes import ConnectionStatus
except:
    import constants
    import ifaces
    import noconflict
    from tabs import ConfigurationWidget, SunTabWidget, MoonTabWidget
    from s2ttypes import ConnectionStatus

class NavBarWidget(QtWidgets.QWidget):
    """
    Navigaton bar that allows the user to change between tabs.
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
        self.conn_status = conn_status
        self.solys2_w = solys2_w
        self._build_layout()

    def _build_layout(self):
        super().__init__()
        self.sun_but = QtWidgets.QPushButton("SUN")
        self.sun_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sun_but.clicked.connect(self.press_sun)
        self.moon_but = QtWidgets.QPushButton("MOON")
        self.moon_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.moon_but.clicked.connect(self.press_moon)
        self.conf_but = QtWidgets.QPushButton("CONF")
        self.conf_but.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.conf_but.clicked.connect(self.press_conf)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.sun_but, 1)
        self.layout.addWidget(self.moon_but, 1)
        self.layout.addWidget(self.conf_but)
        self.update_button_enabling()

    def set_enabled_buttons(self, enabled: bool):
        """
        Enables or disables all the navigation buttons.
        """
        self.sun_but.setEnabled(enabled)
        self.moon_but.setEnabled(enabled)
        self.conf_but.setEnabled(enabled)

    def update_button_enabling(self):
        """
        Updates the enabled status of the buttons based on if the connection_status
        is connected.
        """
        enabled = self.conn_status.is_connected
        self.set_enabled_buttons(enabled)
    
    @QtCore.Slot()
    def press_sun(self):
        """Press the SUN button."""
        self.solys2_w.change_tab_sun()

    @QtCore.Slot()
    def press_moon(self):
        """Press the MOON button."""
        self.solys2_w.change_tab_moon()

    @QtCore.Slot()
    def press_conf(self):
        """Press the CONFIGURATION button."""
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
    can_close : bool
        Flag that lets the window know if the widget should not be closed.
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
        self.can_close = True
        self._build_layout()
    
    def _build_layout(self):
        self.navbar_w = NavBarWidget(self, self.conn_status)
        self.content_w: Union[ConfigurationWidget, SunTabWidget] = \
            ConfigurationWidget(self, self.conn_status)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.navbar_w)
        self.main_layout.addWidget(self.content_w)
    
    def connection_changed(self):
        """
        Function called when the connection status (self.conn_status) has changed.
        It will update the navigation bar and the GUI.
        """
        self.navbar_w.update_button_enabling()
    
    def set_disabled_navbar(self, disabled: bool):
        """
        Set the disabled status for all the navbar buttons.

        Parameters
        ----------
        disabled : bool
            Disabled status.
        """
        self.navbar_w.set_enabled_buttons(not disabled)
    
    def set_enabled_close_button(self, enabled: bool):
        """
        Set the enabled status for the close button.

        Parameters
        ----------
        enabled : bool
            Enabled status.
        """
        self.can_close = enabled

    class TabEnum(Enum):
        """Enum representing all existing tabs"""
        SUN = 0
        MOON = 1
        CONF = 2

    def _change_tab(self, tab: TabEnum):
        """
        Changes tab to the chosen one.
        
        Parameters
        ----------
        tab : TabEnum
            Selected tab which the GUI will change to.
        """
        self.main_layout.removeWidget(self.content_w)
        self.content_w.deleteLater()
        if tab == Solys2Widget.TabEnum.SUN:
            self.content_w = SunTabWidget(self, self.conn_status)
        elif tab == Solys2Widget.TabEnum.MOON:
            self.content_w = MoonTabWidget(self, self.conn_status)
        else:
            self.content_w = ConfigurationWidget(self, self.conn_status)
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
        if solys2_w.can_close:
            return super().closeEvent(event)
        event.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)

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
    window.setMinimumSize(600, 500)
    window.setCentralWidget(main_widget)
    window.show()
    window.setWindowTitle(constants.APPLICATION_NAME)
    window.setStyleSheet(filepathToStr(constants.MAIN_QSS_PATH))
    window.setWindowIcon(QtGui.QIcon(resource_path(constants.ICON_PATH)))
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()