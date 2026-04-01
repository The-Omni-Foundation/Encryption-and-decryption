import os
from cryptography.fernet import Fernet
from pathlib import Path

def encrypt_item(target_path, fernet_key):
    """Encrypts a single file given its path."""
    with open(target_path, "rb") as file:
        original_data = file.read()
    
    encryptedstuff = fernet_key.encrypt(original_data)

    with open(target_path, "wb") as file:
        file.write(encryptedstuff)

#get name, then add .key at end
keyname_raw = input("Name of key (Do not add any extensions at the end) ")

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

path = input("enter path to folder or file here ")


if os.path.isfile(path):
    encrypt_item(path, fernet_key)
elif os.path.isdir(path):

    #for every filename in files IN the path, join the filename to the root
    for root, dirs, files in os.walk(path):

        for filename in files:

            if filename == keyname:
                continue

            filename = os.path.join(root, filename)
            encrypt_item(filename, fernet_key)

                



