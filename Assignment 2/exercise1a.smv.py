V = ['A', 'B', 'C', 'D'] # Villages
C = {'A':120, 'B':160, 'C':100, 'D':160} # Capacity per village
I = {'A':80, 'B':80, 'C':80, 'D':80} # Initial amount per village
T = 240 # Initial truck load
L = 240 # Max truck load
S = 'S' # Initial truck location
D = {
    'A': {'B': 17, 'C': 12, 'S': 15},
    'B': {'A': 17, 'C': 10, 'D': 20},
    'C': {'A': 12, 'B': 10, 'D': 20, 'S': 15},
    'D': {'B': 20, 'C': 20},
    'S': {'A': 15, 'C': 15}
}

Vplus = ['S'] + V

print 'MODULE main'

print ''
print 'DEFINE x := [%s];' % ', '.join(['[%s]' % ', '.join([str(D[k1][k2] if k2 in D[k1] else 1000) for k2 in Vplus]) for k1 in Vplus])

for k in V:
    print 'VAR %s : 0..%d;' % (k.lower(), C[k])
print 'VAR t : 0..%d;' % (len(Vplus) - 1)
print 'VAR l : 0..%d;' % L
print 'VAR r : 0..1;'; # Consumption rate

print ''
print 'INIT'
print ' & '.join(
    ['%s = %s' % (k.lower(), I[k]) for k in V] \
    + ['l = %d' % T, 't = %d' % (Vplus.index(S))]
)

print ''
print 'TRANS'
print 'TRUE'
for i in range(len(V)):
    print '& next(%s) = %s - x[t][next(t)] * r + (next(t) = %s ? (l - next(l)) : 0)' % (V[i].lower(), V[i].lower(), i+1)

print ''
print 'LTLSPEC G (r = 1)'