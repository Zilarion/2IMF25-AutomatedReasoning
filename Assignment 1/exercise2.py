from itertools import combinations, product
from z3 import *

def overlap(s1, e1, s2, e2):
    return And(s1 <= e2, s2 <= e1)

def main(W, H, C, p):
    n = len(C)

    x, y, w, h = [[Int('%s_%d' % (var, i)) for i in range(n)] for var in 'xywh']

    s = Solver()

    for i in range(n):
        # On chip
        s.add(
            x[i] >= 1,
            x[i] + w[i] <= W,
            y[i] >= 1,
            y[i] + h[i] <= H,
        )

        # Size
        s.add(Or(
            And(w[i] == C[i][0], h[i] == C[i][1]),
            And(w[i] == C[i][1], h[i] == C[i][0])
        ))

    # No overlap
    for i, j in combinations(range(n), 2):
        s.add(Not(And(
            overlap(x[i], x[i] + w[i], x[j], x[j] + w[j]),
            overlap(y[i], y[i] + h[i], y[j], y[j] + h[j])
        )))

    # Connected to power component
    #for i in range(p, n):
    #    s.add(Or([And(
    #        overlap(x[i], x[i] + w[i], x[j] - 1, x[j] + w[j] + 1),
    #        overlap(y[i], y[i] + h[i], y[j] - 1, y[j] + h[j] + 1)
    #    ) for j in range(p)]))

    # TODO: minimal distance between power components

    return s, (x,y,w,h)

C = [(4, 3), (4, 3), (4, 5), (4, 6), (5, 20), (6, 9), (6, 10), (6, 11), (7, 8), (7, 12), (10, 10), (10, 20)]
W = 30
H = 30
p=2
n = len(C)
s, vars = main(W, H, C, p)

print(s.check())

model = s.model()
chips = range(1, p+1) + [chr(ord('A') + i) for i in range(n-p)]
grid = [['.'] * W for _ in range(H)]
for i in range(n):
    x,y,w,h = [int(str(model.evaluate(var[i]))) for var in vars]
    print chips[i], '|', x,y,w,h
    for a, b in product(range(y, y+h), range(x, x+w)):
        grid[a-1][b-1] = chips[i]

print '\n'.join([''.join(row) for row in grid])
