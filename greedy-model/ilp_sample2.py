import pulp
import time

def main():
  # index
  I = [0, 1, 2, 3, 4]

  # values
  V = [4, 2, 2, 1, 10]

  # weights
  W = [12, 2, 1, 1, 4]

  # define the capacity
  b = 15

  # define the problem
  problem = pulp.LpProblem("1", pulp.LpMaximize)

  # define the variable sets
  X = {}
  for i in I:
    X[i] = pulp.LpVariable("x" + str(i), 0, 1, pulp.LpInteger)

  # define the objective function
  problem += pulp.lpSum(V[i] * X[i] for i in I), "total value"

  # define the constraints
  problem += sum(W[i] * X[i] for i in I) <= b, "constraints-1"

  print(problem)
  print(pulp.solvers.CPLEX_CMD().available())
  solver = pulp.solvers.CPLEX_CMD()
  result_status = problem.solve(solver)
  print('結果: ', pulp.LpStatus[result_status])
  print('目的関数値: ', pulp.value(problem.objective))
  for i in I:
    print(X[i].name, X[i].value())



if __name__ == '__main__':
  start = time.time()

  # write some processing codes here
  main()

  elapsed_time = time.time() - start
  print('実行時間: ', elapsed_time)