import random as rand
from Crypto.Cipher import AES
import binascii, os, sys

key = os.urandom(16)

iv = os.urandom(16)

aesCBC = AES.new(key, AES.MODE_CBC, iv)
aesECB = AES.new(key, AES.MODE_ECB)

# read file
in_file = open("plaintext.txt", "rb")
# get bytes from file
data = in_file.read()
in_file.close()
# check if total bytes are multiples of 16, add padding as needed
mod = len(data) % 16
if mod:
    data += bytes(16 - mod)

ecb = aesECB.encrypt(data)
cbc = aesCBC.encrypt(data)

print("ECB Encrypt => ",ecb.hex(),"\n")
print("CBC Encrypt => ",cbc.hex(),"\n")

aesCBC = AES.new(key, AES.MODE_CBC, iv)
aesECB = AES.new(key, AES.MODE_ECB)

ecb = aesECB.decrypt(ecb)
cbc = aesCBC.decrypt(cbc)

print("ECB Decrypt => \n" + ecb.decode("utf-8") + "\n")
print("CBC Decrypt => \n" + cbc.decode("utf-8") + "\n")