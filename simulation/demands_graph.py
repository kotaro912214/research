import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

# demands = np.random.normal(loc=0.3, scale=0.3, size=(self.TIME + 1, self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS))
demands = np.random.normal(loc=0.7, scale=0, size=120*5**2)
demands = np.round(demands).astype('int')
for i in range(120 * 5 ** 2):
    if (demands[i] < 0):
        demands[i] = 0

plt.hist(demands, bins=50)
plt.xlim(-2.5, 2.5)
plt.show()
plt.savefig('normal_graph.png')
