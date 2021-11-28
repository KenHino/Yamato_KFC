import numpy as np
from numpy import core
import numpy
import pandas as pd
import random
from scipy.spatial import distance

N_cargo = 10

MORNING = 180 # 朝9時から12時までの180分
AFTERNOON = 480 # 12時から20時までの480分

coordinate = [[random.randint(1,10) for i in range(2)] for j in range(N_cargo)]
coordinate.insert(0,[0,0]) # 原点の追加

distance_matrix = []

for i in range(len(coordinate)-1):
    distance_array = []
    distance_matrix.append(distance_array)
    for j in range(len(coordinate)-1):
        # 距離 + なにかにする
        a = int(distance.euclidean(coordinate[i], coordinate[j]))
        if not i == j and random.random() < 0.9 :
            a += abs(int(np.random.normal(loc = 5, scale = 0)))
        distance_array.append(a)

time_matrix = []

for i in range(len(coordinate)-1):
    time_array = []
    time_matrix.append(time_array)
    for j in range(len(coordinate)-1):
        time_array.append(distance_matrix[i][j]* 10)

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