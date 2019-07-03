import numpy as np

TIME = 3 * 180
NUMBER_OF_EMPLOYEES = 4
NUMBER_OF_STATIONS = 5
NUMBER_OF_AVAILABLE_VEHICLES_AT_0 = 3

S = list(range(NUMBER_OF_STATIONS))
T_step = np.array(list(range(TIME)))
Demands = np.random.randint(0, 2, (TIME - 1, NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))
for t in T_step:
  if (t == TIME - 1):
    break
  for i in S:
    for j in S:
      if (i == j):
        Demands[t][i][j] = 0

print(Demands)