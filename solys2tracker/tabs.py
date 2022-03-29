"""
This module contains the main tabs that will be present in the application.

It exports the following classes:
    * ConfigurationWidget: The Configuration Tab.
    * SunTabWidget: The Sun Tab.
    * MoonTabWidget: The Moon Tab.
"""

"""___Built-In Modules___"""
from typing import Tuple, List
from enum import Enum

"""___Third-Party Modules___"""
from PySide2 import QtWidgets, QtCore, QtGui
from solys2 import solys2 as s2

"""___Solys2Tracker Modules___"""
try:
    from solys2tracker.s2ttypes import ConnectionStatus, BodyEnum
    from solys2tracker import ifaces
    from solys2tracker import noconflict
    from solys2tracker.common import add_spacer
    from solys2tracker.bodywidgets import BodyMenuWidget, BodyTrackWidget, BodyCrossWidget, BodyBlackWidget
    from solys2tracker.configwidgets import ConnectionWidget, ConfigNavBarWidget, SpiceWidget, LogWidget, \
        AdjustWidget
except:
    import ifaces
    import noconflict
    from s2ttypes import ConnectionStatus, BodyEnum
    from common import add_spacer
    from bodywidgets import BodyMenuWidget, BodyTrackWidget, BodyCrossWidget, BodyBlackWidget
    from configwidgets import ConnectionWidget, ConfigNavBarWidget, SpiceWidget, LogWidget, \
        AdjustWidget

"""___Authorship___"""
__author__ = 'Javier Gatón Herguedas'
__created__ = "2022/03/18"
__maintainer__ = "Javier Gatón Herguedas"
__email__ = "gaton@goa.uva.es"
__status__ = "Development"

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
        self.h_spacers = []
        self.v_spacers = []
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.navbar_w = ConfigNavBarWidget(self, self.conn_status)
        self.content_w = ConnectionWidget(self, self.conn_status)
        add_spacer(self.main_layout, self.h_spacers)
        self.main_layout.addWidget(self.navbar_w)
        add_spacer(self.main_layout, self.h_spacers)
        self.main_layout.addWidget(self.content_w, 1)
        add_spacer(self.main_layout, self.h_spacers)

    def connection_changed(self):
        """
        Function called when the connection status (self.conn_status) has changed.
        It will update the navigation bar and the GUI.
        """
        self.solys2_w.connection_changed()
        self.navbar_w.update_button_enabling()
    
    def set_disabled_navbar(self, disabled: bool):
        """
        Set the disabled status for all navbar buttons.

        Parameters
        ----------
        disabled : bool
            Chosen disabled status.
        """
        self.solys2_w.set_disabled_navbar(disabled)
    
    def set_disabled_config_navbar(self, disabled: bool):
        """
        Set the disabled status for all configuration sub-navbar buttons.

        Parameters
        ----------
        disabled : bool
            Chosen disabled status.
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
        self.solys2_w.set_enabled_close_button(enabled)

    class PageEnum(Enum):
        """Enum representing all existing pages"""
        CONNECTION = 0
        SPICE = 1
        LOG = 2
        ADJUST = 3

    def _change_tab(self, page: PageEnum):
        """
        Changes tab to the chosen one.
        
        Parameters
        ----------
        page : PageEnum
            Selected page which the GUI will change to.
        """
        self.main_layout.removeWidget(self.content_w)
        self.content_w.deleteLater()
        if page == ConfigurationWidget.PageEnum.CONNECTION:
            self.content_w = ConnectionWidget(self, self.conn_status)
        elif page == ConfigurationWidget.PageEnum.SPICE:
            self.content_w = SpiceWidget(self, self.conn_status)
        elif page == ConfigurationWidget.PageEnum.LOG:
            self.content_w = LogWidget(self, self.conn_status)
        else:
            self.content_w = AdjustWidget(self, self.conn_status)
        self.main_layout.addWidget(self.content_w, 1)

    def change_tab_connection(self) -> None:
        """
        Change the tab to the CONNECTION tab.
        """
        self._change_tab(ConfigurationWidget.PageEnum.CONNECTION)

    def change_tab_spice(self) -> None:
        """
        Change the tab to the SPICE tab.
        """
        self._change_tab(ConfigurationWidget.PageEnum.SPICE)

    def change_tab_log(self) -> None:
        """
        Change the tab to the LOG tab.
        """
        self._change_tab(ConfigurationWidget.PageEnum.LOG)

    def change_tab_adjust(self) -> None:
        """
        Change the tab to the ADJUST tab.
        """
        self._change_tab(ConfigurationWidget.PageEnum.ADJUST)

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
        self.title_str = "SUN ☼"
        self.menu_options = ["Track", "Cross", "Mesh"]
        self.description_str = "PUT ON THE FILTER!"
        self._build_layout()
    
    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.page_w = BodyMenuWidget(self, self.title_str, self.menu_options, self.description_str)
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
            self.page_w = BodyTrackWidget(self, body, self.conn_status,
                self.conn_status.logfile, self.conn_status.kernels_path)
        elif option == self.menu_options[1]:
            self.page_w = BodyCrossWidget(self, body, self.conn_status,
                self.conn_status.logfile, self.conn_status.kernels_path)
        else:
            self.page_w = BodyCrossWidget(self, body, self.conn_status, 
                self.conn_status.logfile, self.conn_status.kernels_path, is_mesh = True)
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
        self.title_str = "MOON ☾"
        self.menu_options = ["Track", "Cross", "Mesh", "Black"]
        self.description_str = "TAKE OFF THE FILTER"
        self._build_layout()
    
    def _build_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.page_w = BodyMenuWidget(self, self.title_str, self.menu_options, self.description_str)
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
