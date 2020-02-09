import numpy as np


def poisson():
    LAMBDA = 50
    # TIME = 240
    # N = 10
    SIZE = 10 ** 5
    dic = [None] * 101
    for i in range(101):
        dic[i] = 0
    demands = np.random.poisson(lam=LAMBDA, size=(SIZE))
    for i in range(len(demands)):
        dic[demands[i]] += 1
    print(dic)


def normal():
    # loc = mu
    # scale = sigma = lambda^0.5
    MU = 50
    SIGMA = MU ** 0.5
    SIZE = 10 ** 5
    dic = [None] * 101
    for i in range(101):
        dic[i] = 0
    demands = np.random.normal(loc=MU, scale=SIGMA, size=(SIZE))
    for i in range(len(demands)):
        dic[np.round(demands[i]).astype('int')] += 1
    print(dic)


normal()
