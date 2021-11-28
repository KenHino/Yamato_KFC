import numpy as np
# import scipy
import math
import itertools
# import matplotlib.pyplot as plt
import random
from copy import deepcopy


class simulator:

    def __init__(self, coordinate, distance_matrix, time_matrix, arrive_time, 
            initial_guess='random', now_time=0, max_iter=1000, alpha=0.5):
        self.coordinate = coordinate
        self.distance_matrix = distance_matrix
        self.time_matrix = time_matrix
        self.arrive_time = arrive_time

        self.now_time = now_time
        self.time = now_time
        self.max_iter = max_iter
        self.N_iter = 0
        self.alpha = alpha # 0 < alpha <1
        self.infty = pow(10,15)
        self.N_cargo = len(coordinate)

        if initial_guess == 'random':
            self.order = [0] + random.sample([k for k in range(1, self.N_cargo)], self.N_cargo-1) + [0]

        else:
            self.order = [0] + [k for k in range(self.N_cargo)] + [0]

        self.cost_total, time_list = self.cost_function_total()
        self.time = now_time

    def cost_function_2opt(self, i_cargo, j_cargo, time_update=True):
        
        weight = [0.5, 0.5]
        #weight = [1,0]

        #print(self.time)
        if self.arrive_time[j_cargo][0] <=\
                self.time + self.time_matrix[i_cargo][j_cargo][self.time] \
                <= self.arrive_time[j_cargo][1]:
            dum = weight[0] * self.distance_matrix[i_cargo][j_cargo]\
                    + weight[1] * self.time_matrix[i_cargo][j_cargo][self.time]
            if time_update:
                self.time += self.time_matrix[i_cargo][j_cargo][self.time]
        elif self.time + self.time_matrix[i_cargo][j_cargo][self.time] < self.arrive_time[j_cargo][0]:
            dum = weight[0] * self.distance_matrix[i_cargo][j_cargo]\
                    + weight[1] * (self.arrive_time[j_cargo][0] - self.time)
            if time_update:
                self.time = self.arrive_time[j_cargo][0]
        else:
            dum = self.infty
            if time_update:
                self.time += self.time_matrix[i_cargo][j_cargo][self.time]

        return dum, deepcopy(self.time)

    def cost_function_total(self):
        self.time = deepcopy(self.now_time)
        dum = 0
        time_list = [0]
        for cargo_index in range(self.N_cargo):
            i_cargo, j_cargo = self.order[cargo_index:cargo_index+2]
            cost_ij, time_ij = self.cost_function_2opt(i_cargo, j_cargo)
            dum += cost_ij
            time_list.append(time_ij)

        return dum, time_list
    
    def Temperature(self):
        return pow(self.alpha, self.N_iter/self.max_iter)

    def is_swap(self, i_cargo, j_cargo, k_cargo, l_cargo):
        ''' 
        before i->j->k->l
        after  i->k->j->l
        '''

        time_i = deepcopy(self.time)
        cost_ij, time_ij = self.cost_function_2opt(i_cargo, j_cargo)
        cost_jk, time_jk = self.cost_function_2opt(j_cargo, k_cargo)
        cost_kl, time_kl = self.cost_function_2opt(k_cargo, l_cargo)
        cost_before = cost_ij + cost_jk + cost_kl

        self.time = time_i
        cost_ik, time_ik = self.cost_function_2opt(i_cargo, k_cargo)
        cost_kj, time_kj = self.cost_function_2opt(k_cargo, j_cargo)
        cost_jl, time_jl = self.cost_function_2opt(j_cargo, l_cargo)
        cost_after = cost_ik + cost_kj + cost_jl

        #print(i_cargo,j_cargo,k_cargo,l_cargo,cost_before,cost_after)
        if  cost_before >= cost_after:
            self.time = time_ik
            return True
        else:
            rand = random.random()
            temp = self.Temperature()
            if rand < math.exp((cost_before-cost_after)/temp) or\
                    (cost_before >= self.infty and cost_before//self.infty == cost_after//self.infty):
                self.time = time_ik
                return True
            else:
                self.time = time_ij
                return False

    def optimize(self, from_start=True):
        if from_start:
            cargo_index = 0
        else:
            assert False , 'Not Yet Implemented'

        for N_iter in range(self.max_iter):
            self.N_iter = N_iter
            if cargo_index == 0:
                self.time = deepcopy(self.now_time)

            i_cargo, j_cargo, k_cargo, l_cargo = self.order[cargo_index:cargo_index+4]

            flag = self.is_swap(i_cargo,j_cargo,k_cargo,l_cargo)
            if flag:
                self.order[cargo_index+1:cargo_index+3] = [k_cargo, j_cargo]
            else:
                pass
            if cargo_index + 2 == self.N_cargo-1:
                cargo_index = 0
            else:
                cargo_index += 1
            

    
    def output(self):
        cost, time_list = self.cost_function_total()
        return cost, time_list, self.order
