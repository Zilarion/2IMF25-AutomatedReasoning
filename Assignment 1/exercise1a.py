from itertools import combinations, product
from z3 import *

def main(I, J, c):
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

    K = 4

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

    return s


s = main(I=8, J=8, c=8000)

print(s.check())
print(s.model())