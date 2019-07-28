from z3 import *

def dfs(t):
    print(t)
    print(t.decl().name())
    print('---------')
    level = 0
    if not t.num_args():
        if not t.decl().name()=="Real":
            level+=1
        return level
    for i in range(0,t.num_args()):
        temp = dfs(t.arg(i))
        if(t.decl().name()=='*'):
            level = level+temp
        else:
            level = max(level,temp)
    return level
x = Real('x')
y = Real('y')

A = x+x*x*y-2*x+4+(x*(2+x)+x*y)*2
B = simplify(A)
print(dfs(B))
print(A)
print(B)
