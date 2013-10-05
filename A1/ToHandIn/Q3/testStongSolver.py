import math
from StrongFiniteDiffSolver import StrongFiniteDiffSolver


#horizontalLines = [0, 0.02, 0.028, 0.035, 0.04, 0.045, 0.053, 0.063, 0.074, 0.085, 0.1]
#verticalLines = [0, 0.2, 0.03, 0.04,0.05, 0.055, 0.06, 0.065, 0.07, 0.08, 0.088, 0.1]

horizontalLines = [0, 0.01, 0.2, 0.027, 0.032, 0.04, 0.052, 0.062, 0.072, 0.085, 0.093, 0.1]
verticalLines = [0, 0.01, 0.02, 0.027, 0.033, 0.042, 0.052, 0.06, 0.072, 0.085,0.093, 0.1]



#solver = StrongFiniteDiffSolver(horizontalLines, verticalLines)
solver = StrongFiniteDiffSolver([i*0.01 for i in range(11)], [i*0.01 for i in range(11)])
print(solver.mesh)
iterations = solver.solveWithSOR(1.24)
potential = solver.getComputedPotential (0.06, 0.04)
print("{:.3f}	{:.6f}".format(iterations, potential))