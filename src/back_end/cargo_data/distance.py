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
    time_matrix = [[[0 for _ in range(T)] for i_cargo in range(N_cargo)] for j_cargo in range(N_cargo)]

    def rush(time):
        '''関数を書く'''
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
                time_matrix[i_cargo][j_cargo][time] = (distance_matrix[i][j] / verocity) + rush(time)*random.random()



    #for i in range(N_cargo):
        #prob = random.random()
        #if prob < 0.2:
            #pass
        #elif prob < 0.4:
            #pass
        #else:
    # [[random.randint(1,10) for i in range(2)]

    # print(coordinate)
    # print(distance_matrix)
    print(numpy.array(distance_matrix))
    print(numpy.array(time_matrix))
    df = pd.DataFrame(numpy.array(distance_matrix))
    print(df)
    # df = pd.read_csv('test_distance.csv', index_col=0)
    return coordinate, arrive_time, distance_matrix, time_matrix
