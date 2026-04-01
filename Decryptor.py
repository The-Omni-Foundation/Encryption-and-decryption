import os
from cryptography.fernet import Fernet
from pathlib import Path

def decrypt_items(target_path, key):
    with open(target_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = key.decrypt(encrypted_data)

    with open(target_path, "wb") as file:
        file.write(decrypted_data)


#loading existing key
key_raw = input("Enter name of key (don't include .key) ")

if not key_raw.lower().endswith(".key"):
    key_name = key_raw + ".key"
else:
    key_name = key_raw

try: 
    with open(key_name, "rb") as key_file:
        key = key_file.read()

    fernet_key = Fernet(key)

except Exception as e:
    print(f"Could not decrypt: {e}")

#get path
path = input("Enter path to encrypted items ")

if os.path.isfile(path):

    decrypt_items(path, fernet_key)

elif os.path.isdir(path):

    for root, dirs, files in os.walk(path):

        for filename in files:
            if filename == key_name:
                continue

            full_path = os.path.join(root, filename)
            
            try:
                decrypt_items(full_path, fernet_key)

            except Exception as e:
                print(f"Could not decrypt: {e}")
