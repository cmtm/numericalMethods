from NetworkSolver import NetworkSolver

ns1 = NetworkSolver(open("network1.txt", 'r'))
print(ns1.solveSystemCholesky())

ns2 = NetworkSolver(open("network2.txt", 'r'))
print(ns2.solveSystemCholesky())

ns3 = NetworkSolver(open("network3.txt", 'r'))
print(ns3.solveSystemCholesky())