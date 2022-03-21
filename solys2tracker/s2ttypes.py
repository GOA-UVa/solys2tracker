from dataclasses import dataclass

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
        if self.port is None:
            self.port = 15000
        if self.password is None:
            self.password = "solys"
        if self.is_connected is None:
            self.is_connected = False
