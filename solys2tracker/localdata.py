"""___Built-In Modules___"""
import pickle
from typing import Dict

"""___Third-Party Modules___"""
# import here

"""___Solys2Tracker Modules___"""
try:
    from . import constants
except:
    import constants

def save_value(key: str, value: str):
    d = get_all_values()
    d[key] = value
    f = open(constants.DATA_FILE_PATH, "wb")
    pickle.dump(d, f)
    f.close()

def get_all_values() -> Dict[str, str]:
    try:
        f=open(constants.DATA_FILE_PATH,"rb")
        d=pickle.load(f)
        f.close()
        return d
    except:
        return {}

def get_value(key: str) -> str:
    d = get_all_values()
    if key in d:
        return d[key]
    return ""