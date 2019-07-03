import numpy as np
import random
import math
import pprint
import pulp
import time
# import pandas as pd
# import os
# import sys
# import datetime

"""
here, i define the sets of the datas
"""

def my_round(val, digit=0):
  p = 10 ** digit
  return int((val * p * 2 + 1) // 2 / p)

#     data definition     #########################################################################

# define the main constant variables
NUMBER_OF_EMPLOYEES = 4
NUMBER_OF_STATIONS = 5
TIME = 3 * 60
NUMBER_OF_AVAILABLE_VEHICLES_AT_0 = 3
# cost of rejecting a client demand for returning a car into a station
C_IN = 100
# cost of rejecting a client demand for taking a car from a station
C_OUT = 250
# cost of using one one staff during the day
C_E = 10000 * (TIME / (8*60))

# define a set of the car stations
S = list(range(NUMBER_OF_STATIONS))

# define the step time matrix
T_step = np.array(list(range(TIME)))
# define the time which transportation between station i to j will take
T_trans = [
  [0, 5, 10, 7, 5],
  [5, 0, 18, 13, 10],
  [10, 18, 0, 19, 4],
  [7, 13, 19, 0, 21],
  [5, 10, 4, 21, 0]
]

# define the Employees
E = list(range(NUMBER_OF_EMPLOYEES))

# prams for the cost function by using the car
price_per_L = 136.3
distance_per_L = 35000
price_per_distance = price_per_L / distance_per_L
# v[m/min]
v_mean = 25000 / 60
price_per_min = price_per_distance * v_mean

# define the cost while transport from station i to station j
C = [[0 for i in range(NUMBER_OF_STATIONS)] for j in range(NUMBER_OF_STATIONS)]
for i in range(NUMBER_OF_STATIONS):
  for j in range(NUMBER_OF_STATIONS):
    C[i][j] = my_round(T_trans[i][j] * price_per_min)

# make the S x T nodes matrix a row vector
SxT = [[(i, t) for t in T_step] for i in S]
V = [(i, t) for i in S for t in range(TIME)]

# A1, waiting activity arcs sets
A1 = [(V[i], V[i + 1]) for i in range(len(V) - 1)]

# A2, moving activity arcs sets
A2 = []
for i in range(NUMBER_OF_STATIONS):
  for j in range(i + 1, NUMBER_OF_STATIONS):
    for t in T_step:
      if (i != j and t + T_trans[i][j] < TIME):
        A2.append((SxT[i][t], SxT[j][t + T_trans[i][j]]))

# A3, relocation activity arcs sets
A3 = []
for i in range(NUMBER_OF_STATIONS):
  for j in range(i + 1, NUMBER_OF_STATIONS):
    for t in T_step:
      if (i != j and t + T_trans[i][j] < TIME):
        A3.append((SxT[i][t], SxT[j][t + T_trans[i][j]]))

# define the demand matrix by random
Demands = np.random.randint(0, 2, (TIME, NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))
for t in T_step:
  if (t == TIME - 1):
    break
  for i in S:
    for j in S:
      if (i == j):
        Demands[t][i][j] = 0

# number of available cars at station i at time step t
AVit = np.zeros([NUMBER_OF_STATIONS, TIME])
# initialize it at time step 0
AVit[:][0] = NUMBER_OF_AVAILABLE_VEHICLES_AT_0

# number of parking slots in each station i
P = np.array([5] * NUMBER_OF_STATIONS)

##################################################################################################




#   define the problem   #########################################################################

problem = pulp.LpProblem("Relocation Problem", pulp.LpMinimize)

# Define the 6 type of decision variables ###########################

# a set of employees which is available
U = {}
for e in E:
  U[e] = pulp.LpVariable("U" + str(e), 0, 1, pulp.LpInteger)

# an arc set of wating activity
# Wait = np.random.randint(0, 2, (TIME - 1, NUMBER_OF_STATIONS, NUMBER_OF_EMPLOYEES))
Wait = {}
for e in E:
  for a1 in A1:
    # wait_e_i_t
    Wait[e, a1] = pulp.LpVariable("wait_" + str(e) + '_' + str(a1[0]) + '_' + str(a1[1]), 0, 1, pulp.LpInteger)
# print(Wait)

# an arc set of moving activity
Move = {}
for e in E:
  for a2 in A2:
    Move[e, a2] = pulp.LpVariable("move_" + str(e) + '_' + str(a2[0]) + '_' + str(a2[1]), 0, 1, pulp.LpInteger)

# an arc set of relocating activity
Rel = {}
for e in E:
  for a3 in A3:
    Rel[e, a3] = pulp.LpVariable("move_" + str(e) + '_' + str(a3[0]) + '_' + str(a3[1]), 0, 1, pulp.LpInteger)

# the num of rejected demand to take a car out of a station i at time step t
OutR_it = {}
for i in S:
  for t in T_step:
    OutR_it[i, t] = pulp.LpVariable("outR_" + str(i) + '_' + str(t), 0, 1, pulp.LpInteger)

# the num of rejected demand to return a car into a station i at time step t
InR_it = {}
for i in S:
  for t in T_step:
    InR_it[i, t] = pulp.LpVariable("inR_" + str(i) + '_' + str(t), 0, 1, pulp.LpInteger)

#####################################################################




# define the objective function  ####################################

first_item = pulp.lpSum(C[a2[0][0]][a2[1][0]] * Move[e, a2] for e in E for a2 in A2) + pulp.lpSum(C[a3[0][0]][a3[1][0]] * Rel[e, a3] for e in E for a3 in A3)
second_item = C_OUT * pulp.lpSum(OutR_it[v[0], v[1]] for v in V)
third_item = C_IN * pulp.lpSum(InR_it[v[0], v[1]] for v in V)
fourth_item = C_E * pulp.lpSum(U[e] for e in E)
problem += first_item + second_item + third_item + fourth_item, "total value"

#####################################################################





# define the constraints ############################################

A2_const1 = []
for a2 in A2:
  if (a2[0][1] == 1):
    A2_const1.append(a2)

A3_const1 = []
for a3 in A3:
  if (a3[0][1] == 1):
    A3_const1.append(a3)

# defin constraints 1
for e in E:
  first_item = pulp.lpSum(Wait[e, ((a1[0][0], 1), (a1[0][0], 2))] for a1 in A1)
  second_item = pulp.lpSum(Move[e, a2_const] for a2_const in A2_const1)
  third_item = pulp.lpSum(Rel[e, a3_const] for a3_const in A3_const1)
  problem += first_item + second_item + third_item == U[e], "constraints-1-" + str(e + 1)

# define constraints 2
for e in E:
  for it in V:
    if (it[1] != 0):
      first_item = Wait[e, (it[0], it[1] - 1), (it[0], )]





# def main():
#   solver = pulp.solvers.CPLEX_CMD()
#   result_status = problem.solve(solver)
#   # print('結果: ', pulp.LpStatus[result_status])
#   # print('目的関数値: ', pulp.value(problem.objective))


if __name__ == '__main__':
  start = time.time()

  # write some processing codes here
  # main()

  elapsed_time = time.time() - start
  print('実行時間: ', elapsed_time)