import math

class FiniteDiffSolver():
	
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
		
		self.mesh = self.generateInitialMesh()
		
	def generateInitialMesh(self):
		# create mesh and set dirchlet boundary values
		mesh = [[10.0 if x <= self.CORE_WIDTH/self.h and y <= self.CORE_HEIGHT/self.h else 0.0 \
		          for x in range(self.nodesWide)] \
				  for y in range(self.nodesHigh)]
		# set neumann boundary values
		rateOfChange = -10*self.h/(self.CABLE_HEIGHT - self.CORE_HEIGHT)
		for y in range(int(self.CORE_HEIGHT/self.h) + 1, self.nodesHigh - 1):
			mesh[y][0] = mesh[y-1][0] + rateOfChange
		
		rateOfChange = -10*self.h/(self.CABLE_WIDTH - self.CORE_WIDTH)
		for x in range(int(self.CORE_WIDTH/self.h) + 1, self.nodesWide - 1):
			mesh[0][x] = mesh[0][x-1] + rateOfChange

		return mesh

	def solveWithSOR(self, w):
		iterations = 0
		while self.computeMaxResidual() > self.MIN_RESIDUAL:
			self.iterateSOR(w)
			iterations += 1
		return iterations
	
	def solveWithJacobi(self):
		iterations = 0
		while self.computeMaxResidual() > self.MIN_RESIDUAL:
			self.iterateJacobi()
			iterations += 1
		return iterations
	
	def getComputedPotential(self, x, y):
		# just a floor, not a round or linear interpolation
		xNode = int(x/self.h)
		yNode = int(y/self.h)
		return self.mesh[yNode][xNode]
		
	def iterateSOR(self, w):	
		for y in range(1, self.nodesHigh - 1):
			for x in range(1, self.nodesWide - 1):
				if x > self.CORE_WIDTH/self.h or y > self.CORE_HEIGHT/self.h:					
					self.mesh[y][x] = (1-w)*self.mesh[y][x] + (w/4)*(self.mesh[y][x-1] \
             		      + self.mesh[y][x+1] + self.mesh[y-1][x] + self.mesh[y+1][x])
						  
	def iterateJacobi(self):
		# generate K+1 th mesh
		oldMesh = self.mesh
		self.generateInitialMesh()
		for y in range(1, self.nodesHigh - 1):
			for x in range(1, self.nodesWide - 1):				
				if x > self.CORE_WIDTH/self.h or y > self.CORE_HEIGHT/self.h:
					self.mesh[y][x] = (1.0/4.0)*(oldMesh[y][x-1] \
             		      + oldMesh[y][x+1] + oldMesh[y-1][x] + oldMesh[y+1][x])
					

	def computeMaxResidual(self):
		maxResidual = 0
		for y in range(1, self.nodesHigh - 1):
			for x in range(1, self.nodesWide - 1):
				if x > self.CORE_WIDTH/self.h or y > self.CORE_HEIGHT/self.h:
					residual = self.mesh[y][x-1] + self.mesh[y][x+1] + self.mesh[y-1][x] + self.mesh[y+1][x] - 4*self.mesh[y][x]
					residual = math.fabs(residual)
					if residual > maxResidual:
						maxResidual = residual
		return maxResidual