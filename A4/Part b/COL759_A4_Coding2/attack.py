
"""
You can define helper function here if you want
"""
# from Crypto.Util import number
import secrets

# def keygen():
#     phi = 0
#     N = 0
#     p = 0
#     q = 0
#     e = 0
#     while(phi % 3 == 0):
#         p = number.getPrime(1024)
#         q = number.getPrime(1024)
#         N = p*q
#         phi = (p-1)*(q-1)
#         e = 3
#     return (N,e)

# def verify(sig, msg, N, e):
#     padded = pow(sig, e, N)
#     # padded_bin = "1" + "0"*2000+"00000000101010101010101010101010"
#     padded_bin = bin(padded)[2:]
#     if not padded_bin.endswith("00000000"+bin(msg)[2:]): # check right part == 0x00 msg
#         return -1
#     if len(padded_bin) != 2033: # check left part == 0x00 0x01
#         return -2
#     rpad_len = (len(bin(msg))+6)//8
#     for i in range(0, 254-rpad_len): # check for 0x00 in between
#         if padded_bin[1+i*8:9+i*8] == "00000000":
#             return 1
#     return 2

# ----------------------------------------------------------------------------------------

# write a funcion to convert a binary string to an integer
def bin_to_int(s):
    power = 1
    result = 0
    for i in range(len(s)-1, -1, -1):
        result += int(s[i]) * power
        power *= 2
    return result

def adj_len(s, N = 2048):
    n = len(s)
    padding = '0'*(N - n)
    return (padding + s)

def flip_bit(s, i):
    sprime = ''
    for j in range(len(s)):
        if (j == i): 
            sprime += '1' if(s[i] == '0') else '0'
        else : 
            sprime += s[j]

    return sprime

def attack(N, e, msg):
    """
    write the code below
    """
    s_bin = '0' * 2048
    msg_bin = bin(msg)[2:]
    msg_byte_size = len(msg_bin) // 8
    target_suffix = '00000000' + adj_len(msg_bin, 8*msg_byte_size)
    prefix = '00000000' + '00000001'

    # iterate s_bin from last char to the first char
    i = len(s_bin) - 1
    j = len(target_suffix) - 1

    while j > -1:
        c = (bin(pow(bin_to_int(s_bin), e, N)))[2:]
        c = adj_len(c)
        c_bit = c[i]
        t = target_suffix[j]
        if(c_bit == t):
            i -= 1
            j -= 1
            continue

        s_bin = flip_bit(s_bin, i)
        i -= 1
        j -= 1

    randomMax = 670
    remaining_Bits = randomMax - len(target_suffix)

    while True:
        randomBits = bin(secrets.randbits(remaining_Bits))[2:].zfill(remaining_Bits)
        s_bin = randomBits + s_bin[-len(target_suffix):]
        s_bin = adj_len(s_bin)
        if(s_bin[1370] != '1') : s_bin = flip_bit(s_bin, 1370)
        if(s_bin[1371] != '1') : s_bin = flip_bit(s_bin, 1371)

        rpad_len = (len(bin(msg))+6)//8
        padded_bin = bin(pow(bin_to_int(s_bin), e, N))[2:]
        found_zero = False
        for i in range(0, 254-rpad_len): # check for 0x00 in between
            if padded_bin[1+i*8:9+i*8] == "00000000":
                found_zero = True
        if(not found_zero):
            break

    """
    return a signature (integer) corresponding to the given message that will get get verified
    """
    print(adj_len(bin(pow(bin_to_int(s_bin), 3, N))[2:]))
    return bin_to_int(s_bin)


# N, e = keygen()
# mten = 611574238157988876616065
# mone = 129
# att = attack(N,3,mten)
# print("VERIF OUTPUT", verify(att, mten, N, e))

# tgt = 0000000010000001100000011000000110000001100000011000000110000001100000011000000110000001