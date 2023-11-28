from rsa import check_padding, encryption, pad
# from rsa import check_padding
import math
"""
Takes a ciphertext, public modulus and public exponent as input as input
PARAMS:
ciphertext: a list of integers of size 128 bytes
N: the public modulus of size 128 bytes
e: the public exponent
"""

pub_key = (3, 783948438612447530520500845779523629098681116915315373171090024704252529272105569277652766190092846991058906985549067848089611892705206703102883806613132978957364381750756122225194752372805842732963804787636530587121476113137183873)


def to_int(cipher_text):
    ct = 0
    for i in cipher_text:
        ct = 256*ct+i
    return ct

def to_list(ct):
    cipher_text = []
    while ct > 0:
        cipher_text.append(ct % 256)
        ct = ct//256
    return cipher_text[::-1]


def step2(M, s, B, N, ct, e):
    # Find s
    if len(M) == 1:
        for (a,b) in M:
            r = math.ceil(2*((b*s - 2*B)/N))
            while True:
                s1 = (2*B+r*N)//b
                found = 0
                while s1 < (3*B+r*N)/a:
                    if check_padding(to_list((ct*pow(s1, e, N)) % N)):
                        found = 1
                        break
                    s1 += 1
                if found:
                    break
                else:
                    r += 1
    else:
        print("M has multiple intervals ", len(M))
        s1=s+1
        while s1 < (3*B):
            if check_padding(to_list((ct*pow(s1, e, N)) % N)):
                break
            s1 += 1
    return s1


def step3(s, M, B, N):
    # Add to the set
    M1 = set()
    for element in M:
        a,b = element
        r = (a*s-3*B+1)//N
        # print(a,b)
        while r<=(b*s-2*B)//N:
            # print((3*B+r*N)//s)
            alpha = max(a, math.ceil((2*B+r*N)/s))
            beta = min(b, math.floor((3*B-1+r*N)/s))
            if alpha <= beta:
                M1.add((alpha, beta))
            r += 1
    return M1

def attack(cipher_text, N, e):
    """
    TODO: Implement your code here
    """
    
    k = N.bit_length()//8
    B = 2**(8*(k-2))
    ct = to_int(cipher_text)

    # First s
    s = N//(3*B)
    while s < 3*B:
        if check_padding(to_list((ct*pow(s, e, N)) % N)):
            break
        s += 1

    print("Got an s value", s)
    # 2B<sm-rn<3B
    # (2B+rn)/s<m<(3B+rn)/s
    a = 2*B
    b = 3*B
    r = 0
    M = set()
    while (3*B+r*N)//s < b:
        alpha = max(a, math.ceil((2*B+r*N)/s))
        beta = min(b, math.floor((3*B+r*N-1)/s))
        if alpha <= beta:
            M.add((alpha, beta))
        r += 1
    print(M)
    while True:
        s = step2(M, s, B, N, ct, e)
        print("Got another s value", s)
        M = step3(s, M, B, N)
        print(M)
        if len(M) == 1:
            for x in M:
                if x[0] == x[1]:
                    pm=to_list(x[0])
                    index=pm.index(0)
                    return pm[index+1:]
            
    """
    Return a list of integers representing the original message
    """
    # return []


if __name__ == "__main__":
    encrypted = encryption(pad([1,2,3,4,5,6,7]))
    # print(check_padding(encrypted))
    d=522632292408298353680333897186349086065787411276876915447393349802835019514737046185101844126728564660705937990366007589349628083368588089099766017405588723862803194332061788333764515745015105586168407686329659333562813224856512227
    m=pow(to_int(encrypted),d,pub_key[1])

    print(m)
    # print(to_list(m))
    print(attack(encrypted, pub_key[1], pub_key[0]))
