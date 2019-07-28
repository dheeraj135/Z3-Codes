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
h = Function('h',IntSort(),IntSort())

phi = And(h(x)>5,h(y)<2,x==y+1)
solve(phi)