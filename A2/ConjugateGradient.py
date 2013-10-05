import math
import Matrices

class ConjugateGradientSolver():
	
	def __init__(self, h):
		self.CABLE_HEIGHT = 0.1
		self.CABLE_WIDTH = 0.1
		self.CORE_HEIGHT = 0.02
		self.CORE_WIDTH = 0.04
		self.CORE_POTENTIAL = 10
		self.MIN_RESIDUAL = 0.0001
		
		
		self.h = h
		self.nodesWide = int(self.CABLE_WIDTH/self.h) + 1
		self.nodesHigh = int(self.CABLE_HEIGHT/self.h) + 1
		self.nodeNumber = 0
		
		self.mesh = self.generateInitialMesh()
		(self.A, self.b) = self.generateAb()
		"""
		# --- test choleski; breaks program ------
		self.A = Matrices.Matrix(self.nodeNumber, self.nodeNumber, self.A)
		self.b = Matrices.Matrix(self.nodeNumber, 1, [[bi] for bi in self.b])
		self.solveCholeski()
		# -----------------------------------------
		"""
		mtrx = Matrices.Matrix(self.nodeNumber, self.nodeNumber, self.A)
		
		self.A = mtrx.getTranspose().multiplyByMatrix(mtrx)
		self.b = mtrx.getTranspose().multiplyByMatrix(Matrices.Matrix(self.nodeNumber, 1, [[bi] for bi in self.b]))
		
		self.doConjugateGradient()
		print('-----------------------')
		x = self.solveCholeski()
		for y in range(self.nodeNumber):
				print(x[y])
			
		
		
		
		
	def generateInitialMesh(self):
			
		# create mesh and set dirchlet boundary values
		mesh = [[('bound', 10.0) if x <= self.CORE_WIDTH/self.h and y <= self.CORE_HEIGHT/self.h \
		          else (('bound', 0.0) if x == self.nodesHigh - 1 or y == self.nodesWide - 1 else None) \
		          for x in range(self.nodesWide)] \
				  for y in range(self.nodesHigh)]
		# set neumann boundary values
		rateOfChange = -10*self.h/(self.CABLE_HEIGHT - self.CORE_HEIGHT)
		for y in range(int(self.CORE_HEIGHT/self.h) + 1, self.nodesHigh - 1):
			mesh[y][0] = ('bound', mesh[y-1][0][1] + rateOfChange)
		
		rateOfChange = -10*self.h/(self.CABLE_WIDTH - self.CORE_WIDTH)
		for x in range(int(self.CORE_WIDTH/self.h) + 1, self.nodesWide - 1):
			mesh[0][x] = ('bound', mesh[0][x-1][1] + rateOfChange)
		
		# number nodes
		for y in range(1, self.nodesHigh):
			for x in range(1, self.nodesWide): 
				if mesh[y][x] == None:
					mesh[y][x] = (self.nodeNumber, 0.0)
					self.nodeNumber += 1
		
		assert self.nodeNumber == 14
		return mesh
	
	def generateAb(self):
		A = [[0 for x in range(self.nodeNumber)] for y in range(self.nodeNumber)]
		b = [0] * self.nodeNumber
		for y in range(1, self.nodesHigh - 1):
			for x in range(1, self.nodesWide - 1):
				if x > self.CORE_WIDTH/self.h or y > self.CORE_HEIGHT/self.h:
					currNodeNum = self.mesh[y][x][0]
					
					A[currNodeNum][currNodeNum] = -4.0
					
					if self.mesh[y][x+1][0] == 'bound':
						b[currNodeNum] -= self.mesh[y][x+1][1]
					else:
						A[currNodeNum][self.mesh[y][x+1][0]] = 1
					if self.mesh[y+1][x][0] == 'bound':
						b[currNodeNum] -= self.mesh[y+1][x][1]
					else:
						A[currNodeNum][self.mesh[y+1][x][0]] = 1
					if self.mesh[y][x-1][0] == 'bound':
						b[currNodeNum] -= self.mesh[y][x-1][1]
					else:
						A[currNodeNum][self.mesh[y][x-1][0]] = 1
					if self.mesh[y-1][x][0] == 'bound':
						b[currNodeNum] -= self.mesh[y-1][x][1]
					else:
						A[currNodeNum][self.mesh[y-1][x][0]] = 1

		return (A, b)
	
	def solveCholeski(self):
		promotedA = Matrices.BehavingMatrix(self.nodeNumber, self.nodeNumber, self.A.getRawDataRef())
		return promotedA.solveSystem(self.b.getTranspose().getRawDataRef()[0])
		
	def doConjugateGradient(self):
		x = Matrices.Matrix(self.nodeNumber, 1, [[0] for y in range(self.nodeNumber)])
		A = self.A
		b = self.b
		r = b - (A * x)
		p = r.clone()
		
		for i in range(self.nodeNumber):
			alpha = (p.getTranspose() * r).getValue(1,1) / (p.getTranspose() * A * p).getValue(1,1)
			x = x + p.scalarMultiply(alpha)
			r = b - A * x
			beta = (-1) * (p.getTranspose() * A * r).getValue(1,1) / (p.getTranspose() * A * p).getValue(1,1)
			p = r + p.scalarMultiply(beta)
			"""
			for y in range(self.nodeNumber):
				print("{:>3}  {:<10.6} {:<10.4}".format(i if y == 0 else "", x.getValue(y+1,1), r.getValue(y+1,1)))
			"""
			# --- Finding norms --------
			infNorm = 0
			twoNorm = 0
			for y in range(1, self.nodeNumber + 1):
				val = abs(r.getValue(y,1))
				if val > infNorm:
					infNorm = val
				twoNorm += r.getValue(y,1)**2
			twoNorm = math.sqrt(twoNorm)
			print("[{},  {}, {}],".format(i, twoNorm, infNorm), end=" ")
			
			# ------------------------
		
		
	
mySolver = ConjugateGradientSolver(0.02)
		