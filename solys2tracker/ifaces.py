"""Ifaces
This module contains interfaces, abstract classes that will be implemented,
that are used in multiple modules in order to avoid ciclical dependencies.

It exports the following interfaces:
    * ISolys2Widget: Interface of the main widget that will contain the main
        functionality and other widgets.
"""

"""___Built-In Modules___"""
# import here

"""___Third-Party Modules___"""
# import here

"""___Solys2Tracker Modules___"""
# import here

"""___Authorship___"""
__author__ = 'Javier Gatón Herguedas'
__created__ = "2022/03/22"
__maintainer__ = "Javier Gatón Herguedas"
__email__ = "gaton@goa.uva.es"
__status__ = "Development"

from abc import ABC, abstractmethod

class ISolys2Widget(ABC):
    """
    Interface of the main widget that will contain the main functionality and other widgets.
    """
    @abstractmethod
    def connection_changed(self) -> None:
        pass