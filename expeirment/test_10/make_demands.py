import csv
import numpy as np

const_dic = {}
with open('./const.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    const_dic[row[0]] = row[1]

NUMBER_OF_STATIONS = int(const_dic['NUMBER_OF_STATIONS'])
TIME = 100

# define the step time matrix
T_step = np.array(list(range(TIME)))

# define a set of the car stations
S = list(range(NUMBER_OF_STATIONS))

# define the demand matrix by random
Demands = np.random.randint(-90, 2, (TIME - 1, NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))
for t in T_step:
  if (t == TIME - 1):
    break
  for i in S:
    for j in S:
      if (i == j or Demands[t][i][j] < 0):
        Demands[t][i][j] = 0

