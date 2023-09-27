from Crypto.Cipher import AES
import sys
import ast

key = b'\xb8\x15\xd4\xeeUO\xdf\xa3\x02\xe9\x8d.\xb2\x10\xfa\x0c'

"""
DO NOT MODIFY THIS FUNCTION
"""
def check_padding(encd):
    encd = bytes(encd)
    iv = encd[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    decd = aes.decrypt(encd[16:])

    padding_bits = decd[0]
    # print(padding_bits)
    # print(list(decd[0:6]))
    if padding_bits > 16 or padding_bits < 1 or len(decd) < padding_bits:
        # print('Invalid Padding')
        return 2
    
    padding = decd[:padding_bits]
    if all([byte == padding_bits for byte in padding]):
        # print('Valid Padding')
        return 0
    else:
        # print('Invalid Padding')
        return 2


def main():
    if len(sys.argv) < 2:
        print(f'Insufficient Number of arguments. Please enter the ciphertext')
        sys.exit(1)
    elif len(sys.argv) > 2:
        print(f'Incorrect number of arguments passed')
        sys.exit(1)
    
    cipher_text = ast.literal_eval(sys.argv[1])
    retcode = check_padding(cipher_text)
    sys.exit(retcode)

if __name__ == '__main__':
    main()