"""Ifaces
This module contains interfaces, abstract classes that will be implemented,
that are used in multiple modules in order to avoid ciclical dependencies.

It exports the following interfaces:
    * ISolys2Widget: Interface of the main widget that will contain the main
        functionality and other widgets.
"""

"""___Built-In Modules___"""
from typing import List

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
        """
        Function called when the connection status (self.conn_status) has changed.
        It will update the navigation bar and the GUI.
        """
        pass

    @abstractmethod
    def change_tab_sun(self) -> None:
        """
        Change the tab to the SUN tab.
        """
        pass

    @abstractmethod
    def change_tab_moon(self) -> None:
        """
        Change the tab to the MOON tab.
        """
        pass

    @abstractmethod
    def change_tab_conf(self) -> None:
        """
        Change the tab to the CONFIGURATION tab.
        """
        pass

    @abstractmethod
    def set_disabled_navbar(self, disabled: bool):
        """
        Set the disabled status for all the navbar buttons.

        Parameters
        ----------
        disabled : bool
            Disabled status.
        """
        pass

    @abstractmethod
    def set_enabled_close_button(self, enabled: bool):
        """
        Set the enabled status for the close button.

        Parameters
        ----------
        enabled : bool
            Enabled status.
        """
        pass

class IBodyTabWidget(ABC):
    @abstractmethod
    def change_to_view(self, option: str) -> None:
        """
        Changes the page view to the selected option. It must be in self.get_menu_options()

        Parameters
        ----------
        option : str
            Selected option that the GUI will change its page to.
        """
        pass

    @abstractmethod
    def set_disabled_navbar(self, disabled: bool) -> None:
        """
        Set the disabled status for all navbar buttons.

        Parameters
        ----------
        disabled : bool
            Chosen disabled status.
        """
        pass

    @abstractmethod
    def get_menu_options(self) -> List[str]:
        """
        Obtain all available page options.

        Returns
        -------
        options : list of str
            List with all available options.
        """
        pass

    @abstractmethod
    def set_enabled_close_button(self, enabled: bool):
        """
        Set the enabled status for the close button.

        Parameters
        ----------
        enabled : bool
            Enabled status.
        """
        pass

class IConfigWidget(ABC):
    
    @abstractmethod
    def connection_changed(self):
        """
        Function called when the connection status (self.conn_status) has changed.
        It will update the navigation bar and the GUI.
        """
        pass

    @abstractmethod
    def set_disabled_navbar(self, disabled: bool):
        """
        Set the disabled status for all navbar buttons.

        Parameters
        ----------
        disabled : bool
            Chosen disabled status.
        """
        pass

    @abstractmethod
    def set_disabled_config_navbar(self, disabled: bool):
        """
        Set the disabled status for all configuration sub-navbar buttons.

        Parameters
        ----------
        disabled : bool
            Chosen disabled status.
        """
        pass

    @abstractmethod
    def set_enabled_close_button(self, enabled: bool):
        """
        Set the enabled status for the close button.

        Parameters
        ----------
        enabled : bool
            Enabled status.
        """
        pass

    @abstractmethod
    def change_tab_connection(self) -> None:
        """
        Change the tab to the CONNECTION tab.
        """
        pass

    @abstractmethod
    def change_tab_spice(self) -> None:
        """
        Change the tab to the SPICE tab.
        """
        pass

    @abstractmethod
    def change_tab_log(self) -> None:
        """
        Change the tab to the LOG tab.
        """
        pass

    @abstractmethod
    def change_tab_adjust(self) -> None:
        """
        Change the tab to the ADJUST tab.
        """
        pass
