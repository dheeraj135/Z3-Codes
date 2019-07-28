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
phi = And(x+y>5,x>1,y>1)
solve(phi)