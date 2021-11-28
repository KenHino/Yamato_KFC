import numpy as np
import random
from scipy.spatial import distance
import pandas as pd


def cargo_data(N_cargo=20,T_end=100):
    AM = [-1, T_end//2] # 朝9時から12時までの180分
    PM = [T_end//2,T_end] # 12時から20時までの480分
    ALL = [-1, T_end]
    verocity = 10 / T_end * 7 # 10 km / h

    coordinate = [(0,0)] + [tuple(random.randint(-10,10) for i in range(2)) for j in range(N_cargo-1)] # (21 km, 21 km)
    arrive_time = [ALL] + [AM]*(N_cargo//4) + [PM]*(N_cargo//4) + [ALL]*(N_cargo - 1 - N_cargo//4 - N_cargo//4)
    distance_matrix = [[ 0 for _ in range(N_cargo) for _ in range(N_cargo)]]
    time_matrix = [[[0 for _ in range(T_end)] for i_cargo in range(N_cargo)] for j_cargo in range(N_cargo)]

    def rush(time,x,y):
        '''関数を書く 特定の場所のみなど'''
        AREA_1 = 5 # random.randint(-10,10)
        AREA_2 = 5 # random.randint(-10,10)
        rush_time = T_end - 20
        if time < rush_time and AREA_1 < x and AREA_1 < y:
            dum = time + random.randint(1,10)
        elif time < rush_time and x < AREA_2 and AREA_1 < y:
            dum = time - random.randint(1,10)
        elif time < rush_time and x < AREA_2 and y < AREA_2:
            dum = time + random.randint(1,10)
        elif time < rush_time and AREA_1 < x and y < AREA_2:
            dum = time - random.randint(1,10)
        else:
            dum = time
        return dum


    for i_cargo in range(N_cargo):
        for j_cargo in range(N_cargo):
            if i_cargo == j_cargo:
                continue
            # 距離 + なにかにする
            d = int(distance.euclidean(coordinate[i_cargo], coordinate[j_cargo]))
            d += abs(int(np.random.normal(loc = 5, scale = 0)))
            distance_matrix[i_cargo][j_cargo] = d
            for time in range(T_end):
                time_matrix[i_cargo][j_cargo][time] = (distance_matrix[i_cargo][j_cargo] / verocity) + rush(time,coordinate[i_cargo],coordinate[j_cargo])*random.random()

    # df = pd.DataFrame(np.array(distance_matrix))
    # df = pd.read_csv('test_distance.csv', index_col=0)
    return coordinate, arrive_time, distance_matrix, time_matrix

cargo_data()