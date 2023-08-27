"""
DO NOT MODIFY THIS FILE
"""

from Crypto.Cipher import DES

def key_gen(index):
    """Gets the nth key with respect to parity bits"""
    keystring = []
    for i in range(8):
        key_byte = index & 127  # 127 == int('1111111', 2)
        hamming_weight = bin(key_byte).count('1')
        if hamming_weight % 2 == 0:
            keystring.append(((key_byte << 1) + 1))
        else:
            keystring.append((key_byte << 1))
        index >>= 7
    return bytes(keystring[::-1])  # reverse order

def encrypt(key, message):
    """Encrypt using single-round-DES"""
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(message)


def decrypt(key, ct):
    """Decrypt using single-round DES"""
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(ct)
