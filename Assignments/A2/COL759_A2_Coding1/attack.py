"""
You can implement helper function here if you want
"""
# import perm
def attack(oracle, pi_func, p):
    """
    The challenger has sampled a bit b <- {0, 1} uniformly randomly:
        If b = 0, the challenger has chosen the PRP
        If b = 1, the challenger has chosen a uniformly random permutation

    Your goal is to predict the bit b that the challenger has sampled given access to p, the public permutation pi(x) used in PRP construction and oracle function

    The oracle function is simulating interacting with a challenger which has previously sampled a random bit b and two uniformly random keys k1 and k2 over the key space
        oracle(x) - returns the output on x where x is from 0 to p-1

    NOTE: 
        1. Ensure that x is from 0 to p-1
        2. A maximum of 5 queries can be made to oracle function
        3. You can make as many query as you want to the pi_func function
        4. For at most 3 queries to oracle, full score will be awarded
        5. For making 4 queries to oracle, 90% of the score will be awarded
        6. For making 5 queries to oracle, 85% of the score will be awarded

    TODO: Implement your code below
    """
    y0=oracle(0)
    y1=oracle(1)
    y2=oracle(2)
    k1=((2*((y1-y2)%p))*pi_func((y0+y2-2*y1)%p))%p
    k2=(y1-k1*(y0-y1))%p
    y0new=(pi_func(k1)+k2)%p
    y1new=(pi_func((k1+1)%p)+k2)%p
    y2new=(pi_func((k1+2)%p)+k2)%p
    if y0==y0new and y1==y1new and y2==y2new:
        return 0
    else:
        return 1
    

if __name__=="__main__":
    p=perm.prp_oracle()
    # print(p.k1,p.k2)
    print(attack(p.oracle,p.pi_func,p.p))