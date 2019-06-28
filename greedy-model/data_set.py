import numpy as np
# import pandas as pd
# import os
# import sys
# import time
# import datetime
import random
import math
import pprint

def my_round(val, digit=0):
  p = 10 ** digit
  return int((val * p * 2 + 1) // 2 / p)

"""
here, i define the sets of the datas
"""
TIME = 10
NUMBER_OF_STATIONS = 5
NUMBER_OF_EMPLOYEES = 5
NUMBER_OF_AVAILABLE_VEHICLES_AT_0 = 3


# define a set of the car stations's coods
# S = np.array([(35, 139)] * 10)
S = list(range(1, 6))

# distances = [
#   [70, 51, 25, 68, 74],
#   [19, 80, 87, 43, 68],
#   [11, 30, 52, 15, 86],
#   [7, 42, 29, 89, 45],
#   [57, 20, 41, 26, 41]
# ]

# velocity = 3

T = [
  [27, 5, 10, 11, 5],
  [17, 12, 18, 9, 10],
  [9, 10, 13, 12, 11],
  [7, 13, 7, 21, 9],
  [19, 3, 4, 6, 10]
]

C = [[0 for i in range(5)] for j in range(5)]
for i in range(5):
  for j in range(5):
    C[i][j] = my_round((T[i][j] / 60) * 1173)


# V = [0] * (NUMBER_OF_STATIONS * TIME)

# an arc set of wating activity
A1 = []
# an arc set of moving activity
A2 = []
# an arc set of relocating activity
A3 = []
# a set of employees which is available
E = [0] * NUMBER_OF_EMPLOYEES

demands = np.random.randint(0, 2, (TIME, NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))

pprint.pprint(C)