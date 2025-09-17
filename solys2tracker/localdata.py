import os
import sys
import pickle
from typing import Dict
import pathlib

try:
    from solys2tracker import constants
except Exception:
    import constants



def _is_valid_appdata(appdata: str) -> bool:
    """Checks if a given appdata path is valid, and tries to modify it if not so it is.

    Parameters
    ----------
    appdata: str
        Appdata folder absolute path

    Returns
    -------
    valid: bool
        Validity of the appdata path.
    """
    if not os.path.exists(appdata):
        try:
            os.makedirs(appdata)
        except Exception:
            return False
    return True


def _get_appdata_folder(platform: str) -> str:
    """Find the theoretical path of the appdata folder for a given platform. Function useful for testing.

    Parameters
    ----------
    platform: str
        System OS platform (darwin, win32 or linux)

    Returns
    -------
    appdata_path: str
        Appdata folder absolute path for that platform
    """
    if platform == "darwin":
        home = pathlib.Path.home()
        appdata = str(home / "Library/Application Support" / constants.APPLICATION_NAME)
    elif platform == "win32":
        appdata = os.path.join(
            os.environ.get("APPDATA", os.path.join(os.getcwd(), "appdata")),
            constants.APPLICATION_NAME,
        )
    else:
        appdata = os.path.expanduser(os.path.join("~", "." + constants.APPLICATION_NAME))
    return appdata


def get_appdata_folder() -> str:
    """Find the path of the appdata folder

    Returns
    -------
    appdata_path: str
        Appdata folder absolute path
    """
    platf = sys.platform
    appdata = _get_appdata_folder(platf)
    if not _is_valid_appdata(appdata):
        print("Appdata folder not valid, using '.'")
        appdata = "."
    return appdata


def get_data_path() -> str:
    return os.path.join(get_appdata_folder(), constants.DATA_FILE_PATH)


def save_value(key: str, value: str):
    d = get_all_values()
    d[key] = value
    f = open(get_data_path(), "wb")
    pickle.dump(d, f)
    f.close()


def get_all_values() -> Dict[str, str]:
    try:
        f=open(get_data_path(),"rb")
        d=pickle.load(f)
        f.close()
    except Exception:
        d = {}
    return d


def get_value(key: str) -> str:
    d = get_all_values()
    if key in d:
        return d[key]
    return ""
