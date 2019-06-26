import numpy as np
import pandas as pd
import os
import sys
import time
import datetime
"""
here, i define the sets of the datas
"""
TIME = 10
NUMBER_OF_STATIONS = 10
NUMBER_OF_EMPLOYEES = 5
NUMBER_OF_AVAILABLE_VEHICLES_AT_0 = 3


# define a set of the car stations's coods
S = np.array([(35, 139), (35, 139), (35, 139), (35, 139), (35, 139)])
V = np.zeros(NUMBER_OF_STATIONS * TIME)

# an arc set of wating activity
A1 = []
# an arc set of moving activity
A2 = []
# an arc set of relocating activity
A3 = []
# a set of employees which is available
E = [0] * NUMBER_OF_EMPLOYEES

