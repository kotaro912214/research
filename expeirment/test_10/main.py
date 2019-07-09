# coding: UTF-8

import numpy as np
import random
import math
import time
import datetime
import csv
np.set_printoptions(threshold=1000000)

# for this version there is no round method, so i define the method by myself
def my_round(val, digit=0):
  p = 10 ** digit
  return int((val * p * 2 + 1) // 2 / p)


#     data definition     #########################################################################

const_dic = {}
with open('C:/Users/kotaro/OneDrive/デスクトップ/research/expeirment/test_10/const.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    const_dic[row[0]] = row[1]

NUMBER_OF_STATIONS = int(const_dic['NUMBER_OF_STATIONS'])
FUEL_CONSUMPTION = int(const_dic['FUEL_CONSUMPTION'])

# define the main constant variables
NUMBER_OF_EMPLOYEES = 4
TIME = 60 * 8
AVAILABLE_VEHICLES_AT_0 = 3
NUMBER_OF_PARKING_SLOTS = 5

# cost of rejecting a client demand for returning a car into a station
C_IN = 100
# cost of rejecting a client demand for taking a car from a station
C_OUT = 205
# cost of using one one staff during the day
C_E = 10000 * (TIME / (8*60))
# price to use the car for customer
PRICE_PER_15 = 205

S_coord = []
with open('C:/Users/kotaro/OneDrive/デスクトップ/research/expeirment/test_10/s_coord.csv', 'r') as f:
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
price_per_meter = price_per_L / distance_per_L
# v[m/min]
v_mean = 30000 / 60
price_per_min = price_per_meter * v_mean

# define the distance matrix between station i and j
Distance = []
with open('C:/Users/kotaro/OneDrive/デスクトップ/research/expeirment/test_10/distance.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    row = list(map(float, row))
    Distance.append(row)

# define the time which is taken to move between station i and j matrix
T_trans = []
with open('C:/Users/kotaro/OneDrive/デスクトップ/research/expeirment/test_10/t_trans.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    row = list(map(int, list(map(float, row))))
    T_trans.append(row)

# define the cost while transport from station i to station j
C = [[0 for i in range(NUMBER_OF_STATIONS)] for j in range(NUMBER_OF_STATIONS)]
for i in range(NUMBER_OF_STATIONS - 1):
  for j in range(i + 1, NUMBER_OF_STATIONS):
    C[i][j] = my_round(T_trans[i][j] * price_per_min)
    C[j][i] = C[i][j]

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

# define the matrix how many cars each station can hold
P = np.array([0] * NUMBER_OF_STATIONS)

# initialize it at time step 0
with open('C:/Users/kotaro/OneDrive/デスクトップ/research/expeirment/test_10/slots.csv', 'r') as f:
  reader = csv.reader(f)
  i = 0
  for row in reader:
    slot = int(row[-1])
    Av[i][0] = slot - 1
    P[i] = slot
    i += 1


##################################################################################################


def main():
  rde = 0
  rdf = 0
  cost = 0
  success = 0
  time_over = 0
  for t in T_step:
    if (t != 0):
      for i in S:
        Av[i][t] += Av[i][t - 1]
    if (t != TIME - 1):      
      for i in S:
        for j in S:
          if (i != j and Demands[t][i][j]):
            if (t + T_trans[i][j] >= TIME):
              time_over += 1
            else:
              if (Av[i][t] == 0):
                rde += 1
              elif (sum(Av[j][t:t + T_trans[i][j] + 1]) == P[j]):
                rdf += 1
              else:
                Av[j][t + T_trans[i][j]] += 1
                Av[i][t] -= 1
                cost += C[i][j]
                if (T_trans[i][j] % 15 == 0):
                  cost -= PRICE_PER_15 * T_trans[i][j] / 15
                else:
                  cost -= PRICE_PER_15 + PRICE_PER_15 * (T_trans[i][j] // 15)
                success += 1
  cost += C_IN * rdf + C_OUT * rde
  path = 'C:/Users/kotaro/OneDrive/デスクトップ/research/expeirment/test_10/result_non_jocky.csv'
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