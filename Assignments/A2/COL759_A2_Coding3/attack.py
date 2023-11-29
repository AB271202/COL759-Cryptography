"""
You can implement helper function here if you want
"""
import decrypt


def attack(ciphertext, decrypt):
    """
    You are given a ciphertext(byte array) of size 48 on some random message of size 48 bytes. 
    You are also given access to the decryption function which takes a ciphertext of size 48 and outputs 48 bytes message corresponding to the ciphertext
    Example Use: decrypt(ciphertext)

    NOTE: 
        1. Ensure that ciphertext send as input to decrypt function is byte array of size 48
        2. Only one query can be made to decrypt function

    TODO: Implement your code below
    """
    ct0=ciphertext[:16]
    decrypted=decrypt(ct0*3)
    print(decrypted)
    m0=decrypted[:16]
    m1=decrypted[16:32]
    result_byte = bytes([m0[i] ^ m1[i] ^ ct0[i] for i in range(16)])
    return result_byte
    """
    Return the key in byte format
    Example of key: b'\xb8\x15\xd4\xeeUO\xdf\xa3\x02\xe9\x8d.\xb2\x10\xfa\x0c'
    """
