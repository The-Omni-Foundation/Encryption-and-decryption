import os
from cryptography.fernet import Fernet
from pathlib import Path
import tkinter
from tkinter import filedialog

def decrypt_items(target_path, key):
    try:
        with open(target_path, "rb") as file:
                encrypted_data = file.read()

        if not encrypted_data.startswith(b'gAAAAA'):
            return

        decrypted_data = key.decrypt(encrypted_data)

        with open(target_path, "wb") as file:
                file.write(decrypted_data)
        print("Success!")
    except Exception as e:
            print(f"Error decrypting {os.path.basename(target_path)}: {type(e).__name__} - {e}")

def find_file_path():
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    root.destroy()
    return path
     
def find_dir_path():
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    root.destroy()
    return path

while True:

        #loading existing key
    key_raw = input("Enter name of key (don't include .key) ")

    if not key_raw.lower().endswith(".key"):
        key_name = key_raw + ".key"
    else:
        key_name = key_raw

    key_path = Path(key_raw).with_suffix(".key")

    if key_path.is_file():
        print("Found!")

    try: 
        with open(key_name, "rb") as key_file:
            key = key_file.read()

        fernet_key = Fernet(key)

    except Exception as e:
        print(f"Could not decrypt: {e}")

    typeofpath = input("file or directory? (f/d) ")

    if typeofpath.lower() in ['d', "directory"]:
            path = find_dir_path()

    elif typeofpath.lower() in ['f', "file"]:
            path = find_file_path()

    if os.path.isfile(path):

        decrypt_items(path, fernet_key)

    elif os.path.isdir(path):

        for root, dirs, files in os.walk(path):

            for filename in files:
                if filename == key_path.name:
                    continue

                full_path = os.path.join(root, filename)
                decrypt_items(full_path, fernet_key)

                
