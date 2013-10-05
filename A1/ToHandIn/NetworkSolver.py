import Matrices

"""
Input file format:
first line is the number of branches in the circuit
following that is an empty line
following that are the J R E values written as 3 space 
	seperated digits
following that is an empty line
following that is the incidence matrix. 
	The digits can be seperated by any number of spaces
	Newlines seperate the rows.

Example network file between dashed lines:
-----------------------------
5

0 2 -5
0 3 0
0 4 0
0 3 0
0 1 0

-1 1 0 0 0
0 -1 1 0 1
0 -1 1 0 1
0 0 -1 0 1
-----------------------------
"""

class NetworkSolver():
	
	def __init__(self, inputFile):
		network = inputFile.read().split('\n')
		network = [line for line in network if line != '\n']
		self.numBranches = int(network[0].strip())
		self.physicalValues = [[float(x) for x in line.split()] for line in network[2:self.numBranches+2]]
		mtrx = [[float(x) for x in line.split()] for line in network[self.numBranches+3:] if line !='']
		self.incidenceMtrx = Matrices.Matrix(len(mtrx), self.numBranches, mtrx)

		
	def computeLeftSide(self):
		# cool trick for making matrix
		conductanceMtrx = Matrices.Matrix(self.numBranches, self.numBranches, \
		                    [[(i == j) * 1/self.physicalValues[j][1] \
		                    for i in range(self.numBranches)] \
							for j in range(self.numBranches)])
		scaledIncidence = self.incidenceMtrx.multiplyByMatrix(conductanceMtrx)
		result = scaledIncidence.multiplyByMatrix(self.incidenceMtrx.getTranspose())
		result = result.getRawDataRef() # just want raw data
		# it's now positive definite so we have to upgrade it
		return Matrices.BehavingMatrix(len(result), len(result), result)
	
	def computeRightSide(self):
		# we'll just return the 1D vector
		# branchValues == J - Y*E
		branchValues = [[J - E/R] for [J, R, E] in self.physicalValues]
		# change it to matrix
		branchValues = Matrices.Matrix(self.numBranches, 1, branchValues)
		return self.incidenceMtrx.multiplyByMatrix(branchValues).getTranspose().getRawDataRef()[0]
		
	def solveSystemCholesky(self):
		return self.computeLeftSide().solveSystem(self.computeRightSide())
		
class SparseNetworkSolver(NetworkSolver):
	def computeLeftSide(self):
		# cool trick for making matrix
		conductanceMtrx = Matrices.Matrix(self.numBranches, self.numBranches, \
		                    [[(i == j) * 1/self.physicalValues[j][1] \
		                    for i in range(self.numBranches)] \
							for j in range(self.numBranches)])
		scaledIncidence = self.incidenceMtrx.multiplyByMatrix(conductanceMtrx)
		result = scaledIncidence.multiplyByMatrix(self.incidenceMtrx.getTranspose())
		result = result.getRawDataRef() # just want raw data
		# it's now positive definite so we have to upgrade it
		return Matrices.BehavingSparseMatrix(len(result), len(result), result)
	
	
	
	
	
	
	
	
	
	