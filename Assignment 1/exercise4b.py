from itertools import combinations, product
from z3 import *

# Range starting at 1 and including last element
def rng(*args):
    def r(i, n):
        return range(i, n+1)

    return r(*args) if len(args) == 2 else r(1, args[0])

def loop(a0, e):
    T = 0
    while True:
        print ('Running with T=%d' % T)
        solver, vars = main(a0, e, T)
        if solver.check() == sat:
            return solver.model(), vars
        T += 1

def main(a0, e, T):
    n = len(a0)

    a = {(i, t): Int('a[%d, %d]' % (i, t)) for i in rng(n) for t in rng(0, T)}
    s = {t: Int('s[%d]' % t) for t in rng(T)}

    solver = Solver()

    solver.add([v >= 0 for v in a.values()]) #TEMP

    # Initial values
    for i in rng(n):
        solver.add(a[i, 0] == a0[i-1])

    for t in rng(T):
        solver.add(
            s[t] > 1,
            s[t] < n
        )

    # Updates
    for i, t in product(rng(2, n-1), rng(T)):
         solver.add(If(
            s[t] == i,
            a[i, t] == a[i-1, t-1] + a[i+1, t-1],
            a[i, t] == a[i, t-1]
        ))

    # First and last stay the same
    for t in rng(T):
        solver.add(
            a[1, t] == a0[0],
            a[n, t] == a0[n-1]
        )

    # Equality
    for i, j in combinations(e, 2):
        solver.add(a[i, T] == a[j, T])

    return solver, (a, s)

a0 = rng(8)
e = [3, 5, 7]
model, (a, s) = loop(a0, e)

a = {k: int(str(model.evaluate(v))) for k, v in a.items()}
s = [int(str(model.evaluate(s[t]))) for t in rng(len(s))]

for t in rng(0, len(s)):
    print [a[i, t] for i in rng(len(a0))]

print('')
print(len(s))
print(s)
