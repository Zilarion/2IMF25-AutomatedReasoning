# Find an NFA M over T = {a, b} with the least possible number of states for which the
# only non-empty words in L(M) of length < 5 are aa, bb, aba, baa, abab, babb and bbba

T = ['a', 'b'] 	# possible transitions
L = ["aa", "bb", "baa", "abab", "babb", "bbba"]	# The requested language


print 'MODULE main'

# Variables
print ''
print 'VAR '
print 's: array 0..5 of {a, b, e};'
print 'i: 0..5'

# Defines
print 'DEFINE'
print 'valid := '
print 'case '
define = '('
for l in L:
	for i in range(0, len(l)):
		define += 's[%d] = %s' % (i, l[i])
		if (l != "bbba" or i < len(l) - 1):
			define += ") | (" if i == len(l) - 1 else " & "
		
print define + ') : TRUE;'
print 'TRUE: FALSE;'
print 'esac;'
# Initial state value
print 's := [e, e, e, e, e]'

# INIT
print ''
print 'INIT'
print 'i = 0'

print ''
print 'TRANS'
print 'next(s) := case'
print	's[i] = a'
print 'esac;'

print 'LTLSPEC G !(TRUE)'