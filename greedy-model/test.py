import pprint
import random
import numpy as np
NUMBER_OF_STATIONS = 5
TIME = 60 * 3
demands = np.random.randint(0, 2, (TIME, NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))