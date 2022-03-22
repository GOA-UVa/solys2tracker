"""Common
This module contains functionalities that are used in multiple modules.

It exports the following functions:
    * add_spacer: Adds a QSpacerItem to the layout, and adds it to the spacers list.
"""

"""___Built-In Modules___"""
from typing import List

"""___Third-Party Modules___"""
from PySide2 import QtWidgets

"""___Solys2Tracker Modules___"""
# import here

"""___Authorship___"""
__author__ = 'Javier Gatón Herguedas'
__created__ = "2022/03/22"
__maintainer__ = "Javier Gatón Herguedas"
__email__ = "gaton@goa.uva.es"
__status__ = "Development"

def add_spacer(layout: QtWidgets.QBoxLayout, spacers: List[QtWidgets.QSpacerItem], w: int = 0, h: int = 0):
    """
    Adds a QSpacerItem to the layout, and adds it to the spacers list.

    Parameters
    ----------
    layout : QBoxLayout
        QBoxLayout where the spacer will be added to.
    spacers : list of QSpacerItem
        List of QSpacerItem where the created spacer will be appended to.
    w : int
        Width of the spacer. Default 0.
    h : int
        Height of the spacer. Default 0.
    """
    spacer = QtWidgets.QSpacerItem(w, h)
    layout.addSpacerItem(spacer)
    spacers.append(spacer)