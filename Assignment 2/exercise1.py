from itertools import combinations, permutations, product
from z3 import *

def rng(*args):
    def r(i, n):
        return range(i, n+1)

    return r(*args) if len(args) == 2 else r(1, args[0])

def loop(type, *args, **kvargs):
    x = 1
    while True:
        print 'Running for x=%d' % x
        solver, vars = main(x, *args, **kvargs)

        if solver.check() == type:
            print 'Solution for x=%d' % x
            return solver, vars

        x += 1


def main(x, C, C_truck, F_0, T_0, S_0, D, cyclic=False):
    solver = Solver()

    n = len(C)

    F = {(i, s): Int('F_%d_%d' % (i, s)) for i, s in product(rng(n), rng(0, x))}
    T = {s: Int('T_%d' % s) for s in rng(0, x)}
    S = {s: Int('S_%d' % s) for s in rng(0, x)}
    A = {s: Int('A_%d' % s) for s in rng(x)}
    L = Int('L')

     # The state should be valid
    for s in rng(x):
        solver.add(And(S[s] >= 0, S[s] <= n))

    # Initial village amount
    for i in rng(n):
        solver.add(F[i, 0] == F_0[i-1])

    # Initial truck amount
    solver.add(T[0] == T_0)

    # Initial state
    solver.add(S[0] == S_0)

    # The villages cannot store a negative amount of food and cannot exceed their capacity
    for i, s in product(rng(n), rng(x)):
        solver.add(And(F[i, s] >= 0, F[i, s] <= C[i-1]))

    # The truck cannot store a negative amount of food and cannot exceed its capacity
    for s in rng(x):
        solver.add(And(T[s] >= 0, T[s] <= C_truck))

    # The state transitions should be valid
    for i, s in product(rng(0, n), rng(x)):
        solver.add(
            Implies(
                S[s-1] == i,
                Or([
                    S[s] == j
                    for j in rng(0, n) if D[i][j] is not None
                ])
            )
        )

    # The new village values should be correct
    for i, j, s in product(rng(0, n), rng(n), rng(x)):
        if D[i][j] is not None:
            solver.add(Implies(
                And(S[s-1] == i, S[s] == j),
                And([
                    F[j, s-1] - D[i][j] >=0,
                    F[j, s] == F[j, s-1] - D[i][j] + A[s]
                ] + [F[k, s] == F[k, s-1] - D[i][j] for k in rng(n) if k != j]),
            ))
    for i, s in product(rng(0, n), rng(x)):
        if D[i][0] is not None:
            solver.add(Implies(
                And(S[s-1] == i, S[s] == 0),
                And([F[j, s] == F[j, s-1] - D[i][0] for j in rng(n)]),
            ))

    # The new truck value should be correct
    for s in rng(x):
        solver.add(T[s] == T[s-1] - A[s])

    if cyclic:
        solver.add(Or([
            And(
                [
                    L == s,
                    S[x] == S[s],
                    T[x] == T[s]
                ] \
                + [F[i, x] == F[i, s] for i in rng(n)]
            )
            for s in rng(x-1)
        ]))

    return solver, (F, T, S, A, L)

# Capacity per village
C = [120, 160, 100, 160]

# Max truck load
C_truck = 240

# Initial amount per village
F_0 = [80, 80, 80, 80]

# Initial truck load
T_0 = 240

# Initial truck location
S_0 = 0

# Distances
D = [
    [None, 15, None, 15, None],
    [15, None, 17, 12, None],
    [None, 17, None, 10, 20],
    [15, 12, 10, None, 20],
    [None, None, 20, 20, None]
]

# Assignment A
print 'Assignment A'
print '---'
loop(unsat, C, C_truck, F_0, T_0, S_0, D)
print ''
print ''

# Assignment B
print 'Assignment B'
print '---'
C_truck = 260
T_0 = 260
solver, (F, T, S, A, L) = loop(sat, C, C_truck, F_0, T_0, S_0, D, cyclic=True)
model = solver.model()
print 'Start loop at %s' % str(model[L])
for i in rng(len(A)):
    print 'Step %s: S=%s, A=%s' % (i, model[S[i]], model[A[i]])
