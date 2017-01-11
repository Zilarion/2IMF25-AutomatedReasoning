from itertools import combinations, product, permutations
from z3 import *

def main(pl, sr, s, at, t, l, T):
  """
  Parameters
  ----------
  sr: spot runway
  pl: plane length required
  s:  required planes to be spotted 
  at: arrival time of planes
  t: time to process this plane
  l: length of each runway
  T: maximum delay
  """
  I = len(at);
  J = len(sr);

  # Resulting action time
  a = [Int('a_%d' % i) for i in range(I)]

  # Resulting runway number
  r = [Int('r_%d' % i) for i in range(I)]

  solver = Solver()

  # Only existing runways may be used
  solver.add(And([And(r[i] <= J - 1, r[i] >= 0) for i in range(I)]))

  # All planes must land before 10:00
  solver.add(And([a[i] + t[i] <= 60 for i in range(I)]))

  # All planes must land on a runway which is long enough
  solver.add(And([Implies(r[i] == j, pl[i] <= l[j]) for i in range(I) for j in range(J)]))

  # Special planes have to land on a spot runway
  solver.add(And([Implies(r[i] == j, Or(Not(s[i]), sr[j])) for i in range(I) for j in range(J)]))

  # Two runways may never be used at the same time
  solver.add(And([Implies(And(r[i] == j, r[ip] == j), Or(a[i] + t[i] <= a[ip], a[ip] + t[ip] <= a[i])) for i, ip in permutations(range(I), 2) for j in range(J)]))  

  # All planes must have landed/taken off after their arrival/departure time
  solver.add(And([a[i] >= at[i] + t[i] for i in range(I)]))

  # Two runways may never be used at the same time
  solver.add(And([Implies(Or(And(r[i] == 3-1, r[ip] == 4-1), And(r[i] == 2-1, r[ip] == 4-1)), Or(a[i] + t[i] <= a[ip], a[ip] + t[ip] <= a[i])) for i, ip in permutations(range(I), 2)]))  

  # Each planes has a maximum of T delay
  solver.add(And([a[i] - t[i] - at[i] <= T for i in range(I)]))

  return solver, (a, r)


J = 6   # Number of runways
I = 50  # Number of planes
l = [3800, 3500, 3450, 3400, 3300, 2014] # Length of each runway

# Plane length required
pl = []
for i in range(I):
  reqL = 2000
  if i <= 10 - 1:
    reqL = 3480
  elif i >= 15 - 1 and i <= 20 - 1:
    reqL = 3800
  elif i >= 40 - 1 and i <= 50 - 1:
    reqL = 3500
  pl.append(reqL)

# Which runways are spot runways
sr = [False for i in range(J)]
sr[1 - 1] = True
sr[3 - 1] = True

# Arrival time of planes
at = [i for i in range(I)]

# Which planes require to be spotted
s = [False for i in range(I)]
s[12 - 1] = True
s[33 - 1] = True
s[34 - 1] = True
s[40 - 1] = True


# The time it takes for this plane to land/take off -> 3 for even plane numbers (i-1) / 4 for odd 
t = [2 if (i%2 == 1) else 2 for i in range(I)]

model = None

T = 5
while True:
  print "Testing with a max delay of", T;
  solv, vars = main(pl, sr, s, at, t, l, T)

  if solv.check() != sat:
    print "unsat!"
    break
  T = T - 1;

  model = solv.model()
  break;

for i in range(I):
  go = int(str(model.evaluate(vars[0][i])))
  runway = int(str(model.evaluate(vars[1][i])))
  print i + 1, "leaves/arrives at 9:%d from runway %d" % (go, runway)
