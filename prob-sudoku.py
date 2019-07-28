#!/usr/bin/python

from z3 import *
import argparse
import itertools
import time

problem1 = [
 [ 9, 0, 0,   0, 1, 0,   5, 0, 0],
 [ 7, 0, 0,   8, 0, 3,   0, 0, 2],
 [ 0, 0, 0,   0, 0, 0,   3, 0, 8],

 [ 0, 7, 8,   0, 2, 5,   6, 0, 0],
 [ 0, 0, 0,   0, 0, 0,   0, 0, 0],
 [ 0, 0, 2,   3, 4, 0,   1, 8, 0],

 [ 8, 0, 9,   0, 0, 0,   0, 0, 0],
 [ 5, 0, 0,   4, 0, 1,   0, 0, 9],
 [ 0, 0, 1,   0, 5, 0,   0, 0, 4]
]

problem2 = [
[ 0, 8, 0,   0, 0, 3,   0, 0, 0],
[ 5, 0, 3,   0, 4, 0,   2, 0, 0],
[ 7, 0, 4,   0, 8, 0,   0, 0, 3],

[ 0, 7, 0,   0, 0, 0,   5, 0, 0],
[ 0, 3, 0,   8, 0, 5,   0, 6, 0],
[ 0, 0, 1,   0, 0, 0,   0, 9, 0],

[ 9, 0, 0,   0, 3, 0,   7, 0, 6],
[ 0, 0, 7,   0, 2, 0,   3, 0, 1],
[ 0, 0, 0,   6, 0, 0,   0, 2, 0]
]
problem3 = [
    [0,0,0, 9,0,0,  0,8,0],
    [0,0,4, 0,5,1,  0,0,0],
    [7,8,0, 0,0,0,  0,9,0],
    
    [0,0,0, 0,9,0,  4,0,2],
    [0,0,8, 0,0,0,  3,0,0],
    [2,0,1, 0,7,0,  0,0,0],

    [0,6,0, 0,0,0,  0,4,7],
    [0,0,0, 3,6,0,  1,0,0],
    [0,5,0, 0,0,9,  0,0,0]
]
problem = problem3
# problem = problem2

# define the problem variables
vs = [[[Bool("X_{}_{}_{}".format(i,j,k)) for k in range(0,9)] for j in range(0,9)] for i in range(0,9) ]
# print(vs)
# Hint: three dimentional array

def sum_to_one( ls ):
    # F = False
    # for i in range(0,n):
    #     F = Or(F,vs[i])
    # T = True
    # for i in range(0,n):
    #     for j in range(i+1,n):
    #         T = And(T,Or(Not(ls[i]),Not(ls[j])))
    # return And(T,F)
    F = Or(ls)
    at_most_one_list = []
    for pair in itertools.combinations(ls,2):
        at_most_one_list.append(Or(Not(pair[0]),Not(pair[1])))
    return And(And(at_most_one_list),F)

# Accumulate constraints in the following list 
Fs = []


# Encode already filled positions
for i in range(0,9):
    for j in range(0,9):
        if(problem[i][j]):
            k = problem[i][j]
            for temp in range(0,9):
                vs[i][j][temp]=False
            vs[i][j][k-1]=True
# Encode for i,j  \sum_k x_i_j_k = 1
for i in range(0,9):
    for j in range(0,9):
        arr = []
        for k in range(0,9):
            arr.append(vs[i][j][k])
        Fs.append(sum_to_one(arr))
# Encode for j,k  \sum_i x_i_j_k = 1
for j in range(0,9):
    for k in range(0,9):
        arr = []
        for i in range(0,9):
            arr.append(vs[i][j][k])
        Fs.append(sum_to_one(arr))
# Encode for i,k  \sum_j x_i_j_k = 1
for i in range(0,9):
    for k in range(0,9):
        arr = []
        for j in range(0,9):
            arr.append(vs[i][j][k])
        Fs.append(sum_to_one(arr))
# Encode for i,j,k  \sum_r_s x_3i+r_3j+s_k = 1
for x in range(0,3):
    for y in range(0,3):
        ini = x*3
        inj = y*3
        for k in range(0,9):
            arr = []
            for i in range(0,3):
                for j in range(0,3):
                    arr.append(vs[i+ini][j+ini][k])
            Fs.append(sum_to_one(arr))

s = Solver()
s.add( And( Fs ) )

if s.check() == sat:
    m = s.model()
    print(m)
    for i in range(9):
        if i % 3 == 0 :
            print ("|-------|-------|-------|")
        for j in range(9):
            if j % 3 == 0 :
                print ("|",end=",")
            for k in range(9):
                # FILL THE GAP
                # val model for the variables
                # val = m[]
                val = m[vs[i][j][k]]
                if is_true( val ):
                    print ("{}".format(k+1),end=",")
            if(problem[i][j]):
                print ("{}".format(problem[i][j]),end=",")
        print ("|")
    print ("|-------|-------|-------|")
else:
    print ("sudoku is unsat")

# print vars
