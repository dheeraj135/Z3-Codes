from z3 import *

def solve1(phi):
    s = Solver()
    s.add(phi)
    r = s.check()
    if r==sat:
        print("sat")
        m = s.model()
        print(m)
    else:
        print("unsat")


A = Bool("A")
B = Bool("B")
C = Bool("C")
X1 = And(A,B)
X2 = Or(B,C)
X3 = And(A,C)
X4 = Not(Or(X2,X3))
D = Or(X4,X1)
print(D)
solve1(D)