from itertools import combinations

def rng(*args):
    def r(i, n):
        return range(i, n+1)

    return r(*args) if len(args) == 2 else r(1, args[0])

def main(a0, e):
    n = len(a0)

    print('MODULE main')

    print('VAR')
    for i in rng(n):
        print('a%d : 0..50;' % i)
    print ('i : 2..%d;' % (n-1))

    print('INIT')
    print(' & '.join(['a%d = %d' % (i, a0[i-1]) for i in rng(n)]))

    print('TRANS')
    for i in rng(2, n-1):
        print('%s (next(i) = %d ? next(a%d) = a%d + a%d : next(a%d) = a%d)' % ((' ' if i==2 else '&'), i, i, i-1, i+1, i, i))
    print('& next(a1) = a1')
    print('& next(a%d) = a%d' % (n, n))

    print('LTLSPEC G !(%s)' % ' & '.join(['a%d = a%d' % (i, j) for i, j in combinations(e, 2)]))

a0 = rng(8)
e = [3, 5, 7]
main(a0, e)