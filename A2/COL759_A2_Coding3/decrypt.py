from Crypto.Cipher import AES

key = b'\xb8\x15\xd4\xeeUO\xdf\xa3\x02\xe9\x8d.\xb2\x10\xfa\x0c'

class decryption_oracle:
    count = 0

    def decrypt(self, ct):
        if(self.count == 0):
            self.count += 1
            try:
                iv = key
                ct = bytes(ct)
                aes = AES.new(key, AES.MODE_CBC, iv=iv)
                pt = aes.decrypt(ct)
                return pt
            except (ValueError, KeyError):
                return None
        return None