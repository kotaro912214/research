import numpy as np
NUMBER_OF_STATIONS = 3
TIME = 30
a = np.zeros((NUMBER_OF_STATIONS, TIME))
print(a)
b = np.arange(TIME)
a = np.insert(a, 0, b)
print(a)
