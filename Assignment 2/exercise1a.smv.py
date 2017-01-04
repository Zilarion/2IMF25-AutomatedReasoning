C = {'A':120, 'B':160, 'C':100, 'D':160}
I = {'A':80, 'B':80, 'C':80, 'D':80}
T = 240
L = 240

print 'MODULE main'
print 'VAR'

for k, v in C:
    print '%s : 0..%d;' % (k, v)

print 'T : {%s};' % (', '.join(C.keys()).lower())
print 'L : 0..%d;' % L
print 'U : 0..%d;' % L

print ''
print 'INIT'
print ' & '.join(['%s = %s' % (k, v) for k, v in I]

print 'TRANS'
for k C.keys():
    print 'next(%s) = %s - dist[T][next(T)] + (old(T) ==  ? U : 0)'