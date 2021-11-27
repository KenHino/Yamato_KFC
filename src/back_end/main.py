import numpy as np
from simulator_cls import simulator

coordinate = [(0,0),(1,1),(2,2),(3,3)]
distance_matrix = [[0, 1, 2, 3],
                   [1, 0, 1, 2],
                   [2, 1, 0, 1],
                   [3, 2, 1, 0]]
time_matrix = [[[0]*20, [1]*20, [4]*20, [9]*20],
               [[1]*20, [0]*20, [1]*20, [4]*20],
               [[4]*20, [1]*20, [0]*20, [1]*20],
               [[9]*20, [4]*20, [1]*20, [0]*20]]

arrive_time = [[-1,100], [-1,10], [-1,10], [-1,20]]


sim = simulator(coordinate, distance_matrix, time_matrix, arrive_time, max_iter=20)
sim.optimize()
print(sim.output())
