"""
DO NOT MODIFY THIS FILE
"""

import zlib
from Crypto.Cipher import AES
import random

key = b'\xb8\x15\xd4\xeeUO\xdf\xa3\x02\xe9\x8d.\xb2\x10\xfa\x0c'
secret = "abcpqrxyzvcxsdwproidmuwm"
# secret = "zzzzzzzzzzzzzzzzzzzzzzzz"
# secret = "zzzzzzzzzzzzzzzzaaaaaaaa"

def compress_func(inp):
    return zlib.compress(inp.encode())

def encrypt(message):
    pt = ":::"+secret+":::"+message
    compa = compress_func(pt)
    iv = [random.randint(0, 255) for i in range(16)]
    iv = bytes(iv)
    aes = AES.new(key, AES.MODE_CFB, iv=iv)
    encd = aes.encrypt(compa)
    return list(iv + encd)