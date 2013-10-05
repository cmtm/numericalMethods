import math
from FiniteDiffSolver import FiniteDiffSolver

# Part b ----------------------------------

for w in [x*0.1 + 1 for x in range(10)]:
	solver = FiniteDiffSolver(0.02)
	iterations = solver.solveWithSOR(w)
	potential = solver.getComputedPotential(0.06, 0.04)
	print("{:.3f}	{:.3f}	{:.6f}".format(w, iterations, potential))

	
# -----------------------------------------
print('\n\n')

# Part c ----------------------------------

# a good w is 1.24
for h in [0.1/(5*math.pow(2,x)) for x in range(0, 10)]:
	solver = FiniteDiffSolver(h)
	iterations = solver.solveWithSOR(1.24)
	potential = solver.getComputedPotential(0.06, 0.04)
	print("{:.3f}	{:.3f}	{:.6f}".format(h, iterations, potential))

#-------------------------------------------
print('\n\n')

# Part d -----------------------------------

for h in [0.1/(5*math.pow(2,x)) for x in range(0, 5)]:
	solver = FiniteDiffSolver(h)
	iterations = solver.solveWithJacobi()
	potential = solver.getComputedPotential(0.06, 0.04)
	print("{:.3f}	{:.6f}".format(iterations, potential))
