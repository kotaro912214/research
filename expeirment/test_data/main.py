# coding: UTF-8

import numpy as np
import random
import math
import pprint
import pulp
import time
import datetime
import csv


# for this version there is no round method, so i define the method by myself
def my_round(val, digit=0):
  p = 10 ** digit
  return int((val * p * 2 + 1) // 2 / p)


#     data definition     #########################################################################

const_dic = {}
with open('./const.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    const_dic[row[0]] = row[1]
NUMBER_OF_STATIONS = int(const_dic['NUMBER_OF_STATIONS'])
FUEL_CONSUMPTION = int(const_dic['FUEL_CONSUMPTION'])

# define the main constant variables
NUMBER_OF_EMPLOYEES = 4
TIME = 8 * 60
AVAILABLE_VEHICLES_AT_0 = 3
NUMBER_OF_PARKING_SLOTS = 5

# cost of rejecting a client demand for returning a car into a station
C_IN = 100
# cost of rejecting a client demand for taking a car from a station
C_OUT = 250
# cost of using one one staff during the day
C_E = 10000 * (TIME / (8*60))

S_coord = []
with open('./s_coord.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    S_coord.append((row[0], row[1]))

# define a set of the car stations
S = list(range(NUMBER_OF_STATIONS))


# define the step time matrix
T_step = np.array(list(range(TIME)))


# define the Employees
E = list(range(NUMBER_OF_EMPLOYEES))

# prams for the cost function by using the car
price_per_L = 136.3
distance_per_L = 35000
price_per_distance = price_per_L / distance_per_L
# v[m/min]
v_mean = 25000 / 60
price_per_min = price_per_distance * v_mean

Distance = []
with open('./distance.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    row = list(map(float, row))
    Distance.append(row)

T_trans = []
with open('./t_trans.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    row = list(map(int, list(map(float, row))))
    T_trans.append(row)

# define the cost while transport from station i to station j
C = [[0 for i in range(NUMBER_OF_STATIONS)] for j in range(NUMBER_OF_STATIONS)]
for i in range(NUMBER_OF_STATIONS):
  for j in range(NUMBER_OF_STATIONS):
    C[i][j] = my_round(Distance[i][j] * price_per_min)

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
Demands = np.random.randint(-90, 2, (TIME - 1, NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))
for t in T_step:
  if (t == TIME - 1):
    break
  for i in S:
    for j in S:
      if (i == j or Demands[t][i][j] < 0):
        Demands[t][i][j] = 0

# number of available cars at station i at time step t
Av = np.zeros([NUMBER_OF_STATIONS, TIME])

with open('./slots.csv', 'r') as f:
  reader = csv.reader(f)
  i = 0
  for row in reader:
    slot = int(row[-1])
    Av[i][0] = slot
    i += 1
print(Av)
# initialize it at time step 0
# for i in S:
#   Av[i][0] = AVAILABLE_VEHICLES_AT_0

# number of parking slots in each station i
P = np.array([NUMBER_OF_PARKING_SLOTS] * NUMBER_OF_STATIONS)

##################################################################################################


def main():
  rde = 0
  rdf = 0
  cost = 0
  success = 0
  time_over = 0
  for t in T_step:
    if (t != TIME - 1):      
      for i in S:
        Av[i][t + 1] += Av[i][t]
      for i in S:
        for j in S:
          if (i != j and Demands[t][i][j]):
            if (t + T_trans[i][j] >= TIME):
              time_over += 1
            else:
              if (Av[i][t] == 0):
                rde += 1
              elif (Av[j][t + T_trans[i][j]] == NUMBER_OF_PARKING_SLOTS - 1):
                rdf += 1
              else:
                Av[j][t + T_trans[i][j]] += 1
                Av[i][t + 1] -= 1
                cost += C[i][j]
                success += 1
  path = './result_non_jocky.csv'
  f = open(path, 'a')
  f.write(str(sum(sum(sum(Demands)))) + ',')
  f.write(str(rdf) + ',')
  f.write(str(rde) + ',')
  f.write(str(success) + ',')
  f.write(str(time_over) + ',')
  f.write(str(cost) + '\n')
  f.close()


if (__name__ == '__main__'):
  start = time.time()

  # write some processing codes here
  main()

  elapsed_time = time.time() - start
  print('実行時間: ', elapsed_time)