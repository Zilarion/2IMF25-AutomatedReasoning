C = {'A':120, 'B':160, 'C':100, 'D':160} # Capacity per village
I = {'A':80, 'B':80, 'C':80, 'D':80} # Initial amount per village
T = 240 # Initial truck load
L = 240 # Max truck load
S = 'S' # Initial truck location
D = {
    'A': {'B': 17, 'C': 12, 'S': 15},
    'B': {'A': 17, 'C': 10, 'D': 20},
    'C': {'A': 12, 'B': 10, 'D': 20, 'S': 15}
    'D': {'B': 20, 'C': 20}
    'S': {'A': 15, 'C': 15}
}

print 'MODULE main'

print 'DEFINE D := [%s]' % ['[%d]' % ', '.join(D[k1][k2] if k2 in D[k1] else 1000 for k2 in C.keys()]) for k1 in C.keys()]

for k, v in C:
    print 'VAR %s : 0..%d;' % (k, v)
print 'VAR T : {%s};' % (', '.join(C.keys()).lower())
print 'VAR L : 0..%d;' % L

print ''
print 'INIT'
print ' & '.join(['%s = %s' % (k, v) for k, v in I].concat(['L = %d' % T, 'T = %s' % S.lower()]))

print 'TRANS'
for k1 in C.keys():
    for k2 in D[k1].keys()
    print 'next(%s) = %s - D[T][next(T)] + (next(S) == %s ? (L - next(L)) : 0)' % (k, k, k, k)

print 'LTLSPEC G !()'