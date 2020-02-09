import numpy as np

ns = 15
d = np.random.randint(400, 1800, size=(ns - 1)).tolist()
d.append(0)
print(d)

t = np.random.randint(4, 16, size=(ns - 1)).tolist()
t.append(0)
print(t)
