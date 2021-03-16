# Encryption-and-decryption-using-AES256-CBC
A GUI application to encrypt and decrypt files and folders using the pyAesCrypt module in Python 3.0.

A GUI application to encrypt and decrypt files and folders using the pyAesCrypt module in Python 3.0. It uses the AES256-CBC to encrypt the files into the .aes extension. These same files can also be decrypted to the original file extension.

AES-256, which has a key length of 256 bits, supports the largest bit size and is practically unbreakable by brute force based on current computing power, making it the strongest encryption standard.

The encryption and decryption require a password. This password will be used for verification during decryption and if the password is incorrect then the decryption will be unsuccessful. 

Before running the application there are some prerequisite modules that need to be installed.

**PREREQUISITES:**

1. **PySimpleGUI module** (using pip install)

This module will be used to design the GUI of the application.

2. **pyAesCrypt module** (using pip install)

This module will be used to encrypt the files into the .aes extension.

**pip command: pip install pyAesCrypt**

**Other pre-installed Python 3.0 modules used are sys, io, os and webbrowser.**

**Working of the application:**

This GUI application has three major sections (windows):

1. Encrypt a text you type on the textbox and save it in an encrypted file. Decrypt that same file into a text file.

2. Encrypt a file and save it in your prefered directory. Decrypt the same files and decide whether to keep the original files or not.

3. Select a folder and encrypt the files in that folder (exclusive of sub-directory). Decrypt these files and decide whether to keep the original files or not. 

**Decrypt the whole folder only if the password for all the files are the same or else the decryption will throw an error.**

In the case of file and folder encryption, the user can delete the original files and keep only the encrypted files.

The user also has the ability to keep or delete the .aes files after decryption.

**Run the start.py file to start the application from the home window.**

**Each file can also be run separately.**
