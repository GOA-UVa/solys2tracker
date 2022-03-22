"""
This module contains the main tabs that will be present in the application.

It exports the following classes:
    * ConfigurationWidget: The Configuration Tab.
"""

"""___Built-In Modules___"""
from typing import List

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from solys2 import solys2 as s2

"""___Solys2Tracker Modules___"""
try:
    from .s2ttypes import ConnectionStatus
    from . import constants
    from . import ifaces
    from . import noconflict
    from .common import add_spacer
except:
    import constants
    import ifaces
    import noconflict
    from s2ttypes import ConnectionStatus
    from common import add_spacer

"""___Authorship___"""
__author__ = 'Javier Gatón Herguedas'
__created__ = "2022/03/18"
__maintainer__ = "Javier Gatón Herguedas"
__email__ = "gaton@goa.uva.es"
__status__ = "Development"

class BodyMenuWidget(QtWidgets.QWidget):
    def __init__(self, body_tab: ifaces.IBodyTabWidget, title_str: str, options: List[str]):
        super().__init__()
        self.body_tab = body_tab
        self.title_str = title_str
        self.options = options
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
        self.buttons = []
        for option in self.options:
            but = QtWidgets.QPushButton(option)
            add_spacer(self.content_layout, self.v_spacers)
            self.content_layout.addWidget(but)
            self.buttons.append(but)
            but.clicked.connect(lambda: self.button_press(option))
        add_spacer(self.content_layout, self.v_spacers)
        # Finish layout
        add_spacer(self.main_layout, self.v_spacers)
        self.main_layout.addLayout(self.content_layout, 1)
        add_spacer(self.main_layout, self.v_spacers)
    
    @QtCore.Slot()
    def button_press(self, option: str):
        self.body_tab.change_to_view(option)

class BodyTrackWidget(QtWidgets.QWidget):
    pass

class BodyCrossWidget(QtWidgets.QWidget):
    pass

class BodyBlackWidget(QtWidgets.QWidget):
    pass
