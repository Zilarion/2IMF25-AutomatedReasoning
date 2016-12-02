from itertools import combinations, product
from z3 import *

def main(W, H, C, p, d):
    n = len(C)

    x, y, w, h = [[Int('%s_%d' % (var, i)) for i in range(n)] for var in 'xywh']

    s = Solver()

    for i in range(n):
        # On chip
        s.add(And(
            x[i] >= 1,
            x[i] + w[i] <= W,
            y[i] >= 1,
            y[i] + h[i] <= H,
        ))

        # Size
        s.add(Or(
            And(w[i] == C[i][0], h[i] == C[i][1]),
            And(w[i] == C[i][1], h[i] == C[i][0])
        ))

    # No overlap
    for i,j in combinations(range(n), 2):
        s.add(Or(
            x[i] + w[i] <= x[j],
            x[j] + w[j] <= x[i],
            y[i] + h[i] <= y[j],
            y[j] + h[j] <= y[i]
        ))

    # Connected to power component
    for i in range(p, n):
        s.add(Or([Or(
            And(y[j] == y[i] + h[i], x[i] < x[j] + w[j], x[j] < x[i] + w[i]),
            And(x[j] + w[j] == x[i], y[i] < y[j] + h[j], y[j] < y[i] + h[i]),
            And(y[j] + h[j] == y[i], x[i] < x[j] + w[j], x[j] < x[i] + w[i]),
            And(x[j] == x[i] + w[i], y[i] < y[j] + h[j], y[j] < y[i] + h[i]),
        ) for j in range(p)]))

    # Minimal distance between power components
    for i,j in combinations(range(p), 2):
        s.add(And(
            Or(
                2 * x[i] + w[i] - (2 * x[j] + w[j]) >=  2 * d,
                2 * x[j] + w[j] - (2 * x[i] + w[i]) >=  2 * d
            ),
            Or(
                2 * y[i] + h[i] - (2 * y[j] + h[j]) >=  2 * d,
                2 * y[j] + h[j] - (2 * y[i] + h[i]) >=  2 * d
            )
        ))

    return s, (x,y,w,h)

d = 17;
C = [(4, 3), (4, 3), (4, 5), (4, 6), (5, 20), (6, 9), (6, 10), (6, 11), (7, 8), (7, 12), (10, 10), (10, 20)]
W = 30
H = 30
p=2
n = len(C)
s, vars = main(W, H, C, p, d)

print(s.check())

model = s.model()
chips = range(1, p+1) + [chr(ord('A') + i) for i in range(n-p)]
grid = [['.'] * W for _ in range(H)]
for i in range(n):
    x,y,w,h = [int(str(model.evaluate(var[i]))) for var in vars]
    print chips[i], '|', x,y,w,h
    for a, b in product(range(y, y+h), range(x, x+w)):
        grid[a-1][b-1] = str(chips[i])

print '\n'.join([''.join(row) for row in grid])
