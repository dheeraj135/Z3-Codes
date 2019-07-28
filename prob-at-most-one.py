#!/usr/bin/python

from z3 import *
import argparse
import itertools
import time

# number of variables
n=10

# constructed list of variables
vs = BoolVector('vs',n)
# vs = [0]*n
# for i in range(0,n):
#     vs[i]=Bool('Bool'+str(i))
# print(vs)

# write function that encodes that exactly one variable is one
def sum_to_one( ls ):
    # F = False
    # for i in range(0,n):
    #     F = Or(F,vs[i])
    # T = True
    # for i in range(0,n):
    #     for j in range(i+1,n):
    #         T = And(T,Or(Not(ls[i]),Not(ls[j])))
    # return And(T,F)
    F = Or(ls)
    at_most_one_list = []
    for pair in itertools.combinations(ls,2):
        at_most_one_list.append(Or(Not(pair[0]),Not(pair[1])))
    return And(And(at_most_one_list),F)
# # call the function
F = sum_to_one( vs )
print(F)

# # construct Z3 solver
s = Solver()
# # add the formula in the solver
s.add(F)
# # check sat value
result = s.check()
if result == sat:
    # get satisfying model
    print(s.model())
    # print only if value is true

else:
    print("unsat")
