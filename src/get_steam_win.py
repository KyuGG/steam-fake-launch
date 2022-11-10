import winreg


def get_steam_path() -> str | None:
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    except:
        hkey = None
    try:
        steam_path = winreg.QueryValueEx(hkey, 'InstallPath')[0].replace('\\', '/')
    except:
        steam_path = None
    winreg.CloseKey(hkey)

    return steam_path
