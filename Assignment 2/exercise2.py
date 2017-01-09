from itertools import combinations, permutations, product
from z3 import *

def loop():
    n = 1
    while True:
        print 'Running for n=%d' % n
        solver, vars = main(n)

        if solver.check() == sat:
            print 'Solution for n=%d' % n
            return solver, vars

        n += 1


def main(n):
    solver = Solver()

    Sigma = ['a', 'b']
    L = ['aa', 'bb', 'baa', 'abab', 'babb', 'bbba']

    Delta = {(i, sigma, j): Bool('Delta[%d, %s, %d]' % (i, sigma, j)) for (i, j), sigma in product(permutations(range(n), 2), Sigma)}
    F = {i: Bool('F[%d]' % i) for i in range(n)}

    T = set([w[0:i] for w in L for i in range(len(L)+1)])
    X = {t: set([sigma for sigma in Sigma if (t+sigma) in T]) for t in T}
    Xf = {t: t in L for t in T}

    R = {(t, i): Bool('O[%s, %d]' % (t, i)) for t, i in product(T, range(n))}

    solver.add(R['', 0] == True)
    for i in range(1, n):
        solver.add(R['', i] == False)

    for t in T:
        for sigma in Sigma:
            for i, j in permutations(range(n), 2):
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
                elif len(t) < 4:
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
                for i, j in permutations(range(n), 2)
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

solver, (Delta, F) = loop()
print solver.model()