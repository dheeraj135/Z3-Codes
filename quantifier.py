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
# 3.4
# u = DeclareSort('U')
# H = Function('Human',u,BoolSort())
# M = Function('Mortal',u,BoolSort())
# x = Const('x',u)

# all_mort = ForAll(x,Implies(H(x),M(x)))

# s = Const('Socrates',u)
# thm = Implies(And(H(s),all_mort),M(s))
# solve((thm))

#3.5

D = DeclareSort('d')
Dk = Function('Drink',D,BoolSort())
x = Const('x',D)
y = Const('y',D)

drink = Exists(x,Implies(Dk(x),ForAll(y,Dk(y))))
solve(drink)
solve(Not(drink))