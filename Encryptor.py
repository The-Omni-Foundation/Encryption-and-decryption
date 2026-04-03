import os
from cryptography.fernet import Fernet
from pathlib import Path
import tkinter
from tkinter import filedialog

def encrypt_item(target_path, fernet_key):
    """Encrypts a single file given its path."""
    try: 
        with open(target_path, "rb") as file:
            original_data = file.read()
        
        encryptedstuff = fernet_key.encrypt(original_data)

        with open(target_path, "wb") as file:
            file.write(encryptedstuff)
            print("Success!")
    except Exception as e:
        print(f"Error during encrypting: {e}")

def find_file_path():
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    root.destroy()
    return path

def file_dir_path():
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    root.destroy()
    return path


while True:

    import_key = input("Do you already have a key to use? Warning, this might not be as secure! (y/n)")
        
    if import_key.lower() == 'y':
        keyname_to_find = input("Please enter your key's name ")
        try:
            key_path = Path(keyname_to_find)

            if key_path.suffix != ".key":
                key_path = key_path.with_suffix(".key")

            if key_path.is_file():
                print(f"Found key! {key_path}")
                keyname = key_path
            else:
                print("Couldnt find :(")
                continue
        except Exception as e:
                print(f"Error: {e}")
                continue

    else: 

        #get name, then add .key at end
        keyname_raw = input("Name of key to add (Do not add any extensions at the end) ")

        try:
            keyname2 = Path(keyname_raw)

            keyname = Path(keyname2).with_suffix(".key")
        except Exception as e:
            print("An error has occurred. Please try again: " + str(e))


        #put generated key to custom-named key
        try:
            with open(keyname, "wb") as key_file:
                key = Fernet.generate_key()
                key_file.write(key)
        except Exception as e:
            print("An error has occurred. Please try again." + str(e))

    #encryption
    with open(keyname, "rb") as key_file:
        key = key_file.read()

    fernet_key = Fernet(key)

    typeoffile = input("file or directory? (f/d)")

    if typeoffile.lower() in ['d', "directory"]:
        path = file_dir_path()

    elif typeoffile.lower() in ['f', "file"]:
        path = find_file_path()

    else:
        print("Unknown answer...")

    if not path:
        print("Cancelled, no files changed")
        continue


    if os.path.isfile(path):
        encrypt_item(path, fernet_key)
    elif os.path.isdir(path):

        #for every filename in files IN the path, join the filename to the root
        for root, dirs, files in os.walk(path):

            for filename in files:

                if filename == keyname.name:
                    print("Skipped key. You're welcome!")
                    continue

                filename = os.path.join(root, filename)
                encrypt_item(filename, fernet_key)

                



