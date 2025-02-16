import requests
import winreg
import subprocess
import os

from find_steam_path import *
from find_install_location import *

def download_to_path(url, fullfile):
    response = requests.get(url)
    if response.status_code == 200:
        with open(fullfile, 'wb') as file:
            file.write(response.content)
        print("File downloaded")
    else:
        print('Failed to download file')

program_name = "Goose Goose Duck"

install_dir = None
if not install_dir:
    install_dir = find_install_location(program_name, winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
if not install_dir:
    install_dir = find_install_location(program_name, winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
if not install_dir:
    install_dir = find_install_location(program_name, winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
if not install_dir:
    install_dir = find_install_location(program_name, winreg.HKEY_CURRENT_USER, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall")

if install_dir:
    print(f"Путь установки '{program_name}': {install_dir}")
    url = 'http://drive.google.com/uc?export=download&id=18Yr6wfSAJZTqhttMFVDNx7pZkez2vJBq'
    filename = 'settings.txt'
    fullfile = install_dir + '\\' + filename
    download_to_path(url, fullfile)
    with open(fullfile, 'r'):
        try:
            subprocess.check_call(
                ["reg", "import", fullfile],
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            print(f"Настройки из файла реестра '{fullfile}' успешно импортированы.")
            if ("\SteamLibrary\steamapps\common" in fullfile):
                steam_path = find_steam_location()
                print(f"Путь установки Steam: {steam_path}")
                subprocess.run([steam_path, "steam://rungameid/1568590"], check=True)
            else:
                subprocess.run([install_dir + "\\Goose Goose Duck.exe"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при импорте файла реестра: {e}")
else:
    print(f"Программа '{program_name}' не найдена в реестре.")



