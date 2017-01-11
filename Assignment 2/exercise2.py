from itertools import product
from z3 import *

def loop(*args):
    n = 1
    while True:
        print 'Running for n=%d' % n
        solver, vars = main(n, *args)

        if solver.check() == sat:
            print 'Solution for n=%d' % n
            return solver, n, vars

        n += 1


def main(n, Sigma, L, l):
    solver = Solver()

    Delta = {(i, sigma, j): Bool('Delta[%d, %s, %d]' % (i, sigma, j)) for (i, j), sigma in product(product(range(n), repeat=2), Sigma)}
    F = {i: Bool('F[%d]' % i) for i in range(n)}

    T = set([w[0:i] for w in L for i in range(len(L)+1)])
    X = {t: set([sigma for sigma in Sigma if (t+sigma) in T]) for t in T}
    Xf = {t: t in L for t in T}

    R = {(t, i): Bool('R[%s, %d]' % (t, i)) for t, i in product(T, range(n))}

    solver.add(R['', 0] == True)
    for i in range(1, n):
        solver.add(R['', i] == False)

    for t in T:
        for sigma in Sigma:
            for i, j in product(range(n), repeat=2):
                if sigma in X[t]:
                    # All incoming reachable
                    solver.add(
                        Implies(
                            And(
                                R[t, i],
                                Delta[i, sigma, j]
                            ),
                            R[t+sigma, j]
                        )
                    )
                elif len(t) < l:
                    # All outgoing allowed
                    solver.add(
                        Implies(
                            R[t, i],
                            Not(Delta[i, sigma, j])
                        )
                    )

        for sigma in X[t]:
            # All desired possible
            solver.add(Or([
                And(
                    R[t, i],
                    Delta[i, sigma, j]
                )
                for i, j in product(range(n), repeat=2)
            ]))

        # Finishing behaviour
        for i in range(n):
            solver.add(
                Implies(
                    R[t, i],
                    F[i] == Xf[t]
                )
            )

    return solver, (Delta, F)

Sigma = ['a', 'b']
L = ['aa', 'bb', 'aba', 'baa', 'abab', 'babb', 'bbba']
l = 4

solver, n, (Delta, F) = loop(Sigma, L, l)
# print solver.to_smt2()
model = solver.model()
for i in range(n):
    print '%d: %s %s' % (i, '[F]' if str(model[F[i]]) == 'True' else '   ', '; '.join(['%s:%s' % (sigma, ','.join([str(j) for j in range(n) if str(model[Delta[i, sigma, j]]) == 'True'])) for sigma in Sigma]))
