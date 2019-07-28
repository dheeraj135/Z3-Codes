from z3 import *

parity_dect = {}
def dfs(t,parity):
    if not t.num_args():
        name = t.decl().name()
        if(name in parity_dect.keys()):
            parity_dect[name] = max(parity_dect[name],parity)
        else:
            parity_dect[name] = parity
    if t.decl().name()=="not":
        parity=(1-parity)
    if t.decl().name()=="=>":
        dfs(t.arg(0),1-parity)
        dfs(t.arg(1),parity)
    elif t.decl().name()=="xor" or t.decl().name()=='=':
        dfs(t.arg(0),parity)
        dfs(t.arg(0),1-parity)
        dfs(t.arg(1),parity)
        dfs(t.arg(1),1-parity)
    else:
        for i in range(0,t.num_args()):
            dfs(t.arg(i),parity)


x = Bool('x')
y = Bool('y')
t = Bool('t')
p = Bool('p')
q = Bool('q')
r = Bool('r')

s = Solver()
first = And(p,Not(And(Not(q),p)))
second = Not(Not(p))
third = Not(p)
fourth = Implies(Implies(t,p),And(Or(p,Not(r)),Or(r,q)))
fifth = And(Or(p,Not(r)),Or(r,q))
s.add(first,second,third,fourth,fifth)
for c in s.assertions():
    parity_dect.clear()
    dfs(c,0)
    print("Positive Vars: ",end="")
    for x in parity_dect.keys():
        if(parity_dect[x]==0):
            print(x,end=" ")
    print()