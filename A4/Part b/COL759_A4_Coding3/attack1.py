# from rsa import check_padding
import rsa

"""
Takes a ciphertext, public modulus and public exponent as input as input
PARAMS:
ciphertext: a list of integers of size 128 bytes
N: the public modulus of size 128 bytes
e: the public exponent
"""
def to_int(cipher_text):
    ct = 0
    for i in cipher_text:
        ct = 256*ct+i
    return ct

def bin_to_int(s):
    power = 1
    result = 0
    for i in range(len(s)-1, -1, -1):
        result += int(s[i]) * power
        power *= 2
    return result

def floor(a, b):
    return a//b 

def ceil(a, b):
    return  a // b + (a % b > 0)


def attack(cipher_text, N, e):
    """
    TODO: Implement your code here
    """
    ct_bin = ''.join(format(byte, '08b') for byte in cipher_text)
    k = len(cipher_text)    # number of bytes in the cipher text
    B = pow(2, 8*(k-2))     # bound
    M = [(2*B, 3*B-1)]
    i = 1         # number of successful values found
    s = ceil(N, (3 * B))

    while True:
        #  DEBUG :
        min_n = M[0][0]
        max_n = M[0][1]
        for r in M: # min_n, max_n based on previous step
            if r[0] < min_n:
                min_n = r[0]
            if r[1] > max_n:
                max_n = r[1]
        print("WAY TO GO:", max_n - min_n)

        if (i > 1 and len(M) == 1):
            a, b = M[0]
            r = floor(2*(b*s - 2*B), N)
            print("Searching CASE I starting:", s)
            counter = 1
            while True:
                s = ceil((2*B + r * N), b)
                s_max = ceil((3*B + r * N), a)
                found = False
                while s <= s_max:
                    ct_mod = (pow(pow(s, e) * (bin_to_int(ct_bin)), 1, N))
                    if (rsa.check_padding(rsa.num_to_bytes(ct_mod))) : 
                        found = True
                        break
                    s += 1
                if found:
                    break
                else:
                    if counter%1000 == 0: print(counter)
                    counter += 1
                r += 1
        else:
            print("Searching CASE II starting:", s)
            while True:
                s += 1
                ct_mod = (pow(pow(s, e) * (bin_to_int(ct_bin)), 1, N))
                if (rsa.check_padding(rsa.num_to_bytes(ct_mod))) :
                    break
        
        # update the set M
        M_new = []

        for m in M:
            a, b = m
            r_min = (a*s - 3*B + 1) // N
            r_max = (b*s - 2*B) // N

            r = r_min
            while r <= r_max:
                a_new = max(a, ceil((2*B + r*N), s))
                b_new = min(b, floor((3*B - 1 + r*N), s))
                if a_new > b or b_new < a:
                    r += 1
                    continue

                if a_new == b_new:
                    ans = list(rsa.num_to_bytes(a_new))[1:]
                    id = ans.index(0)
                    return ans[id+1:]
                    # return list(rsa.num_to_bytes(a_new))

                M_new.append((a_new, b_new))
                r += 1
        
        M = M_new

        print("------------------ FOUND AN S:", s, "Numbered:", i, "-------------------------")
        i += 1

# if __name__=="__main__":
#     pub_key, priv_key = rsa.get_key('key.pkl')
#     e, N = pub_key
#     d = priv_key[0]
#     msg = 'A message for encryption'
#     msg1 = list(bytes(msg, 'raw_unicode_escape'))
#     msg1 = rsa.pad(msg1)
#     ct = rsa.encryption(msg1)
#     crack = attack(ct, N, e)
#     if(crack == msg) : 
#         print("HO GAYA")
#     else : 
#         print("NHI HUA")


if __name__ == "__main__":
    pub_key, priv_key = rsa.get_key('key.pkl')
    message = [255]*80
    message = [1,2,3,4,5,6,7,8,9,0,0,123,45,213,23,111,32]
    encrypted = rsa.encryption(rsa.pad(message))
    # print(check_padding(encrypted))
    d=522632292408298353680333897186349086065787411276876915447393349802835019514737046185101844126728564660705937990366007589349628083368588089099766017405588723862803194332061788333764515745015105586168407686329659333562813224856512227
    m=pow(to_int(encrypted),d,pub_key[1])

    # print(m)
    # print(to_list(m))
    result = attack(encrypted, pub_key[1], pub_key[0])
    print(result)
    print(message == result)
