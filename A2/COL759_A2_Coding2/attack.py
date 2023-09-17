"""
write helper functions below if required
"""

def predict(permute, inverse_permute):
    """
    The challenger has sampled a bit b <- {0, 1} uniformly randomly:
        If b = 0, the challenger has chosen the Luby Rackoff Permutation
        If b = 1, the challenger has chosen a uniformly random permutation
    The permutation is over the space of strings of length 32 bytes, with key space over 3*128 bit keys

    Your goal is to predict the bit b that the challenger has sampled

    The given functions are simulating interacting with a challenger which has previously sampled a random bit b and a uniformly random key over the key space
        1. permute(x) - returns the permutation of x where x is of type bytes and len(x) = 32
        2. inverse_permute(x) - returns the inverse permutation of x where x is of type bytes and len(x) = 32

    NOTE: 
        1. Ensure that x is of type bytes and len(x) = 32 for both permute and inverse_permute
        2. A maximum of 8 queries can be made in total (combining both permute and inverse_permute)
        3. For at most 4 queries, full score will be awarded
        4. For at most 6 queries, 90% of the score will be awarded
        5. For at most 8 queries, 80% of the score will be awarded
        6. For more than 8 queries, 0% of the score will be awarded

    TODO: write your code below
    """

    """
    Return guess of b (either 0 or 1)
    """
    return None

