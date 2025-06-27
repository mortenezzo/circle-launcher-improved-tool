import ctypes
from ctypes import wintypes
import os


def get_path_from_folder_clsid(clsid: str) -> str:
    """
    Retrieve the path associated with a given CLSID from the Windows registry.

    :param clsid: The CLSID to look up.
    :return: The path associated with the CLSID, or an empty string if not found.
    """
    import winreg

    try:
        # Open the CLSID key in the registry
        guid = GUID()
        ctypes.OleDLL("ole32").CLSIDFromString(clsid, ctypes.byref(guid))

        # Llamar a SHGetKnownFolderPath
        path = ctypes.c_wchar_p()
        ctypes.windll.shell32.SHGetKnownFolderPath(
            ctypes.byref(guid),
            0,  # Flags: KF_FLAG_DEFAULT
            None,
            ctypes.byref(path)
        )

        # Liberar memoria y retornar la ruta
        folder_path = path.value
        ctypes.windll.ole32.CoTaskMemFree(path)
        return folder_path
    except FileNotFoundError:
        # If the CLSID is not found, return an empty string
        return ""
    except Exception as e:
        # Handle other exceptions (e.g., permission issues)
        print(f"Error retrieving path for CLSID {clsid}: {e}")
        return ""

class GUID(ctypes.Structure):
    _fields_ = [("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)]