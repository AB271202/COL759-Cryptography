from decrypt import check_padding
from encrypt import encrypt

"""
You can implement helper function here if you want
"""


def attack(cipher_text):
    """
    Takes a ciphertext (list of integers from 0 to 255 [byte array]) as input
    TODO: Implement your code below
    """
    NUM = 256
    print(cipher_text)
    iv = cipher_text[:16]
    first = cipher_text[16:32]
    
    # Find padding
    padding = 0
    for i in range(15, -1, -1):
        iv[i] = (iv[i] + 1) % NUM
        if check_padding(iv+first) == 2:
            padding = i+1
            iv[i] = (iv[i] - 1) % NUM
            break
        iv[i] = (iv[i] - 1) % NUM
    print("Padding: ",padding)

    message = []
    for i in range(padding, 16):
        for j in range(i):
            iv[j] = (iv[j]^(i)^(i+1))

        for k in range(256):
            iv[i]=iv[i]^((i+1)^k)
            if check_padding(iv+first)==0:
                message.append(k)
                break
            iv[i]=iv[i]^((i+1)^k)
            
    """
    Return a list of integers representing the original message
    """
    return message


if __name__ == "__main__":
    string = "Hello World"
    initial = (list((bytes(string, 'raw_unicode_escape'))))
    print(initial)
    print(len(initial))
    final=attack(encrypt(initial))
    print(final)
    print(initial==final)
