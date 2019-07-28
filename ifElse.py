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

x = Int('x')
y = Int('y')
phi = And(3*x+2*y-3==0,y>0)
solve(phi)
