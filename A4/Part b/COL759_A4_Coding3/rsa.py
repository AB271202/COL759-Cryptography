from Crypto.Random import random
import os
import pickle

def invmod(a, n):
    t = 0
    newt = 1
    r = n
    newr = a
    while newr != 0:
        q = r // newr
        (t, newt) = (newt, t - q * newt)
        (r, newr) = (newr, r - q * newr)
    if r > 1:
        raise Exception('unexpected')
    if t < 0:
        t += n
    return t

smallPrimes = [2, 3, 5, 7, 11, 13, 17, 19]

def has_small_prime_factor(p):
    for x in smallPrimes:
        if p % x == 0:
            return True
    return False

def is_probable_prime(p, n):
    for i in range(n):
        a = random.randint(1, p)
        if pow(a, p - 1, p) != 1:
            return False
    return True

def get_probable_prime(bitcount):
    while True:
        p = random.randint(2**(bitcount - 1), 2**bitcount - 1)
        if not has_small_prime_factor(p) and is_probable_prime(p, 5):
            return p

def gen_key(keysize):
    e = 3
    bitcount = (keysize + 1) // 2 # + 1

    p = 7
    while (p - 1) % e == 0:
        p = get_probable_prime(bitcount)

    q = p
    while q == p or (q - 1) % e == 0:
        q = get_probable_prime(bitcount)

    n = p * q
    et = (p - 1) * (q - 1)
    d = invmod(e, et)
    pub = (e, n)
    priv = (d, n)
    return (pub, priv)

def encrypt_num(pub, m):
    (e, n) = pub
    if m < 0 or m >= n:
        raise ValueError(str(m) + ' out of range')
    return pow(m, e, n)

def decrypt_num(priv, c):
    (d, n) = priv
    if c < 0 or c >= n:
        raise ValueError(str(c) + ' out of range')
    return pow(c, d, n)

# Drops leading zero bytes.
def bytes_to_num(s):
    return int.from_bytes(s, byteorder='big')

def num_to_bytes(k):
    return k.to_bytes(MODULUS_SIZE, byteorder='big')

def encrypt_bytes(pub, mbytes):
    m = bytes_to_num(mbytes)
    c = encrypt_num(pub, m)
    cbytes = num_to_bytes(c)
    return cbytes

def decrypt_bytes(priv, cbytes):
    c = bytes_to_num(cbytes)
    m = decrypt_num(priv, c)
    mstr = num_to_bytes(m)
    return mstr


MODULUS_SIZE = 96 # bytes
KEY_FILE = 'key.pkl'

# Read key from the file if it exists, else generate a new one
def get_key(key_file):
    if os.path.isfile(key_file):
        with open(key_file, 'rb') as f:
            key_pair = pickle.load(f)
            return key_pair
    else:
        key_pair = gen_key(MODULUS_SIZE * 8)
        with open(key_file, 'wb') as f:
            pickle.dump(key_pair, f)
        return key_pair

pub_key, priv_key = get_key(KEY_FILE)

"""
PARAMS:
msg: a list of integers representing the message to be encrypted
Returns a list of integers representing the padded message
"""
def pad(msg):
    assert len(msg) <= MODULUS_SIZE - 11 
    remaining = MODULUS_SIZE - 3 - len(msg)
    padding = []
    for i in range(remaining):
        n = random.randint(1, 255)
        padding.append(n)
    data = [0, 2] + padding + [0] + msg
    return data

"""
Takes a message as input, and returns the encrypted ciphertext
PARAMS:
msg: a list of integers representing the message to be encrypted
"""
def encryption(msg):
    msg = bytes(msg)
    enc = encrypt_bytes(pub_key, msg)
    return list(enc)

"""
Takes a ciphertext as input, decrypts it and tells whether it had a valid padding
PARAMS:
encrypted: a list of integers representing the ciphertext
Returns true if it was a valid padding, false otherwise
"""    
def check_padding(encrypted):
    encrypted = bytes(encrypted)
    dec = decrypt_bytes(priv_key, encrypted)
    return dec[0:2] == b'\x00\x02'

def main():
    msg = 'A message for encryption'
    msg = list(bytes(msg, 'raw_unicode_escape'))
    msg = pad(msg)

    encrypted = encryption(msg)
    print(check_padding(encrypted))

if __name__ == '__main__':
    main()