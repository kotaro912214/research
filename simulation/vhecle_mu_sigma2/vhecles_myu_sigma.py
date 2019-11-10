from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
import csv
import numpy as np
from scipy.stats import multivariate_normal

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


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

rsf_tmp = read_matrix('./vms_rsf.csv')
rsf = []
mu = []
sigma = []
for i in range(len(rsf_tmp)):
    if (i < )
    mu.append(float(rsf_tmp[i][0]))
    sigma.append(float(rsf_tmp[i][1]))
    rsf.append(my_round(float(rsf_tmp[i][2]), 2))
rsf = np.array(rsf)
mu = np.array(mu)
sigma = np.array(sigma)
Mu, Sigma = np.meshgrid(mu, sigma)
print(Mu.shape, Sigma.shape)
rsf = rsf.reshape(Mu.shape)
y = np.random.standard_normal(100)
z = np.random.standard_normal(100)
c = np.random.standard_normal(100)

ax.set_xlabel("mu")
ax.set_ylabel("sigma")
ax.set_zlabel("rsf")

# ax.scatter3D(mu, sigma, rsf)
ax.plot_surface(Mu, Sigma, rsf, "o")

plt.show()


# m = 2
# # dimension
# mean = np.zeros(m)
# sigma = np.eye(m)

# N = 5
# x1 = np.linspace(-5, 5, N)
# x2 = np.linspace(-5, 5, N)

# X1, X2 = np.meshgrid(x1, x2)
# X = np.c_[np.ravel(X1), np.ravel(X2)]
# print(x1.shape, X1.shape)
# Y_plot = multivariate_normal.pdf(x=X, mean=mean, cov=sigma)
# print(Y_plot.shape)
# Y_plot = Y_plot.reshape(X1.shape)
# print(Y_plot.shape)
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# surf = ax.plot_surface(X1, X2, Y_plot, cmap='bwr')
# fig.colorbar(surf)
# ax.set_title("Surface Plot")
# fig.savefig('./test.png')
