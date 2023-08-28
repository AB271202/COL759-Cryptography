from des import encrypt, decrypt, key_gen

"""
You can implement helper function here if you want
"""

def attack(message, ciphertext):
    """
    TODO: Implement your code here, You can use encrypt, decrypt and key_gen functions for your attack
    """
    CT1=[]
    CT2=[]
    k1=k2=0
    d=dict()
    for i in range(1,1<<20+1):
        d[encrypt(key_gen(i),message)]=i
        CT2.append(decrypt(key_gen(i),ciphertext))
    
    for i in range(len(CT2)):
        try:
            k1=key_gen(d[CT2[i]])
            k2=key_gen(i+1)
        except:
            continue
    
    
    """
    Return the keys (k1, k2) such that ct = Enc(Enc(m, k1), k2) [ordering of keys matter]
    """
    return (k1,k2)

if __name__=="__main__":
    message=bytes("a"*64,'utf-8')
    k1=key_gen(1)
    k2=key_gen(2)
    ciphertext= encrypt(k2, encrypt(k1,message))
    print(f"k1={k1}, k2={k2}")
    print("The algorithm returned: ")
    s=attack(message, ciphertext)
    print(s)
    print((k1,k2)==s)
    