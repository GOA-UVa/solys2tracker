from enum import Enum
from dataclasses import dataclass

try:
    from solys2tracker import localdata
except:
    import localdata

@dataclass
class SessionStatus:
    """
    Attributes
    ----------
    is_connected : bool
        Flag that tells if the GUI has tried to connect with the current params
        and has succeeded.
    """
    ip: str
    port: int
    password: str
    add_checksum: bool
    is_connected: bool
    logfolder: str
    kernels_path: str
    height: int
    asd_ip: str
    asd_port: int
    asd_folder: str

    def __post_init__(self):
        if self.ip is None:
            self.ip = self._get_ip_data()
        if self.port is None:
            self.port = 15000
        if self.password is None:
            self.password = self._get_password_data()
        if self.add_checksum is None:
            self.add_checksum = False
        if self.is_connected is None:
            self.is_connected = False
        if self.logfolder is None:
            self.logfolder = self._get_logfolder_data()
            if self.logfolder == "":
                self.logfolder = "."
        if self.kernels_path is None:
            self.kernels_path = self._get_kernels_path_data()
        if self.height is None:
            self.height = self._get_height_data()
        if self.asd_ip is None:
            self.asd_ip = self._get_asd_ip_data()
        if self.asd_port is None:
            self.asd_port = self._get_asd_port_data()
        if self.asd_folder is None:
            self.asd_folder = self._get_asd_folder_data()

    def _get_ip_data(self) -> str:
        return localdata.get_value("ip")

    def _get_password_data(self) -> str:
        psw = localdata.get_value("password")
        if not psw:
            psw = "solys"
        return psw

    def _get_kernels_path_data(self) -> str:
        return localdata.get_value("kernels_path")

    def _get_logfolder_data(self) -> str:
        return localdata.get_value("logfolder")

    def _get_height_data(self) -> int:
        height_str = localdata.get_value("height")
        if height_str == "":
            return 0
        return int(height_str)

    def _get_asd_ip_data(self) -> str:
        return localdata.get_value("asd_ip")

    def _get_asd_port_data(self) -> int:
        port = localdata.get_value("asd_port")
        if port == "":
            return 0
        return int(port)

    def _get_asd_folder_data(self) -> str:
        return localdata.get_value("asd_folder")

    def save_ip_data(self):
        localdata.save_value("ip", self.ip)

    def save_password_data(self):
        localdata.save_value("password", self.password)

    def save_kernels_path_data(self):
        localdata.save_value("kernels_path", self.kernels_path)

    def save_logfolder_data(self):
        localdata.save_value("logfolder", self.logfolder)

    def save_height_data(self):
        localdata.save_value("height", self.height)
    
    def save_asd_ip_data(self):
        localdata.save_value("asd_ip", self.asd_ip)

    def save_asd_port_data(self):
        localdata.save_value("asd_port", self.asd_port)

    def save_asd_folder_data(self):
        localdata.save_value("asd_folder", self.asd_folder)

class BodyEnum(Enum):
    SUN = 0
    MOON = 1
