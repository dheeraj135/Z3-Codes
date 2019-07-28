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
h = Function('h',IntSort(),IntSort(),IntSort())

phi = And(h(x,y)<0,h(y,x)>0,y==x+1)
solve(phi)