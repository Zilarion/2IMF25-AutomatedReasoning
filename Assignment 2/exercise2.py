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


def main(n, L):
    solver = Solver()

    Sigma = set([w[i] for w in L for i in range(len(w))])

    Delta = {(i, sigma, j): Bool('Delta[%d, %s, %d]' % (i, sigma, j)) for (i, j), sigma in product(product(range(n), repeat=2), Sigma)}
    F = {i: Bool('F[%d]' % i) for i in range(n)}
    V = {i: Bool('V[%d]' % i) for i in range(n)}

    T = set([w[0:i] for w in L for i in range(len(w)+1)])
    X = {t: set([sigma for sigma in Sigma if (t+sigma) in T]) for t in T}
    Y = {t: t in L for t in T}

    R = {(t, i): Bool('R[%s, %d]' % (t, i)) for t, i in product(T, range(n))}

    solver.add(R['', 0] == True)
    for i in range(1, n):
        solver.add(R['', i] == False)

    # Every trace should be reachable in some state
    for t in T:
        solver.add(Or([R[t, i] for i in range(n)]))

    # Every word should be finishable in some state
    for w in L:
        solver.add(Or([And(R[w, i], F[i]) for i in range(n)]))

    # If a trace is reachable there exists a path to it
    for t in T:
        if t == '':
            continue

        t_accent = t[:-1]
        sigma = t[-1]

        for j in range(n):
            solver.add(Implies(R[t, j], Or([And(R[t_accent, i], Delta[i, sigma, j]) for i in range(n)])))

    for t, sigma in product(T, Sigma):
        for i, j in product(range(n), repeat=2):
            if sigma in X[t]:
                # Reachable states should be indicated so
                solver.add(Implies(And(R[t, i], Delta[i, sigma, j]), R[t + sigma, j]))
            else:
                # A state only has valid outgoing transitions
                solver.add(Implies(R[t, i], Not(Delta[i, sigma, j])))

    # A state only finishes if it is allowed to
    for t, i in product(T, range(n)):
        if not Y[t]:
            solver.add(Implies(R[t, i], Not(F[i])))

    return solver, (Delta, F, V, R, Sigma, T)

L = ['aa', 'bb', 'aba', 'baa', 'abab', 'babb', 'bbba']

solver, n, (Delta, F, V, R, Sigma, T) = loop(L)
model = solver.model()
for i in range(n):
     print '%d: %s %s' % (i, '[F]' if str(model[F[i]]) == 'True' else '   ', '; '.join(['%s:%s' % (sigma, ','.join([str(j) for j in range(n) if str(model[Delta[i, sigma, j]]) == 'True'])) for sigma in Sigma]))
