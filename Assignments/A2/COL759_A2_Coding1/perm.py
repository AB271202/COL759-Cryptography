from Crypto.Util import number
import random

class prp_oracle:
    b = 0
    p = number.getPrime(120)
    k1 = random.randint(0, p-1)
    k2 = random.randint(0, p-1)
    dict_xy = {}
    count = 0

    def pi_func(self, x):
        if(x==0):
            return 0
        return pow(x, -1, self.p) # Modular multiplicative inverse with mod p (x^-1 mod p)
    
    def prp(self, x):
        return (self.pi_func((self.k1+x)%self.p)+self.k2)%self.p 
    
    def oracle(self, x):
        if(self.count == 5):
            return None
        self.count+=1
        if(self.b==0):
            return self.prp(x)
        else:
            if x in self.dict_xy:
                return self.dict_xy[x]
            y = random.randint(0, self.p-1)
            while(y in self.dict_xy.values()):
                y = random.randint(0, self.p-1)
            self.dict_xy[x] = y
            return y