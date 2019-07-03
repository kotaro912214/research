import pulp
import time

def main():
  # index
  I = [0, 1]
  J = [0, 1, 2, 3, 4]

  # values
  V = {}
  Vv = [[4, 2, 2, 1, 10], [2, 1, 5, 3, 3]]
  for i in I:
    for j in J:
      V[i, j] = Vv[i][j]

  # values
  A = {}
  Aa = [[4, 2, 2, 1, 10], [2, 1, 5, 3, 3]]
  for i in I:
    for j in J:
      A[i, j] = Aa[i][j]


  # weights
  W = {}
  Ww = [[12, 2, 1, 1, 4], [3, 1, 9, 5, 4]]
  for i in I:
    for j in J:
      W[i, j] = Ww[i][j]

  # define the capacity
  b = [15, 17]

  # define the problem
  problem = pulp.LpProblem("1", pulp.LpMaximize)

  # define the variable sets
  X = {}
  for i in I:
    for j in J:
      X[i, j] = pulp.LpVariable("x" + str(i) + '_' + str(j), 0, 1, pulp.LpInteger)

  # define the objective function
  problem += pulp.lpSum(V[i, j] * X[i, j] for i in I for j in J) + pulp.lpSum(A[i, j] for i in I for j in J), "total value"

  # define the constraints
  problem += sum(Ww[i][j] * X[i, j] for i in I for j in J) <= b[0], "constraints-1"
  problem += sum(Ww[i][j] * X[i, j] for i in I for j in J) <= b[1], "constraints-2"

  print(problem)
  # print(pulp.solvers.CPLEX_CMD().available())
  solver = pulp.solvers.CPLEX_CMD()
  result_status = problem.solve(solver)
  print('結果: ', pulp.LpStatus[result_status])
  print('目的関数値: ', pulp.value(problem.objective))
  for i in I:
    for j in J:
      print(X[i, j].name, X[i, j].value())



if __name__ == '__main__':
  start = time.time()

  # write some processing codes here
  main()

  elapsed_time = time.time() - start
  print('実行時間: ', elapsed_time)