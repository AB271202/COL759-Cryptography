from encrypt import encrypt
import queue

"""
You can implement helper function here if you want
"""
def FEL(plaintext):
    return len(encrypt(plaintext))

# def recattack(secret,lim,amt):

#     if lim==0:
#         return amt,secret
#     minm=FEL(secret+chr(97))
#     index=0
#     arr=[]
#     for i in range(26):
#         l=FEL(secret+chr(97+i))
#         # print(l)
#         if l<minm:
#             minm=l
#             index=i

#     for i in range(26):
#         l=FEL(secret+chr(97+i))
#         if l==minm:
#             arr.append(recattack(secret+chr(97+i),lim-1, minm))
#     return min(arr)
#     # secret+=chr(97+index)    

def getmin(secret,arr):
    '''
    Returns the minimum secret with one character more, 
    index of the last such character, 
    and modifies the array to contain all the min secrets
    '''
    minm=FEL(secret+chr(97))
    for i in range(26):
        l=FEL(secret+chr(97+i))
        # print(l)
        if l<=minm:
            minm=l
            index=i
    for i in range(26):
            l=FEL(secret+chr(97+i))
            if l==minm:
                arr.append(secret+chr(97+i))
    return minm,index

def attack():
    """
    TODO: Implement your code here, You can use encrypt or decrypt or both function for your attack
    """
    secret=""
    some=0
    while some<24:
        
        arr=[] # Need to so something when multiple strings give the same length!
        minm,index=getmin(secret,arr)
        if len(arr)<=1:            
            secret+=chr(97+index)
            some+=1
        else:
            newarr=[]
            for i in range(len(arr)):
                # print(arr)
                arr2=[]
                # x=arr.pop()
                minm,index = getmin(arr[i],arr2)
                if newarr==[] or minm<newarr[-1][0]:
                    newarr=[(minm, arr2)]
                elif minm==newarr[-1][0]:
                    newarr.append((minm, arr2))
            arr=[]
            for i in range(len(newarr)):
                arr.extend(newarr[i][1])
            secret=arr[0] #NOTE HERE
            some+=2
        # print(some, arr)
        
    """
    Return the secret
    """
    # amt,secret=recattack("",24,FEL(secret+chr(97)))
    return secret

if __name__=="__main__":
    print(attack())
    print(FEL("zzzzzzzzzzzzzzzzzzzzzzzzaa"))
    print(FEL("zzzzzzzzzzzzzzzzzzzzzzzzzz"))
    