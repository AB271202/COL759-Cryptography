from Crypto.Cipher import AES
import random

key = b'\xb8\x15\xd4\xeeUO\xdf\xa3\x02\xe9\x8d.\xb2\x10\xfa\x0c'

def pad(data):
    remaining = 16-len(data)%16
    padding = bytes([remaining] * remaining)
    data = padding + data

    return data

"""
DO NOT MODIFY THIS FUNCTION
"""
def encrypt(message):
    data = bytes(message) 
    data = pad(data)

    iv = [random.randint(0, 255) for i in range(16)]
    iv = bytes(iv)

    aes = AES.new(key, AES.MODE_CBC, iv)
    
    encd = aes.encrypt(data)

    return list(iv + encd)

def main():
    data = 'This is a message for COL759 A4-Q4'
    message = list(bytes(data, 'raw_unicode_escape'))
    
    encd = encrypt(message)
    return encd

if __name__ == '__main__':
    ret = main()
    print(ret)