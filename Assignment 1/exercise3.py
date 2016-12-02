from itertools import combinations, product, permutations
from z3 import *

def main(r, F, S, O, T):
    if T is None:
        T = sum(r)

    n = len(r)

    s = [Int('s_%d' % i) for i in range(n)]

    solver = Solver()

    # First job should start at time 0
    solver.add(Or([s[i] == 0 for i in range(n)]))

    # Each job should start after time 0
    solver.add(And([s[i] >= 0 for i in range(n)]))

    for i, j in permutations(range(n), 2):
        # End before start
        if F[i][j]:
            solver.add(s[j] >= s[i] + r[i])

        # Start before start
        if S[i][j]:
            solver.add(s[j] >= s[i])

    for i, j in combinations(range(n), 2):
        # Non overlapping
        if O[i][j] or O[j][i]:
            solver.add(Or(s[i] + r[i] <= s[j], s[i] >= s[j] + r[j]))

    for i in range(n):
        solver.add(s[i] + r[i] <= T)

    return solver, (s)

n = 12
r = [i+6 for i in range(n)]
F = [[False for j in range(n)] for i in range(n)]
S = [[False for j in range(n)] for i in range(n)]
O = [[False for j in range(n)] for i in range(n)]

F[2][0] = True
F[2][1] = True

F[4][2] = True
F[4][3] = True

F[6][2] = True
F[6][3] = True
F[6][4] = True

S[7][4] = True

F[8][4] = True
F[8][7] = True

F[10][9] = True

F[11][8] = True
F[11][10] = True

O[4][6] = True
O[4][9] = True
O[6][9] = True

T = None

model = None

while True:
    s, vars = main(r, F, S, O, T)

    if s.check() != sat:
        break

    model = s.model()
    T = max([int(str(model.evaluate(vars[i]))) + r[i] for i in range(n)]) - 1


for i in range(n):
    print i + 1, model.evaluate(vars[i])

