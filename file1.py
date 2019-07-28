from z3 import *

def solve(phi):
    s = Solver()
    s.add(phi)
    r = s.check()
    if r==sat:
        print("sat")
        m = s.model()
        print(m)
    else:
        print("unsat")


p1 = Bool("p1")
p2 = Bool("p2")
phi = Or(p1,p2)
solve(phi)