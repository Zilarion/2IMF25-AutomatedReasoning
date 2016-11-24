from itertools import combinations, product
from z3 import *

def main(M, J, w, cooled):
    """
    Parameters
    ----------
    I: int
        Number of trucks
    J: int
        Number of pallets per truck
    c: int
        Truck capacity
    """

    I = len(M)
    K = len(w)

    SKIPPLES = 3

    p = {(i, j, k) : Bool('p[%d,%d,%d]' % (i, j, k))
        for i in range(I)
        for j in range(J)
        for k in range(K)
    }

    s = Solver()

    # One load per pallet
    for i, j in product(range(I), range(J)):
        for k1, k2 in combinations(range(K), 2):
            s.add(Not(And(p[i,j,k1], p[i,j,k2])))

    # Each truck has a capacity that should not be exceeded
    for i in range(I):
        s.add(Sum([p[i,j,k] * w[k] for j, k in product(range(J), range(K))]) <= M[i])

    # Skipples should be could
    for i, j in product(range(cooled, I), range(J)):
        s.add(Not(p[i,j,SKIPPLES]))

    return s


s = main(M=[8000] * 8, J=8, w=[700, 400, 1000, 2500, 200], cooled=3)

print(s.to_smt2())

# print(s.check())
# print(s.model())