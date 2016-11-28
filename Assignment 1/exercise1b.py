from itertools import combinations, product
from z3 import *

def main(M, J, w, cooled, m):
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

    SKIP = 2
    PRIT = 1
    CROT = 3
    NUZ = 0


    p = {(i, j, k) : Bool('p[%d,%d,%d]' % (i, j, k))
        for i in range(I)
        for j in range(J)
        for k in range(K)
    }

    s = Solver()

    # 1) Each truck has a capacity that should not be exceeded
    for i in range(I):
        s.add(Sum([p[i,j,k] * w[k] for j, k in product(range(J), range(K))]) <= M[i])

    # 2) Skipples should be cooled
    for i, j in product(range(cooled, I), range(J)):
        s.add(Not(p[i,j, SKIP]))

    # 3) There should never be two nuzzles on the same truck
    for i in range(I):
        for j1, j2 in combinations(range(J), 2):
            s.add(Not(And(p[i, j1, NUZ], p[i, j2, NUZ])))

    # 4) At most one pallet per position
    for i, j in product(range(I), range(J)):
        for k1, k2 in combinations(range(K), 2):
            s.add(Not(And(p[i,j,k1], p[i,j,k2])))

    # 5) All pallets should be distributed over the trucks
    for k in range(K):
        if (m[k] >= 0):
            s.add(Sum([ If(p[i,j,k], 1, 0) for i, j in product(range(I), range(J))]) == m[k])

    # 6) Prittles and crottles are an explosive combination: they are not allowed to be put in the same truck.
    for i in range(I):
        for j1, j2 in combinations(range(J), 2):
            s.add(Not(And(p[i, j1, PRIT], p[i, j2, CROT])))
            s.add(Not(And(p[i, j1, CROT], p[i, j2, PRIT])))

    return {'solver': s, 'variables': p};


ret = main(M=[8000] * 8, J=8, w=[700, 400, 1000, 2500, 200], cooled=3, m=[4, 19, 8, 10, 20])

s = ret['solver']
p = ret['variables']
pallets = {
    0: 'nuzzles',
    1: 'prittles',
    2: 'skipples',
    3: 'crottles',
    4: 'dupples'
}

# print (s.to_smt2());

if s.check() == sat:
    m = s.model();
    for i, j,k in product(range(8), range(8), range(5)):
        if m.evaluate(p[i,j,k]):
            print "Truck %d at %d has %s" % (i,j,pallets[k])
else:
    print "Failed to solve"

