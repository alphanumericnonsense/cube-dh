#
# d even
# 8 | kappa for convenience, coefficients mod 2**kappa
#

from Crypto.Hash import SHAKE256
from Crypto.Hash import SHA3_256
import os
import sys
import numpy as np
from itertools import product
import time

def gen_T(seed, d, n, kappa):
    """
    Random tensor T from seed using SHAKE
    """
    kappa_mask = 2**kappa - 1
    shake = SHAKE256.new()
    shake.update(seed)
    shape = tuple(n for i in range(d))
    T = np.zeros(shape=shape, dtype=int)
    for ind in product(range(n), repeat=d):
        T[ind] = int.from_bytes(shake.read((kappa+7)//8), "big") & kappa_mask
    return T

def gen_AorB(seed, d, n, kappa):
    """
    Random d/2-tuple of matrices from seed using SHAKE
    """
    kappa_mask = 2**kappa - 1
    shake = SHAKE256.new()
    shake.update(seed)
    shape = (d//2, n, n)
    AorB = np.zeros(shape=shape, dtype=int)
    for dim in range(d//2):
        for i in range(n):
            for j in range(n):
                AorB[dim, i, j] = int.from_bytes(shake.read((kappa+7)//8), "big") & kappa_mask
    return AorB

def act_A(T, A, d, n, kappa):
    """
    Return action of d/2-tuple of matrices A on first d/2 dims of T
    """
    kappa_mask = 2**kappa - 1
    shape = tuple(n for i in range(d))
    TA = np.zeros(shape=shape, dtype=int)

    for dim in range(d//2): # over Alice's dims
        mat = A[dim,:,:]
        for ind in product(range(n), repeat=d): # over all entries of T
            bv = ind[dim] # standard basis index, e_bv
            col = mat[:,bv] # this column of mat replaces e_bv
            for k in range(n):
                tmp_ind = list(ind)
                tmp_ind[dim] = k
                tmp_ind = tuple(tmp_ind)
                TA[tmp_ind] += (col[k] * T[ind]) & kappa_mask
                TA[tmp_ind] = TA[tmp_ind] & kappa_mask
    return TA

def act_B(T, B, d, n, kappa):
    """
    Return action of d/2-tuple of matrices B on last d/2 dims of T
    """
    kappa_mask = 2**kappa - 1
    shape = tuple(n for i in range(d))
    TB = np.zeros(shape=shape, dtype=int)

    for dim in range(d//2):
        mat = B[dim,:,:]
        for ind in product(range(n), repeat=d): # over all entries of T
            bv = ind[dim + d//2] # standard basis index, e_bv
            col = mat[:,bv] # this column of mat replaces e_bv
            for k in range(n):
                tmp_ind = list(ind)
                tmp_ind[dim + d//2] = k
                tmp_ind = tuple(tmp_ind)
                TB[tmp_ind] += (col[k] * T[ind]) & kappa_mask
                TB[tmp_ind] = TB[tmp_ind] & kappa_mask
    return TB

def random_exchange(d, n, kappa):
    seed_T = os.urandom(32)
    seed_A = os.urandom(16)
    seed_B = os.urandom(16)

    T = gen_T(seed_T, d, n, kappa)
    A = gen_AorB(seed_A, d, n, kappa)
    B = gen_AorB(seed_B, d, n, kappa)

    print("T (public):\n", T)
    print('\n')
    print("A (secret):\n", A)
    print('\n')
    print("B (secret):\n", B)
    print('\n')

    sha3 = SHA3_256.new()
    T_B = act_B(T, B, d, n, kappa)
    T_AB = act_A(T_B, A, d, n, kappa)
    T_AB_bytes = b""
    for ind in product(range(n), repeat=d):
        T_AB_bytes += int(T_AB[ind]).to_bytes(kappa//8, 'big')
    sha3.update(T_AB_bytes)
    keyAB = sha3.digest()

    sha3 = SHA3_256.new()
    T_A = act_A(T, A, d, n, kappa)
    T_BA = act_B(T_A, B, d, n, kappa)
    T_BA_bytes = b""
    for ind in product(range(n), repeat=d):
        T_BA_bytes += int(T_BA[ind]).to_bytes(kappa//8, 'big')
    sha3.update(T_BA_bytes)
    keyBA = sha3.digest()

    print("T_A (public):\n", T_A)
    print('\n')
    print("T_B (public):\n", T_B)
    print('\n')
    print("T_AB = T_BA (secret):\n", T_AB)
    print('\n')

    if keyAB == keyBA:
        key = keyAB
        success = True
    else:
        key = None
        success = False
    return (key, seed_T, seed_A, seed_B, success)

if __name__ == "__main__":
    # parameter set 2
    kappa = 16
    n = 2
    d = 4
    print(f"parameters : n = {n}, d = {d}, kappa = {kappa}\n")
    t0 = time.time()
    key, seed_T, seed_A, seed_B, success = random_exchange(d,n,kappa)
    t1 = time.time()
    if success:
        print(f"SUCCESS ({t1-t0} seconds)\nkey = {key.hex()}")
    else:
        print("FAIL")
