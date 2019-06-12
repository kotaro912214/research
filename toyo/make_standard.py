import random
import pandas as pd
import numpy as np
import time

def make_sample():
  path = './sample.csv'
  f = open(path, 'w')
  N = 10**6
  for i in range(N):
    if (i == N - 1):
      f.write(str(random.randint(1, 200)))
    else:
      f.write(str(random.randint(1, 200)) + '\n')
  f.close()


def make_csv_array():
  df = pd.read_csv('./sample.csv', header=None)
  return df

def write_csv_array(arr):
  path = './result.csv'
  f = open(path, 'w')
  for i in range(len(arr)):
    f.write(str(arr[i]) + '\n')
  f.close()

def main():
  make_sample()
  df = make_csv_array()
  x = np.array(df.values.flatten())
  x_mean = np.mean(x)
  s = np.std(x)
  for i in range(len(x)):
    x[i] = (x[i] - x_mean) / s
  write_csv_array(x)
  


if __name__ == '__main__':
  start = time.time()

  # write some processing codes here
  main()

  elapsed_time = time.time() - start
  print ("time:{0}".format(elapsed_time) + "[sec]")