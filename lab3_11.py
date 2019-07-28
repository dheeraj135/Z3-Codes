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

F = DeclareSort('F')
inp = Const('inp',F)
f = Function('f',F,F)
L1 = Const('L1',F)
L2 = Const('L2',F)
g = Function('f',F,F)
k = Function('k',F,F)
h = Function('h',F,F)
c = Function('c',F,BoolSort())
d = Function('d',F,F)
L4 = Const('L4',F)
L3 = Const('L3',F)
L5 = Const('L5',F)
L1N = Const('L1N',F)
L2N = Const('L2N',F)
L4N = Const('L4N',F)
L3N = Const('L3N',F)
L5N = Const('L5N',F)

L1 = f(inp)
L2 = L1
L3 = k(g(L1))
L4 = h(L1)
L5 = If(c(L2),L3,d(L4))

L1N = f(inp)
L2N = c(L1N)
L3N = If(c(L1N),g(L1N),h(L1N))
L5N = If(L2N,k(L3N),d(L3N))
print(L3)
solve(L5==L5N)
solve(Not(L5==L5N))