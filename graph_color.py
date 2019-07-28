from z3 import *
import time
import matplotlib.pyplot as plt

f = open("edges.txt","r")
stack = []
adjList = {}
rev_graph = {}
n =0 
m =0
arr = []

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


def read(f,k):
    i =0 
    first = 1 
    global n
    global m
    f = open("edges.txt","r")
    for x in f:
        if i>k:
            break
        i+=1
        a,b = x.split(',')
        a = int(a)
        b = int(b)
        if first:
            n = a
            m=b
            first=0
            continue
        # print(a,b)
        if a in adjList.keys():
            adjList[a].append(b)
        else:
            adjList[a]=[b]
    for i in range(1,n+1):
        if i not in adjList.keys():
            adjList[i]=[]
    m = min(m,k)
    f.close()

def color_graph(d):
    global arr
    arr = [  [Bool("x_{}_{}".format(i,j))  for j in range(d)] for i in range(n+1)]
    F = []
    for a in adjList.keys():
        for b in adjList[a]:
            for x in range(d):
                # print(a,b,x)
                F.append(Or(Not(arr[a][x]),Not(arr[b][x])))
        temp = False
        for x in range(d):
            temp = Or(temp,arr[a][x])
        F.append(temp)
    F = And(F)
    return F
temp = 100
arrx = []
arry = []
for i in range(1,500,10):
    adjList = {}
    read(f,i)

    d = 2
    # print(n)
    # print(adjList)

    F = color_graph(d)
    s = Solver()
    s.add(F)
    start = time.clock()
    r = s.check()
    end = time.clock()
    arrx.append(i)
    arry.append(end-start)
    print(i,end-start)
    if r==sat:
        print("sat")
        # m = s.model()
        # for i in range(1,n+1):
        #     print(i,end=": ")
        #     for j in range(0,d):
        #         if(is_true(m[arr[i][j]])):
        #             print(j,end=" ")
        #     print()
    else:
        print("unsat")

plt.plot(arrx,arry)
plt.show()