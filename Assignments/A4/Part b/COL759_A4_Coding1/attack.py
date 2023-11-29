from mrsa import dec, restart_system
import math


# from Crypto.Util import number

# def restart_system():
#     x=number.getPrime(10)
#     y=number.getPrime(10)
#     return (x*y,7), number.getPrime(24)

def gcd(x,y):
    if y>x:
        return gcd(y,x)
    while True:
        x,y=y, x%y
        if y==0: return x

def extended_euclid(a, b):
    if b==0:
        return (1,0)
    else:
        x,y=extended_euclid(b,a%b)
        return (y,x-(a//b)*y)

def inverse(e,N):
    d,_=extended_euclid(e,N)
    return d%N
    

def attack():
    """
    Function details:
    restart_system(): It will return ((N, e), ct) where (N, e) is the public key and ct is the ciphertext you have to decrypt
        - You can call it maximum of 200 times
    dec(ct, N, d): It will return message corresponding to the given ciphertext ct using N and d
    """
    
    L=[]
    for i in range(200):
        (N, e), ct = restart_system()
        
        for i in L:
            p=gcd(i,N)
            if p!=1 and p!=N and p!=N:
                q=N//p
                phiN=(p-1)*(q-1)
                d = inverse(e, phiN)
                return dec(ct, N, d)
        L.append(N)
    """
    return the message corresponding to the ciphertext you got from restart_sytem
    """
    
# print(attack())


