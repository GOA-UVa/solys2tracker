"""___Built-In Modules___"""
import pickle
from dataclasses import dataclass

"""___Third-Party Modules___"""
# import here

"""___Solys2Tracker Modules___"""
try:
    from . import constants
except:
    import constants

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

    def __post_init__(self):
        if self.ip is None:
            self.ip = self._get_ip_data()
        if self.port is None:
            self.port = 15000
        if self.password is None:
            self.password = "solys"
        if self.is_connected is None:
            self.is_connected = False
    
    def _get_ip_data(self) -> str:
        try:
            f=open(constants.DATA_FILE_PATH,"rb")
            d=pickle.load(f)
            f.close()
            return d["ip"]
        except:
            return ""

    def save_ip_data(self):
        f = open(constants.DATA_FILE_PATH, "wb")
        data = {"ip":self.ip}
        pickle.dump(data, f)
        f.close()
