import numpy as np
a = np.random.randint(0, 1, (5, 5))
for i in range(5 - 1):
  for j in range(i + 1, 5):
    a[i][j] += 1
print(a)