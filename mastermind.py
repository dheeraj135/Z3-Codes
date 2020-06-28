#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import logging
colors = ['white','blue','red','green','yellow','pink','lightblue','maroon']
## ans = [red,blue,lb,maroon]

logger = logging.getLogger(__name__)

def sum_to_one(ls):
    return PbEq([(x,1) for x in ls], 1)

def sum_to_x(ls, sumx):
    return PbEq([(x,1) for x in ls], sumx)

def sum_atleast(ls, sumx):
    return PbGe([(x,1) for x in ls], sumx)

class mastermind:
    def __init__(self,num_positions=4,play_online=0):
        self.num_colors = len(colors)
        self.num_positions = num_positions

        self.base_matrix = [  [Bool ("e_{}_{}".format(i,j))  for j in range(self.num_colors)] for i in range(self.num_positions)]

        self.z3_solver = Solver()

        self.ans = [0]*self.num_positions

        self.finl_ans = []
        self.do_testing = 0
        self.base_conditions = [sum_to_one(x) for x in self.base_matrix]
        self.z3_solver.add(And(self.base_conditions))

        self.play_online = play_online

        if play_online:
            logger.debug("Setting up selenium")
            self.play_url = 'http://master-mind-17.herokuapp.com/'
            options = Options()
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')
            # options.add_argument("--no-sandbox")
            # options.add_argument("--disable-dev-shm-usage")
            self.browser=webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=options)
            self.start_online_game()

    def select_online_color(self,color):
        self.browser.find_elements_by_xpath(f"//*[local-name() = 'svg'][@color='{color}']")[-1].find_element_by_tag_name('circle').click()
        logger.info(f'Clicked {color} circle.')
    
    def perform_online_move(self,move,move_number):
        table = self.browser.find_element_by_xpath(f"//table/tbody/tr[{move_number}]")
        # time.sleep(2)
        for i in range(4):
            self.select_online_color(colors[move[i]])
            svg_element = table.find_elements_by_tag_name('svg')[i].find_element_by_tag_name('circle')
            actions = ActionChains(self.browser)
            actions.move_to_element(svg_element)
            actions.click(svg_element)
            actions.perform()
            # svg_element.find_element_by_tag_name('circle').click()
        self.check_button.click()
        rw = table.find_elements_by_tag_name('td')
        print("Hello")
        try:
            data = self.browser.find_element_by_class_name('modal-title').text
            print(data)
            return 4,0
        except:
            print('Game still going on.')
        return int(rw[2].text),int(rw[3].text)

    def start_online_game(self):
        self.browser.get(self.play_url)
        buttons = self.browser.find_elements_by_tag_name('button')
        start_button = buttons[1]
        self.check_button = buttons[2]
        logger.info(f'Clicking Start Button!.')
        start_button.click()
        logger.info(f'Clicked Start Button!.')

    def check_move(self, move ):    
        red =0
        white =0 
        colors_move = [0]*self.num_colors
        colors_ans = [0]*self.num_colors
        for i in range(self.num_positions):
            if(self.ans[i]==move[i]):
                red+=1
            else:
                colors_ans[self.ans[i]]+=1
                colors_move[move[i]]+=1
        for i in range(self.num_colors):
            white+=min(colors_ans[i],colors_move[i])
        return red,white

    def get_nope_condition(self,move, arr):
        conds = []
        for i in arr:
            conds.append(self.base_matrix[i][move[i]]==False)
        return And(conds)

    def get_all_zeros(self,move,arr):
        conds = []
        colors = {move[i] for i in arr}

        for color in colors:
            for i in arr:
                conds.append(self.base_matrix[i][color]==False)
        return And(conds)

    def get_white_condition(self,move, arr, white):
        base_cond = self.get_nope_condition(move,arr)
        conds = []
        for whites in itertools.combinations(arr,white):
            colors = [move[white] for white in whites]
            color_dict = {}
            for color in colors:
                color_dict[color] = color_dict.get(color,0)+1
            temp_conds = []
            for color in range(self.num_colors):
                temp_arr = [self.base_matrix[i][color] for i in arr]
                temp_conds.append(sum_atleast(temp_arr,color_dict.get(color,0)))
            conds.append(And(temp_conds))
        return And(sum_atleast(conds,1),base_cond)

    def get_all_conditions(self,move, red, white, num_pos):
        arr = [i for i in range(num_pos)]
        if red:
            conds = []
            for reds in itertools.combinations(arr,red):
                arr2 = arr[:]
                for red in reds:
                    arr2.remove(red)
                if white:
                    white_conds = self.get_white_condition(move,arr2,white)
                else:
                    white_conds = self.get_all_zeros(move,arr2)
                temp_conds = []
                for i in reds:
                    temp_conds.append(self.base_matrix[i][move[i]]==True)
                temp_conds = And(temp_conds)
                temp_conds = And(temp_conds,white_conds)
                conds.append(temp_conds)
            return sum_to_one(conds)
        elif white:
            return self.get_white_condition(move,arr,white)
        else:
            return self.get_all_zeros(move,arr)

    def add_a_guess_solution(self,move,red,white):
        self.z3_solver.add(self.get_all_conditions(move,red,white,self.num_positions))

    def get_a_solution(self):
        sol = [0]*self.num_positions
        # print(z3_solver)
        if self.z3_solver.check() == sat:
            m = self.z3_solver.model()
            for i in range(self.num_positions):
                for j in range(self.num_colors):
                    val = m[self.base_matrix[i][j]]
                    # print(f'{val}',end=' ')
                    if is_true( val ):
                        sol[i] = j
                # print('')
            return sol
        else:
            # print(z3_solver)
            print(self.z3_solver.unsat_core())
            print("some thing bad happened! no more moves!\n")
            raise Exception('Failed!')

    def get_response(self):
        red = int(input("Enter red count: "))
        white = int(input("Enter white count: "))
        if white+red > self.num_positions:
            raise Exception("bad input!")
        return red,white

    def print_move( self,move ):
        for i in range(self.num_positions):
            c = colors[move[i]]
            print(c, end=' '),
        print("\n")

    def play_game(self):
        red = 0
        num_moves = 0

        while red < self.num_positions:
            num_moves+=1

            move = self.get_a_solution()

            print("found a move:")
            self.print_move( move )

            if self.play_online:
                print(move)
                red,white = self.perform_online_move(move,num_moves)
            elif not self.do_testing:
                red, white = self.get_response()
            else:
                red,white = self.check_move(move)
            print(red,white)
            self.add_a_guess_solution( move, red, white )

        print("Game solved!")
        print("Num Moves: ",num_moves)
        return num_moves

    def play_test(self,ans):
        self.ans = ans
        self.do_testing = 1
        moves = self.play_game()
        self.do_testing = 0
        return moves

def perform_test():
    ans = [0]*num_positions

    for x in range(num_positions):
        ans[x]=random.randint(0,num_colors-1)
    print(ans)
    master = mastermind(num_positions=num_positions)
    return master.play_test(ans=ans)

if __name__=='__main__':
    do_testing = 0
    play_online = 1
    test_cases = 1000
    num_positions = 4
    num_colors = len(colors)
    finl_ans = []
    if do_testing:
        for i in range(test_cases):
            finl_ans.append(perform_test())
        print(finl_ans)
        s = sum(finl_ans)
        print(s)
        print(f'Max: {max(finl_ans)}')
        print("Average steps: ",s/test_cases)
    else:
        master = mastermind(play_online=play_online,num_positions=num_positions)
        master.play_game()
