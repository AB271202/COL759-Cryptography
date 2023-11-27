from rsa import check_padding, encryption
import math
"""
Takes a ciphertext, public modulus and public exponent as input as input
PARAMS:
ciphertext: a list of integers of size 128 bytes
N: the public modulus of size 128 bytes
e: the public exponent
"""

pub_key = (3, 783948438612447530520500845779523629098681116915315373171090024704252529272105569277652766190092846991058906985549067848089611892705206703102883806613132978957364381750756122225194752372805842732963804787636530587121476113137183873)


def step2(M, s, B, N, ct):
    # Find s
    if len(M) == 1:
        el = M.pop()
        a = el[0]
        b = el[1]
        r = 2*(b*s - 2*B)//N
        while True:
            s1 = (2*B-r*N)//b
            while s1 < (3*B-r*N)//a:
                if check_padding(to_list((ct*pow(s1, e, N)) % N)):
                    break
                s1 += 1
            r += 1
    return s1


def step3(s1, M, B, N):
    # Add to the set
    M1 = set()
    for element in M:
        r = 0
        a=element[0]
        b=element[1]
        while (3*B+r*N)/s1 < b:
            alpha = max(a, math.ceil((2*B+r*N)/s1))
            beta = min(b, math.floor((3*B+r*N)/s1))
            if alpha <= beta:
                M1.add((alpha, beta))
            r += 1
    return M1


def to_int(cipher_text):
    ct = 1
    for i in cipher_text:
        ct = 16*ct+i
    return ct


def to_list(ct):
    cipher_text = []
    while ct > 0:
        cipher_text.append(ct % 256)
        ct = ct//256
    return cipher_text[::-1]


def attack(cipher_text, N, e):
    """
    TODO: Implement your code here
    """
    k = N.bit_length()//8
    B = 2**(8*(k-2))
    s = N//(3*B)
    ct = to_int(cipher_text)
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
        beta = min(b, math.floor((3*B+r*N)/s))
        if alpha <= beta:
            M.add((alpha, beta))
        r += 1
    print(M)
    while True:
        s=step2(M,s,B,N,ct)
        print(s)
        M=step3(s, M, B, N)
        if len(M)==1:
            x=M.pop()
            if x[0]==x[1]:
                return to_list(M)
            else:
                M.add(x)
    """
    Return a list of integers representing the original message
    """
    # return []


if __name__ == "__main__":
    print(attack(encryption([1, 2, 3, 4, 5, 6, 7]), pub_key[1], pub_key[0]))
