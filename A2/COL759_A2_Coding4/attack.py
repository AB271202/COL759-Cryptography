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
    padding = 0
    for i in range(15, -1, -1):
        iv[i] = (iv[i] + 1) % NUM
        if check_padding(iv+first) == 2:
            padding = i+1
            iv[i] = (iv[i] - 1) % NUM
            break
        iv[i] = (iv[i] - 1) % NUM
    print("Padding: ",padding)
    print(iv)
    print(first)
    message = []
    for i in range(padding, padding+1):
        for j in range(i):
            iv[j] = (iv[j]^(padding+i)^(padding+i+1))
        # print(iv)
        # check_padding(iv+first)
        for k in range(256):
            iv[i]=(iv[i]^((padding+i+1)^k))
            if check_padding(iv+first)==0:
                print(i)
                message.append(i)
                break
            iv[i]=(iv[i]^((padding+i+1)^k))
    """
    Return a list of integers representing the original message
    """
    return message


if __name__ == "__main__":
    string = "Hello World"
    print(list((bytes(string, 'raw_unicode_escape'))))
    print(len(list((bytes(string, 'raw_unicode_escape')))))
    print(attack(encrypt(list(bytes(string, 'raw_unicode_escape')))))
