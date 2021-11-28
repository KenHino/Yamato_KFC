from django.shortcuts import render
from django.http import HttpResponse

import sys
sys.path.append("../../../back_end")
from simulator_cls import simulator
import pickle

def main():

    #coordinate = [(0,0),(1,1),(2,2),(3,3)]
    #distance_matrix = [[0, 1, 2, 3],
    #                   [1, 0, 1, 2],
    #                   [2, 1, 0, 1],
    #                   [3, 2, 1, 0]]
    #time_matrix = [[[0]*20, [1]*20, [4]*20, [9]*20],
    #               [[1]*20, [0]*20, [1]*20, [4]*20],
    #               [[4]*20, [1]*20, [0]*20, [1]*20],
    #               [[9]*20, [4]*20, [1]*20, [0]*20]]
    #
    #arrive_time = [[-1,100], [-1,10], [10,10], [-1,20]]

    with open('../../back_end/cargo_data/coordinate.binaryfile', 'rb') as c:
        coordinate = pickle.load(c)
    with open('../../back_end/cargo_data/distance_matrix.binaryfile', 'rb') as d:
        distance_matrix = pickle.load(d)
    with open('../../back_end/cargo_data/time_matrix.binaryfile', 'rb') as t:
        time_matrix = pickle.load(t)
    with open('../../back_end/cargo_data/arrive_time.binaryfile', 'rb') as a:
        arrive_time = pickle.load(a)



    sim = simulator(coordinate, distance_matrix, time_matrix, arrive_time, max_iter=10**5, alpha=0.5)
    sim.optimize()
    cost, time_list, order = sim.output()
    # print('cost',cost)
    # print('time',time_list)
    # print('order', order)

    return cost, time_list, order, coordinate, arrive_time

def index(request):
    context = {}
    cost, time_list, order, coordinate, arrive_time = main()
    context["cost"] = cost
    context["time_list"] = time_list
    context["order"] = order
    context["coordinate"] = coordinate
    context["arrive_time"] = arrive_time
    # if request.method == 'POST':
    #     context["currentTime"] = request.POST["currentTime"]
    #     return render(request, 'yamato/index.html', context)
    return render(request, 'yamato/index.html', context)