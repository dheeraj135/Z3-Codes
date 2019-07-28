#!/usr/bin/python3

# Mastermind is a two player game.
# There are n colors. Let k < n be a positive number.
# 
# 1. Player one chooses a hidden sequence of k colors (colors may repeat)
# 2. The game proceeds iteratively as follows until player two has guessed
#    the sequence correctly.
#   2.1 Player two makes a guess of sequence of k colors
#   2.2 Player one gives feedback to player two by giving
#     * the number of correct in both position and color, and
#     * the number of correct colors in the wrong positions.
#
# Play online
# http://www.webgamesonline.com/mastermind/index.php

# Objective of this exercise - Implement player two
#
#  Bonus point
#     - Support for imperfect player one. Imagine player one is a childs.
#       Sometimes (s)he may give wrong feedback. 
#     - Optimizations for faster codebreaking
#

from z3 import *
import argparse
import itertools
import time
import random

n=8
k=4

vs = [  [Bool ("e_{}_{}".format(i,j))  for j in range(n)] for i in range(k)]

base_cons = []

# TODO: add basic constraints
def sum_to_one( ls ):
    F = Or(ls)
    at_most_one_list = []
    for pair in itertools.combinations(ls,2):
        at_most_one_list.append(Or(Not(pair[0]),Not(pair[1])))
    return And(And(at_most_one_list),F)

def sum_atleast(ls,num):
    temp = []
    for ele in ls:
        temp.append(If(ele,1,0))
    add = 0
    for x in range(len(temp)):
        add = add+temp[x]
    return (add>=num)

for i in range(k):
    base_cons.append(sum_to_one(vs[i]))

s = Solver()

s.add( And(base_cons) )

def exist(ele,i):
    for k in ele:
        if(k==i):
            return True
    return False

def add_a_guess_solution( guess, reds, whites ):
    guess_cons = True # add constraints due to a guess
    arr = [0]*k
    for i in range(k):
        arr[i]=i
    cases = []
    # print(guess)
    for ele in itertools.combinations(arr,whites):
        color_count = [0]*n
        case2 = []
        white_case = []
        for x in ele:
            color_count[guess[x]]+=1
            white_case.append(vs[x][guess[x]]==False)
        # print(ele,color_count)
        for x in range(n):
            arrx = []
            for i in range(k):
                arrx.append(vs[i][x])
            at_least = sum_atleast(arrx,color_count[x])
            # print(at_least)
            case2.append(at_least)
        white_case=And(white_case)

        arr_red = []
        cases_red = []
        for x in range(k):
            if x not in ele:
                arr_red.append(x)
        for ele_red in itertools.combinations(arr_red,reds):
            case2_red = []
            for x in ele_red:
                case2_red.append(vs[x][guess[x]]==True)
            case2_red = And(case2_red)
            

            no_case = []
            no_where = []
            for x in range(k):
                if x not in ele and x not in ele_red:
                    no_where.append(x)
            for x in no_where:
                no_case.append(vs[x][guess[x]]==False)
            no_case = And(no_case)
            case2_red = And(case2_red,no_case)
            cases_red.append(case2_red)

        cases_red = Or(cases_red)
        # cases.append(And(case2))
        case2 = And(case2)
        case2 = And(case2,white_case)
        case2 = And(case2,cases_red)
        cases.append(case2)

    cases = Or(cases)
    s.add( cases )

    if whites==0 and reds:
        arr = [0]*k
        for i in range(k):
            arr[i]=i
        cases = []
        for ele in itertools.combinations(arr,reds):
            case2 = []
            # print(ele)
            for x in ele:
                # print(x,guess[x])
                case2.append(vs[x][guess[x]]==True)
            case2 = And(case2)
            # cases.append(case2)
            
            no_case = []
            no_where = []
            for x in range(k):
                if x not in ele:
                    no_where.append(x)
            for x in no_where:
                no_case.append(vs[x][guess[x]]==False)
            no_case = And(no_case)
            # print(no_case)
            case2 = And(case2,no_case)
            cases.append(case2)
        cases = Or(cases)
        s.add(cases)

    if reds==0 and whites==0:
            no_case = []
            no_where = []
            for x in range(k):
                no_where.append(x)
            for x in no_where:
                no_case.append(vs[x][guess[x]]==False)
            no_case = And(no_case)
            s.add(no_case)

    s.add( guess_cons )


color_name =  { 0:'R', 1:'G', 2:'B', 3:'Y', 4:'Br', 5:'O', 6:'Bl', 7:'W', }
if n > 8:
    for i in range(8,n):
        color_name[i] = 'C'+str(i)

def print_move( move ):
    for i in range(k):
        c = color_name[move[i]]
        print(c, end=' '),
    print("\n")

        
def get_a_solution():
    sol = [0]*k
    if s.check() == sat:
        m = s.model()
        for i in range(k):
            for j in range(n):
                val = m[vs[i][j]]
                if is_true( val ):
                    sol[i] = j
        return sol
    else:
        print("some thing bad happened! no more moves!\n")
        raise Exception('Failed!')

def get_response():
    red = int(input("Enter red count: "))
    white = int(input("Enter white count: "))
    if white+red > k:
        raise Exception("bad input!")
    return red,white
    
def play_game():
    guess_list_dct = {}
    guess_list = []
    response_list = []
    red = 0
    while red < k:
        if len(guess_list) == 0:
            # TODO: start with random guess
            move = [0]*k
        else:
            move = get_a_solution()
            if move in guess_list:
                print("Random")
                for i in range(k):
                    move[i]=random.randint(0,n-1)
        guess_list.append(move)
        # guess_list_dct[move]=1
        print("found a move:")
        print_move( move )
        red, white = get_response()
        add_a_guess_solution( move, red, white )
    print("Game solved!")
    

play_game()
