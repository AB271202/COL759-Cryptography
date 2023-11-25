from Crypto.Util import number

def keygen():
    phi = 0
    N = 0
    p = 0
    q = 0
    e = 0
    while(phi % 3 == 0):
        p = number.getPrime(1024)
        q = number.getPrime(1024)
        N = p*q
        phi = (p-1)*(q-1)
        e = 3
    return (N,e)

def verify(sig, msg, N, e):
    padded = pow(sig, e, N)
    # padded_bin = "1" + "0"*2000+"00000000101010101010101010101010"
    padded_bin = bin(padded)[2:]
    if not padded_bin.endswith("00000000"+bin(msg)[2:]): # check right part == 0x00 msg
        return -1
    if len(padded_bin) != 2033: # check left part == 0x00 0x01
        return -2
    rpad_len = (len(bin(msg))+6)//8
    for i in range(0, 254-rpad_len): # check for 0x00 in between
        if padded_bin[1+i*8:9+i*8] == "00000000":
            return 1
    return 2
    