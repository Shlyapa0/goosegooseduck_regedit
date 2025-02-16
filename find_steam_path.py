import winreg
import os

def find_steam_location():
    steam_path = None
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass
    except OSError:
        pass
    if not steam_path:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
            steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass
        except OSError:
            pass
    if not steam_path:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass #Key not found
    if steam_path:
        steam_path = os.path.normpath(steam_path)  # Normalize the path
        steam_path = os.path.join(steam_path, "Steam.exe")
        if not os.path.exists(steam_path):
            steam_path = None
    return steam_path