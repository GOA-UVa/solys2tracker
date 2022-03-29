"""___Built-In Modules___"""
from enum import Enum
from dataclasses import dataclass

"""___Third-Party Modules___"""
# import here

"""___Solys2Tracker Modules___"""
try:
    from solys2tracker import localdata
except:
    import localdata

_DEFAULT_LOGFILE = "log.temp.out.txt"

@dataclass
class ConnectionStatus:
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
    is_connected: bool
    logfile: str
    kernels_path: str

    def __post_init__(self):
        if self.ip is None:
            self.ip = self._get_ip_data()
        if self.port is None:
            self.port = 15000
        if self.password is None:
            self.password = "solys"
        if self.is_connected is None:
            self.is_connected = False
        if self.logfile is None:
            self.logfile = self._get_logfile_data()
            if self.logfile == "":
                self.logfile = _DEFAULT_LOGFILE
        if self.kernels_path is None:
            self.kernels_path = self._get_kernels_path_data()
    
    def _get_ip_data(self) -> str:
        return localdata.get_value("ip")

    def _get_kernels_path_data(self) -> str:
        return localdata.get_value("kernels_path")

    def _get_logfile_data(self) -> str:
        return localdata.get_value("logfile")

    def save_ip_data(self):
        localdata.save_value("ip", self.ip)
    
    def save_kernels_path_data(self):
        localdata.save_value("kernels_path", self.kernels_path)

    def save_logfile_data(self):
        localdata.save_value("logfile", self.logfile)

    def set_logfolder(self, logfolder: str):
        self.logfile = logfolder + "/" + _DEFAULT_LOGFILE

class BodyEnum(Enum):
    SUN = 0
    MOON = 1
