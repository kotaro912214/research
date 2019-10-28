import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

# demands = np.random.normal(loc=0.3, scale=0.3, size=(self.TIME + 1, self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS))
demands = np.random.normal(loc=0.3, scale=0.8, size=10**5)
demands = np.round(demands).astype('int')
for i in range(10 ** 5):
    if (demands[i] < 0):
        demands[i] = 0

plt.hist(demands, bins=50)
plt.xlim(-2.5, 2.5)
plt.show()
plt.savefig('normal_graph.png')
