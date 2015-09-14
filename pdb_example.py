# Experiment with the Python debugger, pdb
# inspired by https://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/

##########################
# PDB commands:
# l = current location
# n = step next
# s = step into
# b = list and set breakpoints
# c = continue (run till next break point)
# ![var] = set or reference variable in script
##########################

import pdb

def combine(s1,s2):      # define subroutine combine, which...
    s3 = s1 + s2 + s1    # sandwiches s2 between copies of s1, ...
    s3 = '"' + s3 +'"'   # encloses it in double quotes,...
    return s3            # and returns it.

a = "aaa"
pdb.set_trace() # Here we start debugging!
b = "bbb"
c = "ccc"
final = combine(a,b)
print final
