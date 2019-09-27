def my_round(val, digit=0):
  p = 10 ** digit
  return int((val * p * 2 + 1) // 2 / p)