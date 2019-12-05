import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv

matplotlib.use('Agg')

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


rse_tmp = read_matrix('./100_rse.csv')
rse = [None] * len(rse_tmp)
for i in range(len(rse)):
    rse[i] = rse_tmp[i][-1]
rse = [175] + rse
rse = np.array(rse).astype(int)

rsf_tmp = read_matrix('./100_rsf.csv')
rsf = [None] * len(rsf_tmp)
for i in range(len(rsf)):
    rsf[i] = rsf_tmp[i][-1]
rsf = [0] + rsf
rsf = np.array(rsf).astype(int)

x = np.linspace(0, 100, 101, dtype=int)
plt.plot(x, rse, color="red", label='rse')
plt.plot(x, rsf, color="blue", label='rsf')
plt.legend()
plt.grid()
plt.title('a number of srf or rse and vhecles')
plt.xlim(0, 100)
plt.ylim(0, max(max(rse), max(rsf)) * 1.1)
plt.xlabel('a number of vhecles')
plt.ylabel('a number of rse or rsf')
plt.savefig('./rsfrse.png')
plt.clf()
