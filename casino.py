import numpy as np
import math

DEPOSIT = 100
walet = DEPOSIT * 1
bet = 1
TIMES = 1000
loss = 1
odd, even = 0, 0

for i in range(TIMES):
    if (even >= 7 or odd >= 8):
        loss = 0
        even = 0
        odd = 0
    bet = loss
    if (walet <= bet):
        print("game over")
        print(walet, bet)
        exit()
    num = np.random.randint(37)
    print("--------------")
    print(walet, bet)
    print("the number is {}".format(num))
    print("--------------")
    if (num == 0):
        if (odd >= 3 or even >= 3):
            walet -= bet
            loss += bet
        even = 0
        odd = 0
    elif (num % 2 == 0):
        if (odd >= 3):
            walet += bet
            loss = 1
        elif (even >= 3):
            walet -= bet
            loss += bet
        even += 1
        odd = 0
    else:
        if (even >= 3):
            walet += bet
            loss = 1
        elif (odd >= 3):
            walet -= bet
            loss += bet
        even = 0
        odd += 1
print(walet)
