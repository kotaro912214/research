import pulp
import numpy as np

# define array for constraints and objective function
A = np.array([[3, 1, 2], [1, 3, 0], [0, 2, 4]])
b = np.array([60, 36, 48])
c = np.array([150, 200, 300])
(m, n) = A.shape

# define LpProblem obeject
prob = pulp.LpProblem(name='production', sense=pulp.LpMaximize)
x = [pulp.LpVariable('x' + str(i + 1), lowBound=0) for i in range(n)]
prob += pulp.lpDot(c, x)
for i in range(m):
  prob += pulp.lpDot(A[i], x) <= b[i], 'ineq' + str(i)

print(prob)
prob.solve()
print('status: ', pulp.LpStatus[prob.status])
print('Optimal value = ', pulp.value(prob.objective))
for v in prob.variables():
  print(v.name, '=', v.varValue)