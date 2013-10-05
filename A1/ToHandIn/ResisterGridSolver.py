import NetworkSolver
import time

"""
# this prints all the node voltages
for N in range(2, 11):
	file = open("output{}.txt".format(N), 'r')
	ns = NetworkSolver(file)
	print (' '.join(["{:10.6}".format(num).rjust(7) for num in ns.solveSystemCholesky()]))
	file.close()
print('\n\n\n')
"""
# Part a ---------------------------------------------------------
# this just prints effective resistance
# since this is a voltage divider, we know that R/(R+1) = vn
# where R is the mesh resistance and vn is the final node voltage
# solving for R, we find it to be vn/(1-vn)
print("{}   {}   {}".format('N'.rjust(3), 'R'.rjust(8), 'Time'.rjust(8)))
for N in range(2, 11):
	file = open("output{}.txt".format(N), 'r')
	ns = NetworkSolver.NetworkSolver(file)
	t0 = time.time()
	vn = ns.solveSystemCholesky()[-1]
	duration = time.time() - t0
	resistance = vn/(1-vn)
	print("{}   {:.6f}   {:3.6f}".format(str(N).rjust(3), resistance, duration))
print('\n\n\n')
# Part c -----------------------------------------------------------
# same as above but with sparse optimisation
print("{}   {}   {}   {}".format('N'.rjust(3), 'R'.rjust(8), 'Time'.rjust(8), 'Half-bandwidth'.rjust(20)))
for N in range(2, 11):
	file = open("output{}.txt".format(N), 'r')
	ns = NetworkSolver.SparseNetworkSolver(file)
	t0 = time.time()
	(x, halfBandwidth) = ns.solveSystemCholesky()
	vn = x[-1]
	duration = time.time() - t0
	resistance = vn/(1-vn)
	print("{}   {:.6f}   {:3.6f}   {:14.3f}".format(str(N).rjust(3), resistance, duration, halfBandwidth))