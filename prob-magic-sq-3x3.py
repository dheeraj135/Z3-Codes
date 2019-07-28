#!/usr/bin/python3

#
# A 3x3 magic square contains all integers from 1 to 9.
# Sum of all rows, columns, and diagonals are same.
#

from z3 import * 
import itertools
import time
# import matplotlib

def solve(n):
    # variables for the entries of the magic square
    vs = [  [Int("x_{}_{}".format(i,j))  for j in range(n)] for i in range(n)]

    # create constraints
    #   -- all entries are between 1-9
    #   -- all entries are distinct
    #   There is a sum value t
    #   -- sum of rows is t
    #   -- sum of columns is t
    #   -- sum of diagonals is t
    cond_1_9_list = []
    for i in range(0,n):
        for j in range(0,n):
            cond_1_9_list.append(vs[i][j]<n*n+1)
            cond_1_9_list.append(vs[i][j]>0)
    cond_1_9 = And(cond_1_9_list)
    # cond_unique = []
    # for i in range(0,3):
    #     for j in range(0,3):
    #         for k in range(0,3):
    #             for l in range(0,3):
    #                 if((i,j)>(k,l)):
    #                     cond_unique.append(Not(vs[i][j]==vs[k][l]))
    # cond_unique = And(cond_unique)
    cond_unique = Distinct(list(itertools.chain.from_iterable(vs)))
    sums = [0]*(2*n+2)
    for i in range(0,n):
        for j in range(0,n):
            sums[i]+=vs[i][j]
            sums[j+n]+=vs[i][j]
        sums[2*n]+=vs[i][i]
        sums[2*n+1]+=vs[i][n-i-1]
    # sums.append(vs[0][0]+vs[1][1]+vs[2][2])
    # sums.append(vs[0][2]+vs[1][1]+vs[2][0])
    same_sum = True
    for i in range(0,len(sums)):
        same_sum=And(same_sum,sums[i]==sums[0])
    phi = And(cond_1_9,cond_unique,same_sum)
    s = Solver()
    s.add(phi)

    r = s.check()
    if r == sat:
        # m = s.model()
        # for i in range(n):
        #     for j in range(n):
        #         print( "|-----",end="")
        #     print("|")
        #     for j in range(n):
        #         print("|  ", end ="")
        #         val = m[vs[i][j]]
        #         print( val, end ="  ")
        #     print("|")
        # for j in range(n):
        #     print( "|-----",end="")
        # print("|")
        print("sat")
    else:
        print("unsat")

x = []
y = []
for i in range(1,9):
    start = time.clock()
    solve(i)
    end = time.clock()
    tot_time = end-start
    x.append(i)
    y.append(tot_time)
    print(i,tot_time)
