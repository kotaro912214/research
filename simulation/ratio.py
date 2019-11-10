import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv

matplotlib.use('Agg')

def my_round(val, digit=0):
    p = 10 ** digit
    if (digit == 0):
        return int((val * p * 2 + 1) // 2 / p)
    else:
        return (val * p * 2 + 1) // 2 / p


def read_matrix(filename):
    matrix = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            matrix.append(row)
        if (len(matrix) == 1):
            return matrix[0]
        else:
            return matrix


ratio_rse = []
station_vhecles = []
for i in range(1, 21):
    station_vhecles = read_matrix('./ratio' + str(i) + '/station_vhecles.csv')
    station_vhecles = list(map(int, station_vhecles))
    ratio_rse.append(my_round(int(read_matrix('./ratio' + str(i) + '/vms_rse.csv')[-2]) / np.sum(station_vhecles), 2))

print(ratio_rse)


# x = np.linspace(0, 50, 51, dtype=int)
# plt.plot(x, rse, color="red", label='rse')
# plt.plot(x, rsf, color="blue", label='rsf')
# plt.legend()
# plt.grid()
# plt.title('a number of srf or rse and vhecles')
# plt.xlim(0, 50)
# plt.ylim(0, max(max(rse), max(rsf)) * 1.1)
# plt.xlabel('a number of vhecles')
# plt.ylabel('a number of rse or rsf')
# plt.savefig('./rsfrse.png')
# plt.clf()
