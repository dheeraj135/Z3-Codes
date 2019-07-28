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

u = DeclareSort('U')

c = Const('c',u)
d = Const('d',u)
f = Function('f',u,u)

P = Function('P',u,BoolSort())
phi = And(f(c)==c,Not(P(c)))
solve(phi)