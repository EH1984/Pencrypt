#!/usr/bin/env python
import tarfile
import sys
import gnupg
import getpass
import os


class PyEncrypt:

    def __init__(self, file):
        self.file = file.rstrip('/')
        self.gpg = gnupg.GPG(gnupghome="GNUPG DIRECTORY")
        self.choice = input("(e)ncrypt or (d)ecrypt or (c)ancel?")

    def pencrypt(self):
        try:
            # TAR
            tar = tarfile.open(self.file+".tar.gz", "w:gz")
            tar.add(self.file)
            tar.close()

            # ENCRYPT
            with open(self.file+".tar.gz", 'rb') as f:
                status = self.gpg.encrypt_file(
                    f, recipients="YOUR EMAIL", output=self.file+'.tar.gz.gpg')

                print('ok: ', status.ok)
                print('status: ', status.status)
                print('stderr: ', status.stderr)

            # CLEANUP
            print("Removing other files")
            os.system("rm -rf " + self.file)
            os.system("rm -rf " + self.file + ".tar.gz")
        except:
            print("Something went wrong!!!")

    def pdecrypt(self):
        try:
            # GETPASS
            passw = getpass.getpass("Enter your password!!!")
            # DECRYPTING
            with open(self.file, 'rb') as f:
                status = self.gpg.decrypt_file(
                    f, passphrase=passw, output=self.file.rstrip('.gpg'))

            print('ok: ', status.ok)
            print('status: ', status.status)
            print('stderr: ', status.stderr)
            # UNTAR
            tar = tarfile.open(self.file.rstrip(".gpg"))
            tar.extractall()
            tar.close()
            # REMOVE FILES
            print("Removing files")
            os.system("rm -rf " + self.file)
            os.system("rm -rf " + self.file.rstrip('.gpg'))
        except:
            print(
                "Either this was not a gpg file, password was incorrect or something else")
            print("Work in progress!!!")


# Start of program logic
# Recieve a file from the user to encrypt/decrypt
try:
    file1 = sys.argv[1]
except:
    print("You must give a file to encrypt/decrypt!!!")
    exit(0)

# Create an instance of the encrypt class
e = PyEncrypt(file1)

# Get a choice from the user to either encrypt or decrypt
if e.choice == "e":
    e.pencrypt()
elif e.choice == "d":
    e.pdecrypt()
elif e.choice == "c":
    print("Exiting..... Goodbye!!!")
    exit(0)
else:
    print("Pick e for encrypt or d for decrypt")
    print("This only works on folders at the moment")
    exit(0)
