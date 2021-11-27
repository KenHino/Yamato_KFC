import numpy as np
import scipy
import math
import itertools
import matplotlib.pyplot as plt
import random
from copy import deepcopy


class simulator:

    def __init__(self, coordinate, distance_matrix, time_matrix, arrive_time, 
            initial_guess='random', now_time=0, max_iter=1000, alpha=0.5):
        self.coordinate = coordinate
        self.distance_matrix = distance_matrix
        self.time_matrix = time_matrix
        self.arrive_time = arrive_time
        self.N_cargo = len(coordinate)

        if initial_guess == 'random':
            self.order = [0] + random.sample([k for k in range(1, self.N_cargo)], self.N_cargo-1) + [0]

        else:
            self.order = [0] + [k for k in range(self.N_cargo)] + [0]

        self.cost_total = self.cost_function_total()
        self.now_time = now_time
        self.max_iter = max_iter
        self.N_iter = 0
        self.alpha = alpha # 0 < alpha <1

    def cost_function_2opt(self, i_cargo, j_cargo):
        
        weight = [0.5,0.5]
        
        if self.arrive_time[j_cargo][0] <= self.now_time + self.time_matrix[i_cargo][j_cargo][self.now_time] <= self.arrive_time[j_cargo][1]:
            dum = weight[0] * self.distance_matrix[i_cargo][j_cargo] + weight[1] * self.time_matrix[i_cargo][j_cargo][self.now_time]
        else:
            dum = float('inf')

        return dum

    def cost_function_total(self):
        
        self.now_time = self.time_matrix[self.order[0]][self.order[1]][0]
        dum = self.cost_function_2opt(self.order[0], self.order[1])
        
        for k in range(self.N_cargo-2):
            i_cargo, j_cargo, k_cargo, l_cargo = self.order[k:k+4]
            dt = self.time_matrix[j_cargo][k_cargo][self.now_time]
            
            dum += self.cost_function_2opt(j_cargo, k_cargo)
            self.now_time += dt

        dum += self.cost_function_2opt(self.order[-2], self.order[-1])
        
        return dum
    
    def Temperature(self):
        return pow(self.alpha, self.N_iter/self.max_iter)

    def is_swap(self, i_cargo, j_cargo, k_cargo, l_cargo):
        ''' 
        before i->j->k->l
        after  i->k->j->l
        '''

        cost_before = self.cost_function_2opt(i_cargo, j_cargo)\
                    + self.cost_function_2opt(j_cargo, k_cargo)\
                    + self.cost_function_2opt(k_cargo, l_cargo)
        cost_after  = self.cost_function_2opt(i_cargo, k_cargo)\
                    + self.cost_function_2opt(k_cargo, j_cargo)\
                    + self.cost_function_2opt(j_cargo, l_cargo)

        if cost_before > cost_after:
            return True
        else:
            rand = random.random()
            temp = self.Temperature()
            if rand < math.exp((cost_before-cost_after)/temp):
                return True
            else:
                return False

    def optimize(self, from_start=True):
        if from_start:
            cargo_index = 0
        else:
            assert False , 'Not Yet Implemented'

        for N_iter in range(self.max_iter):
            self.N_iter = N_iter

            if cargo_index == 1:
                self.now_time = 0

            i_cargo, j_cargo, k_cargo, l_cargo = self.order[cargo_index:cargo_index+4]

            if self.is_swap(i_cargo,j_cargo,k_cargo,l_cargo):
                self.now_time += self.time_matrix[k_cargo][j_cargo][self.now_time]
                self.order[cargo_index+1:cargo_index+3] = [k_cargo, j_cargo]
            else:
                self.now_time += self.time_matrix[j_cargo][k_cargo][self.now_time]

            if cargo_index + 2 + 1== self.N_cargo-1:
                cargo_index = 0
            else:
                cargo_index += 1

    
    def output(self):
        return [self.cost_function_total, self.order]












