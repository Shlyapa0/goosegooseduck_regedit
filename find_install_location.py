import winreg

def find_install_location(display_name, keypart, registry_key):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_key)
        i = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(key, i)
                i += 1
                try:
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        display_name_value = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        if display_name_value == display_name:
                            try:
                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                return install_location #return install path
                            except FileNotFoundError:
                                pass
                    except FileNotFoundError:
                        pass
                    finally:
                        winreg.CloseKey(subkey)
                except OSError:
                    print("Failed to open subkey (permission issues?)")
            except OSError:  # No more subkeys
                break

    except FileNotFoundError:
        print(f"Key '{registry_key}' not found.")
        return None

    finally:
        if 'key' in locals():
            winreg.CloseKey(key)

    return None