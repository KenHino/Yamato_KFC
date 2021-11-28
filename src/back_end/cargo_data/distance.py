import numpy as np
import random
from scipy.spatial import distance
from math import pi, atan2
import pickle

def circles_intersection_area(P1, r1, P2, r2):
    x1, y1 = P1; x2, y2 = P2

    dd = (x1 - x2)**2 + (y1 - y2)**2

    if (r1 + r2)**2 <= dd:
        return 0.0

    if dd <= (r1 - r2)**2:
        return pi*min(r1, r2)**2

    p1 = (r1**2 - r2**2 + dd)
    p2 = (r2**2 - r1**2 + dd)

    S1 = r1**2 * atan2((4*dd*r1**2 - p1**2)**.5, p1)
    S2 = r2**2 * atan2((4*dd*r2**2 - p2**2)**.5, p2)
    S0 = (4*dd*r1**2 - p1**2)**.5 / 2

    return S1 + S2 - S0



def cargo_data(N_cargo=20,T_end=100):
    AM = [-1, T_end//2] # 朝9時から12時までの180分
    PM = [T_end//2,T_end] # 12時から20時までの480分
    ALL = [-1, T_end]
    verocity = 10 / T_end * 7 # 10 km / h

    coordinate = [(0,0)] + [tuple(random.randint(-10,10) for i in range(2)) for j in range(N_cargo-1)] # (21 km, 21 km)
    arrive_time = [ALL] + [AM]*(N_cargo//4) + [PM]*(N_cargo//4) + [ALL]*(N_cargo - 1 - N_cargo//4 - N_cargo//4)
    distance_matrix = [[ 0 for _ in range(N_cargo)] for _ in range(N_cargo)]
    time_matrix = [[[0 for _ in range(T_end)] for i_cargo in range(N_cargo)] for j_cargo in range(N_cargo)]

    def rush(time,coord_1,coord_2):
        '''関数を書く 特定の場所のみなど'''
        rushtime_1 = [0,T_end//5]
        rushtime_2 = [T_end//5*4, T_end]


        if rushtime_1[0] <= time <=rushtime_1[1] or rushtime_2[0] <= time <= rushtime_2[1]:
            coef = 0.5
            P1 = [(coord_1[0] + coord_2[0])/2, (coord_1[1] + coord_2[1])/2]
            r1 = distance.euclidean(coord_1, coord_2)/2
            P2 = [0,0]
            r2 = 5
            additional_time = circles_intersection_area(P1, r1, P2, r2)*coef
        else:
            additional_time = 0

        return additional_time


    max_time = 0
    for i_cargo in range(N_cargo):
        for j_cargo in range(N_cargo):
            if i_cargo == j_cargo:
                continue
            # 距離 + なにかにする
            d = (distance.euclidean(coordinate[i_cargo], coordinate[j_cargo]))
            d += abs((np.random.normal(loc = 5, scale = 0)))
            distance_matrix[i_cargo][j_cargo] = d
            for time in range(T_end):
                time_matrix[i_cargo][j_cargo][time] = int((distance_matrix[i_cargo][j_cargo] / verocity)\
                        + rush(time,coordinate[i_cargo],coordinate[j_cargo]))//7
                max_time = max(max_time, time_matrix[i_cargo][j_cargo][time])

    max_time *= N_cargo
    zeros = [0 for _  in range(T_end, max_time)]
    for i_cargo in range(N_cargo):
        for j_cargo in range(N_cargo):
            time_matrix[i_cargo][j_cargo] += zeros
    # df = pd.DataFrame(np.array(distance_matrix))
    # df = pd.read_csv('test_distance.csv', index_col=0)
    return coordinate, arrive_time, distance_matrix, time_matrix

if __name__ == '__main__':
    coordinate, arrive_time, distance_matrix, time_matrix = cargo_data(N_cargo=20)
    #print(coordinate)
    #print(arrive_time)
    #print(distance_matrix)
    print(time_matrix)
    with open('coordinate.binaryfile', 'wb') as c:
        pickle.dump(coordinate, c)
    with open('arrive_time.binaryfile', 'wb') as a:
        pickle.dump(arrive_time, a)
    with open('distance_matrix.binaryfile', 'wb') as d:
        pickle.dump(distance_matrix, d)
    with open('time_matrix.binaryfile', 'wb') as t:
        pickle.dump(time_matrix, t)
